/**
   @file InputHandler.cpp
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief InputHandler library cpp file
   @version 1.0
   @date 2022-03-18

   @copyright Copyright (c) 2022
*/
/*
 Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 version 3 as published by the Free Software Foundation.
 */

#include "InputHandler.h"

/*
    public methods
*/

void UserInput::listSettings(UserInput *inputprocess)
{
    size_t buf_sz = _term_len_ + _delim_len_ + _c_str_delim_len_ + 3; // +3; 2 null separators and terminator
    // allocate char buffer large enough to print these potential control characters
    char *buf = new char[buf_sz * UI_ESCAPED_CHAR_PGM_LEN]();
    size_t idx = 0;       
    UserInput::_ui_out(PSTR("src/config/InputHandler_config.h:\n"
                            "UI_MAX_ARGS %u max allowed arguments per unique command_id\n"
                            "UI_MAX_CMD_LEN (root command) %u characters\n"
                            "UI_MAX_IN_LEN %u bytes\n"
                            "\nUserInput constructor:\n"
                            "username = \"%s\"\n"
                            "end_of_line_characters = \"%s\", escaped for display\n"
                            "token_delimiter = \"%s\", escaped for display\n"
                            "c_string_delimiter = \"%s\", escaped for display\n"
                            "_data_pointers_[root(1) + _max_depth_ + _max_args_] == [%02u]\n"
                            "_max_depth_ (found from input Parameters) = %u\n"
                            "_max_args_ (found from input Parameters) = %u\n"),
                       UI_MAX_ARGS,
                       UI_MAX_CMD_LEN,
                       UI_MAX_IN_LEN,
                       _username_,
                       _addEscapedControlCharToBuffer(buf, idx, _term_, _term_len_),
                       _addEscapedControlCharToBuffer(buf, idx, _delim_, _delim_len_),
                       _addEscapedControlCharToBuffer(buf, idx, _c_str_delim_, _c_str_delim_len_),
                       (1U + _max_depth_ + _max_args_),
                       _max_depth_,
                       _max_args_);
    delete[] buf; // free
}

void UserInput::defaultFunction(void (*function)(UserInput *))
{
    _default_function_ = function;
}

void UserInput::addCommand(CommandConstructor &command)
{
    size_t max_depth_found = 0; // for _data_pointers_ array sizing
    size_t max_args_found = 0;  // for _data_pointers_ array sizing
    Parameters prm;             // this Parameters struct is referenced by the helper function _addCommandAbort()
    bool err = false;           // Parameters struct error sentinel
    /*
        the reason we run through the whole Parameters array instead of breaking
        on error is to give users clues as to what might be wrong with their
        command Parameters
    */
    for (size_t i = 0; i < command.param_array_len; ++i)
    {
        memcpy_P(&prm, &(command.prm[i]), sizeof(prm));
        if (!UserInput::_addCommandAbort(command, prm)) // input Parameters error checking
        {
            err = true;
        }
        else
        {
            // if the current command's tree depth is greater than what we have found
            max_depth_found = (command.tree_depth > max_depth_found)
                                  ? command.tree_depth
                                  : max_depth_found;
            // if the current command's max num args is greater than what we have found
            max_args_found = (prm.max_num_args > max_args_found)
                                 ? prm.max_num_args
                                 : max_args_found;
        }
    }
    if (!err) // if no error
    {
        if (_commands_count_ == 0) // do once
        {
            _term_len_ = strlen(_term_);
            _delim_len_ = strlen(_delim_);
            _c_str_delim_len_ = strlen(_c_str_delim_);
            _output_buffer_bytes_left_ = _output_buffer_len_;
        }
        _commands_count_++; // increment _commands_count_

        // set _max_depth_ to max_depth_found if it is greater than _max_depth_
        _max_depth_ = (max_depth_found > _max_depth_)
                          ? max_depth_found
                          : _max_depth_;
        // set _max_args_ to max_args_found if it is greater than _max_args_
        _max_args_ = (max_args_found > _max_args_)
                         ? max_args_found
                         : _max_args_;

        // linked-list
        if (_commands_head_ == NULL) // the list is empty
        {
            _commands_head_ = _commands_tail_ = &command; // (this) is the beginning of the list
        }
        else
        {
            _commands_tail_->next_command = &command; // single linked-list (next only)
            _commands_tail_ = &command;               // move the tail to (this)
        }
    }
}

bool UserInput::begin()
{
    size_t ptrs = 1U + _max_depth_ + _max_args_;
    _data_pointers_ = new char *[ptrs]();
    if (_data_pointers_ == nullptr)
    {
        UserInput::_ui_out(PSTR("ERROR! Cannot allocate ram for _data_pointers_\n"));
        _begin_ = false;
        delete[] _data_pointers_;
        return _begin_;
    }
    _begin_ = true;
    return _begin_;
}

void UserInput::listCommands()
{
    if (!_begin_)
    {
        UserInput::_ui_out(PSTR("Use begin() in setup()"));
        return;
    }
    CommandConstructor *cmd;
    if (_username_[0] == _null_)
    {
        UserInput::_ui_out(PSTR("Commands available:\n"));
    }
    else
    {
        UserInput::_ui_out(PSTR("Commands available to %s:\n"), _username_);
    }
    uint8_t i = 1;
    for (cmd = _commands_head_; cmd != NULL; cmd = cmd->next_command, ++i)
    {
        char buffer[UI_MAX_CMD_LEN];
        memcpy_P(&buffer, cmd->prm->command, sizeof(buffer));
        UserInput::_ui_out(PSTR(" %02u. <%s>\n"), i, buffer);
    }
}

