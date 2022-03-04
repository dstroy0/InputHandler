/**
   @file InputHandler.h
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief InputHandler library header file
   @version 1.0
   @date 2022-03-02

   @copyright Copyright (c) 2022
*/
/*
 Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 version 3 as published by the Free Software Foundation.
 */
#ifndef __USER_INPUT_HANDLER_H__
#define __USER_INPUT_HANDLER_H__

#include "InputHandler_config.h"

/**
 * @defgroup UserInput Constants
 * @{
 */
/**
 * @brief ui_defaults_progmem_ptr enum
 * @enum UI_PROGMEM_DEFAULTS_ENUM
 */
enum UI_PROGMEM_DEFAULTS_ENUM
{
    username_e, ///<  ui_defaults_progmem_ptr[0]
    eol_e,      ///<  ui_defaults_progmem_ptr[1]
    t_delim_e,  ///<  ui_defaults_progmem_ptr[2]
    c_delim_e,  ///<  ui_defaults_progmem_ptr[3]
    null_e,     ///<  ui_defaults_progmem_ptr[4]
    neg_e,      ///<  ui_defaults_progmem_ptr[5]
    dot_e,      ///<  ui_defaults_progmem_ptr[6]
    err_e       ///<  ui_defaults_progmem_ptr[7]
};

/**
 * @brief default constructor string literals
 * \snippet InputHandler.h ui_defaults_progmem_def
 */
const PROGMEM char* const ui_defaults_progmem_ptr[] = {
    //![ui_defaults_progmem_def]
    "user", //  default username
    "\r\n", //  default end of line characters
    " ",    //  default token delimiter
    "\"",   //  default c-string delimiter
    "\0",   //  null
    "-",    //  negative sign
    ".",    //  dot
    "error" //  error
    //![ui_defaults_progmem_def]
};

/**
 * @brief ui_input_type_strings enum
 * @enum UITYPE
 */
enum class UITYPE
{
    UINT8_T,  ///<  ui_input_type_strings[0]
    UINT16_T, ///<  ui_input_type_strings[1]
    UINT32_T, ///<  ui_input_type_strings[2]
    INT16_T,  ///<  ui_input_type_strings[3]
    FLOAT,    ///<  ui_input_type_strings[4]
    CHAR,     ///<  ui_input_type_strings[5]
    C_STRING, ///<  ui_input_type_strings[6]
    NOTYPE,   ///<  ui_input_type_strings[7]
    _LAST     ///<  reserved
};

/**
 * @brief type string literals
 * \snippet InputHandler.h ui_input_type_strings_def
 */
const PROGMEM char* const ui_input_type_strings[] = {
    //![ui_input_type_strings_def]
    "uint8_t",     //  8-bit unsigned integer
    "uint16_t",    //  16-bit unsigned integer
    "uint32_t",    //  32-bit unsigned integer
    "int16_t",     //  16-bit signed integer
    "float",       //  32-bit floating point number
    "char",        //  single char
    "c-string",    //  c-string without spaces if not enclosed with ""
    "type-unknown" //  user defined NOTYPE
    //![ui_input_type_strings_def]
};

/** @} */

/**
 * @brief forward declaration of UserInput class for
 * UserCallbackFunctionparameters class
 */
class UserInput;

/**
 * @brief User defined function parameters
 */
class UserCommandParameters
{
public:
    /**
     * @brief UserCommandParameters Constructor
     *
     * Creates a new instance of this class.  Before using, construct a UserInput object.
     * @param user_defined_command_to_match The command which when entered will call a function
     * @param user_defined_function_to_call The function called when the command is matched
     * @param number_of_arguments the number of arguments the function expects
     * @param argument_type_array a pointer to the argument type array or a single argument type
     */

    // no arguments
    UserCommandParameters(const char* user_defined_command_to_match,
                          void (*user_defined_function_to_call)(UserInput*))
        : command(user_defined_command_to_match),
          function(user_defined_function_to_call),
          command_length(strlen_P(command)),
          next_command_parameters(NULL),
          num_args(0),          
          _arg_type(NULL),
          arg_type(UITYPE::_LAST),
          argument_flag(0)          
    {
    }

    // argument array
    UserCommandParameters(const char* user_defined_command_to_match,
                          void (*user_defined_function_to_call)(UserInput*),
                          size_t number_of_arguments,
                          const UITYPE argument_type_array[])
        : command(user_defined_command_to_match),
          function(user_defined_function_to_call),
          command_length(strlen_P(command)),
          next_command_parameters(NULL),
          num_args(number_of_arguments),          
          _arg_type(argument_type_array),
          arg_type(UITYPE::_LAST),
          argument_flag(1)          
    {
    }

    // single argument type (default NOTYPE)
    UserCommandParameters(const char* user_defined_command_to_match,
                          void (*user_defined_function_to_call)(UserInput*),
                          size_t number_of_arguments,
                          const UITYPE argument_type = UITYPE::NOTYPE)
        : command(user_defined_command_to_match),
          function(user_defined_function_to_call),
          command_length(strlen_P(command)),
          next_command_parameters(NULL),
          num_args(number_of_arguments),          
          _arg_type(NULL),                    
          arg_type(argument_type),
          argument_flag(2)          
    {        
    }

