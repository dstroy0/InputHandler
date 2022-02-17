/*
 Copyright (C) 2022 D. Quigg <dquigg123@gmail.com>

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 version 2 as published by the Free Software Foundation.
 */

/**
 * @file InputHandler.h
 *
 * Class declarations for UserInput and UserCallbackFunctionParameters
 * USER_INPUT_TYPES enum declaration
 */

#ifndef __USER_INPUT_HANDLER_H__
#define __USER_INPUT_HANDLER_H__

#include <Arduino.h>
#if defined(ARDUINO_ARCH_SAM)
#include <avr/dtostrf.h>
#endif
#if defined(__MBED_CONFIG_DATA__)
#include <stdio.h> 
char *dtostrf (double val, signed char width, unsigned char prec, char *sout) {
  char fmt[20];
  sprintf_P(fmt, PSTR("%%%d.%df"), width, prec);
  sprintf_P(sout, fmt, val);
  return sout;
}
#endif

#ifndef USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS
#define USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS 32U
#endif

#ifndef UINT16_MAX
#define UINT16_MAX 65535
#endif

#ifndef UINT8_MAX
#define UINT8_MAX 255
#endif

#ifndef USER_INPUT_MAX_INPUT_LENGTH
#define USER_INPUT_MAX_INPUT_LENGTH UINT16_MAX
#endif

#ifdef DEBUG_USER_INPUT
#define _DEBUG_USER_INPUT
#endif

/**
 * @}
 * @defgroup User input types
 * @{
 */
enum USER_INPUT_TYPES
{
    USER_INPUT_TYPE_UINT8_T,
    USER_INPUT_TYPE_UINT16_T,
    USER_INPUT_TYPE_UINT32_T,
    USER_INPUT_TYPE_INT16_T,
    USER_INPUT_TYPE_FLOAT,
    USER_INPUT_TYPE_CHAR,
    USER_INPUT_TYPE_C_STRING,
    _LAST_USER_INPUT_TYPES_enum
};

static constexpr const PROGMEM char *_default_username = "user";               /** default username */
static constexpr const PROGMEM char *_default_end_of_line_characters = "\r\n"; /** default end of line (EOL) characters */
static constexpr const PROGMEM char *_default_token_delimiter = " ";           /** default token delimiter */
static constexpr const PROGMEM char *_default_c_string_delimiter = "\"";       /** default c-string delimiter */
static constexpr const PROGMEM char *null_ = "\0";                             /** null '\0' */
/** input type string array */
static constexpr const PROGMEM char *_input_type_strings[] = {
    "uint8_t",
    "uint16_t",
    "uint32_t",
    "int16_t",
    "float",
    "char",
    "c-string"};
static constexpr const PROGMEM char *_negative_sign = "-"; /** negative sign '-' */
static constexpr const PROGMEM char *_dot = ".";           /** period '.' */
static constexpr const PROGMEM char *error = "error";      /** error string */

/**
 * @}
 * @brief forward declaration of UserInput class for
 * UserCallbackFunctionparameters class
 */
class UserInput;

/**
 * @}
 * @brief User defined function parameters
 */
class UserCallbackFunctionParameters
{
public:
    uint16_t num_args;                                                 /** number of function arguments */
    const uint8_t *_arg_type;                                          /** function argument type array pointer */
    const char *command;                                               /** command to match */
    uint16_t command_length;                                           /** length of command */
    void (*function)(UserInput *);                                     /** pointer to function */
    UserCallbackFunctionParameters *next_callback_function_parameters; /** UserCallBackFunctionParameters iterator/pointer */

    /**
     * UserCallbackFunctionParameters Constructor
     *
     * Creates a new instance of this class.  Before using, construct a UserInput object.
     * @param user_defined_command_to_match The command which when entered will call a function
     * @param user_defined_function_to_call The function called when the command is matched
     * @param args args is a variadic parameter pack
     */
    template <typename... Arguments>
    UserCallbackFunctionParameters(const char *user_defined_command_to_match,
                                   void (*user_defined_function_to_call)(UserInput *),
                                   const Arguments &...args)
        : command(user_defined_command_to_match),
          function(user_defined_function_to_call),
          command_length(strlen_P(command)),
          next_callback_function_parameters(NULL),
          num_args(sizeof...(Arguments))
    {
        static const uint8_t _arg[] = {static_cast<uint8_t>(args)...}; /** args is expanded into the array _arg */
        _arg_type = _arg;                                              /** point to the array in memory */
    }
};