void UserInput::readCommandFromBuffer(uint8_t *data, size_t len)
{
    // error checking
    if (!_begin_) // error
    {
        return;
    }
    if (len > UI_MAX_IN_LEN) // 65535 - 1(index align) - 1(space for null '\0')
    {
        UserInput::_ui_out(PSTR(">%s$ERROR: input is too long.\n"), _username_);
        return;
    }

    // this is declared here to test if _token_buffer_ == nullptr (error condition)
    _token_buffer_ = new char[len + 1U](); // place to chop up the input
    if (_token_buffer_ == nullptr)         // if there was an error allocating the memory
    {
        UserInput::_ui_out(PSTR(">%s$ERROR: cannot allocate ram for _token_buffer_.\n"), _username_);
        return;
    }
    // end error checking

    size_t num_ptrs = (1U + _max_depth_ + _max_args_);
    size_t tokens_received = 0;    // amount of delimiter separated tokens  
    //_rec_num_arg_strings_ = 0;     // number of tokens read from data    
    bool launch_attempted = false; // made it to launchFunction if true
    bool command_matched = false;  // error sentinel
    CommandConstructor *cmd;       // command parameters pointer
    Parameters prm;                // Parameters struct    

    // delimiter string literal array       
    const char* delimiters[] =
    {
        _delim_        
    };
    // delimiter length string literal array
    size_t delimiter_lens[] =
    {
        _delim_len_        
    };

    // tokenize the input
    tokens_received = UserInput::getTokens(data,                    // input data uint8_t array
                                           len,                     // input len
                                           _token_buffer_,          // pointer to char array, size of len + 1
                                           buffSZ(_token_buffer_),  // the size of token_buffer
                                           _data_pointers_,         // token_buffer pointers
                                           _data_pointers_index_,   // index of token_buffer pointer array
                                           num_ptrs,                // _data_pointers_[MAX], _data_pointers_index_[MAX]
                                           delimiters,              // delimiter string literal array, const char**
                                           delimiter_lens,          // delimiter strlen array
                                           buffSZ(delimiter_lens),  // delimiters[MAX], delimiter_lens[MAX]
                                           _c_str_delim_,           // const char* c-string delimiter
                                           _c_str_delim_len_,       // c-string delim len
                                           _null_,                  // token_buffer sep char, _null_ == '\0'
                                           _control_char_sequence_);// control character sequence
    
    _data_pointers_index_max_ = tokens_received; // set index max to tokens received

    if (tokens_received == 0) // error condition
    {
        delete[] _token_buffer_;
        UserInput::_ui_out(PSTR(">%s$ERROR: No tokens retrieved.\n"), _username_);
        return;
    }
    // end error condition

    bool *input_type_match_flag = new bool[_max_args_](); // argument type-match flag array
    bool all_arguments_valid = true;                      // error sentinel

    for (cmd = _commands_head_; cmd != NULL; cmd = cmd->next_command) // iterate through CommandConstructor linked-list
    {
        // cmd->prm[0].command is a pointer to the root command c-string in PROGMEM
        size_t cmd_len_pgm = pgm_read_dword(&(cmd->prm[0].command_length));
        if (memcmp_P(_data_pointers_[0],
                     cmd->prm[0].command,
                     cmd_len_pgm) == false) // match root command
        {
            memcpy_P(&prm, &(cmd->prm[0]), sizeof(prm)); // move Parameters variables from PROGMEM to sram for work
            _current_search_depth_ = 1;                  // start searching for subcommands at depth 1
            _data_pointers_index_ = 1;                   // index 1 of _data_pointers_ is the token after the root command
            command_matched = true;                      // root command match flag
            _failed_on_subcommand_ = 0;                  // subcommand error index
            bool subcommand_matched = false;             // subcommand match flag
            uint16_t command_id = root;
            // see if command has any subcommands, validate input types, try to launch function
            UserInput::_launchLogic(cmd,                   // CommandConstructor pointer, contains target function pointer
                                    prm,                   // ReadCommandFromBuffer Parameters structure reference
                                    tokens_received,       // how many tokens were retrieved
                                    all_arguments_valid,   // type error sentinel
                                    launch_attempted,      // function launch sentinel
                                    input_type_match_flag, // type error flag array
                                    subcommand_matched,    // subcommand match flag
                                    command_id);           // Parameters command unique id
            break;                                         // break command iterator for loop
        }                                                  // end command logic
    }                                                      // end root command for loop
    if (!launch_attempted && _default_function_ != NULL)   // if there was no command match and a default function is configured
    {
        UserInput::_readCommandFromBufferErrorOutput(cmd,
                                                     prm,
                                                     command_matched,
                                                     input_type_match_flag,
                                                     all_arguments_valid,
                                                     data);
        (*_default_function_)(this); // run the default function
    }

    // cleanup
    for (size_t i = 0; i < (1U + _max_depth_ + _max_args_); ++i) // reinit _data_pointers_
    {
        _data_pointers_[i] = NULL;
    }
    delete[] _token_buffer_;
    delete[] input_type_match_flag;
}

