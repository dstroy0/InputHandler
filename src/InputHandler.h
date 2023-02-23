/* library version 0.9a */
/**
 * @file InputHandler.h
 * @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
 * @brief InputHandler library header file
 * @version 1.2
 * @date 2023-02-06
 *
 * @copyright Copyright (c) 2022
 */
/*
 Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 version 3 as published by the Free Software Foundation.
 */
#if !defined(__USER_INPUT_HANDLER_H__)
    #define __USER_INPUT_HANDLER_H__

    // user configurable items located in src/config/config.h and src/config/advanced_config.h
    // see examples/all_platforms/advanced/GetCommandFromStream.ino for an example
    #include "config/noedit.h"
namespace InputHandler
{
// lib specific namespaces
using namespace ih_t;
using namespace ih_auto;
class UserInput; // forward declaration for Parameters
/**
 * @brief Command parameters setup
 *
 * Every command and subcommand has an associated Parameters object, this is the information
 * that the input process needs to know about your command.
 */
struct Parameters
{
    void (*function)(
        UserInput*);    ///< void function pointer, void your_function(UserInput *inputProcess)
    bool has_wildcards; ///< if true this command has one or more wildcard char
    char command[IH_MAX_CMD_STR_LEN + 1U]; ///< command string + nullchar
    max_cmd_str_len command_length;        ///< command length in characters
    cmd_id_grp parent_command_id;          ///< parent command's unique id root-MAX
    cmd_id_grp command_id;                 ///< this command's unique id root-MAX
    max_tree_depth_per_cmd depth;          ///< command tree depth root-MAX
    max_num_child_cmds
        sub_commands; ///< how many subcommands does this command have 0 - UI_MAX_SUBCOMMANDS
    UI_ARG_HANDLING argument_flag; ///< argument handling flag
    max_args_per_cmd num_args; ///< minimum number of arguments this command expects 0 - UI_MAX_ARGS
    max_args_per_cmd max_num_args; ///< maximum number of arguments this command expects 0 -
                                   ///< UI_MAX_ARGS, cannot be less than num_args
    UITYPE arg_type_arr[IH_MAX_ARGS_PER_COMMAND]; ///< argument UITYPE array
};
/**
 * @defgroup classes classes
 */
///@{
/**
 * @class Command
 *
 * @brief Pointers to information about the command and the linked-list.
 *
 * The purpose of this class is to set up the command for use with
 * UserInput::addCommand().  It contains a pointer to the next command
 * in the singly-linked-list which is NULL before the command is accepted
 * into the process, a pointer to Parameters in PROGMEM,
 * the length of the parameters array, the depth of the command tree
 * you desire to add to the list, and a pointer to CommandRunTimeCalc
 * if this command contains wildcard commands.
 *
 */
class Command
{
public:
    /**
     * @brief Constructor method.
     *
     * Linked-list primer: https://www.programiz.com/dsa/linked-list
     *
     * These  are chained together as a linked-list; this
     * object contains a reference to the next node
     * in the linked-list.  The list is linked together each call to
     * UserInput::addCommand().
     *
     * Before using, construct a UserInput object and a Parameters object.
     * @param parameters pointer to parameters struct or array of parameters structs
     * @param parameter_array_elements number of elements in the parameter array
     * @param tree_depth depth of command tree
     */
    Command(const Parameters* parameters, const max_cmds_per_tree parameter_array_elements = 1,
        const max_tree_depth_per_cmd tree_depth = 0)
        : prm(parameters),
          param_array_len(parameter_array_elements),
          tree_depth(tree_depth + 1U),
          calc(NULL),
          next_command(NULL)
    {
    }
    const Parameters* prm; ///< pointer to PROGMEM Parameters array
    const max_cmds_per_tree
        param_array_len; ///< user input param array len, either as digits or through nprms
    const max_cmds_per_tree tree_depth; ///< user input depth + 1
    CommandRuntimeCalc* calc;           ///< pointer to CommandRuntimeCalc struct
    Command* next_command;              ///< Command iterator/pointer
};

/**
 * @class UserInput
 *
 * @brief Parses user input, formats an output buffer if defined.
 *
 * This class contains methods that deal with parsing user input by
 * looking for "interesting" predefined combinations of 0-255 char
 * values, and formatting an output buffer with useful human readable
 * information.
 *
 */

class UserInput
{
public:
    /**
     * @brief UserInput constructor, no output by default
     *
     * UserInput has no output by default due to the default values passed in by the constructor.
     * The constructor disables output by setting UserInput::\_output_enabled_ to false if
     * `output_buffer` is NULL.
     *
     * @param input_prm InputParameters PROGMEM pointer. NULL by default, which makess the
     * ctor use ihconst::default_parameters.
     * @param output_buffer class output char buffer, implementation specific.  NULL by default.
     * @param output_buffer_len size of output_buffer, use @link buffsz() @endlink to prevent
     * accidental buffer sizing errors.
     */
    UserInput(const InputParameters* input_prm = NULL, char* output_buffer = NULL,
        size_t output_buffer_len = 0)
        : _input_prm_ptr_((input_prm == NULL) ? &ihconst::default_parameters : input_prm),
          _output_buffer_(output_buffer),
          _output_buffer_len_(output_buffer_len),
          _output_enabled_((output_buffer == NULL) ? false : true),
          _output_buffer_bytes_left_(output_buffer_len),
          _term_len_(strlen_P(((input_prm == NULL) ? (char*)ihconst::default_parameters.eol_char
                                                   : (char*)input_prm->eol_char))),
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
          _begin_(false),
          _halt_(false)
    {
        // load input parameters from PROGMEM
        memcpy_P(&_input_prm_, _input_prm_ptr_, sizeof(_input_prm_));
    }

