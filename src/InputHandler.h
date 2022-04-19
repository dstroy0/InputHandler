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
 * @brief command wildcard flag enum
 * @enum UI_WC_FLAG
 */
enum UI_WC_FLAG
{
    no_wildcards = false, ///< this command has no wildcard char (false (0))
    has_wildcards = true  ///< this command contains one or more wildcard char (true (1))
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
    UINT8_T,    ///<  8-bit unsigned integer
    UINT16_T,   ///<  16-bit unsigned integer
    UINT32_T,   ///<  32-bit unsigned integer
    INT16_T,    ///<  16-bit signed integer
    FLOAT,      ///<  32-bit float
    CHAR,       ///<  8-bit char
    START_STOP, ///<  array of 8-bit char
    NOTYPE,     ///<  no type validation
    NO_ARGS,    ///<  no arguments expected
    _LAST       ///<  reserved
};

/**
 * input type string literal PROGMEM array
 * @brief type string literals
 */
const PROGMEM char UserInput_type_strings_pgm[10][UI_INPUT_TYPE_STRINGS_PGM_LEN] = {
    "UINT8_T",   // 8-bit unsigned integer
    "UINT16_T",  // 16-bit unsigned integer
    "UINT32_T",  // 32-bit unsigned integer
    "INT16_T",   // 16-bit signed integer
    "FLOAT",     // 32-bit floating point number
    "CHAR",      // single char
    "STARTSTOP", // c-string enclosed with start/stop delimiters
    "NOTYPE",    // user defined NOTYPE
    "NO_ARGS",   // no arguments expected
    "error"      // error
};

/**
 * @brief InputProcessDelimiterSequences struct holds user defined input data delimiters
 *
 */
struct InputProcessDelimiterSequences
{
    size_t num_seq;                                                   ///< the number of token delimiters in delimiter_sequences
    uint8_t delimiter_lens[UI_MAX_DELIM_SEQ];                         ///< delimiter sequence lens
    char delimiter_sequences[UI_MAX_DELIM_SEQ][UI_DELIM_SEQ_PGM_LEN]; ///< string-literal "" delimiter sequence array
};

/**
 * @brief InputProcessStartStopSequences struct holds regex-like start-stop match sequence pairs
 *
 */
struct InputProcessStartStopSequences
{
    size_t num_seq;                                                                   ///< num start/stop sequences
    uint8_t start_stop_sequence_lens[UI_MAX_START_STOP_SEQ];                          ///< start stop sequence lens
    char start_stop_sequence_pairs[UI_MAX_START_STOP_SEQ][UI_START_STOP_SEQ_PGM_LEN]; ///< start/stop sequences.  Match start, match end, copy what is between
};

/**
 * @brief IH_pname is a char array typedef the size of UI_PROCESS_NAME_PGM_LEN
 *
 */
typedef char IH_pname[UI_PROCESS_NAME_PGM_LEN];

/**
 * @brief IH_eol is a char array typedef the size of UI_EOL_SEQ_PGM_LEN
 *
 */
typedef char IH_eol[UI_EOL_SEQ_PGM_LEN];

/**
 * @brief IH_input_cc is a char array typedef the size of UI_INPUT_CONTROL_CHAR_SEQ_PGM_LEN
 *
 */
typedef char IH_input_cc[UI_INPUT_CONTROL_CHAR_SEQ_PGM_LEN];

/**
 * @brief IH_wcc is a two char array that represents the wildcard char and a null terminator
 *
 */
typedef char IH_wcc[2];

/**
 * @brief UserInput input process parameters, constructor parameters
 *
 */
struct InputProcessParameters
{
    const IH_pname* pname;                           ///< this process' name, can be NULL
    const IH_eol* peol;                              ///< end of line term
    const IH_input_cc* pinputcc;                     ///< two char len sequence to input a control char
    const IH_wcc* pwcc;                              ///< single char wildcard char
    const InputProcessDelimiterSequences* pdelimseq; ///< reference to InputProcessDelimiterSequences struct
    const InputProcessStartStopSequences* pststpseq; ///< reference to InputProcessStartStopSequences struct
};

const PROGMEM IH_pname _pname = "";         ///< default process name
const PROGMEM IH_eol _peol = "\r\n";        ///< default process eol characters
const PROGMEM IH_input_cc _pinputcc = "##"; ///< default process input control character sequence
const PROGMEM IH_wcc _pwcc = "*";           ///< default process wildcard char