void UserInput::getCommandFromStream(Stream &stream, size_t rx_buffer_size)
{
    if (!_begin_) // error
    {
        return;
    }
    if (_stream_buffer_allocated_ == false)
    {
        _stream_data_ = new uint8_t[rx_buffer_size]; // an array to store the received data
        if (_stream_data_ == nullptr)                // if there was an error allocating the memory
        {
            UserInput::_ui_out(PSTR(">%s$ERROR: cannot allocate ram for _stream_data_\n"), _username_);
            return;
        }
        _stream_buffer_allocated_ = true;
        _term_index_ = 0;
    }
    char *rc = (char *)_stream_data_; // point rc to allocated memory
    while (stream.available() > 0 && _new_stream_data_ == false)
    {
        rc[_stream_data_index_] = stream.read();
        if (rc[_stream_data_index_] == _term_[_term_index_])
        {
            _stream_data_[_stream_data_index_] = _null_;
            if (_term_index_ < _term_len_)
            {
                _term_index_++;
            }
            if (_term_index_ == _term_len_)
            {
                _new_stream_data_ = true;
            }
        }
        if (_stream_data_index_ < rx_buffer_size)
        {
            _stream_data_index_++;
        }
    }
    if (_new_stream_data_ == true)
    {
        UserInput::readCommandFromBuffer(_stream_data_, _stream_data_index_);
        _stream_data_index_ = 0;
        _new_stream_data_ = false;
        delete[] _stream_data_;
        _stream_buffer_allocated_ = false;
    }
}

char *UserInput::nextArgument()
{
    // return NULL if there are no more arguments
    if (_data_pointers_index_ < (_max_depth_ + _max_args_) &&
        _data_pointers_index_ < _data_pointers_index_max_)
    {
        _data_pointers_index_++;
        return _data_pointers_[_data_pointers_index_];
    }
    else
    {
        return NULL;
    }
    return NULL; // guard return
}

bool UserInput::outputIsAvailable()
{
    return _output_flag_;
}

bool UserInput::outputIsEnabled()
{
    return _output_enabled_;
}

void UserInput::outputToStream(Stream &stream)
{
    if (UserInput::outputIsAvailable()) // if there's something to print
    {
        stream.println(_output_buffer_); // print output_buffer, which is formatted into a string by UserInput's methods
        UserInput::clearOutputBuffer();
    }
}

void UserInput::clearOutputBuffer(bool overwrite_contents)
{
    if (UserInput::outputIsEnabled())
    {
        _output_buffer_bytes_left_ = _output_buffer_len_; //  reset output_buffer's index        
        if (!overwrite_contents)
        {
            _output_buffer_[0] = _null_; // soft reinit _output_buffer_ 
        }
        else
        {
            for(size_t i = 0; i < _output_buffer_len_; ++i)
            {
                _output_buffer_[i] = _null_;    // overwrite buffer contents
            }
        }
    }
    _output_flag_ = false;
}

size_t UserInput::getTokens(uint8_t *data,
                            size_t len,
                            char *token_buffer,
                            size_t token_buffer_len,
                            char **token_pointers,
                            uint8_t &token_pointer_index,
                            size_t num_token_ptrs,
                            const char **delimiter_strings,
                            size_t *delimiter_lens,
                            size_t num_delimiters,
                            const char *c_str_delim,
                            size_t c_str_delim_len,
                            char &token_buffer_sep,
                            const char *control_char_sequence)
{
    size_t data_pos = 0;
    size_t token_buffer_index = 0;    
    token_pointer_index = 0;
    bool point_to_beginning_of_token = true; // assign pointer to &token_buffer[token_buffer_index] if true

    while (data_pos < len)
    {
        UserInput::_getTokensDelimiters(data,
                                        data_pos,
                                        delimiter_strings,
                                        delimiter_lens,
                                        num_delimiters,
                                        token_buffer,
                                        token_buffer_index,
                                        point_to_beginning_of_token,
                                        token_buffer_sep);

        if (c_str_delim != NULL && c_str_delim[0] == (char)data[data_pos])
        {
            UserInput::_getTokensCstrings(data,
                                          len,
                                          data_pos,
                                          c_str_delim,
                                          c_str_delim_len,
                                          token_buffer,
                                          token_buffer_index,
                                          point_to_beginning_of_token,
                                          token_pointers,
                                          token_pointer_index,
                                          token_buffer_sep);
        }
        else // non c-string
        {
            UserInput::_getTokensChar(data,
                                      len,
                                      data_pos,
                                      token_buffer,
                                      token_buffer_index,
                                      point_to_beginning_of_token,
                                      token_pointers,
                                      token_pointer_index,
                                      token_buffer_sep,
                                      control_char_sequence);
        }
    }
    return token_pointer_index;
}

