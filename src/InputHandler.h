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
 * @brief Parameters argument_flag enum
 * @enum UI_ARGUMENT_FLAG_ENUM
 */
enum UI_ARGUMENT_FLAG_ENUM
{
    no_arguments,           ///<  no arguments expected
    single_type_argument,   ///<  every argument is of the same type
    argument_type_array     ///<  there is an array of input types
};

/**
 * @brief UserInput type specifier
 * @enum UITYPE
 */
enum class UITYPE
{
    UINT8_T,  ///<  8-bit unsigned integer
    UINT16_T, ///<  16-bit unsigned integer
    UINT32_T, ///<  32-bit unsigned integer
    INT16_T,  ///<  16-bit signed integer
    FLOAT,    ///<  32-bit float
    CHAR,     ///<  8-bit char
    C_STRING, ///<  array of 8-bit char
    NOTYPE,   ///<  no type validation
    NO_ARGS,  ///<  no arguments expected
    _LAST     ///<  reserved
};

/**
 * @brief type string literals
 * \snippet InputHandler.h ui_input_type_strings_pgm_def
 */
//![ui_input_type_strings_pgm_def]
const char ui_input_type_strings_pgm[10][UI_INPUT_TYPE_STRINGS_PGM_LEN] PROGMEM = 
{    
    "UINT8_T",      //  8-bit unsigned integer
    "UINT16_T",     //  16-bit unsigned integer
    "UINT32_T",     //  32-bit unsigned integer
    "INT16_T",      //  16-bit signed integer
    "FLOAT",        //  32-bit floating point number
    "CHAR",         //  single char
    "C-STRING",     //  c-string without spaces if not enclosed with ""
    "NOTYPE",       //  user defined NOTYPE
    "NO_ARGS",      //  no arguments expected
    "error"         //  error    
};

/**
 * @brief escaped control char
 * \snippet InputHandler.h ui_escaped_char_pgm_def
 */
//![ui_escaped_char_pgm_def]
const char ui_escaped_char_pgm[12][UI_ESCAPED_CHAR_PGM_LEN] PROGMEM =
{    
    "\\0",
    "\\a",
    "\\b",
    "\\t",    
    "\\n",
    "\\v",
    "\\f",
    "\\r",
    "\\e",    
    "\\\"",
    " ",
    "er"    
};

/**
 * @brief forward declaration of UserInput class for
 * Parameters struct and CommandConstructor class
 */

class UserInput;

/**
 * @brief Parameters struct, this is the container that holds your command parameters
 * \snippet InputHandler.h ui_parameters_struct_def
 */
struct Parameters
{
    //![ui_parameters_struct_def]
    void (*function)(UserInput *);
    char command[UI_MAX_CMD_LEN];
    uint16_t command_length;
    uint8_t depth;
    uint8_t sub_commands;
    UI_ARGUMENT_FLAG_ENUM argument_flag;
    uint8_t num_args;
    uint8_t max_num_args;
    UITYPE _arg_type[UI_MAX_ARGS];
    //![ui_parameters_struct_def]
};
/** @} */

/**
 * @brief user command constructor class
 */
class CommandConstructor
{
public:
    /**
     * @brief CommandConstructor Constructor
     * 
     * https://www.programiz.com/dsa/linked-list
     * 
     * These are chained together as a linked-list; this object contains a reference `next_command_parameters` to the next
     * node in the CommandConstructor linked-list.
     *
     * Before using, construct a UserInput object and a CommandParameters object.     
     * @param parameters pointer to parameters struct or array of parameters structs
     * @param parameter_elements number of elements in the parameter array
     * @param tree_depth depth of command tree    
     */
    CommandConstructor(const Parameters *parameters,
                       const uint8_t parameter_elements = 1,
                       const uint8_t tree_depth = 0)
        : prm(parameters)
        , _param_array_len(parameter_elements)
        , _tree_depth(tree_depth)        
        , next_command_parameters(NULL)
    {
    }    
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
     * @brief UserInput Constructor, no output by default
     *
     * @param output_buffer default NULL, if not NULL set _output_enabled == true
     * @param output_buffer_len default ZERO, set to length of output_buffer
     * @param username default NULL, set to project or equipment name
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
        , _term_index_(0)
        , default_function_(NULL)
        , commands_head_(NULL)
        , commands_tail_(NULL)
        , commands_count_(0)
        , _output_flag(false)
        , token_buffer(NULL)
        , data_pointers{NULL}
        , data_pointers_index(0)
        , data_pointers_index_max(0)
        , rec_num_arg_strings(0)
        , failed_on_subcommand(0)
        , _current_search_depth(1)
        , _null_('\0')
        , _neg_('-')
        , _dot_('.')
        , stream_buffer_allocated(false)
        , new_stream_data(false)
        , stream_data(NULL)
        , stream_data_index(0)
    {
    }

    /**
     * @brief returns a pointer to the next token in token_buffer or NULL if there are no more tokens
     *
     * @return char*
     */
    char *NextArgument();

    /**
     * @brief adds user commands to the input process
     *
     * @param command reference to CommandConstructor
     */
    void AddCommand(CommandConstructor &command);

    /**
     * @brief read command(s) from a uint8_t (unsigned char) buffer
     *
     * @param data a buffer with characters
     * @param len the size of the buffer
     */
    void ReadCommandFromBuffer(uint8_t *data, size_t len);