/**
 * @brief default delimiter sequences
 *
 */
const PROGMEM InputProcessDelimiterSequences _pdelimseq = {
    2,         ///< number of delimiter sequences
    {1, 1},    ///< delimiter sequence lens
    {" ", ","} ///< delimiter sequences
};

/**
 * @brief default start stop sequences
 *
 */
const PROGMEM InputProcessStartStopSequences _pststpseq = {
    1,           ///< num start stop sequence pairs
    {1, 1},      ///< start stop sequence lens
    {"\"", "\""} ///< start stop sequence pairs
};

/**
 * @brief UserInput default InputProcessParameters
 *
 */
const PROGMEM InputProcessParameters _DEFAULT_UI_INPUT_PRM_ = {
    &_pname,     ///< process name
    &_peol,      ///< process eol term
    &_pinputcc,  ///< process input control char sequence
    &_pwcc,      ///< process wildcard char
    &_pdelimseq, ///< process default delimiter sequences
    &_pststpseq  ///< process default start/stop sequences
};

/**
 * @brief forward declaration of UserInput class for
 * CommandParameters struct and CommandConstructor class
 */
class UserInput;

/**
 * @brief CommandRuntimeCalc struct contains arrays and indices determined at runtime
 *
 */
struct CommandRuntimeCalc
{
    uint8_t num_prm_with_wc;             ///< the number of Parameters structs in this command that contain IH_wcc[0]; the WildCard Character
    uint8_t* idx_of_prm_with_wc;         ///< indices of Parameters struct that contain wcc
    uint8_t* num_memcmp_ranges_this_row; ///< the number of memcmp ranges for this Parameters command string, array members always an even number
    uint8_t** memcmp_ranges_arr;         ///< 2d array[row][col], each [row] is for one Parameters command string which contains wcc
};

/**
 * @brief CommandParameters struct, this is the container that holds your command parameters
 *
 * Every command and subcommand has an associated CommandParameters object, this is the information
 * that the input process needs to know about your command
 */
struct CommandParameters
{
    void (*function)(UserInput*);      ///< void function pointer, void your_function(UserInput *inputProcess)
    bool has_wildcards;                ///< if true this command has one or more wildcard char
    char command[UI_MAX_CMD_LEN + 1U]; ///< command string + '\0'
    uint16_t command_length;           ///< command length in characters
    uint16_t parent_command_id;        ///< parent command's unique id root-65535
    uint16_t command_id;               ///< this command's unique id root-65535
    uint8_t depth;                     ///< command tree depth root-255
    uint8_t sub_commands;              ///< how many subcommands does this command have 0 - UI_MAX_SUBCOMMANDS
    UI_ARG_HANDLING argument_flag;     ///< argument handling flag
    uint8_t num_args;                  ///< minimum number of arguments this command expects 0 - UI_MAX_ARGS
    uint8_t max_num_args;              ///< maximum number of arguments this command expects 0 - UI_MAX_ARGS, cannot be less than num_args
    UITYPE arg_type_arr[UI_MAX_ARGS];  ///< argument UITYPE array
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
     * Before using, construct a UserInput object and a CommandParameters object.
     * @param parameters pointer to parameters struct or array of parameters structs
     * @param parameter_array_elements number of elements in the parameter array
     * @param tree_depth depth of command tree
     */
    CommandConstructor(const CommandParameters* parameters,
                       const uint8_t parameter_array_elements = 1,
                       const uint8_t tree_depth = 0)
        : prm(parameters),
          param_array_len(parameter_array_elements),
          tree_depth(tree_depth + 1U),
          calc(NULL),
          next_command(NULL)
    {
    }
    const CommandParameters* prm;     ///< pointer to PROGMEM CommandParameters array
    const uint8_t param_array_len;    ///< user input param array len, either as digits or through nprms
    const uint8_t tree_depth;         ///< user input depth + 1
    CommandRuntimeCalc* calc;         ///< pointer to CommandRuntimeCalc struct
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
     * @param output_buffer char buffer
     * @param output_buffer_len size of output_buffer buffsz(output_buffer)
     * @param input_prm InputProcessParameters struct
     */
    UserInput(char* output_buffer = NULL, size_t output_buffer_len = 0, const InputProcessParameters* input_prm = NULL)
        : _output_buffer_(output_buffer),
          _output_buffer_len_(output_buffer_len),
          _input_prm_ptr_((input_prm == NULL) ? &_DEFAULT_UI_INPUT_PRM_ : input_prm),
          _output_enabled_((output_buffer == NULL) ? false : true),
          _output_buffer_bytes_left_(output_buffer_len),
          _term_len_(strlen_P(((input_prm == NULL) ? (char*)_DEFAULT_UI_INPUT_PRM_.peol : (char*)input_prm->peol))),
          _term_index_(0),
          _default_function_(NULL),
          _commands_head_(NULL),
          _commands_tail_(NULL),
          _commands_count_(0),
          _max_depth_(0),
          _max_args_(0),
          _input_type_match_flags_(NULL),
          _output_flag_(false),
          _token_buffer_(NULL),
          _data_pointers_(NULL),
          _data_pointers_index_(0),
          _data_pointers_index_max_(0),
          _p_num_ptrs_(0),
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
        memcpy_P(&_input_prm_, _input_prm_ptr_, sizeof(_input_prm_));
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
     * This function inspects CommandParameters for errors and
     * reports the errors to the user if they have enabled output.
     * If an error is detected in the root command or any of
     * its subcommands, the entire command tree is rejected.
     * No sizing for dynamically allocated variables takes place.
     *
     * @param command reference to CommandConstructor
     */
    void addCommand(CommandConstructor& command);