bool UserInput::validateNullSepInput(UITYPE arg_type,
                                     char **token_pointers,
                                     size_t token_pointer_index,
                                     char &neg_sign,
                                     char &float_sep)
{
    size_t strlen_data = strlen(token_pointers[token_pointer_index]);    
    size_t start = ((char)token_pointers[token_pointer_index][0] == neg_sign) ? 1 : 0;
    
    // for unsigned integers, integers, and floating point numbers
    if ((uint8_t)arg_type <= (size_t)UITYPE::FLOAT)
    {
        size_t found_dot = 0;
        size_t num_digits = 0;
        size_t not_digits = 0;
        if ((uint8_t)arg_type < (size_t)UITYPE::INT16_T && start == 1) // error
        {
            return false; // uint cannot be negative
        }        
        for (size_t j = start; j < strlen_data; ++j)
        {
            if (token_pointers[token_pointer_index][j] == float_sep)
            {
                found_dot++;
            }
            else if (isdigit(token_pointers[token_pointer_index][j]) == true)
            {
                num_digits++;
            }
            else
            {
                not_digits++;
            }
        }        
        //int/uint error test
        if ((uint8_t)arg_type <= (uint8_t)UITYPE::INT16_T && 
            (found_dot > 0U || not_digits > 0U || (num_digits + start) != strlen_data))
        {
            return false;
        }
        //float error test
        if ((uint8_t)arg_type == (uint8_t)UITYPE::FLOAT && 
            (found_dot > 1U || not_digits > 0U || (num_digits + found_dot + start) != strlen_data))
        {
            return false;
        }
        return true; // no errors
    }

    // char and c-string
    if ((uint8_t)arg_type == (uint8_t)UITYPE::CHAR ||
        (uint8_t)arg_type == (uint8_t)UITYPE::C_STRING)
    {
        if ((uint8_t)arg_type == (uint8_t)UITYPE::CHAR && strlen_data > 1) // error
        {
            return false; // looking for a single char value, not a c-string
        }
        for (size_t j = 0; j < strlen_data; ++j)
        {   // if we encounter anything that isn't one of these four things, something isn't right
            size_t test_bool[4] = {false};
            test_bool[0] = isprint(token_pointers[token_pointer_index][j]);
            test_bool[1] = ispunct(token_pointers[token_pointer_index][j]);
            test_bool[2] = iscntrl(token_pointers[token_pointer_index][j]);
            test_bool[3] = isdigit(token_pointers[token_pointer_index][j]);
            // no match
            if (test_bool[0] == false &&
                test_bool[1] == false &&
                test_bool[2] == false &&
                test_bool[3] == false)
            {
                return false;
            }
        }
        return true;
    }

    // no type specified
    if ((uint8_t)arg_type == (uint8_t)UITYPE::NOTYPE)
    {        
        return true; // no type validation performed
    }
    return false; // error, unknown type
}

/*
    private methods
*/
void UserInput::_ui_out(const char *fmt, ...)
{
    if (UserInput::outputIsEnabled())
    {
        va_list args;        // ... parameter pack list
        va_start(args, fmt); // set the parameter pack list index here
        int err = vsnprintf_P(_output_buffer_ + abs((int)_output_buffer_bytes_left_ - (int)_output_buffer_len_), _output_buffer_bytes_left_, fmt, args);
        va_end(args);                   // we are done with the parameter pack
        if (err > _output_buffer_bytes_left_) // overflow condition
        {
            // attempt warn
            snprintf_P(_output_buffer_, _output_buffer_len_,
                       PSTR("Insufficient output buffer, increase output buffer to %d bytes.\n\0"),
                       (abs(err - (int)_output_buffer_bytes_left_) + (int)_output_buffer_len_));
            _output_flag_ = true;
            return;
        }
        else if (err < 0) // encoding error
        {
            // attempt warn
            snprintf_P(_output_buffer_, _output_buffer_len_, PSTR("Encoding error.\n\0"));
            _output_flag_ = true;
            return;
        }
        else
        {
            _output_buffer_bytes_left_ -= err;
        }
        _output_flag_ = true;
    }
}

