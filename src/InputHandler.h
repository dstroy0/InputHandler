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

#include "config/InputHandler_config.h"

/**
 * @defgroup UserInput Constants
 * @{
 */

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
    NO_ARGS,  ///<  ui_input_type_strings[8]
    _LAST     ///<  reserved
};

/**
 * @brief type string literals
 * \snippet InputHandler.h ui_input_type_strings_def
 */
const char ui_input_type_strings[9][UI_INPUT_TYPE_STRINGS_MAX_LEN] PROGMEM = {
    //![ui_input_type_strings_def]
    "uint8_t",      //  8-bit unsigned integer
    "uint16_t",     //  16-bit unsigned integer
    "uint32_t",     //  32-bit unsigned integer
    "int16_t",      //  16-bit signed integer
    "float",        //  32-bit floating point number
    "char",         //  single char
    "c-string",     //  c-string without spaces if not enclosed with ""
    "type-unknown", //  user defined NOTYPE
    "error"         //  error
    //![ui_input_type_strings_def]
};

/**
 * @brief argument_flag type enum
 * @enum UI_ARGUMENT_FLAG_ENUM
 */
enum UI_ARGUMENT_FLAG_ENUM
{
    no_arguments,
    single_type_argument,
    argument_type_array
};

/**
 * @brief Parameters struct
 * \snippet InputHandler.h ui_parameters_struct_def
 */
struct Parameters
{
    //![ui_parameters_struct_def]
    uint8_t depth;
    uint8_t sub_commands;
    char command[USER_INPUT_MAX_COMMAND_LENGTH];
    uint16_t command_length;
    UI_ARGUMENT_FLAG_ENUM argument_flag;
    uint8_t num_args;
    uint8_t max_num_args;
    UITYPE _arg_type[USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS];
    //![ui_parameters_struct_def]
};
/** @} */

/**
 * @brief forward declaration of UserInput class for
 * CommandConstructor class
 */

class UserInput;
/**
 * @brief user command constructor
 */
class CommandConstructor
{
public:
    /**
     * @brief CommandConstructor Constructor
     *
     * Creates a new instance of this class.
     * Before using, construct a UserInput object and a CommandParameters object.
     * @param func pointer to a function
     * @param parameters pointer to parameters struct or array of parameters structs
     * @param subcommands number of subcommands
     * @param tree_depth depth of command tree
     */
    CommandConstructor(void (*func)(UserInput *),
                       const Parameters *parameters,
                       const uint8_t tree_depth = 0,
                       const uint8_t parameter_elements = 0)
        : function(func)
        , prm(parameters)
        , _tree_depth(tree_depth)
        , _param_array_len(parameter_elements)
        , next_command_parameters(NULL)
    {
    }
    void (*function)(UserInput *);
    const Parameters *prm;
    const uint8_t _tree_depth;
    const uint8_t _param_array_len;
    CommandConstructor *next_command_parameters; /** CommandConstructor iterator/pointer */
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
              const char *username = "",
              const char *end_of_line_characters = "\r\n",
              const char *token_delimiter = " ",
              const char *c_string_delimiter = "\"")
        : _output_buffer(output_buffer)
        , _output_enabled((output_buffer == NULL) ? false : true)
        , _string_pos(0)
        , _output_buffer_len(output_buffer_len)
        , _username_(username)
        , _term_(end_of_line_characters)
        , _delim_(token_delimiter)
        , _c_str_delim_(c_string_delimiter)
        , default_function_(NULL)
        , commands_head_(NULL)
        , commands_tail_(NULL)
        , commands_count_(0)
        , max_num_user_defined_args(0)
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
     * @param command reference to CommandConstructor
     */
    void AddCommand(CommandConstructor &command);

    /**
     * @brief read command(s) from a buffer
     *
     * @param data a buffer with characters
     * @param len the size of the buffer
     */
    void ReadCommandFromBuffer(uint8_t *data, size_t len);

    /**
     * @brief Get the Command From a Stream object
     *
     * @param stream the stream to reference
     * @param rx_buffer_size the size of our receive buffer
     */
    void GetCommandFromStream(Stream &stream, size_t rx_buffer_size = 32);

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
    void ListSettings(UserInput *inputprocess);

    /**
     * @brief Set the default function, which is the function called
     * when there is no command match, or when input is invalid.
     *
     * @param function a pointer to a user specified function
     */
    void DefaultFunction(void (*function)(UserInput *));

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

protected:
    /**
     * @brief Tries to get a token from an input string
     *
     * @param token_buffer the place where we store tokens
     * @param data input data
     * @param len length of input data
     * @param data_index index of data
     */
    bool getToken(char *token_buffer, uint8_t *data, size_t len, size_t *data_index);

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
     * @param opt command options reference
     */
    void launchFunction(const CommandConstructor *parameters);

    /**
     * @brief function launch logic
     *
     * @param cmd CommandConstructor ptr
     * @param prm Parameters reference
     * @param data uint8_t array ptr
     * @param len size_t array length
     * @param all_arguments_valid boolean array
     * @param data_index size_t array index
     * @param match boolean command match flag
     * @param input_type_match_flag boolean type match flag array
     */
    void launchLogic(CommandConstructor *cmd,
                     Parameters &prm,
                     uint8_t *data,
                     size_t len,
                     bool &all_arguments_valid,
                     size_t &data_index,
                     bool &match,
                     bool *input_type_match_flag);

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

    /**
     * @brief Get the UITYPE equivalent for the argument, internally we use uint8_t
     *
     * @param opt command options structure reference
     * @param index argument number
     * @return uint8_t argument type
     */
    uint8_t getArgType(Parameters &opt, size_t index = 0);

private:
    /*
        UserInput Constructor variables
    */
    char *_output_buffer;                   //  pointer to output char buffer
    bool _output_enabled;                   //  true if _output_buffer is not NULL
    size_t _string_pos;                     //  _output_buffer's index
    const size_t _output_buffer_len;        //  _output_buffer's size
    const char *_username_;                 //  username
    const char *_term_;                     //  end of line characters
    const char *_delim_;                    //  token delimiter
    const char *_c_str_delim_;              //  c-string delimiter
    void (*default_function_)(UserInput *); //  pointer to default function
    CommandConstructor *commands_head_;     //  pointer to object list
    CommandConstructor *commands_tail_;     //  pointer to object list
    size_t commands_count_;                 //  how many commands are there
    size_t max_num_user_defined_args;       //  max number of arguments used

    char _null_ = '\0'; //  char '\0'
    char _neg_ = '-';   //  char '-'
    char _dot_ = '.';   //  char '.'

    /*
        member function variables
    */
    bool _output_flag = false;                                             //   output is available flag, set by member functions
    char *token_buffer = NULL;                                             //   pointer to tokenized c-string
    char *data_pointers[USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS] = {0}; //   token_buffer pointers
    size_t data_pointers_index = 0;                                        //   data_pointer's index
    size_t rec_num_arg_strings = 0;                                        //   number of tokens after first valid token
    size_t subcommand_tokens = 0;

    /*
        GetCommandFromStream variables
    */
    bool stream_buffer_allocated = false; // this flag is set true on GetCommandFromStream entry if a buffer is not allocated
    bool new_stream_data = false;         // if there is new data in *stream_data this is true
    uint8_t *stream_data = NULL;          // pointer to stream input, a string of char
    uint16_t stream_data_index = 0;       // the index of stream_data
};

#endif