    /**
     * @brief Allocates memory for `_data_pointers_`, sets `_begin_`
     *
     * @return true if allocation successful
     * @return false if allocation unsuccessful
     */
    bool begin();

    /**
     * @brief Lists UserInput class settings, useful for implementation debugging. REQUIRES 570 byte output_buffer.
     *
     * Lists all pertinient process information:
     * class configuration, constructor variables,
     * and the amount of pointers that were dynamically
     * allocated in UserInput::begin()
     *
     * REQUIRES 570 byte output_buffer.  If an insufficient buffer size is declared,
     * UserInput::_ui_out() will warn the user to increase the buffer to the required size.
     *
     * @param inputProcess pointer to class instance
     */
    void listSettings(UserInput* inputProcess);

    /**
     * @brief Lists commands that will respond to user input if `_begin_` == true
     * else it will inform the user to use begin() in setup()
     */
    void listCommands();

    /**
     * @brief read command(s) from a uint8_t (unsigned char) buffer
     * silent return if `_begin_` == false
     * @param data a buffer with characters
     * @param len the size of the buffer
     * @param num_zdc size of CommandParameters pointers array
     * @param zdc array of CommandParameters pointers
     */
    void readCommandFromBuffer(uint8_t* data, size_t len, const size_t num_zdc = 0, const CommandParameters** zdc = NULL);

    /**
     * @brief Gets bytes from a Stream object and feeds a buffer to ReadCommandFromBuffer
     *
     * https://www.arduino.cc/reference/en/language/functions/communication/stream/
     *
     * silent return if `_begin_` == false
     * @param stream the stream to reference
     * @param rx_buffer_size the size of our receive buffer
     * @param num_zdc size of CommandParameters pointers array
     * @param zdc array of CommandParameters pointers
     */
    void getCommandFromStream(Stream& stream, size_t rx_buffer_size = 32, const size_t num_zdc = 0, const CommandParameters** zdc = NULL);

    /**
     * @brief returns a pointer to the next token in UserInput::_token_buffer_ or NULL if there are no more tokens
     *
     * @return char*
     */
    char* nextArgument();

