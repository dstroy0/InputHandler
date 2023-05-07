/**
   @file Functions.h
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief Functions for MultiFile.ino
   @version 0.9
   @date 2022-03-20

   @copyright Copyright (c) 2022
*/

#if !defined(__CLI_FUNCTIONS__)
    #define __CLI_FUNCTIONS__

    #include "cli_setup.h"

/*
   default function, called if nothing matches or if there is an error
*/
void unrecognized(ih::Input* inputProcess)
{
    // error output
    inputProcess->outputToStream(Serial);
}

/*
   lists commands available to the user
*/
void help(ih::Input* inputProcess) { inputProcess->listCommands(); }

/*
   test all available input types
*/
void test_input_types(ih::Input* inputProcess)
{
    inputProcess->outputToStream(Serial); // class output, doesn't have to output to the input stream
    char* str_ptr = inputProcess->nextArgument(); //  init str_ptr and point it at the next argument input by the user
    char* strtoul_ptr = 0; //  this is for strtoul
    uint32_t strtoul_result = strtoul(str_ptr, &strtoul_ptr, 10); // get the result in base10
    uint8_t eight_bit = (strtoul_result <= UINT8_MAX) ? (uint8_t)strtoul_result : 0U; // if the result is less than UINT8_MAX then set eight_bit, else eight_bit = 0

    str_ptr = inputProcess->nextArgument();
    strtoul_ptr = 0;
    strtoul_result = strtoul(str_ptr, &strtoul_ptr, 10);
    uint16_t sixteen_bit = (strtoul_result <= UINT16_MAX) ? (uint16_t)strtoul_result : 0U;

    str_ptr = inputProcess->nextArgument();
    strtoul_ptr = 0;
    uint32_t thirtytwo_bit = strtoul(str_ptr, &strtoul_ptr, 10);

    str_ptr = inputProcess->nextArgument();
    int sixteen_bit_int = atoi(str_ptr);

    str_ptr = inputProcess->nextArgument();
    float thirtytwo_bit_float = (float)atof(str_ptr);

    str_ptr = inputProcess->nextArgument();
    char _char = *str_ptr;

    str_ptr = inputProcess->nextArgument();
    char c_string[64] = {'\0'};
    snprintf_P(c_string, 64, PSTR("%s"), str_ptr);

    str_ptr = inputProcess->nextArgument();
    char unknown_string[64] = {'\0'};
    snprintf_P(unknown_string, 64, PSTR("%s"), str_ptr);

    char float_buffer[32] = {'\0'}; //  dtostrf buffer
    char out[512] = {'\0'}; //  function output buffer
    uint16_t string_pos = 0; // function output buffer index

    /*
         format out[] with all of the arguments received
    */
    string_pos += snprintf_P(out + string_pos, 512,
        PSTR("Test user input types:\n"
             " uint8_t %u\n"
             " uint16_t %u\n"
             " uint32_t %lu\n"
             " int %d\n"
             " float %s\n"
             " char %c\n"
             " c-string %s\n"
             " unknown-type %s\n"),
        eight_bit, sixteen_bit, thirtytwo_bit, sixteen_bit_int, dtostrf(thirtytwo_bit_float, 2, 3, float_buffer), _char, c_string, unknown_string);

    Serial.println(out);
}

#endif