    /**
     * @brief Sets UserInput::\_default_function_.
     * When there is no command match, or when input is invalid, this function is called
     * if UserInput::\_default_function_ is not NULL.
     *
     * [UserInput::defaultfunction
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=defaultFunction(void
     * (*function)(UserInput*)))
     *
     * @param function a pointer to a user specified function to use as the default function with
     * the format of `void (*function)(UserInput*)`.
     */
    void defaultFunction(void (*function)(UserInput*));

    /**
     * @brief Adds user commands to the input process.
     *
     * This function inspects the input parameters for errors and
     * reports the errors to the user if the user has enabled output
     * by defining an output buffer when instantiating UserInput.
     * If an error is detected, the entire command tree is rejected.
     *
     * No further action is taken.
     *
     * [UserInput::addCommand
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=addCommand(Command&
     * command))
     *
     * @param command reference to Command object
     */
    void addCommand(Command& command);

    /**
     * @brief Allocates memory to run the input process.
     *
     * Allocates memory for:
     * UserInput::\_data_pointers_
     * UserInput::\_input_type_match_flags_
     *
     * sets UserInput::\_begin_ to true if successful.
     *
     * [UserInput::begin
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=begin())
     *
     * @return true if allocation successful
     * @return false if allocation unsuccessful
     */
    bool begin();

    /**
     * @brief Lists UserInput class settings, useful for implementation debugging.
     *
     * Lists class configuration, constructor variables,
     * and the amount of pointers that were dynamically
     * allocated in UserInput::begin().
     *
     * REQUIRES a 700 byte output_buffer.  If an insufficient buffer size is declared,
     * UserInput::\ihout() will first empty the output buffer and then warn the user
     * to increase the buffer to the required size.
     *
     * [UserInput::listSettings
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=listSettings(UserInput*
     * inputProcess))
     *     
     */
    void listSettings();

    /**
     * @brief Lists commands available to the user.
     *
     * Lists commands that will respond to user input if UserInput::\_begin_ is true. Else it will
     * inform the user to use UserInput::begin() in `setup()`.
     *
     * [UserInput::listCommands
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=listCommands())
     *
     */
    void listCommands();

