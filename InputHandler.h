/** @file */
/*
 Copyright (C) 2022 D. Quigg <dquigg123@gmail.com>

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 version 2 as published by the Free Software Foundation.
 */
#ifndef __USER_INPUT_HANDLER_H__
#define __USER_INPUT_HANDLER_H__

#include "InputHandler_config.h"

/**
 * @defgroup UserInput Constants
 * Constants stored in nonvolatile program memory
 * @{
 */

/** _UI namespace */
namespace _UI
{
    /**
     * @var _UI::UI_PROGMEM_DEFAULTS_ENUM
     * @brief enum map for ui_defaults_progmem_ptr
     */
    enum UI_PROGMEM_DEFAULTS_ENUM
    {
        username_e,
        eol_e,
        t_delim_e,
        c_delim_e,
        null_e,
        neg_e,
        dot_e,
        err_e
    };

    /**
     * @var _UI::UITYPE
     * @brief enum map for ui_input_type_strings
     */
    enum class UITYPE
    {
        UINT8_T,  /**< UserInput type 1 */
        UINT16_T, /**< UserInput type 2 */
        UINT32_T, /**< UserInput type 3 */
        INT16_T,  /**< UserInput type 4 */
        FLOAT,    /**< UserInput type 5 */
        CHAR,     /**< UserInput type 6 */
        C_STRING, /**< UserInput type 7 */
        _LAST     /**< reserved */
    };

    /** 
     * @var _UI::ui_defaults_progmem_ptr
     * @brief default constructor strings 
     */
    static const char *const ui_defaults_progmem_ptr[] PROGMEM = {
        "user", /**< default username */
        "\r\n", /**< default end of line (EOL) characters */
        " ",    /**< default token delimiter */
        "\"",   /**< default c-string delimiter */
        "\0",   /**< null '\\0' */
        "-",    /**< negative sign '-' */
        ".",    /**< period '.' */
        "error" /**< error string */
    };

    /** 
     * @var _UI::ui_input_type_strings
     * @brief user input type strings 
     */
    static const char *const ui_input_type_strings[] PROGMEM = {
        "uint8_t",  
        "uint16_t",
        "uint32_t", 
        "int16_t",  
        "float",    
        "char",     
        "c-string"
    };
}
using namespace _UI;

/** @} */

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
     * @param number_of_arguments the number of arguments the function expects
     * @param argument_type_array a pointer to the argument array
     */
    UserCallbackFunctionParameters(const char *user_defined_command_to_match,
                                   void (*user_defined_function_to_call)(UserInput *),
                                   size_t number_of_arguments = 0,
                                   const UITYPE argument_type_array[] = NULL)
        : command(user_defined_command_to_match),
          function(user_defined_function_to_call),
          command_length(strlen_P(command)),
          next_callback_function_parameters(NULL),
          num_args(number_of_arguments),
          _arg_type(argument_type_array)
    {
    }
    const char *command;                                               /** command to match */
    void (*function)(UserInput *);                                     /** pointer to function */
    uint16_t command_length;                                           /** length of command */
    UserCallbackFunctionParameters *next_callback_function_parameters; /** UserCallBackFunctionParameters iterator/pointer */
    uint16_t num_args;                                                 /** number of function arguments */
    const UITYPE *_arg_type;                                           /** function argument type array pointer */
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
     * @brief UserInput Constructor with NO output by default
     *
     * Creates a new instance.  If you want output, declare a buffer size, buffer, and index.
     *
     * @param output_buffer NULL
     * @param output_buffer_len ZERO
     * @param username NULL
     * @param end_of_line_characters EOL term, default is '\\r\\n'
     * @param token_delimiter token demarcation
     * @param c_string_delimiter c-string demarcation
     */
    UserInput(char *output_buffer = NULL,
              size_t output_buffer_len = 0,
              const char *username = NULL,
              const char *end_of_line_characters = NULL,
              const char *token_delimiter = ui_defaults_progmem_ptr[t_delim_e],
              const char *c_string_delimiter = ui_defaults_progmem_ptr[c_delim_e])
        : _output_buffer(output_buffer),
          _string_pos(0),
          _output_buffer_len(output_buffer_len),
          _username_((username == NULL) ? ui_defaults_progmem_ptr[username_e] : username),
          _term_((end_of_line_characters == NULL) ? ui_defaults_progmem_ptr[eol_e] : end_of_line_characters),
          _delim_((token_delimiter == NULL) ? ui_defaults_progmem_ptr[t_delim_e] : token_delimiter),
          _c_str_delim_((c_string_delimiter == NULL) ? ui_defaults_progmem_ptr[c_delim_e] : c_string_delimiter),
          _null_(ui_defaults_progmem_ptr[null_e]),
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
    void AddUserCommand(UserCallbackFunctionParameters &command);

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
    void GetCommandFromStream(Stream &stream, uint16_t rx_buffer_size = 32);

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

    /**
     * @brief is class output enabled
     *
     * @return true if enabled
     * @return false if not enabled
     */
    bool OutputIsEnabled();

    /**
     * @brief direct class output to stream, clears output buffer automatically
     *
     * @param stream the stream to print to
     */
    void OutputToStream(Stream &stream);

    /**
     * @brief clears output buffer and puts _string_pos back at 0
     *
     */
    void ClearOutputBuffer();

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

    /**
     * @brief combines backslash and character and into valid control characters
     *
     * @param input the char after a backslash ie 'r'
     * @return the control character char value ie '\\r'
     */
    char combineControlCharacters(char input);

private:
    /*
        UserInput Constructor variables
    */
    char *_output_buffer;
    size_t _string_pos;
    const size_t _output_buffer_len;
    const char *_username_;
    const char *_term_;
    const char *_delim_;
    const char *_c_str_delim_;
    const char *_null_;
    void (*default_handler_)(UserInput *);
    UserCallbackFunctionParameters *commands_head_;
    UserCallbackFunctionParameters *commands_tail_;
    size_t commands_count_;

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
