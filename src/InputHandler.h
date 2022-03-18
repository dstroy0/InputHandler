/**
 * @file InputHandler.h
 * @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
 * @brief InputHandler library header file
 * @version 1.0
 * @date 2022-03-02
 *
 * @copyright Copyright (c) 2022
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
 * @defgroup Constants
 * @{
 */

/**
 * @brief Parameters argument_flag enum
 * @enum UI_ARGUMENT_FLAG_ENUM
 */
enum UI_ARGUMENT_FLAG_ENUM
{
    no_args,  ///<  no arguments expected
    one_type, ///<  every argument is of the same type
    type_arr  ///<  there is an array of input types
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
 * input type string literal PROGMEM array
 * @brief type string literals
 */
const PROGMEM char UserInput_type_strings_pgm[10][UI_INPUT_TYPE_STRINGS_PGM_LEN] =
    {
        "UINT8_T",  // 8-bit unsigned integer
        "UINT16_T", // 16-bit unsigned integer
        "UINT32_T", // 32-bit unsigned integer
        "INT16_T",  // 16-bit signed integer
        "FLOAT",    // 32-bit floating point number
        "CHAR",     // single char
        "C-STRING", // c-string without spaces if not enclosed with ""
        "NOTYPE",   // user defined NOTYPE
        "NO_ARGS",  // no arguments expected
        "error"     // error
};

/**
 * escaped char string literal PROGMEM array
 * @brief escaped control char
 */
const PROGMEM char UserInput_escaped_char_pgm[12][UI_ESCAPED_CHAR_PGM_LEN] =
    {
        "\\0",  // null
        "\\a",  // bell
        "\\b",  // backspace
        "\\t",  // horizontal tab
        "\\n",  // newline
        "\\v",  // vertical tab
        "\\f",  // form feed
        "\\r",  // carriage return
        "\\e",  // GCC escape sequence
        "\\\"", // quotation mark
        " ",    // space
        "er"    // error
};

/**
 * @brief forward declaration of UserInput class for
 * Parameters struct and CommandConstructor class
 */
class UserInput;

/**
 * User Command Parameters struct
 * @brief Parameters struct, this is the container that holds your command parameters
 */
struct Parameters
{
    void (*function)(UserInput *);       ///< function pointer
    char command[UI_MAX_CMD_LEN];        ///< command string array
    uint16_t command_length;             ///< command length in characters
    uint8_t depth;                       ///< command tree depth
    uint8_t sub_commands;                ///< how many subcommands does this command have
    UI_ARGUMENT_FLAG_ENUM argument_flag; ///< argument handling flag
    uint8_t num_args;                    ///< minimum number of arguments this command expects
    uint8_t max_num_args;                ///< maximum number of arguments this command expects
    UITYPE _arg_type[UI_MAX_ARGS];       ///< argument type array
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
        : prm(parameters), 
          _param_array_len(parameter_elements), 
          _tree_depth(tree_depth), 
          next_command_parameters(NULL)
    {
    }
    const Parameters *prm;
    const uint8_t _tree_depth;
    const uint8_t _param_array_len;
    CommandConstructor *next_command_parameters; /** CommandConstructor iterator/pointer */
};

/**
 * @brief User input handler methods
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
        : _output_buffer_(output_buffer),
          _output_enabled_((output_buffer == NULL) ? false : true),
          _string_pos_(0),
          _output_buffer_len_(output_buffer_len),
          _username_(username),
          _term_(end_of_line_characters),
          _delim_(token_delimiter),
          _c_str_delim_(c_string_delimiter),
          _term_index_(0),
          _default_function_(NULL),
          _commands_head_(NULL),
          _commands_tail_(NULL),
          _commands_count_(0),
          _output_flag_(false),
          _token_buffer_(NULL),
          _data_pointers_{NULL},
          _data_pointers_index_(0),
          _data_pointers_index_max_(0),
          _rec_num_arg_strings_(0),
          _failed_on_subcommand_(0),
          _current_search_depth_(1),
          _null_('\0'),
          _neg_('-'),
          _dot_('.'),
          _stream_buffer_allocated_(false),
          _new_stream_data_(false),
          _stream_data_(NULL),
          _stream_data_index_(0)
    {
    }

    /**
     * @brief lists UserInput class settings
     *
     * @param inputprocess pointer to class instance
     */
    void listSettings(UserInput *inputprocess);

    /**
     * @brief Set the default function, which is the function called
     * when there is no command match, or when input is invalid.
     *
     * @param function a pointer to a user specified function
     */
    void defaultFunction(void (*function)(UserInput *));

    /**
     * @brief adds user commands to the input process
     *
     * @param command reference to CommandConstructor
     */
    void addCommand(CommandConstructor &command);

    /**
     * @brief lists commands that will respond to user input
     *
     */
    void listCommands();