    /**
     * @brief Reads predefined command(s) from a buffer.
     *
     * @warning This function will silent return if UserInput::\_begin_ is false!
     *
     * [UserInput::readCommandFromBuffer()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=readCommandFromBuffer(
     *  uint8_t* data, size_t len, const size_t num_zdc = 0, const Parameters** zdc = NULL))
     *
     * @param data a buffer with characters
     * @param len the size of the buffer
     * @param num_zdc size of Parameters zero delimiter command pointers array
     * @param zdc array of Parameters zero delimiter command pointers
     */
    void readCommandFromBuffer(
        uint8_t* data, size_t len, const size_t num_zdc = 0, const Parameters** zdc = NULL);

    /**
     * @brief Gets bytes from a Stream object and feeds a buffer to readCommandFromBuffer.
     *
     * [Stream object
     * reference](https://www.arduino.cc/reference/en/language/functions/communication/stream/)
     *
     * @warning This function will silent return if UserInput::\_begin_ is false!
     *
     * [UserInput::getCommandFromStream()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=getCommandFromStream(Stream%24
     * stream, size_t rx_buffer_size, const size_t num_zdc, const Parameters** zdc))
     *
     * @param stream the stream to reference
     * @param rx_buffer_size the size of our receive buffer
     * @param num_zdc size of Parameters zero delimiter command pointers array
     * @param zdc array of Parameters zero delimiter command pointers
     */
    void getCommandFromStream(Stream& stream, size_t rx_buffer_size = IH_MAX_PROC_INPUT_LEN,
        const size_t num_zdc = 0, const Parameters** zdc = NULL);

    /**
     * @brief Returns a pointer to the next token in UserInput::\_token_buffer_.
     *
     * Returns NULL if no more tokens were parsed.
     *
     * [UserInput::nextArgument()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=nextArgument())
     *
     * @return valid pointer if there is another token else NULL.
     */
    char* nextArgument();

    /**
     * @brief Returns a pointer to argument_number token in UserInput::\_token_buffer_
     *
     * Returns NULL if argument_number's token doesn't exist.
     *
     * [UserInput::getArgument()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=getArgument(size_t
     * argument_number))
     *
     * @param argument_number The argument number to retrieve.
     * @return valid pointer if argument_number exists else NULL.
     */
    char* getArgument(size_t argument_number);

    /**
     * @brief Output is available from UserInput if True.
     *
     * (True) if greater than 0
     * (False) if 0
     *
     * [UserInput::outputIsAvailable()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=outputIsAvailable())
     *
     * @return The number of bytes available for output, or zero if there is no output available.
     */
    size_t outputIsAvailable();

    /**
     * @brief UserInput output flag.
     *
     * [UserInput::outputIsAvailable()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=outputIsEnabled())
     *
     * @return true if enabled
     * @return false if not enabled
     */
    bool outputIsEnabled();

    /**
     * @brief Direct UserInput output to a Stream.
     *
     * This also clears the output buffer automatically after writing to the
     * Stream is complete.
     *
     * [UserInput::outputToStream()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=outputToStream(Stream%24
     * stream))
     *
     * @param stream The Stream to write to.
     */
    void outputToStream(Stream& stream);

    /**
     * @brief Clears the output buffer if defined.
     *
     * Soft clear by default, writes null to the first char in the output buffer.
     *
     * [UserInput::outputIsAvailable()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=clearOutputBuffer(bool
     * overwrite_contents))
     *
     * @param overwrite_contents boolean switch, clearOutputBuffer(true) writes null to entire
     * UserInput::\_output_buffer_
     */
    void clearOutputBuffer(bool overwrite_contents = false);

    /**
     * @brief UserInput::getTokens() input data structure.
     */
    struct getTokensParam
    {
        uint8_t* data;                ///< pointer to uint8_t array
        size_t len;                   ///< length of uint8_t array
        size_t data_pos;              ///< index of data
        char* token_buffer;           ///< pointer to null terminated char array
        size_t token_buffer_len;      ///< size of data + 1 + 1(if there are zero delim commands)
        size_t token_buffer_index;    ///< index of token_buffer
        size_t num_token_ptrs;        ///< token_pointers[MAX]
        uint8_t& token_pointer_index; ///< index of token_pointers
        char** token_pointers;        ///< array of token_buffer pointers
        bool point_to_beginning_of_token; ///< assign pointer to &token_buffer[token_buffer_index]
                                          ///< if true
        char& token_buffer_sep;           ///< token_buffer token delimiter
    };