void UserInput::_readCommandFromBufferErrorOutput(CommandConstructor *cmd,
                                                  Parameters &prm,
                                                  bool &command_matched,
                                                  bool *input_type_match_flag,
                                                  bool &all_arguments_valid,
                                                  uint8_t *data)
{
    // format a string with useful information
    if (UserInput::outputIsEnabled())
    {
        /*
            potential silent crash if _failed_on_subcommand_ > cmd->param_array_len
            user introduced error condition, if they enter a parameter array length that is
            greater than the actual array length
        */
        if (_failed_on_subcommand_ > cmd->param_array_len) // error (deprecated with Parameters checking, redundant)
        {
            memcpy_P(&prm, &(cmd->prm[0]), sizeof(prm));
            UserInput::_ui_out(PSTR("OOB Parameters array element access attempted for command %s.\n"
                                    "CommandConstructor(Parameters, !fix this number!, tree_depth)\n"),
                               prm.command);
            return;
        }
        memcpy_P(&prm, &(cmd->prm[_failed_on_subcommand_]), sizeof(prm));
        UserInput::_ui_out(PSTR(">%s$Invalid input: "), _username_);
        if (command_matched == true)
        {
            // constrain err_n_args to UI_MAX_ARGS + 1
            size_t err_n_args = ((_data_pointers_index_max_ - _failed_on_subcommand_ - 1U) > (UI_MAX_ARGS + 1))
                                    ? (UI_MAX_ARGS + 1)
                                    : (_data_pointers_index_max_ - _failed_on_subcommand_ - 1U);
            if (err_n_args > 0)
            {
                for (size_t i = 0; i < (_failed_on_subcommand_ + 1U); ++i)
                {
                    UserInput::_ui_out(PSTR("%s "), _data_pointers_[i]); // add subcommands to echo
                }
                UserInput::_ui_out(PSTR("\n"));
                bool print_subcmd_err = true;
                for (size_t i = 0; i < prm.max_num_args; ++i)
                {
                    if (input_type_match_flag[i] == false ||
                        _data_pointers_[1 + _failed_on_subcommand_ + i] == NULL)
                    {
                        uint8_t _type = (uint8_t)UserInput::_getArgType(prm, i);
                        char _type_char_array[UI_INPUT_TYPE_STRINGS_PGM_LEN];
                        memcpy_P(&_type_char_array, &UserInput_type_strings_pgm[_type], sizeof(_type_char_array));
                        if ((UITYPE)_type != UITYPE::NO_ARGS && _data_pointers_[1 + _failed_on_subcommand_ + i] == NULL)
                        {
                            UserInput::_ui_out(PSTR(" 'INPUT NOT RECEIVED'*(%s REQUIRED)\n"), _type_char_array);
                        }
                        else
                        {
                            if (prm.sub_commands > 0 && print_subcmd_err == true)
                            {
                                print_subcmd_err = false;
                                UserInput::_ui_out(PSTR(" '%s'*(ENTER VALID SUBCOMMAND)\n"), _data_pointers_[1 + _failed_on_subcommand_ + i]);
                            }
                            else if ((prm.sub_commands == 0 || err_n_args > 1) && (UITYPE)_type == UITYPE::NO_ARGS)
                            {
                                UserInput::_ui_out(PSTR(" '%s'*(LEAVE BLANK)\n"), _data_pointers_[1 + _failed_on_subcommand_ + i]);
                            }
                            else
                            {
                                UserInput::_ui_out(PSTR(" '%s'*(%s)\n"), _data_pointers_[1 + _failed_on_subcommand_ + i], _type_char_array);
                            }
                        }
                    }
                    else
                    {
                        UserInput::_ui_out(PSTR(" '%s'(OK)\n"), _data_pointers_[1 + _failed_on_subcommand_ + i]);
                    }
                }
                UserInput::_ui_out(PSTR("\n"));
                return;
            }
            UserInput::_ui_out(PSTR("%s\n"), (char *)data);
            return;
        }
        else // command not matched
        {
            UserInput::_ui_out(PSTR("%s\n command <%s> unknown\n"), (char *)data, _data_pointers_[0]);
        }
    }
}

void UserInput::_launchFunction(CommandConstructor *cmd,
                                Parameters &prm,
                                size_t tokens_received)
{
    if (UserInput::outputIsEnabled())
    {
        UserInput::_ui_out(PSTR(">%s$"), _username_);
        for (size_t i = 0; i < _data_pointers_index_max_; ++i)
        {
            size_t strlen_data = strlen(_data_pointers_[i]);
            for (size_t j = 0; j < strlen_data; ++j)
            {
                if (iscntrl(_data_pointers_[i][j])) // format buffer with escaped char
                {
                    char buf[UI_ESCAPED_CHAR_PGM_LEN]{};
                    UserInput::_ui_out(PSTR("%s"), UserInput::_escapeCharactersSoTheyPrint(_data_pointers_[i][j], buf));
                }
                else
                {
                    UserInput::_ui_out(PSTR("%c"), _data_pointers_[i][j]); // single char
                }
            }
            UserInput::_ui_out(PSTR(" ")); // add a space
        }
        UserInput::_ui_out(PSTR("\n"));
    }
    _data_pointers_index_ = _current_search_depth_ - 1;

    if (prm.function != NULL)
    {
        #if defined(__DEBUG_LAUNCH_FUNCTION__)
        UserInput::_ui_out(PSTR("launch command_id %u\n"), prm.command_id);
        #endif
        prm.function(this);
    }
    else
    {
        memcpy_P(&prm, &(cmd->prm[0]), sizeof(prm));
        #if defined(__DEBUG_LAUNCH_FUNCTION__)
        UserInput::_ui_out(PSTR("launch command_id %u\n"), prm.command_id);
        #endif
        prm.function(this);
    }
}