    /**
     * @brief returns a pointer to `argument_number` token in UserInput::_token_buffer_ or NULL if there is no `argument_number` token
     *
     * @return char*
     */
    char* getArgument(size_t argument_number);

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
        uint8_t* data;                ///< pointer to uint8_t array
        size_t len;                   ///< length of uint8_t array
        char* token_buffer;           ///< pointer to null terminated char array
        size_t token_buffer_len;      ///< size of data + 1 + 1(if there are zero delim commands)
        size_t num_token_ptrs;        ///< token_pointers[MAX]
        uint8_t& token_pointer_index; ///< index of token_pointers
        char** token_pointers;        ///< array of token_buffer pointers
        char& token_buffer_sep;       ///< token_buffer token delimiter
    };

    /**
     * @brief puts tokens into the token buffer pointed to in getTokensParam
     *
     * @param gtprm UserInput::getTokensParam struct reference
     * @param input_prm reference to InputProcessParameters struct
     *
     * @return size_t number of tokens retrieved
     */
    size_t getTokens(getTokensParam& gtprm, const InputProcessParameters& input_prm);

    /**
     * @brief validateNullSepInputParam struct
     *
     */
    struct validateNullSepInputParam
    {
        UITYPE arg_type;            ///< the UITYPE to test
        char** token_pointers;      ///< pointers to null separated tokens
        size_t token_pointer_index; ///< index of token_pointers to test
        char& neg_sign;             ///< single char neg sign, if different than '-' parseInt and the like will not assign your input negative
        char& float_sep;            ///< whole and fraction separator
    };

    /**
     * @brief Tries to determine if input is valid in NULL TERMINATED char arrays
     *
     * @param vprm validateNullSepInputParam struct reference
     *
     * @return true argument-type is valid
     * @return false argument-type is not valid
     */
    bool validateNullSepInput(validateNullSepInputParam& vprm);

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

    // (potentially) user entered constructor variables
    char* _output_buffer_;                         ///< pointer to the output char buffer
    size_t _output_buffer_len_;                    ///< _output_buffer_ size in bytes
    const InputProcessParameters* _input_prm_ptr_; ///< user input constructor parameters pointer
    // end user entered constructor variables

    bool _output_enabled_;             ///< true if _output_buffer_ is not NULL (the user has defined and passed an output buffer to UserInput's constructor)
    size_t _output_buffer_bytes_left_; ///< index of _output_buffer_, messages are appended to the output buffer and this keeps track of where to write to next without overwriting

    uint8_t _term_len_;   ///< _term_ length in characters, determined in begin()
    uint8_t _term_index_; ///< _term_ index, match all characters in term or reject the message

    void (*_default_function_)(UserInput*); ///< pointer to the default function

    // linked-list
    CommandConstructor* _commands_head_; ///< pointer to object list
    CommandConstructor* _commands_tail_; ///< pointer to object list
    // end linked-list

    uint8_t _commands_count_;       ///< how many commands are there
    uint8_t _max_depth_;            ///< max command depth found
    uint8_t _max_args_;             ///< max command or subcommand arguments found
    bool* _input_type_match_flags_; ///< bool array _input_type_match_flags_[_max_args_]

    bool _output_flag_; ///< output is available flag, set by member functions

    char* _token_buffer_;              ///< pointer to tokenized c-string
    char** _data_pointers_;            ///< token_buffer pointers
    uint8_t _data_pointers_index_;     ///< data_pointer index
    uint8_t _data_pointers_index_max_; ///< data_pointer index max
    uint8_t _p_num_ptrs_;              ///< "p"rocess number of pointers, computed in UserInput::begin()

    uint8_t _rec_num_arg_strings_;  ///< number of tokens after first valid token
    uint8_t _failed_on_subcommand_; ///< subcommand error index
    uint8_t _current_search_depth_; ///< current subcommand search depth

    char _null_; ///< char '\0'
    char _neg_;  ///< char '-'
    char _dot_;  ///< char '.'

    bool _stream_buffer_allocated_; ///< this flag is set true on GetCommandFromStream entry if a buffer is not allocated
    bool _new_stream_data_;         ///< if there is new data in *stream_data this is true
    uint8_t* _stream_data_;         ///< pointer to stream input, a string of char
    uint16_t _stream_data_index_;   ///< the index of stream_data

    bool _begin_; ///< begin() error flag

    InputProcessParameters _input_prm_; ///< user input process parameters pointer struct

    //  end constructor initialized variables

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
     * @param prm CommandParameters struct reference
     * @param command_matched boolean reference
     * @param all_arguments_valid argument error sentinel
     * @param data raw data in
     */
    void _readCommandFromBufferErrorOutput(CommandConstructor* cmd, CommandParameters& prm, bool& command_matched, bool& all_arguments_valid, uint8_t* data);

    /**
     * @brief launches either (this) function or the root command function
     *
     * @param cmd CommandConstructor pointer
     * @param prm CommandParameters struct reference
     * @param tokens_received amount of tokens in the token buffer
     * @param pname IH_pname char array
     */
    void _launchFunction(CommandConstructor* cmd, CommandParameters& prm, size_t tokens_received, const IH_pname& pname);

    /**
     * @brief UserInput:_launchLogic() parameters structure
     */
    struct _launchLogicParam
    {
        CommandConstructor* cmd;     ///< CommandConstructor ptr
        CommandParameters& prm;      ///< CommandParameters struct reference
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
     * @brief determines if input CommandParameters struct is valid before adding to linked-list
     *
     * @param cmd CommandConstructor reference
     * @param prm reference to CommandParameters struct in addCommand
     * @return true if there are no errors
     * @return false if there were one or more errors
     */
    bool _addCommandAbort(CommandConstructor& cmd, CommandParameters& prm);

    /**
     * @brief Get the UITYPE equivalent for the argument, internally we use uint8_t
     *
     * @param prm command options structure reference
     * @param index argument number
     * @return UITYPE argument type
     */
    UITYPE _getArgType(CommandParameters& prm, size_t index = 0);

    /**
     * @brief validate the arguments as specified in the user defined CommandParameters struct
     *
     * @param tokens_received how many tokens are left after matching is performed
     * @param input_type_match_flag input type validation flags
     * @param prm CommandParameters struct reference
     * @param all_arguments_valid error sentinel
     */
    void _getArgs(size_t& tokens_received, bool* input_type_match_flag, CommandParameters& prm, bool& all_arguments_valid);

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
     * @param input_prm reference to InputProcessParameters struct
     * @param data_pos data index
     * @param token_buffer_index token_buffer index
     * @param point_to_beginning_of_token boolean sentinel
     */
    void _getTokensDelimiters(getTokensParam& gtprm, const InputProcessParameters& input_prm, size_t& data_pos, size_t& token_buffer_index, bool& point_to_beginning_of_token);

    /**
     * @brief get delimited c-strings from input data
     *
     * @param gtprm reference to getTokensParam struct in getTokens
     * @param input_prm reference to InputProcessParameters struct
     * @param data_pos data index
     * @param token_buffer_index token_buffer index
     * @param point_to_beginning_of_token boolean sentinel
     */
    void _getTokensCstrings(getTokensParam& gtprm, const InputProcessParameters& input_prm, size_t& data_pos, size_t& token_buffer_index, bool& point_to_beginning_of_token);

    /**
     * @brief add uchar to token_buffer
     *
     * @param gtprm reference to getTokensParam struct in getTokens
     * @param input_prm reference to InputProcessParameters struct
     * @param data_pos data index
     * @param token_buffer_index token_buffer index
     * @param point_to_beginning_of_token boolean sentinel
     */
    void _getTokensChar(getTokensParam& gtprm, const InputProcessParameters& input_prm, size_t& data_pos, size_t& token_buffer_index, bool& point_to_beginning_of_token);

    /**
     * @brief split a zero delimiter command, separate command and string with token delimiter for further processing
     *
     * @param pdelimseq reference to process delimiter sequence struct
     * @param data input data
     * @param len input data length
     * @param split_input place to split input
     * @param input_len split input len
     * @param num_zdc zero delim commands
     * @param zdc num zdc
     * @return true if split
     * @return false no match no split
     */
    bool _splitZDC(InputProcessDelimiterSequences& pdelimseq, uint8_t* data, size_t len, char* split_input, size_t input_len, const size_t num_zdc, const CommandParameters** zdc);

    /**
     * @brief calculates memcmp ranges for a given command around wildcard char, noninclusive
     *
     * @param command reference to a CommandConstructor class
     * @param prm reference to a CommandParameters struct
     * @param prm_idx prm index
     * @param memcmp_ranges_idx index of memcmp_ranges
     * @param memcmp_ranges memcmp ranges array
     */
    void _calcCmdMemcmpRanges(CommandConstructor& command, CommandParameters& prm, size_t prm_idx, uint8_t& memcmp_ranges_idx, uint8_t* memcmp_ranges);

    /**
     * @brief compares str to cmd->prm[prm_idx].command
     *
     * @param cmd pointer to CommandConstructor
     * @param prm_idx index of CommandParameters to array test
     * @param str c-string
     * @return true if match
     * @return false if no match
     */
    bool _compareCommandToString(CommandConstructor* cmd, size_t prm_idx, char* str);
    // end private methods
};

#endif
