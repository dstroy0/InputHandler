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
 * @defgroup UserInput class constants
 * @{
 */

/**
 * @brief command identifier enum
 * @enum UI_CMD_ID
 */
enum UI_CMD_ID
{
    root ///< this is the root command id
};

/**
 * @brief strongly typed argument handling flags
 * @enum UI_ARG_HANDLING
 */
enum class UI_ARG_HANDLING
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
const PROGMEM char UserInput_type_strings_pgm[10][UI_INPUT_TYPE_STRINGS_PGM_LEN] = {
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
 * @brief forward declaration of UserInput class for
 * Parameters struct and CommandConstructor class
 */
class UserInput;

/**
 * @brief Parameters struct, this is the container that holds your command parameters
 *
 * Every command and subcommand has an associated Parameters object, this is the information
 * that the input process needs to know about your command
 */
struct Parameters
{
    void (*function)(UserInput*);     ///< void function pointer, void your_function(UserInput *inputProcess)
    char command[UI_MAX_CMD_LEN + 1]; ///< command string + '\0'
    uint16_t command_length;          ///< command length in characters
    uint16_t parent_command_id;       ///< parent command's unique id root-65535
    uint16_t command_id;              ///< this command's unique id root-65535
    uint8_t depth;                    ///< command tree depth root-255
    uint8_t sub_commands;             ///< how many subcommands does this command have 0 - UI_MAX_SUBCOMMANDS
    UI_ARG_HANDLING argument_flag;    ///< argument handling flag
    uint8_t num_args;                 ///< minimum number of arguments this command expects 0 - UI_MAX_ARGS
    uint8_t max_num_args;             ///< maximum number of arguments this command expects 0 - UI_MAX_ARGS, cannot be less than num_args
    UITYPE arg_type_arr[UI_MAX_ARGS]; ///< argument UITYPE array
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
     * Linked-list primer: https://www.programiz.com/dsa/linked-list
     *
     * These constructors are chained together as a linked-list; this CommandConstructor
     * object contains a reference CommandConstructor::next_command to the next node
     * in the linked-list.  The list is linked together in UserInput::addCommand().
     *
     * Before using, construct a UserInput object and a Parameters object.
     * @param parameters pointer to parameters struct or array of parameters structs
     * @param parameter_array_elements number of elements in the parameter array
     * @param tree_depth depth of command tree
     */
    CommandConstructor(const Parameters* parameters,
                       const uint8_t parameter_array_elements = 1,
                       const uint8_t tree_depth = 0)
        : prm(parameters),
          param_array_len(parameter_array_elements),
          tree_depth(tree_depth + 1U),
          next_command(NULL)
    {
    }
    const Parameters* prm;            ///< pointer to PROGMEM Parameters array
    const uint8_t param_array_len;    ///< user input param array len, either as digits or through _N_prms
    const uint8_t tree_depth;         ///< user input depth + 1
    CommandConstructor* next_command; ///< CommandConstructor iterator/pointer
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
     * @brief UserInput constructor, no output by default
     *
     * UserInput has no output by default due to the default values passed in by the constructor.
     * The constructor disables output by setting `_output_enabled_` to false if output_buffer is
     * NULL.
     *
     * @param output_buffer default NULL, if not NULL the constructor will set `_output_enabled_` true
     * @param output_buffer_len default ZERO, size this to length of output_buffer
     * @param username default NULL, set to project, equipment, or user name
     * @param end_of_line_characters EOL term, default is '\\r\\n'
     * @param token_delimiter token demarcation
     * @param c_string_delimiter c-string demarcation
     * @param input_control_char_sequence two character sequence that precedes a switch char
     */
    UserInput(char* output_buffer = NULL,
              size_t output_buffer_len = 0,
              const char* username = NULL,
              const char* end_of_line_characters = "\r\n",
              const char* token_delimiter = " ",
              const char* c_string_delimiter = "\"",
              const char* input_control_char_sequence = "##")
        : _output_buffer_(output_buffer),
          _output_enabled_((output_buffer == NULL) ? false : true),
          _output_buffer_len_(output_buffer_len),
          _output_buffer_bytes_left_(output_buffer_len),
          _username_(username),
          _term_(end_of_line_characters),
          _delim_(token_delimiter),
          _c_str_delim_(c_string_delimiter),
          _control_char_sequence_(input_control_char_sequence),
          _term_index_(0),
          _default_function_(NULL),
          _commands_head_(NULL),
          _commands_tail_(NULL),
          _commands_count_(0),
          _output_flag_(false),
          _token_buffer_(NULL),
          _data_pointers_(NULL),
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
          _stream_data_index_(0),
          _begin_(false)
    {
    }

    /**
     * @brief Set the default function, which is the function called
     * when there is no command match, or when input is invalid.
     *
     * If this function is not NULL it will be called whenever there is invalid
     * input.
     * @param function a pointer to a user specified function
     */
    void defaultFunction(void (*function)(UserInput*));

    /**
     * @brief adds user commands to the input process
     *
     * This function inspects Parameters for errors and
     * reports the errors to the user if they have enabled output.
     * If an error is detected, in the root command or any of
     * its subcommands the entire command tree is rejected, and
     * no sizing for dynamically allocated variables takes place.
     *
     * @param command reference to CommandConstructor
     */
    void addCommand(CommandConstructor& command);

    /**
     * @brief allocates memory for `_data_pointers_`, sets `_begin_`
     *
     * @return true if allocation successful
     * @return false if allocation unsuccessful
     */
    bool begin();

    /**
     * @brief lists UserInput class settings
     *
     * Lists all pertinient process information:
     * class configuration, constructor variables,
     * and the amount of pointers that were dynamically
     * allocated in UserInput::begin()
     *
     * @param inputprocess pointer to class instance
     */
    void listSettings(UserInput* inputprocess);

    /**
     * @brief lists commands that will respond to user input if `_begin_` == true
     * else it will inform the user to use begin() in setup()
     */
    void listCommands();

    /**
     * @brief read command(s) from a uint8_t (unsigned char) buffer
     * silent return if `_begin_` == false
     * @param data a buffer with characters
     * @param len the size of the buffer
     * @param num_zdc size of Parameters pointers array
     * @param zdc array of Parameters pointers
     */
    void readCommandFromBuffer(uint8_t* data, size_t len, const size_t num_zdc = 0, const Parameters** zdc = NULL);

    /**
     * @brief Gets bytes from a Stream object and feeds a buffer to ReadCommandFromBuffer
     *
     * https://www.arduino.cc/reference/en/language/functions/communication/stream/
     *
     * silent return if `_begin_` == false
     * @param stream the stream to reference
     * @param rx_buffer_size the size of our receive buffer
     * @param num_zdc size of Parameters pointers array
     * @param zdc array of Parameters pointers
     */
    void getCommandFromStream(Stream& stream, size_t rx_buffer_size = 32, const size_t num_zdc = 0, const Parameters** zdc = NULL);

    /**
     * @brief returns a pointer to the next token in UserInput::_token_buffer_ or NULL if there are no more tokens
     *
     * @return char*
     */
    char* nextArgument();

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
    void outputToStream(Stream& stream);

    /**
     * @brief clears output buffer
     *
     * @param overwrite_contents boolean switch, clearOutputBuffer(true) writes null to entire _output_buffer_
     */
    void clearOutputBuffer(bool overwrite_contents = false);

    /**
     * @brief UserInput::getTokensParam UserInput::getTokens() parameters data structure
     */
    struct getTokensParam
    {
        uint8_t* data;                     ///< pointer to uint8_t array
        size_t len;                        ///< length of uint8_t array
        char* token_buffer;                ///< pointer to null terminated char array
        size_t token_buffer_len;           ///< size of data + 1 + 1(if there are zero delim commands)
        char** token_pointers;             ///< array of token_buffer pointers
        uint8_t& token_pointer_index;      ///< index of token_pointers
        size_t num_token_ptrs;             ///< token_pointers[MAX]
        const char** delimiter_strings;    ///< array of const char* delimiter strings
        size_t* delimiter_lens;            ///< strlen of each delimiter
        size_t num_delimiters;             ///< delimiter_strings[MAX] && delimiter_lens[MAX]
        const char* c_str_delim;           ///< const char* c string delimiter
        size_t c_str_delim_len;            ///< strlen of c string delimiter
        char& token_buffer_sep;            ///< token_buffer token delimiter
        const char* control_char_sequence; ///< two character sequence preceding a switch char
    };

    /**
     * @brief puts tokens into the token buffer pointed to in getTokensParam
     *
     * @param gtprm UserInput::getTokensParam struct reference
     * @return size_t number of tokens retrieved
     */
    size_t getTokens(getTokensParam& gtprm);

    /**
     * @brief Tries to determine if input is valid in NULL TERMINATED char arrays
     *
     * @param arg_type the UITYPE to test
     * @param token_pointers pointers to null separated tokens
     * @param token_pointer_index index of token_pointers to test
     * @param neg_sign single char neg sign, if different than '-' parseInt and the like will not assign your input negative
     * @param float_sep whole and fraction separator
     *
     * @return true argument-type is valid
     * @return false argument-type is not valid
     */
    bool validateNullSepInput(UITYPE arg_type,
                              char** token_pointers,
                              size_t token_pointer_index,
                              char& neg_sign,
                              char& float_sep);

protected:
    /**
     * @brief transform 2d matrix indices to flat array index
     *
     * use this to access a dynamically allocated array like a 2d matrix,
     * this is much more performant than looping to allocate a (n>1)d array,
     * and looping again to free allocated ram.
     *
     * @param m_width width of the matrix
     * @param row row you want to access
     * @param col column you want to access
     * @return size_t the transformed index
     */
    size_t mIndex(size_t m_width, size_t row, size_t col) const
    {
        return row + m_width * col;
    }

private:
    /*
        UserInput Constructor variables
    */
    // user entered constructor variables
    char* _output_buffer_;               ///< pointer to the output char buffer
    bool _output_enabled_;               ///< true if _output_buffer_ is not NULL (the user has defined and passed an output buffer to UserInput's constructor)
    const uint16_t _output_buffer_len_;  ///< _output_buffer_ size in bytes
    uint16_t _output_buffer_bytes_left_; ///< index of _output_buffer_, messages are appended to the output buffer and this keeps track of where to write to next without overwriting

    const char* _username_;              ///< username/project name/equipment name
    const char* _term_;                  ///< end of line characters, terminating characters, default is CRLF
    uint8_t _term_len_;                  ///< _term_ length in characters, determined in begin()
    const char* _delim_;                 ///< input argument delimiter, space by default
    uint8_t _delim_len_;                 ///< _delim_ length in characters, determined in begin()
    const char* _c_str_delim_;           ///< c-string delimiter, default is enclosed with quotation marks "c-string"
    uint8_t _c_str_delim_len_;           ///< _c_str_delim_ length in characters, determined in begin()
    const char* _control_char_sequence_; ///< input a control char sequence
    // end user entered constructor variables

    // constructor initialized variables
    uint8_t _term_index_; ///< _term_ index, match all characters in term or reject the message

    void (*_default_function_)(UserInput*); ///< pointer to the default function
    CommandConstructor* _commands_head_;    ///< pointer to object list
    CommandConstructor* _commands_tail_;    ///< pointer to object list
    uint8_t _commands_count_;               ///< how many commands are there
    uint8_t _max_depth_;                    ///< max command depth found
    uint8_t _max_args_;                     ///< max command or subcommand arguments found

    bool _output_flag_;                ///< output is available flag, set by member functions
    char* _token_buffer_;              ///< pointer to tokenized c-string
    char** _data_pointers_;            ///< token_buffer pointers
    uint8_t _data_pointers_index_;     ///< data_pointer index
    uint8_t _data_pointers_index_max_; ///< data_pointer index max
    uint8_t _rec_num_arg_strings_;     ///< number of tokens after first valid token
    uint8_t _failed_on_subcommand_;    ///< subcommand error index
    uint8_t _current_search_depth_;    ///< current subcommand search depth
    char _null_;                       ///< char '\0'
    char _neg_;                        ///< char '-'
    char _dot_;                        ///< char '.'

    bool _stream_buffer_allocated_; ///< this flag is set true on GetCommandFromStream entry if a buffer is not allocated
    bool _new_stream_data_;         ///< if there is new data in *stream_data this is true
    uint8_t* _stream_data_;         ///< pointer to stream input, a string of char
    uint16_t _stream_data_index_;   ///< the index of stream_data

    bool _begin_; ///< begin() error flag
    // end constructor initialized variables

    // private methods
    /**
     * @brief UserInput vsnprintf
     * https://www.cplusplus.com/reference/cstdio/vsprintf/
     * @param fmt   the format string
     * @param ...   arguments
     */
    void _ui_out(const char* fmt, ...);

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
    void _readCommandFromBufferErrorOutput(CommandConstructor* cmd,
                                           Parameters& prm,
                                           bool& command_matched,
                                           bool* input_type_match_flag,
                                           bool& all_arguments_valid,
                                           uint8_t* data);

    /**
     * @brief launches either (this) function or the root command function
     *
     * @param cmd CommandConstructor pointer
     * @param prm Parameters struct reference
     * @param tokens_received amount of tokens in the token buffer
     */
    void _launchFunction(CommandConstructor* cmd, Parameters& prm, size_t tokens_received);

    /**
     * @brief UserInput:_launchLogic() parameters structure
     */
    struct _launchLogicParam
    {
        CommandConstructor* cmd;     ///< CommandConstructor ptr
        Parameters& prm;             ///< Parameters struct reference
        size_t tokens_received;      ///< number of tokens retrieved from input data
        bool& all_arguments_valid;   ///< boolean array
        bool& launch_attempted;      ///< launch attempted flag
        bool* input_type_match_flag; ///< boolean type match flag array
        bool& subcommand_matched;    ///< boolean subcommand match flag
        uint16_t& command_id;        ///< 16 bit command id
    };
    /**
     * @brief function launch logic, recursive on subcommand match
     *
     * @param LLprm
     */
    void _launchLogic(_launchLogicParam& LLprm);

    /**
     * @brief Escapes control characters so they will print
     *
     * @param input the input char
     * @param buf the output buffer
     *
     * @return pointer to buf, so you can use this inside of _ui_out()
     */
    char* _escapeCharactersSoTheyPrint(char input, char* buf);

    /**
     * @brief Triggers on a control character sequence, if the char immediately
     * after the control char is a char known to UserInput::_combineControlCharacters
     * this returns a control char, else it returns the input char
     *
     * @param input the char the control character sequence
     * @return the control character char value ie '\\r'
     */
    char _combineControlCharacters(char input);

    /**
     * @brief determines if input Parameters struct is valid before adding to linked-list
     *
     * @param cmd CommandConstructor reference
     * @param prm reference to Parameters struct in addCommand
     * @return true if there are no errors
     * @return false if there were one or more errors
     */
    bool _addCommandAbort(CommandConstructor& cmd, Parameters& prm);

    /**
     * @brief Get the UITYPE equivalent for the argument, internally we use uint8_t
     *
     * @param prm command options structure reference
     * @param index argument number
     * @return UITYPE argument type
     */
    UITYPE _getArgType(Parameters& prm, size_t index = 0);

    /**
     * @brief validate the arguments as specified in the user defined Parameters struct
     *
     * @param tokens_received how many tokens are left after matching is performed
     * @param input_type_match_flag input type validation flags
     * @param prm Parameters struct reference
     * @param all_arguments_valid error sentinel
     */
    void _getArgs(size_t& tokens_received,
                  bool* input_type_match_flag,
                  Parameters& prm,
                  bool& all_arguments_valid);

    /**
     * @brief adds escaped control characters to a buffer
     *
     * @param buf output buffer
     * @param idx buffer index
     * @param input string to escape
     * @param input_len length of string
     * @return pointer to null terminated escaped control char string
     */
    char* _addEscapedControlCharToBuffer(char* buf, size_t& idx, const char* input, size_t input_len);

    /**
     * @brief find delimiters in input data
     *
     * @param gtprm reference to getTokensParam struct in getTokens
     * @param data_pos data index
     * @param token_buffer_index token_buffer index
     * @param point_to_beginning_of_token boolean sentinel
     */
    void _getTokensDelimiters(getTokensParam& gtprm, size_t& data_pos, size_t& token_buffer_index, bool& point_to_beginning_of_token);

    /**
     * @brief get delimited c-strings from input data
     *
     * @param gtprm reference to getTokensParam struct in getTokens
     * @param data_pos data index
     * @param token_buffer_index token_buffer index
     * @param point_to_beginning_of_token boolean sentinel
     */
    void _getTokensCstrings(getTokensParam& gtprm, size_t& data_pos, size_t& token_buffer_index, bool& point_to_beginning_of_token);

    /**
     * @brief add uchar to token_buffer
     *
     * @param gtprm reference to getTokensParam struct in getTokens
     * @param data_pos data index
     * @param token_buffer_index token_buffer index
     * @param point_to_beginning_of_token boolean sentinel
     */
    void _getTokensChar(getTokensParam& gtprm, size_t& data_pos, size_t& token_buffer_index, bool& point_to_beginning_of_token);

    /**
     * @brief split a zero delimiter command, separate command and string with token delimiter for further processing
     *
     * @param data uint8_t array
     * @param len data len
     * @param token_buffer pointer to char array
     * @param token_buffer_len len of char array
     * @param num_zdc number of zero delim commands
     * @param zdc pointers to zero delim commands
     */
    void _splitZDC(uint8_t* data, size_t len, char* token_buffer, size_t token_buffer_len, const size_t num_zdc, const Parameters** zdc);
    // end private methods
};

#endif