void UserInput::_launchLogic(CommandConstructor *cmd,
                             Parameters &prm,
                             size_t tokens_received,
                             bool &all_arguments_valid,
                             bool &launch_attempted,
                             bool *input_type_match_flag,
                             bool &subcommand_matched,
                             uint16_t &command_id)
{
    // error
    if (tokens_received > 1 &&
        prm.sub_commands == 0 &&
        prm.max_num_args == 0)
    {
        #if defined(__DEBUG_LAUNCH_LOGIC__)
        UserInput::_ui_out(PSTR(">%s$launchLogic: too many tokens for command_id %u\n"), _username_, prm.command_id);
        #endif
        return;
    }

    // command with no arguments
    if (subcommand_matched == false &&
        tokens_received == 1 &&
        prm.max_num_args == 0)
    {
        #if defined(__DEBUG_LAUNCH_LOGIC__)
        UserInput::_ui_out(PSTR(">%s$launchLogic: command_id %u\n"), _username_, prm.command_id);
        #endif

        launch_attempted = true;                                          // don't run default callback
        UserInput::_launchFunction(cmd, prm, tokens_received); // launch the matched command
        return;
    }

    // subcommand with no arguments
    if (tokens_received == 1 &&
        _current_search_depth_ > 1 &&
        subcommand_matched == true &&
        prm.max_num_args == 0)
    {
        #if defined(__DEBUG_LAUNCH_LOGIC__)
        UserInput::_ui_out(PSTR(">%s$launchLogic: command_id %u\n"), _username_, prm.command_id);
        #endif
        launch_attempted = true;                                          // don't run default callback
        UserInput::_launchFunction(cmd, prm, tokens_received); // launch the matched command
        return;
    }

    // command with arguments, potentially has subcommands but none were entered
    if ( //_current_search_depth > 1 &&
        subcommand_matched == false &&
        tokens_received > 1 &&
        prm.max_num_args > 0)
    {
        UserInput::_getArgs(tokens_received, input_type_match_flag, prm, all_arguments_valid);
        if (_rec_num_arg_strings_ >= prm.num_args &&
            _rec_num_arg_strings_ <= prm.max_num_args &&
            all_arguments_valid == true)
        {
            #if defined(__DEBUG_LAUNCH_LOGIC__)
            UserInput::_ui_out(PSTR(">%s$launchLogic: command_id %u\n"), _username_, prm.command_id);
            #endif
            launch_attempted = true;                                          // don't run default callback
            UserInput::_launchFunction(cmd, prm, tokens_received); // launch the matched command
        }
        // if !match, error
        return;
    }

    // command with arguments (max depth)
    if (_current_search_depth_ == (cmd->tree_depth) &&
        tokens_received > 1 &&
        prm.max_num_args > 0 &&
        prm.sub_commands == 0)
    {
        UserInput::_getArgs(tokens_received, input_type_match_flag, prm, all_arguments_valid);
        //  if we received at least min and less than max arguments and they are valid
        if (_rec_num_arg_strings_ >= prm.num_args &&
            _rec_num_arg_strings_ <= prm.max_num_args &&
            all_arguments_valid == true)
        {
            #if defined(__DEBUG_LAUNCH_LOGIC__)
            UserInput::_ui_out(PSTR(">%s$launchLogic: command_id %u\n"), _username_, prm.command_id);
            #endif
            launch_attempted = true;                                          // don't run default callback
            UserInput::_launchFunction(cmd, prm, tokens_received); // launch the matched command
        }
        // if !match, error
        return;
    }

    // subcommand search
    subcommand_matched = false;
    #if defined(__DEBUG_SUBCOMMAND_SEARCH__)
    UserInput::_ui_out(PSTR(">%s$launchLogic: search depth (%d)\n"), _username_, _current_search_depth);
    #endif
    if (_current_search_depth_ <= (cmd->tree_depth)) // dig starting at depth 1
    {
        // this index starts at one because the parameter array's first element will be the root command
        for (size_t j = 1; j < (cmd->param_array_len + 1U); ++j) // through the parameter array
        {
            size_t cmd_len_pgm = pgm_read_dword(&(cmd->prm[0].command_length));
            if (memcmp_P(_data_pointers_[_data_pointers_index_],
                         cmd->prm[j].command,
                         cmd_len_pgm) == false) // match subcommand string
            {
                memcpy_P(&prm, &(cmd->prm[j]), sizeof(prm));
                if (prm.depth == _current_search_depth_ && prm.parent_command_id == command_id)
                {
                    #if defined(__DEBUG_SUBCOMMAND_SEARCH__)
                    UserInput::_ui_out(PSTR(">%s$launchLogic: subcommand (%s) match, "
                                            "command_id (%u), (%d) subcommands, max_num_args (%d)\n"),
                                       _username_, prm.command, prm.command_id, prm.sub_commands, prm.max_num_args);
                    #endif
                    // subcommand matched
                    if (tokens_received > 0)
                    {
                        tokens_received--;       // subtract subcommand from tokens received
                        _data_pointers_index_++; // increment to the next token
                    }
                    command_id = prm.command_id; // set command_id to matched subcommand
                    subcommand_matched = true;   // subcommand matched
                    _failed_on_subcommand_ = j;  // set error index
                    break;                       // break out of the loop
                }
            }
        }
        if (_current_search_depth_ < (cmd->tree_depth))
        {
            _current_search_depth_++;
        }
    }                               // end subcommand search
    if (subcommand_matched == true) // recursion
    {
        #if defined(__DEBUG_SUBCOMMAND_SEARCH__)
        UserInput::_ui_out(PSTR("recurse, command_id (%u)\n"), prm.command_id);
        #endif
        UserInput::_launchLogic(cmd,
                                prm,
                                tokens_received,
                                all_arguments_valid,
                                launch_attempted,
                                input_type_match_flag,
                                subcommand_matched,
                                command_id);
    }
}