    /**
     * @brief Gets bytes from a Stream object and feeds a buffer to ReadCommandFromBuffer
     * 
     * https://www.arduino.cc/reference/en/language/functions/communication/stream/
     *
     * @param stream the stream to reference
     * @param rx_buffer_size the size of our receive buffer
     */
    void GetCommandFromStream(Stream &stream, size_t rx_buffer_size = 32);

    /**
     * @brief lists commands that will respond to user input
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
     * @brief clears output buffer, sets index to zero
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
     * 
     * @return true if there is a token
     * @return false for no token
     */
    bool getToken(char *token_buffer, uint8_t *data, size_t len, size_t *data_index);

    /**
     * @brief Tries to determine if input is valid
     *
     * @param arg_type the type of argument we are testing
     * @param data_pointers_index index of token pointers
     * 
     * @return true type is valid
     * @return false type not valid
     */
    bool validateUserInput(uint8_t arg_type, size_t data_pointers_index);

    /**
     * @brief launches a function
     *
     * @param cmd CommandConstructor pointer
     * @param prm Parameters struct reference
     * @param prm_idx Parameters array index
     * @param tokens_received amount of tokens in the token buffer
     */
    void launchFunction(CommandConstructor *cmd, Parameters& prm, uint8_t& prm_idx, size_t tokens_received);

    /**
     * @brief function launch logic
     *
     * @param cmd CommandConstructor ptr
     * @param prm Parameters reference
     * @param prm_idx Parameters array index
     * @param tokens_received number of tokens retreived from input data
     * @param all_arguments_valid boolean array     
     * @param match boolean command match flag
     * @param input_type_match_flag boolean type match flag array
     * @param subcommand_matched boolean subcommand match flag
     */
    void launchLogic(CommandConstructor *cmd,
                     Parameters &prm,
                     uint8_t& prm_idx,
                     size_t tokens_received,
                     bool &all_arguments_valid,
                     bool &match,
                     bool *input_type_match_flag,
                     bool &subcommand_matched);

    /**
     * @brief Escapes control characters so they will print
     *
     * @param input the input char
     * @param buf a reference to the output buffer
     * 
     * @return pointer to buf, so you can use this inside of _ui_out()
     */
    char* escapeCharactersSoTheyPrint(char input, char& buf);

    /**
     * @brief Triggers on a user input backslash, if the char immediately 
     * after the backslash would be a valid control char it returns the 
     * control char. ie if you input char(\) + char(r)  this will return 
     * the control character '\\r'
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
    
    /**
     * @brief validate the arguments as specified in the user defined Parameters struct
     * 
     * @param tokens_received how many tokens are left after matching is performed
     * @param input_type_match_flag input type validation flags
     * @param prm Parameters struct reference
     * @param all_arguments_valid error sentinel
     */
    void getArgs(size_t &tokens_received,
                 bool *input_type_match_flag,
                 Parameters &prm,
                 bool &all_arguments_valid);

private:
    /*
        UserInput Constructor variables
    */
    // user entered constructor variables
    char *_output_buffer;            //  pointer to the output char buffer
    bool _output_enabled;            //  true if _output_buffer is not NULL
    size_t _string_pos;              //  _output_buffer's index
    const size_t _output_buffer_len; //  _output_buffer's size

    const char *_username_;    //  username
    const char *_term_;        //  end of line characters
    const char *_delim_;       //  token delimiter
    const char *_c_str_delim_; //  c-string delimiter
    // end user entered constructor variables

    // constructor initialized variables
    size_t _term_index_;       //  eol index

    void (*default_function_)(UserInput *); //  pointer to default function
    CommandConstructor *commands_head_;     //  pointer to object list
    CommandConstructor *commands_tail_;     //  pointer to object list
    size_t commands_count_;                 //  how many commands are there

    bool _output_flag;                    // output is available flag, set by member functions
    char *token_buffer;                   // pointer to tokenized c-string
    char *data_pointers[UI_MAX_ARGS + 1]; // token_buffer pointers
    size_t data_pointers_index;           // data_pointer index
    size_t data_pointers_index_max;       // data_pointer index max
    size_t rec_num_arg_strings;           // number of tokens after first valid token
    size_t failed_on_subcommand;          // subcommand error index
    size_t _current_search_depth;         // current subcommand search depth
    char _null_;                          //  char '\0'
    char _neg_;                           //  char '-'
    char _dot_;                           //  char '.'

    bool stream_buffer_allocated; // this flag is set true on GetCommandFromStream entry if a buffer is not allocated
    bool new_stream_data;         // if there is new data in *stream_data this is true
    uint8_t *stream_data;         // pointer to stream input, a string of char
    size_t stream_data_index;     // the index of stream_data
    // end constructor initialized variables

    // private methods
    /**
     * @brief UserInput vsnprintf
     * https://www.cplusplus.com/reference/cstdio/vsprintf/
     * @param fmt   the format string
     * @param ...   arguments
     */
    void _ui_out(const char *fmt, ...);

    /**
     * @brief ReadCommandFromBuffer error output
     * 
     * @param cmd CommandConstructor pointer
     * @param prm Parameters struct reference
     * @param command_matched boolean reference     
     * @param input_type_match_flag boolean argument type match flag array
     * @param all_arguments_valid argument error sentinel
     * @param data raw data in
     */
    void _ReadCommandFromBufferErrorOutput(CommandConstructor *cmd,
                                           Parameters &prm,
                                           bool &command_matched,                                           
                                           bool *input_type_match_flag,
                                           bool &all_arguments_valid,
                                           uint8_t* data);
    // end private methods                                           
};

#endif
