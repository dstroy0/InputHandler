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
    size_t buf_sz = _term_len_ + _delim_len_ + _c_str_delim_len_ + 3; // +3 null separators
    // allocate char buffer large enough to print these potential control characters
    char *buf = new char[buf_sz * UI_ESCAPED_CHAR_PGM_LEN]();
    size_t idx = 0;    
    char *term = _addEscapedControlCharToBuffer(buf, idx, _term_, _term_len_);
    char *delim = _addEscapedControlCharToBuffer(buf, idx, _delim_, _delim_len_);
    char *c_str_delim = _addEscapedControlCharToBuffer(buf, idx, _c_str_delim_, _c_str_delim_len_);    
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
                       term,
                       delim,
                       c_str_delim,
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
    size_t ptrs = 1 + _max_depth_ + _max_args_;
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

    size_t tokens_received = 0;    // amount of delimiter separated tokens
    size_t token_buffer_index = 0; // token buffer index
    size_t data_index = 0;         // data iterator
    _data_pointers_index_ = 0;     // token buffer pointers
    _rec_num_arg_strings_ = 0;     // number of tokens read from data
    bool match = false;            // command string match
    bool command_matched = false;  // error sentinel
    CommandConstructor *cmd;       // command parameters pointer
    Parameters prm;                // Parameters struct
    size_t ptrs = 1 + _max_depth_ + _max_args_;
    /*
        this tokenizes an input buffer, it should work with any 8 bit input type that represents char
        char tokenized_string[] = "A\0Tokenized\0C-string\0"
        char non_tokenized_string[] = "A Non Tokenized C-string" <-- still has a \0 at the end of the string to terminate it
    */
    // reinit _data_pointers_
    for (size_t i = 0; i < ptrs; ++i)
    {
        _data_pointers_[i] = NULL;
    }

    while (true)
    {
        if (UserInput::getToken(data, len, data_index, token_buffer_index) == true)
        {
            tokens_received++;           // increment tokens_received
            if (tokens_received == ptrs) // index sentinel
            {
                break;
            }
        }
        else
        {
            break;
        }
    }
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
                                    match,                 // function launch sentinel
                                    input_type_match_flag, // type error flag array
                                    subcommand_matched,    // subcommand match flag
                                    command_id);           // Parameters command unique id
            break;                                         // break command iterator for loop
        }                                                  // end command logic
    }                                                      // end root command for loop
    if (!match && _default_function_ != NULL)              // if there was no command match and a default function is configured
    {
        UserInput::_readCommandFromBufferErrorOutput(cmd,
                                                     prm,
                                                     command_matched,
                                                     input_type_match_flag,
                                                     all_arguments_valid,
                                                     data);
        (*_default_function_)(this); // run the default function
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

void UserInput::clearOutputBuffer()
{
    if (UserInput::outputIsEnabled())
    {
        _output_buffer_bytes_left_ = _output_buffer_len_; //  reset output_buffer's index
        //  this maybe doesnt need to be done
        for (size_t i = 0; i < _output_buffer_len_; ++i)
        {
            _output_buffer_[i] = _null_; // reinit output_buffer
        }
    }
    _output_flag_ = false;
}

/*
    protected methods
*/
bool UserInput::getToken(uint8_t *data, size_t len, size_t &data_index, size_t& token_buffer_index)
{
    bool got_token = false;
    char incoming = _null_;              // cast data[data_index] to char and run tests on incoming
    bool token_flag[2] = {false, false}; // token state machine, point to a token once        
    
    for (size_t i = data_index; i < len; ++i)
    {
        incoming = (char)data[data_index];
        
        if (iscntrl(incoming)) // remove hanging control characters
        {            
            _token_buffer_[token_buffer_index] = _null_;
            token_buffer_index++;      
        }
        else if (incoming == _delim_[0]) // if _delim_len_ == 1 this is a match, else scan for whole delim
        {
            if (_delim_len_ == 1) // incoming is equal to _delim_[0] and the delimiter is one character in length
            {                
                _token_buffer_[token_buffer_index] = _null_;
                token_buffer_index++;
                data_index++;
                got_token = true;
                break;
            }
            else
            {                
                bool delim_char_match = true; // error flag
                size_t idx = data_index;
                char inc;
                for (size_t j = 1; j < (_delim_len_ + 1U); ++j)
                {
                    if ((j + i) < len)
                    {
                        idx++;
                        inc = (char)data[idx];
                        if (inc != _delim_[i])
                        {
                            delim_char_match = false;
                            break; // delimiter char pattern not matched
                        }
                    }
                    else
                    {
                        delim_char_match = false;
                        break; // delimiter char pattern terminated early
                    }
                }
                if (delim_char_match == true) // replace delimiter pattern with null
                {
                    _token_buffer_[token_buffer_index] = _null_;
                    data_index = data_index + _delim_len_;
                    token_buffer_index++;
                    got_token = true;
                    break;
                }
            }
        }
        else if (incoming == *_c_str_delim_) // switch logic for c-string input
        {            
            _token_buffer_[token_buffer_index] = _null_; // replace the c-string delimiter
            if ((data_index + 1U) < len) //  don't need to do this if we're at the end of user input
            {
                bool point_to_beginning_of_c_string = true; // c-string pointer assignment flag
                data_index++;
                token_buffer_index++;
                for (size_t j = data_index; j < len; ++j) // this for loop starts at whatever data_index is equal to and has the potential to iterate up to len
                {
                    incoming = (char)data[data_index]; // fetch the next incoming char
                    if (incoming == *_c_str_delim_)     // if the next incoming char is a '\"'
                    {
                        _token_buffer_[token_buffer_index] = _null_; // replace the c-string delimiter
                        data_index++;                      // increment data_index
                        token_buffer_index++;
                        got_token = true;                        
                        break;
                    }
                    _token_buffer_[token_buffer_index] = incoming;     // else assign incoming to _token_buffer_[data_index]
                    if (point_to_beginning_of_c_string == true) // a pointer will be assigned if point_to_beginning_of_c_string == true
                    {
                        _data_pointers_[_data_pointers_index_] = &_token_buffer_[token_buffer_index]; // point to this position in _token_buffer_
                        _data_pointers_index_++;                                               //  increment pointer index
                        point_to_beginning_of_c_string = false;                                //  only set one pointer per c-string
                        got_token = true;
                        #if defined(__DEBUG_GET_TOKEN__)
                        UserInput::_ui_out(PSTR("\n>%s$DEBUG: got the c-string token.\n"), _username_);
                        #endif
                    }
                    data_index++; // increment data index
                    token_buffer_index++;
                }
            }
        }
        else // this is a non c-string token
        {
            if (incoming == '\\' && (data_index + 1 < len))
            {                
                if (iscntrl(UserInput::_combineControlCharacters((char)data[data_index + 1])))
                {                    
                    _token_buffer_[token_buffer_index] = UserInput::_combineControlCharacters((char)data[data_index + 1]);
                    data_index++;
                    token_buffer_index++;
                }
                else
                {
                    _token_buffer_[token_buffer_index] = incoming;
                    token_buffer_index++;
                }                
            }
            else
            {
                _token_buffer_[token_buffer_index] = incoming; // assign incoming to _token_buffer_ at data_index 
                token_buffer_index++;
            }
            token_flag[0] = true;                   // set token available sentinel to true
        }

        if (token_flag[0] != token_flag[1]) // if the token state has changed
        {
            if (token_flag[0] == true) // if there's a new token
            {
                _data_pointers_[_data_pointers_index_] = &_token_buffer_[token_buffer_index - 1]; // assign a pointer the beginning of it                          
                _data_pointers_index_++;                                               // and increment the pointer index                
            }
            else
            {
                #if defined(__DEBUG_GET_TOKEN__)
                UserInput::_ui_out(PSTR("\n>%s$DEBUG: UserInput::getToken got_token == true token state machine.\n"),
                        _username_);
                #endif
                got_token = true;
                break;
            }
            token_flag[1] = token_flag[0]; // track the state
        }
        if (token_flag[0] == true && data_index == (len - 1))
        {
            #if defined(__DEBUG_GET_TOKEN__)
            UserInput::_ui_out(PSTR("\n>%s$DEBUG: UserInput::getToken() got_token == true end of data.\n"),
                    _username_);
            #endif
            got_token = true;
        }

        if (data_index < len) // if we are at the end of input data
        {
            data_index++; // increment buffer index                   
        }

        if (got_token == true)
        {
            #if defined(__DEBUG_GET_TOKEN__)
            UserInput::_ui_out(PSTR("\n>%s$DEBUG: UserInput::getToken() break for loop.\n"), _username_);
            #endif
            break;
        }
    }
    return got_token;
}

bool UserInput::validateUserInput(uint8_t arg_type, size_t _data_pointers_index_)
{
    size_t strlen_data = strlen(_data_pointers_[_data_pointers_index_]);
    bool found_negative_sign = ((char)_data_pointers_[_data_pointers_index_][0] == _neg_) ? true : false;
    size_t start = (found_negative_sign == true) ? 1 : 0;

    // for unsigned integers, integers, and floating point numbers
    if (arg_type <= (size_t)UITYPE::FLOAT)
    {
        uint8_t found_dot = 0;
        uint8_t num_digits = 0;
        uint8_t not_digits = 0;
        if (arg_type < (size_t)UITYPE::INT16_T && start == 1) // error
        {
            return false; // uint cannot be negative
        }        
        for (size_t j = start; j < strlen_data; ++j)
        {
            if (_data_pointers_[_data_pointers_index_][j] == _dot_)
            {
                found_dot++;
            }
            else if (isdigit(_data_pointers_[_data_pointers_index_][j]) == true)
            {
                num_digits++;
            }
            else
            {
                not_digits++;
            }
        }        
        //int/uint error test
        if (arg_type <= (uint8_t)UITYPE::INT16_T && 
            (found_dot > 0U || not_digits > 0U || (num_digits + start) != strlen_data))
        {
            return false;
        }
        //float error test
        if (arg_type == (uint8_t)UITYPE::FLOAT && 
            (found_dot > 1U || not_digits > 0U || (num_digits + found_dot + start) != strlen_data))
        {
            return false;
        }
        return true; // no errors
    }

    // char and c-string
    if (arg_type == (uint8_t)UITYPE::CHAR ||
        arg_type == (uint8_t)UITYPE::C_STRING)
    {
        if (arg_type == (uint8_t)UITYPE::CHAR && strlen_data > 1) // error
        {
            return false; // looking for a single char value, not a c-string
        }
        for (size_t j = 0; j < strlen_data; ++j)
        {   // if we encounter anything that isn't one of these four things, something isn't right
            size_t test_bool[4] = {false};
            test_bool[0] = isprint(_data_pointers_[_data_pointers_index_][j]);
            test_bool[1] = ispunct(_data_pointers_[_data_pointers_index_][j]);
            test_bool[2] = iscntrl(_data_pointers_[_data_pointers_index_][j]);
            test_bool[3] = isdigit(_data_pointers_[_data_pointers_index_][j]);
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
    if (arg_type == (uint8_t)UITYPE::NOTYPE)
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
        if (err >= _output_buffer_bytes_left_) // overflow condition
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
        if (_failed_on_subcommand_ > cmd->param_array_len) // error
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
                        uint8_t _type = UserInput::_getArgType(prm, i);
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
                             bool &match,
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

        match = true;                                          // don't run default callback
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
        match = true;                                          // don't run default callback
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
            match = true;                                          // don't run default callback
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
            match = true;                                          // don't run default callback
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
                                match,
                                input_type_match_flag,
                                subcommand_matched,
                                command_id);
    }
}

char *UserInput::_escapeCharactersSoTheyPrint(char input, char *buf)
{
    if (input < (char)32 || input == (char)34)
    {
        buf[0] = (char)92;
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
    buf[0] = input; // pass through input
    buf[1] = _null_; // terminate
    return buf; // not a control char
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

uint8_t UserInput::_getArgType(Parameters &prm, size_t index)
{
    if (prm.argument_flag == UI_ARG_HANDLING::no_args) return static_cast<uint8_t>(UITYPE::NO_ARGS);
    if (prm.argument_flag == UI_ARG_HANDLING::one_type) return static_cast<uint8_t>(prm.arg_type_arr[0]);
    if (prm.argument_flag == UI_ARG_HANDLING::type_arr) return static_cast<uint8_t>(prm.arg_type_arr[index]);

    return static_cast<uint8_t>(UITYPE::_LAST); // return error if no match
}

void UserInput::_getArgs(size_t &tokens_received,
                         bool *input_type_match_flag,
                         Parameters &prm,
                         bool &all_arguments_valid)
{
    _rec_num_arg_strings_ = 0; // number of tokens read from data
    for (size_t i = 0; i < (tokens_received - 1U); ++i)
    {
        input_type_match_flag[i] = UserInput::validateUserInput(UserInput::_getArgType(prm, i),
                                                                _data_pointers_index_ + i); // validate the token
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