    const char* command;                            /** command to match */
    void (*function)(UserInput*);                   /** pointer to function */
    size_t command_length;                          /** length of command */
    UserCommandParameters* next_command_parameters; /** UserCommandParameters iterator/pointer */
    size_t num_args;                                /** number of function arguments */    
    const UITYPE* _arg_type;                        /** function argument array pointer */
    const UITYPE arg_type;                          /** single argument type */
    uint8_t argument_flag;                          /** switches how we iterate through arguments */
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
    UserInput(char* output_buffer = NULL,
              size_t output_buffer_len = 0,
              const char* username = NULL,
              const char* end_of_line_characters = NULL,
              const char* token_delimiter = ui_defaults_progmem_ptr[t_delim_e],
              const char* c_string_delimiter = ui_defaults_progmem_ptr[c_delim_e])
        : _output_buffer(output_buffer),
          _output_enabled((output_buffer == NULL) ? false : true),
          _string_pos(0),
          _output_buffer_len(output_buffer_len),
          _username_((username == NULL) ? ui_defaults_progmem_ptr[username_e] : username),
          _term_((end_of_line_characters == NULL) ? ui_defaults_progmem_ptr[eol_e] : end_of_line_characters),
          _delim_((token_delimiter == NULL) ? ui_defaults_progmem_ptr[t_delim_e] : token_delimiter),
          _c_str_delim_((c_string_delimiter == NULL) ? ui_defaults_progmem_ptr[c_delim_e] : c_string_delimiter),
          _null_(ui_defaults_progmem_ptr[null_e]),
          default_function_(NULL),
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
    char* NextArgument();

    /**
     * @brief adds user commands
     *
     * @param command reference to UserCommandParameters
     */
    void AddCommand(UserCommandParameters& command);

    /**
     * @brief read command(s) from a buffer
     *
     * @param data a buffer with characters
     * @param len the size of the buffer
     */
    void ReadCommandFromBuffer(uint8_t* data, size_t len);

    /**
     * @brief Get the Command From a Stream object
     *
     * @param stream the stream to reference
     * @param rx_buffer_size the size of our receive buffer
     */
    void GetCommandFromStream(Stream& stream, size_t rx_buffer_size = 32);

    /**
     * @brief lists commands available to the user
     *
     */
    void ListCommands();

    /**
     * @brief lists UserInput class settings
     *
     * @param inputprocess pointer to class instance
     */
    void ListSettings(UserInput* inputprocess);

    /**
     * @brief Set the default function, which is the function called
     * when there is no command match, or when input is invalid.  It
     * is overloaded so you are able perform your own error output or
     * use the UserInput pointer to access class methods.
     *
     * @param function a pointer to a user specified function
     */
    void DefaultFunction(void (*function)(UserInput*));
    void DefaultFunction(void (*function)());

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
    void OutputToStream(Stream& stream);

    /**
     * @brief clears output buffer and puts _string_pos back at 0
     *
     */
    void ClearOutputBuffer();

protected:
    /**
     * @brief Tries to get a token from an input string
     *
     * @param token_buffer the place where we store tokens
     * @param data input data
     * @param len length of input data
     * @param data_index index of data
     */
    bool getToken(char* token_buffer, uint8_t* data, size_t len, size_t* data_index);

    /**
     * @brief Tries to determine if input is valid
     *
     * @param cmd Function parameter pointer
     * @param arg_type the type of argument we are testing
     * @param data_pointers_index index of token pointers
     */
    bool validateUserInput(uint8_t arg_type, size_t data_pointers_index);

    /**
     * @brief launches a function
     *
     * @param cmd Function parameter pointer
     */
    void launchFunction(UserCommandParameters* cmd);

    /**
     * @brief Escapes control characters so they will print
     *
     * @param input the input string
     * @param output the output string
     */
    void escapeCharactersSoTheyPrint(const char* input, char* output);

    /**
     * @brief combines backslash and character and into valid control characters
     *
     * @param input the char after a backslash ie 'r'
     * @return the control character char value ie '\\r'
     */
    char combineControlCharacters(char input);

    /**
     * @brief Get the UITYPE for the argument
     * 
     * @param cmd UserCommandParameters pointer
     * @param index argument number
     * @return uint8_t argument type
     */
    uint8_t getArgType(UserCommandParameters *cmd, size_t index = 0);

private:
    /*
        UserInput Constructor variables
    */
    char* _output_buffer;                  //  pointer to output char buffer
    bool _output_enabled;                  //  true if _output_buffer is not NULL
    size_t _string_pos;                    //  _output_buffer's index
    const size_t _output_buffer_len;       //  _output_buffer's size
    const char* _username_;                //  username
    const char* _term_;                    //  end of line characters
    const char* _delim_;                   //  token delimiter
    const char* _c_str_delim_;             //  c-string delimiter
    const char* _null_;                    //  char null '\0'
    void (*default_function_)(UserInput*); //  pointer to default function
    UserCommandParameters* commands_head_; //  pointer to object list
    UserCommandParameters* commands_tail_; //  pointer to object list
    size_t commands_count_;                //   how many commands are there

    /*
        member function variables
    */
    bool _output_flag = false;                                             //   output is available flag, set by member functions
    char* token_buffer = NULL;                                             //   pointer to tokenized c-string
    char* data_pointers[USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS] = {0}; //   token_buffer pointers
    size_t data_pointers_index = 0;                                        //   data_pointer's index
    size_t rec_num_arg_strings = 0;                                        //   number of tokens after first valid token

    /*
        GetCommandFromStream variables
    */
    bool stream_buffer_allocated = false; // this flag is set true on GetCommandFromStream entry if a buffer is not allocated
    bool new_stream_data = false;         // if there is new data in *stream_data this is true
    uint8_t* stream_data = NULL;          // pointer to stream input, a string of char
    uint16_t stream_data_index = 0;       // the index of stream_data
};

#endif