char *UserInput::_escapeCharactersSoTheyPrint(char input, char *buf)
{
    if (input < (char)32 || input == (char)34)
    {
        buf[0] = (char)92; // (char)92 == '\\'
        switch (input)
        {
        case (char)'\0': {buf[1] = '0'; break;}
        case (char)'\a': {buf[1] = 'a'; break;}
        case (char)'\b': {buf[1] = 'b'; break;}
        case (char)'\t': {buf[1] = 't'; break;}
        case (char)'\n': {buf[1] = 'n'; break;}
        case (char)'\v': {buf[1] = 'v'; break;}
        case (char)'\f': {buf[1] = 'f'; break;}
        case (char)'\r': {buf[1] = 'r'; break;}
        case (char)'\e': {buf[1] = 'e'; break;}
        case (char)'\"': {buf[1] = '"'; break;}
        default: break;
        }
        buf[2] = _null_; // terminate
        return buf;
    }
    buf[0] = input;  // pass through input
    buf[1] = _null_; // terminate the string
    return buf;      // not a control char
}

char UserInput::_combineControlCharacters(char input)
{
    switch (input)
    {
    case '0': return (char)'\0';
    case 'a': return (char)'\a';
    case 'b': return (char)'\b';
    case 't': return (char)'\t';
    case 'n': return (char)'\n';
    case 'v': return (char)'\v';
    case 'f': return (char)'\f';
    case 'r': return (char)'\r';
    case 'e': return (char)'\e';
    case '"': return (char)'\"';
    default:  return (char)'*'; // * error
    }
}

bool UserInput::_addCommandAbort(CommandConstructor &cmd, Parameters &prm)
{
    bool error = true;
    if (prm.function == NULL && prm.depth == 0)
    {
        UserInput::_ui_out(PSTR("root command function pointer cannot be NULL\n"));
        error = false;
    }
    size_t cmd_len = strlen(prm.command);
    if (cmd_len > UI_MAX_CMD_LEN)
    {
        UserInput::_ui_out(PSTR("command too long, increase UI_MAX_CMD_LEN or reduce command length.\n"));
        error = false;
    }
    if (cmd_len != prm.command_length)
    {
        if (cmd_len > prm.command_length)
        {
            UserInput::_ui_out(PSTR("command_length too large for command\n"));
        }
        else
        {
            UserInput::_ui_out(PSTR("command_length too small for command\n"));
        }
        error = false;
    }
    if (prm.depth > UI_MAX_DEPTH)
    {
        UserInput::_ui_out(PSTR("depth\n"));
        error = false;
    }
    if (prm.sub_commands > UI_MAX_SUBCOMMANDS)
    {
        UserInput::_ui_out(PSTR("sub_commands\n"));
        error = false;
    }
    if (prm.num_args > UI_MAX_ARGS)
    {
        UserInput::_ui_out(PSTR("num_args\n"));
        error = false;
    }
    if (prm.max_num_args > UI_MAX_ARGS)
    {
        UserInput::_ui_out(PSTR("max_num_args\n"));
        error = false;
    }
    if (prm.num_args > prm.max_num_args)
    {
        UserInput::_ui_out(PSTR("num_args must be less than max_num_args\n"));
        error = false;
    }
    if (error == false)
    {
        if (prm.depth > 0)
        {
            UserInput::_ui_out(PSTR("%s Parameters error! Subcommand not added.\n"),
                               prm.command);
        }
        else
        {
            UserInput::_ui_out(PSTR("%s Parameters error! Command not added.\n"),
                               prm.command);
        }
    }
    return error;
}

UITYPE UserInput::_getArgType(Parameters &prm, size_t index)
{
    if (prm.argument_flag == UI_ARG_HANDLING::no_args) return UITYPE::NO_ARGS;
    if (prm.argument_flag == UI_ARG_HANDLING::one_type) return prm.arg_type_arr[0];
    if (prm.argument_flag == UI_ARG_HANDLING::type_arr) return prm.arg_type_arr[index];

    return UITYPE::_LAST; // return error if no match
}

void UserInput::_getArgs(size_t &tokens_received,
                         bool *input_type_match_flag,
                         Parameters &prm,
                         bool &all_arguments_valid)
{
    _rec_num_arg_strings_ = 0; // number of tokens read from data
    for (size_t i = 0; i < (tokens_received - 1U); ++i)
    {
        input_type_match_flag[i] = UserInput::validateNullSepInput(UserInput::_getArgType(prm, i),
                                                                   _data_pointers_,
                                                                   _data_pointers_index_ + i,
                                                                   _neg_,
                                                                   _dot_); // validate the token
        _rec_num_arg_strings_++;
        if (input_type_match_flag[i] == false) // if the token was not valid input
        {
            all_arguments_valid = false; // set the error sentinel
        }
    }
}

char *UserInput::_addEscapedControlCharToBuffer(char *buf, size_t &idx, const char *input, size_t input_len)
{
    char *start = &buf[idx];
    char tmp_esc_chr[UI_ESCAPED_CHAR_PGM_LEN]{};
    for (size_t i = 0; i < input_len; ++i)
    {
        *tmp_esc_chr = *UserInput::_escapeCharactersSoTheyPrint(input[i], tmp_esc_chr);
        for (uint8_t i = 0; i < strlen(tmp_esc_chr); ++i)
        {
            buf[idx] = tmp_esc_chr[i];
            idx++;
        }
    }
    buf[idx] = _null_; // terminate string
    idx++;
    return start;
}