    /**
     * @brief Puts tokens into the token buffer pointed to by the input UserInput::getTokensParam.
     *
     * To use this function outside of UserInput you must declare a UserInput::getTokensParam.
     *
     * This can be used with different InputParameters than the ones provided to the
     * UserInput Constructor method.
     *
     * [UserInput::getTokens()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=getTokens(getTokensParam%24
     * gtprm, const InputParameters%24 input_prm))
     *
     * @param gtprm UserInput::getTokensParam struct reference
     * @param input_prm reference to InputParameters struct
     *
     * @return size_t number of tokens retrieved
     */
    size_t getTokens(getTokensParam& gtprm, const InputParameters& input_prm);

    /**
     * @brief null separated input
     *
     */
    struct validateNullSepInputParam
    {
        UITYPE arg_type;            ///< the UITYPE to test
        char** token_pointers;      ///< pointers to null separated tokens
        size_t token_pointer_index; ///< index of token_pointers to test
        char& neg_sign;  ///< single char neg sign, if different than '-' parseInt and the like will
                         ///< not assign your input negative
        char& float_sep; ///< whole and fraction separator
    };

    /**
     * @brief Tries to determine if input is valid in NULL TERMINATED char arrays.
     *
     * [UserInput::validateNullSepInput()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=validateNullSepInput(validateNullSepInputParam%24
     * vprm))
     *
     * @param vprm validateNullSepInputParam struct reference
     *
     * @return true argument-type is valid
     * @return false argument-type is not valid
     */
    bool validateNullSepInput(validateNullSepInputParam& vprm);

    /**
     * @brief Transform 2d matrix indices to flat array index.
     *
     * Use this to access a dynamically allocated array like a 2d matrix,
     * this is much more performant than looping to allocate a (n>1)d array,
     * and looping again to free allocated ram.
     *
     * @code{.cpp}
     * // usage
     * #include <InputHandler.h>
     * size_t matrix_index = UserInput::mIndex(0,0,0);
     * @endcode
     * @code{.c}
     * // source
     * size_t mIndex(size_t m_width, size_t row, size_t col) const { return row * m_width + col; }
     * @endcode
     *
     * @param m_width;
     * @param row row you want to access
     * @param col column you want to access
     * @return size_t the transformed index
     */
    size_t mIndex(size_t m_width, size_t row, size_t col) const { return row * m_width + col; }

    /**
     * @brief UserInput vsnprintf
     * https://www.cplusplus.com/reference/cstdio/vsprintf/
     *
     * [UserInput::ihout()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=ihout(const
     * char* fmt, ...))
     *
     * Puts the message into the defined output buffer.
     *
     * @param fmt   the format string
     * @param ...   arguments
     */
    void ihout(const char* fmt, ...);

private:
    /*
        UserInput Constructor variables
    */

    // (potentially) user entered constructor variables
    const InputParameters* _input_prm_ptr_; ///< user input constructor parameters pointer
    char* _output_buffer_;                  ///< pointer to the output char buffer
    const size_t _output_buffer_len_;       ///< UserInput::\_output_buffer_ size in bytes
    // end user entered constructor variables

    bool _output_enabled_; ///< true if UserInput::\_output_buffer_ is not NULL (the user has
                           ///< defined and passed an output buffer to UserInput's constructor)
    size_t _output_buffer_bytes_left_; ///< index of UserInput::\_output_buffer_, messages are
                                       ///< appended to the output buffer and this keeps track of
                                       ///< where to write to next without overwriting

    uint8_t _term_len_;   ///< _term_ length in characters, determined in UserInput::UserInput().
    uint8_t _term_index_; ///< _term_ index, match all characters in term or reject input.

    void (*_default_function_)(UserInput*); ///< pointer to the default function.

    // linked-list
    Command* _commands_head_; ///< pointer to Command singly-linked-list head.
    Command* _commands_tail_; ///< pointer to Command singly-linked-list tail.
    // end linked-list