/**
 * @}
 * @brief User input handler
 */
class UserInput
{
public:
    /**
     * @name Primary public interface
     *
     *  These are the methods you use to operate the input handler
     */
    /**@{*/

    /**
     * UserInput Constructor
     *
     * Creates a new instance of this driver.  Before using, you declare an output buffer and size.
     *
     * See [Related Pages](pages.html) for device specific information <br>
     *
     * @param output_buffer Class output is put into this buffer
     * @param output_buffer_string_pos Where are we at in the output buffer
     * @param username Name of user
     * @param end_of_line_characters EOL term, default is '\r\n'
     * @param token_delimiter token demarcation
     * @param c_string_delimiter c-string demarcation
     */
    UserInput(char *output_buffer,
              uint16_t *output_buffer_string_pos,
              uint16_t output_buffer_len,
              const char *username = _default_username,
              const char *end_of_line_characters = _default_end_of_line_characters,
              const char *token_delimiter = _default_token_delimiter,
              const char *c_string_delimiter = _default_c_string_delimiter)
        : _output_buffer(output_buffer),
          _string_pos(output_buffer_string_pos),
          _output_buffer_len(output_buffer_len),
          _username_(username),
          _term_(end_of_line_characters),
          _delim_(token_delimiter),
          _c_str_delim_(c_string_delimiter),
          _null_(null_),
          default_handler_(NULL),
          commands_head_(NULL),
          commands_tail_(NULL),
          commands_count_(0)
    {
    }

    char *NextArgument();

    void AddUserCommand(UserCallbackFunctionParameters *command);

    void ReadCommand(uint8_t *data, size_t len);

    void GetCommandFromStream(Stream &stream,
                              uint16_t rx_buffer_size = 128,
                              const char *end_of_line_character = _default_end_of_line_characters);

    void ListUserCommands();

    void ListUserInputSettings(UserInput *inputprocess);

    void SetDefaultHandler(void (*function)(UserInput *));

    bool OutputIsAvailable();

#ifdef _DEBUG_USER_INPUT
    bool EnableDebugOutput = false;
#endif

protected:
    /**
     * Tries to get a token from an input string
     *
     * @param token_buffer the place where we store tokens
     * @param data input data
     * @param len length of input data
     * @param data_index index of data
     */
    bool getToken(char *token_buffer, uint8_t *data, size_t len, uint16_t *data_index);

    /**
     * Tries to determine if input is valid
     *
     * @param cmd Function parameter pointer
     * @param arg_type the type of argument we are testing
     * @param data_pointers_index index of token pointers
     */
    bool validateUserInput(UserCallbackFunctionParameters *cmd, uint8_t arg_type, uint16_t data_pointers_index);

    /**
     * launches a function
     *
     * @param cmd Function parameter pointer
     */
    void launchFunction(UserCallbackFunctionParameters *cmd);

    /**
     * Escapes control characters so they will print
     *
     * @param input the input string
     * @param output the output string
     */
    void escapeCharactersSoTheyPrint(const char *input, char *output);

private:
    const char *_username_;
    const char *_term_;
    const char *_delim_;
    const char *_c_str_delim_;
    const char *_null_;

    char *_output_buffer;
    uint16_t *_string_pos;
    uint16_t _output_buffer_len;
    bool _output_flag = false;

    void (*default_handler_)(UserInput *);
    UserCallbackFunctionParameters *commands_head_;
    UserCallbackFunctionParameters *commands_tail_;
    uint16_t commands_count_;

    char *token_buffer = NULL;
    boolean serial_buffer_allocated = false;
    uint8_t *serial_data = NULL;
    boolean new_serial_data = false;
    uint16_t serial_data_index = 0;
    char *data_pointers[USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS] = {0};
    uint16_t data_pointers_index = 0;
    uint16_t rec_num_arg_strings = 0;
};

#endif