void UserInput::_getTokensDelimiters(uint8_t *data,
                                     size_t &data_pos,
                                     const char **delimiter_strings,
                                     size_t *delimiter_lens,
                                     size_t num_delimiters,
                                     char *token_buffer,
                                     size_t &token_buffer_index,
                                     bool &point_to_beginning_of_token,
                                     char &sep)
{
    for (size_t i = 0; i < num_delimiters; ++i) // skip over delimiters
    {
        if (delimiter_strings[i][0] == (char)data[data_pos])
        {
            if (delimiter_lens[i] > 1U)
            {
                char *ptr = (char *)&data[data_pos];
                if (memcmp(delimiter_strings[i], ptr, delimiter_lens[i]) == 0)
                {
                    // match
                    data_pos += delimiter_lens[i] + 1U;
                    point_to_beginning_of_token = true;
                    token_buffer[token_buffer_index] = sep;
                    token_buffer_index++;
                    break;
                }
            }
            else
            {
                // match
                data_pos++;
                point_to_beginning_of_token = true;
                token_buffer[token_buffer_index] = sep;
                token_buffer_index++;
                break; // break for loop
            }
        }
    }
}

void UserInput::_getTokensCstrings(uint8_t *data,
                                   size_t len,
                                   size_t &data_pos,
                                   const char *c_str_delim,
                                   size_t c_str_delim_len,
                                   char *token_buffer,
                                   size_t &token_buffer_index,
                                   bool &point_to_beginning_of_token,
                                   char **token_pointers,
                                   uint8_t &token_pointer_index,
                                   char &sep)
{
    if (c_str_delim_len > 1U)
    {
        char *ptr = (char *)&data[data_pos];
        if (memcmp(c_str_delim, ptr, c_str_delim_len) == 0)
        {
            // match
            data_pos += c_str_delim_len + 1U;
            // point to beginning of c-string
            ptr = (char *)&data[data_pos];
            // search for next c-string delimiter
            char *end_ptr = (char *)memchr(ptr, c_str_delim[0], (len - data_pos));
            while (end_ptr != NULL ||
                   data_pos < len)
            {
                if (memcmp(c_str_delim, end_ptr, c_str_delim_len) == 0)
                {
                    // match
                    // memcpy c-string to token buffer
                    size_t size = ((end_ptr - (char *)data) - (ptr - (char *)data));
                    if ((size + 1U) < (len - data_pos))
                    {
                        memcpy(token_buffer + token_buffer_index, ptr, size);
                        token_pointers[token_pointer_index] = &token_buffer[token_buffer_index];
                        token_pointer_index++;
                        token_buffer_index += size + 1U;
                        token_buffer[token_buffer_index] = sep;
                        token_buffer_index++;
                        data_pos += size + 1U;
                    }
                    break;
                }
                else
                {
                    end_ptr = (char *)memchr(end_ptr, c_str_delim[0], (len - data_pos));
                    data_pos += end_ptr - (char *)data;
                }
            }
        }
    }
    else
    {
        // match
        data_pos++;
        // point to beginning of c-string
        char *ptr = (char *)&data[data_pos];
        // search for next c-string delimiter
        char *end_ptr = (char *)memchr(ptr, c_str_delim[0], (len - data_pos));
        if (end_ptr != NULL)
        {
            // memcpy
            size_t size = ((end_ptr - (char *)data) - (ptr - (char *)data));
            if ((size + 1U) < (len - data_pos))
            {
                memcpy(token_buffer + token_buffer_index, ptr, size);
                token_pointers[token_pointer_index] = &token_buffer[token_buffer_index];
                token_pointer_index++;
                token_buffer_index += size + 1U;
                token_buffer[token_buffer_index] = sep;
                token_buffer_index++;
                data_pos += size + 1U;
            }
        }     
    }
}

void UserInput::_getTokensChar(uint8_t *data,
                               size_t len,
                               size_t &data_pos,
                               char *token_buffer,
                               size_t &token_buffer_index,
                               bool &point_to_beginning_of_token,
                               char **token_pointers,
                               uint8_t &token_pointer_index,
                               char& token_buffer_sep,
                               const char *control_char_sequence)
{
    if ((char)data[data_pos] == control_char_sequence[0] && 
        (char)data[data_pos + 1U] == control_char_sequence[1] && 
        (data_pos + 2 < len))
    {
        if (iscntrl(UserInput::_combineControlCharacters((char)data[data_pos + 1])))
        {
            token_buffer[token_buffer_index] = UserInput::_combineControlCharacters((char)data[data_pos + 2]);
            if (point_to_beginning_of_token)
            {
                token_pointers[token_pointer_index] = &token_buffer[token_buffer_index];
                token_pointer_index++;
                point_to_beginning_of_token = false;
            }
            data_pos = data_pos + 2;
            token_buffer_index++;
        }
    }
    else
    {
        token_buffer[token_buffer_index] = data[data_pos];
        if (point_to_beginning_of_token)
        {
            token_pointers[token_pointer_index] = &token_buffer[token_buffer_index];
            token_pointer_index++;
            point_to_beginning_of_token = false;
        }
        token_buffer_index++;
        data_pos++;
    }
}