    max_cmds_per_tree _commands_count_; ///< How many commands were accepted from input Parameters.
    max_tree_depth_per_cmd
        _max_depth_;             ///< Max command depth found in the accepted input Parameters.
    max_args_per_cmd _max_args_; ///< Max command or subcommand arguments found in the accepted
                                 ///< input Parameters.
    type_match_flags* _input_type_match_flags_; ///< Bool array the size of UserInput::\_max_args_.

    bool _output_flag_; ///< Output is available flag, set by member functions.

    char* _token_buffer_;                       ///< pointer to tokenized c-string
    char** _data_pointers_;                     ///< token_buffer pointers
    max_args_per_cmd _data_pointers_index_;     ///< data_pointer index
    max_args_per_cmd _data_pointers_index_max_; ///< data_pointer index max
    max_args_per_cmd
        _p_num_ptrs_; ///< UserInput process number of pointers, computed in UserInput::begin().

    max_args_per_cmd _rec_num_arg_strings_;        ///< number of tokens after first valid token
    max_num_child_cmds _failed_on_subcommand_;     ///< subcommand error index
    max_tree_depth_per_cmd _current_search_depth_; ///< current subcommand search depth

    char _null_; ///< char null
    char _neg_;  ///< char '-'
    char _dot_;  ///< char '.'

    bool _stream_buffer_allocated_; ///< this flag is set true on GetCommandFromStream entry if a
                                    ///< buffer is not allocated
    bool _new_stream_data_;         ///< if there is new data in *stream_data this is true
    uint8_t* _stream_data_;         ///< pointer to stream input, a string of char
    uint16_t _stream_data_index_;   ///< the index of stream_data

    bool _begin_; ///< begin() error flag
    bool _halt_;  ///< fatal error flag

    InputParameters _input_prm_; ///< user input process parameters pointer struct
    //  end constructor initialized variables

    /**
     * @brief Used internally by UserInput::readCommandFromBuffer() and passed by reference.
     *
     * Instantiated in UserInput::readCommandFromBuffer() and passed by reference to subfunctions.
     *
     */
    struct _rcfbprm
    {
        bool launch_attempted;    ///< function launch attempted if true
        bool command_matched;     ///< matched root command if true
        bool all_arguments_valid; ///< argument error sentinel
        bool subcommand_matched;  ///< matched a subcommand
        Command* cmd;             ///< pointer to Command
        Command* all_wcc_cmd;     ///< pointer to Command
        UI_COMPARE result;        ///< result of UserInput::\_compareCommandToString()
        cmd_id_grp command_id;    ///< type set by macro
        size_t idx;               ///< Parameters index
        size_t all_wcc_idx;       ///< index of Parameters that has an all wcc command
        size_t input_len;         ///< length of input data
        size_t token_buffer_len;  ///< length of token buffer
        size_t tokens_received;   ///< how many tokens we received
        Parameters prm;           ///< Parameters struct
        uint8_t* input_data;      ///< pointer to input_data
        uint8_t* split_input;     ///< pointer to UserInput::\_splitZDC() modified data
    };

    // private methods

    #if defined(ENABLE_readCommandFromBufferErrorOutput) || defined(DOXYGEN_XML_BUILD)
    /**
     * @brief ReadCommandFromBuffer error output
     *
     * [UserInput::_readCommandFromBufferErrorOutput()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=_readCommandFromBufferErrorOutput(_rcfbprm%24
     *  rprm))
     *
     * @param rprm reference to UserInput::\_rcfbprm
     */
    void _readCommandFromBufferErrorOutput(_rcfbprm& rprm);
    #endif // end ENABLE_readCommandFromBufferErrorOutput

    /**
     * @brief launches either (this) function or the root command function
     *
     * [UserInput::_launchFunction()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=_launchFunction(_rcfbprm%24
     * rprm, const ProcessName%24 pname))
     *
     * @param rprm reference to UserInput::\_rcfbprm
     * @param pname ProcessName char array
     */
    void _launchFunction(_rcfbprm& rprm, const ProcessName& pname);

    /**
     * @brief function launch logic, recursive on subcommand match
     *
     * [UserInput::_launchLogic()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=_launchLogic(_rcfbprm%24
     * rprm))
     *
     * @param rprm reference to UserInput::\_rcfbprm
     */
    void _launchLogic(_rcfbprm& rprm);

