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
#define UI_PGM_READ_DWORD(x) pgm_read_dword(x)
#define UI_SNPRINTF_P(s_, sz_, f_, ...) snprintf_P(s_, sz_, f_, ##__VA_ARGS__)

#if defined(ARDUINO_SAMD_VARIANT_COMPLIANCE) || defined(__MBED_CONFIG_DATA__)
#include <avr/dtostrf.h>
#endif

#if defined(ARDUINO_SAM_DUE)
#define UI_PGM_READ_DWORD_(x)
#undef UI_SNPRINTF_P
#define UI_SNPRINTF_P(s_, sz_, f_, ...) snprintf(s_, sz_, f_, ##__VA_ARGS__)
#include <avr/dtostrf.h>
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
 * @enum USER_INPUT_TYPES
 * @brief contains acceptable input types and a final member _LAST_USER_INPUT_TYPES_enum which should not be used.
 *
 */
enum USER_INPUT_TYPES
{
    USER_INPUT_TYPE_UINT8_T,    /**< UserInput type 0 */
    USER_INPUT_TYPE_UINT16_T,   /**< UserInput type 1 */
    USER_INPUT_TYPE_UINT32_T,   /**< UserInput type 2 */
    USER_INPUT_TYPE_INT16_T,    /**< UserInput type 3 */
    USER_INPUT_TYPE_FLOAT,      /**< UserInput type 4 */
    USER_INPUT_TYPE_CHAR,       /**< UserInput type 5 */
    USER_INPUT_TYPE_C_STRING,   /**< UserInput type 6 */
    _LAST_USER_INPUT_TYPES_enum /**< reserved */
};

static constexpr const PROGMEM char *_default_username = "user";               /**< default username */
static constexpr const PROGMEM char *_default_end_of_line_characters = "\r\n"; /**< default end of line (EOL) characters */
static constexpr const PROGMEM char *_default_token_delimiter = " ";           /**< default token delimiter */
static constexpr const PROGMEM char *_default_c_string_delimiter = "\"";       /**< default c-string delimiter */
static constexpr const PROGMEM char *null_ = "\0";                             /**< null '\\0' */
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
 * @brief forward declaration of UserInput class for
 * UserCallbackFunctionparameters class
 */
class UserInput;

/**
 * @brief User defined function parameters
 */
class UserCallbackFunctionParameters
{
public:
    /**
     * @brief UserCallbackFunctionParameters Constructor
     *
     * Creates a new instance of this class.  Before using, construct a UserInput object.
     * @param user_defined_command_to_match The command which when entered will call a function
     * @param user_defined_function_to_call The function called when the command is matched
     * @param args args is a variadic parameter pack of USER_INPUT_TYPE
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

        _arg_type = _arg; /** point to the array in memory */
    }
    const char *command;                                               /** command to match */
    void (*function)(UserInput *);                                     /** pointer to function */
    uint16_t command_length;                                           /** length of command */
    UserCallbackFunctionParameters *next_callback_function_parameters; /** UserCallBackFunctionParameters iterator/pointer */
    uint16_t num_args;                                                 /** number of function arguments */
    const uint8_t *_arg_type;                                          /** function argument type array pointer */
};

/**
 * @brief User input handler
 */
class UserInput
{
public:
    /**
     * @name UserInput class
     *
     * These are the methods you use to operate the input handler
     */

    /**
     * @brief UserInput Constructor
     *
     * Creates a new instance.  Before using, declare an output buffer and output buffer size.
     *
     * @param output_buffer Class output is put into this buffer
     * @param output_buffer_string_pos Where are we at in the output buffer
     * @param output_buffer_len Size of the output buffer
     * @param username Name of user
     * @param end_of_line_characters EOL term, default is '\\r\\n'
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
    /**
     * @brief returns a pointer to the next token in token_buffer
     *
     * @return char*
     */
    char *NextArgument();

    /**
     * @brief adds user commands
     *
     * @param command pointer to UsercallbackFunctionParameters
     */
    void AddUserCommand(UserCallbackFunctionParameters *command);

    /**
     * @brief read command(s) from a buffer
     *
     * @param data a buffer with characters
     * @param len the size of the buffer
     */
    void ReadCommand(uint8_t *data, size_t len);

    /**
     * @brief Get the Command From a Stream object
     *
     * @param stream the stream to reference
     * @param rx_buffer_size the size of our receive buffer
     * @param end_of_line_character the line terminating character(s)
     */
    void GetCommandFromStream(Stream &stream,
                              uint16_t rx_buffer_size = 128,
                              const char *end_of_line_character = _default_end_of_line_characters);

    /**
     * @brief lists commands available to the user
     *
     */
    void ListUserCommands();

    /**
     * @brief lists UserInput class settings
     *
     * @param inputprocess pointer to class instance
     */
    void ListUserInputSettings(UserInput *inputprocess);

    /**
     * @brief Set the Default Handler, which is the function called
     * when there is no command match, or when input is invalid.
     *
     * @param function a pointer to a user specified function
     */
    void SetDefaultHandler(void (*function)(UserInput *));

    /**
     * @brief is class output available
     *
     * @return true if output is available
     * @return false if no output is available
     */
    bool OutputIsAvailable();

#ifdef _DEBUG_USER_INPUT
    bool EnableDebugOutput = false;
#endif

protected:
    /**
     * @brief Tries to get a token from an input string
     *
     * @param token_buffer the place where we store tokens
     * @param data input data
     * @param len length of input data
     * @param data_index index of data
     */
    bool getToken(char *token_buffer, uint8_t *data, size_t len, uint16_t *data_index);

    /**
     * @brief Tries to determine if input is valid
     *
     * @param cmd Function parameter pointer
     * @param arg_type the type of argument we are testing
     * @param data_pointers_index index of token pointers
     */
    bool validateUserInput(UserCallbackFunctionParameters *cmd, uint8_t arg_type, uint16_t data_pointers_index);

    /**
     * @brief launches a function
     *
     * @param cmd Function parameter pointer
     */
    void launchFunction(UserCallbackFunctionParameters *cmd);

    /**
     * @brief Escapes control characters so they will print
     *
     * @param input the input string
     * @param output the output string
     */
    void escapeCharactersSoTheyPrint(const char *input, char *output);

    char combineControlCharacters(char input);

private:
    /*
        UserInput Constructor variables
    */
    char *_output_buffer;
    uint16_t *_string_pos;
    uint16_t _output_buffer_len;
    const char *_username_;
    const char *_term_;
    const char *_delim_;
    const char *_c_str_delim_;
    const char *_null_;
    void (*default_handler_)(UserInput *);
    UserCallbackFunctionParameters *commands_head_;
    UserCallbackFunctionParameters *commands_tail_;
    uint16_t commands_count_;

    /*
        member function variables
    */
    bool _output_flag = false;                                             // output is available flag, set by member functions
    char *token_buffer = NULL;                                             //  pointer to tokenized c-string
    char *data_pointers[USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS] = {0}; //
    uint16_t data_pointers_index = 0;
    uint16_t rec_num_arg_strings = 0;

    /*
        GetCommandFromStream variables
    */
    boolean stream_buffer_allocated = false; // this flag is set true on GetCommandFromStream entry if a buffer is not allocated
    uint8_t *stream_data = NULL;             // pointer to stream input, a string of char
    boolean new_stream_data = false;         //  if there is new data in *stream_data this is true
    uint16_t stream_data_index = 0;          //  the index of stream_data
};

#endif