    /**
     * @brief read command(s) from a uint8_t (unsigned char) buffer
     *
     * @param data a buffer with characters
     * @param len the size of the buffer
     */
    void readCommandFromBuffer(uint8_t *data, size_t len);

    /**
     * @brief Gets bytes from a Stream object and feeds a buffer to ReadCommandFromBuffer
     *
     * https://www.arduino.cc/reference/en/language/functions/communication/stream/
     *
     * @param stream the stream to reference
     * @param rx_buffer_size the size of our receive buffer
     */
    void getCommandFromStream(Stream &stream, size_t rx_buffer_size = 32);

    /**
     * @brief returns a pointer to the next token in token_buffer or NULL if there are no more tokens
     *
     * @return char*
     */
    char *nextArgument();

    /**
     * @brief is class output available
     *
     * @return true if output is available
     * @return false if no output is available
     */
    bool outputIsAvailable();

    /**
     * @brief is class output enabled
     *
     * @return true if enabled
     * @return false if not enabled
     */
    bool outputIsEnabled();

    /**
     * @brief direct class output to stream, clears output buffer automatically
     *
     * @param stream the stream to print to
     */
    void outputToStream(Stream &stream);

    /**
     * @brief clears output buffer, sets index to zero
     *
     */
    void clearOutputBuffer();

protected:
    /**
     * @brief Tries to get a token from an input string
     *
     * @param data input data
     * @param len length of input data
     * @param data_index index of data
     *
     * @return true if there is a token
     * @return false for no token
     */
    bool getToken(uint8_t *data, size_t len, size_t *data_index);

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
     * @brief Get the UITYPE equivalent for the argument, internally we use uint8_t
     *
     * @param opt command options structure reference
     * @param index argument number
     * @return uint8_t argument type
     */
    uint8_t getArgType(Parameters &prm, size_t index = 0);

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
    char *_output_buffer_;            ///< pointer to the output char buffer
    bool _output_enabled_;            ///< true if _output_buffer is not NULL
    size_t _string_pos_;              ///< _output_buffer's index
    const size_t _output_buffer_len_; ///< _output_buffer's size

    const char *_username_;    ///< username
    const char *_term_;        ///< end of line characters
    const char *_delim_;       ///< token delimiter
    const char *_c_str_delim_; ///< c-string delimiter
    // end user entered constructor variables

    // constructor initialized variables
    size_t _term_index_; ///< eol index

    void (*_default_function_)(UserInput *); ///< pointer to default function
    CommandConstructor *_commands_head_;     ///< pointer to object list
    CommandConstructor *_commands_tail_;     ///< pointer to object list
    size_t _commands_count_;                 ///< how many commands are there

    bool _output_flag_;                     ///< output is available flag, set by member functions
    char *_token_buffer_;                   ///< pointer to tokenized c-string
    char *_data_pointers_[UI_MAX_ARGS + 1]; ///< token_buffer pointers
    size_t _data_pointers_index_;           ///< data_pointer index
    size_t _data_pointers_index_max_;       ///< data_pointer index max
    size_t _rec_num_arg_strings_;           ///< number of tokens after first valid token
    size_t _failed_on_subcommand_;          ///< subcommand error index
    size_t _current_search_depth_;          ///< current subcommand search depth
    char _null_;                            ///< char '\0'
    char _neg_;                             ///< char '-'
    char _dot_;                             ///< char '.'

    bool _stream_buffer_allocated_; ///< this flag is set true on GetCommandFromStream entry if a buffer is not allocated
    bool _new_stream_data_;         ///< if there is new data in *stream_data this is true
    uint8_t *_stream_data_;         ///< pointer to stream input, a string of char
    size_t _stream_data_index_;     ///< the index of stream_data
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
    void _readCommandFromBufferErrorOutput(CommandConstructor *cmd,
                                           Parameters &prm,
                                           bool &command_matched,
                                           bool *input_type_match_flag,
                                           bool &all_arguments_valid,
                                           uint8_t *data);

    /**
     * @brief launches a function
     *
     * @param cmd CommandConstructor pointer
     * @param prm Parameters struct reference
     * @param prm_idx Parameters array index
     * @param tokens_received amount of tokens in the token buffer
     */
    void _launchFunction(CommandConstructor *cmd, Parameters &prm, uint8_t &prm_idx, size_t tokens_received);

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
    void _launchLogic(CommandConstructor *cmd,
                      Parameters &prm,
                      uint8_t &prm_idx,
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
    char *_escapeCharactersSoTheyPrint(char input, char &buf);

    /**
     * @brief Triggers on a user input backslash, if the char immediately
     * after the backslash would be a valid control char it returns the
     * control char. ie if you input char(\) + char(r)  this will return
     * the control character '\\r'
     *
     * @param input the char after a backslash ie 'r'
     * @return the control character char value ie '\\r'
     */
    char _combineControlCharacters(char input);
    // end private methods
};

#endif