    /**
     * @brief Escapes control characters so they will print
     *
     * [UserInput::_escapeCharactersSoTheyPrint()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=_escapeCharactersSoTheyPrint(char
     * input, char* buf))
     *
     * @param input the input char
     * @param buf the output buffer
     *
     * @return pointer to buf, so you can use this inside of ihout()
     */
    char* _escapeCharactersSoTheyPrint(char input, char* buf);

    /**
     * @brief Triggers on the input a control character sequence.
     *
     * If the char immediately after the control char is a char known
     * to UserInput::\_combineControlCharacters this returns a control char,
     * else it returns the input char.
     *
     * [UserInput::_combineControlCharacters()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=_combineControlCharacters(char
     * input))
     *
     * @param input the char the control character sequence
     * @return the control character char value
     */
    char _combineControlCharacters(char input);

    /**
     * @brief prints detected Parameters errors
     *
     * @param error ihconst::CMD_ERR_IDX member
     * @param cmd null term char array
     * @return true never
     * @return false each call
     */
    bool _addCommandErrorMessage(ihconst::CMD_ERR_IDX error, char* cmd);
    /**
     * @brief determines if input Parameters struct is valid before adding to linked-list
     *
     * [UserInput::_addCommandAbort()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=_addCommandAbort(Command%24
     * cmd, Parameters%24 prm))
     *
     * @param cmd Command reference
     * @param prm reference to Parameters struct in addCommand
     * @return true if there are no errors
     * @return false if there were one or more errors
     */
    bool _addCommandAbort(Command& cmd, Parameters& prm);

    /**
     * @brief Get the UITYPE equivalent for the argument, internally we use uint8_t
     *
     * [UserInput::_getArgType()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=_getArgType(Parameters%24
     * prm, size_t index))
     *
     * @param prm command options structure reference
     * @param index argument number
     * @return UITYPE argument type
     */
    UITYPE _getArgType(Parameters& prm, size_t index = 0);

    /**
     * @brief validate the arguments as specified in the user defined Parameters struct
     *
     * [UserInput::_getArgs()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=_getArgs(_rcfbprm%24
     * rprm))
     *
     * @param rprm reference to UserInput::\_rcfbprm
     */
    void _getArgs(_rcfbprm& rprm);

    /**
     * @brief adds escaped control characters to a buffer
     *
     * [UserInput::_addEscapedControlCharToBuffer()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=_addEscapedControlCharToBuffer(char*
     * buf, size_t%24 idx, const char* input, size_t input_len))
     *
     * @param buf output buffer
     * @param idx buffer index
     * @param input string to escape
     * @param input_len length of string
     * @return pointer to null terminated escaped control char string
     */
    char* _addEscapedControlCharToBuffer(
        char* buf, size_t& idx, const char* input, size_t input_len);

    /**
     * @brief find delimiters in input data
     *
     * [UserInput::_getTokensDelimiters()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=_getTokensDelimiters(getTokensParam%24
     * gtprm, const InputParameters%24 input_prm))
     *
     * @param gtprm reference to getTokensParam struct in getTokens
     * @param input_prm reference to InputParameters struct
     */
    void _getTokensDelimiters(getTokensParam& gtprm, const InputParameters& input_prm);

    /**
     * @brief get delimited c-strings from input data
     *
     * [UserInput::_getTokensStartStop()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=_getTokensStartStop(getTokensParam%24
     * gtprm, const InputParameters%24 input_prm))
     *
     * @param gtprm reference to getTokensParam struct in getTokens
     * @param input_prm reference to InputParameters struct
     */
    void _getTokensStartStop(getTokensParam& gtprm, const InputParameters& input_prm);

    /**
     * @brief add uchar to token_buffer
     *
     * [UserInput::_getTokensChar()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=_getTokensChar(getTokensParam%24
     * gtprm, const InputParameters%24 input_prm))
     *
     * @param gtprm reference to getTokensParam struct in getTokens
     * @param input_prm reference to InputParameters struct
     */
    void _getTokensChar(getTokensParam& gtprm, const InputParameters& input_prm);

    /**
     * @brief split a zero delimiter command, separate command and string with token delimiter for
     * further processing
     *
     * [UserInput::_splitZDC()
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=_splitZDC(_rcfbprm%24
     * rprm, const size_t num_zdc, const Parameters** zdc))
     *
     * @param rprm reference to UserInput::\_rcfbprm
     * @param num_zdc zero delim commands
     * @param zdc num zdc
     * @return true if split
     * @return false no match no split
     */
    bool _splitZDC(_rcfbprm& rprm, const size_t num_zdc, const Parameters** zdc);

    /**
     * @brief calculates memcmp ranges for a given command around wildcard char, noninclusive
     *
     * [UserInput::_calcCmdMemcmpRanges
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=void%20UserInput::_calcCmdMemcmpRanges)
     *
     * @param command reference to a Command class
     * @param prm reference to a Parameters struct
     * @param prm_idx prm index
     * @param memcmp_ranges_idx index of memcmp_ranges
     * @param memcmp_ranges memcmp ranges array
     */
    void _calcCmdMemcmpRanges(Command& command, Parameters& prm, size_t prm_idx,
        memcmp_idx_t& memcmp_ranges_idx, max_per_root_memcmp_ranges* memcmp_ranges);

    /**
     * @brief compares (memcmp) str to cmd->prm[prm_idx].command
     *
     * [UserInput::_compareCommandToString
     * source](https://github.com/dstroy0/InputHandler/blob/main/src/InputHandler.cpp#:~:text=_compareCommandToString(Command*
     * cmd, size_t prm_idx, char* str))
     *
     * @param cmd pointer to Command
     * @param prm_idx index of Parameters to compare
     * @param str c-string
     * @return UI_COMPARE match type
     */
    UI_COMPARE _compareCommandToString(Command* cmd, size_t prm_idx, char* str);

    #if defined(__UI_VERBOSE__) && defined(ENABLE_listCommands)
    /**
     * @brief used internally by listCommands()
     *
     */
    struct _searchStruct
    {
        Command* cmd;         // pointer to a Command
        Parameters& prm;      // pointer to a Parameters
        uint8_t* sort_array;  // partial command array
        uint8_t** sorted_ptr; // pointer array
        uint8_t& sorted_idx;  // index of pointer array
        uint8_t& ls_value;    // value to search for
        int& lsize;           // linear search index
        uint8_t& prev_dp;     // depth
        uint8_t& sc_num;      // subcommand number
    };
    /**
     * @brief recursive linear array search
     *
     * @param s _searchStruct
     * @return int index of match else -1
     */
    int _linearSearch(_searchStruct& s); // recursive linear search
    /**
     * @brief recursive linear matrix search
     *
     * @param s _searchStruct
     * @param lmsize matrix index
     * @param lms_values match values
     * @return int index of match else -1
     */
    int _linearMatrixSearch(
        _searchStruct& s, int& lmsize, uint8_t* lms_values); // recursive linear "matrix" search
    /**
     * @brief sorts a pointer array to print commands by heirarchy
     *
     * @param s _searchStruct
     * @param lmsize recursive sort matrix index
     * @param lms_values matrix search values
     * @return true on success
     * @return false on fail
     */
    bool _sortSubcommands(_searchStruct& s, int& lmsize, uint8_t* lms_values); // recursive sort
    /**
     * @brief prints s.cmd->prm[index]
     *
     * @param s _searchStruct
     * @param index index of the parameter to print
     */
    void _printCommand(
        _searchStruct& s, uint8_t index); // print a single command at s.cmd->prm[index]
    #endif
    /**
     * @brief lib fatal error
     *
     * @param var_id _reserved by default, else prints fatal allocation message for var_id
     * @return true if _begin_ not set
     *                 or _halt_ is set
     *                 or var_id != _reserved
     * @return false on fallthrough
     */
    bool _fatalError(ihconst::VAR_ID var_id = ihconst::VAR_ID::_reserved);
    // end private methods
};
///@}
};
#endif // header guard include

// end of file
