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

    UserInput::_ui_out(PSTR("username = \"%s\"\n"), _username_);

    UserInput::_ui_out(PSTR("end_of_line_characters = \""));
    char term_buf[strlen(_term_)][UI_ESCAPED_CHAR_PGM_LEN];
    for (size_t i = 0; i < strlen(_term_); ++i)
    {
        UserInput::_ui_out(PSTR("%s"), (iscntrl(_term_[i])
                                 ? UserInput::_escapeCharactersSoTheyPrint(_term_[i], *term_buf[i])
                                 : &_term_[i]));
    }
    UserInput::_ui_out(PSTR("\"\n"));

    UserInput::_ui_out(PSTR("token_delimiter = \""));
    char delim_buf[strlen(_delim_)][UI_ESCAPED_CHAR_PGM_LEN];
    for (size_t i = 0; i < strlen(_delim_); ++i)
    {
        UserInput::_ui_out(PSTR("%s"), (iscntrl(_delim_[i])
                                 ? UserInput::_escapeCharactersSoTheyPrint(_delim_[i], *delim_buf[i])
                                 : &_delim_[i]));
    }
    UserInput::_ui_out(PSTR("\"\n"));

    UserInput::_ui_out(PSTR("c_string_delimiter = \""));
    char _c_str_delim_buf[strlen(_c_str_delim_)][UI_ESCAPED_CHAR_PGM_LEN];
    for (size_t i = 0; i < strlen(_c_str_delim_); ++i)
    {
        UserInput::_ui_out(PSTR("%s"), (iscntrl(_c_str_delim_[i])
                                 ? UserInput::_escapeCharactersSoTheyPrint(_c_str_delim_[i], *_c_str_delim_buf[i])
                                 : &_c_str_delim_[i]));
    }
    UserInput::_ui_out(PSTR("\"\n"));
}

void UserInput::defaultFunction(void (*function)(UserInput *))
{
    _default_function_ = function;
}

void UserInput::addCommand(CommandConstructor &command)
{    
    if (_commands_head_ == NULL)
    {
        _commands_head_ = _commands_tail_ = &command;
    }
    else
    {
        _commands_tail_->next_command_parameters = &command;
        _commands_tail_ = &command;
    }
    _commands_count_++;
}

void UserInput::listCommands()
{
    CommandConstructor *cmd;
    UserInput::_ui_out(PSTR("Commands available%s%s:\n"),
                       (_username_ != "") ? PSTR(" to ") : PSTR(""), _username_);
    uint8_t i = 1;
    for (cmd = _commands_head_; cmd != NULL; cmd = cmd->next_command_parameters, ++i)
    {
        char buffer[UI_MAX_CMD_LEN];
        memcpy_P(&buffer, cmd->prm->command, sizeof(buffer));
        UserInput::_ui_out(PSTR(" %02u. <%s>\n"), i, buffer);
    }
}

void UserInput::readCommandFromBuffer(uint8_t *data, size_t len)
{
    // error checking
    if (len > (UI_MAX_IN_LEN - 2)) // 65535 - 1(index align) - 1(space for null '\0')
    {
        UserInput::_ui_out(PSTR(">%s$ERROR: input is too long.\n"), _username_);
        return;
    }

    // this is declared here to test if _token_buffer_ == nullptr (error condition)
    _token_buffer_ = new char[len + 1](); // place to chop up the input
    if (_token_buffer_ == nullptr)        // if there was an error allocating the memory
    {
        UserInput::_ui_out(PSTR(">%s$ERROR: cannot allocate ram for _token_buffer_.\n"), _username_);
        return;
    }
    // end error checking

    // reinit _data_pointers_
    for (size_t i = 0; i < (UI_MAX_ARGS + 1); ++i)
    {
        _data_pointers_[i] = NULL;
    }

    uint8_t tokens_received = 0;  // amount of delimiter separated tokens
    size_t data_index = 0;        // data iterator
    _data_pointers_index_ = 0;    // token buffer pointers
    _rec_num_arg_strings_ = 0;    // number of tokens read from data
    bool match = false;           // command string match
    bool command_matched = false; // error sentinel
    CommandConstructor *cmd;      // command parameters pointer
    Parameters prm;               // Parameters struct

    /*
        this tokenizes an input buffer, it should work with any 8 bit input type that represents char
        char tokenized_string[] = "A\0Tokenized\0C-string\0"
        char non_tokenized_string[] = "A Non Tokenized C-string" <-- still has a \0 at the end of the string to terminate it
    */
    while (true)
    {
        if (UserInput::getToken(data, len, &data_index) == true)
        {
            tokens_received++;                        // increment tokens_received
            if (tokens_received == (UI_MAX_ARGS + 1)) // index sentinel
            {
                break;
            }
        }
        else
        {
            break;
        }
    }
    _data_pointers_index_max_ = tokens_received;    // set index max to tokens received
    
    if (tokens_received == 0) // error condition
    {
        delete[] _token_buffer_;
        UserInput::_ui_out(PSTR(">%s$ERROR: No tokens retrieved.\n"), _username_);        
        return;
    }
    // end error condition

    bool input_type_match_flag[UI_MAX_ARGS] = {false};  // argument type-match flag array
    bool all_arguments_valid = true; // error sentinel

    for (cmd = _commands_head_; cmd != NULL; cmd = cmd->next_command_parameters) // iterate through CommandConstructor linked-list
    {
        // cmd->prm[0] is a reference to the root command Parameters struct
        if (memcmp_P(_data_pointers_[0], cmd->prm[0].command, (uint16_t)pgm_read_dword(&(cmd->prm[0].command_length))) == false) // match root command
        {
            memcpy_P(&prm, &(cmd->prm[0]), sizeof(prm)); // move Parameters variables from PROGMEM to sram for work
            _current_search_depth_ = 1;      // start searching for subcommands at depth 1
            _data_pointers_index_ = 1;       // index 1 of _data_pointers_ is the token after the root command
            command_matched = true;          // root command match flag
            _failed_on_subcommand_ = 0;      // subcommand error index
            bool subcommand_matched = false; // subcommand match flag
            uint8_t prm_idx = 0;
            // see if command has any subcommands, validate input types, try to launch function
            UserInput::_launchLogic(cmd,        // CommandConstructor pointer, contains target function pointer
                         prm,                   // ReadCommandFromBuffer Parameters structure reference
                         prm_idx,               // Parameters array index
                         tokens_received,       // how many tokens were retrieved
                         all_arguments_valid,   // type error sentinel
                         match,                 // function launch sentinel
                         input_type_match_flag, // type error flag array
                         subcommand_matched);   // subcommand match flag
            break;                              // break command iterator for loop
        }                                       // end command logic
    }                                           // end root command for loop
    if (!match && _default_function_ != NULL)   // if there was no command match and a default function is configured
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
}

void UserInput::getCommandFromStream(Stream &stream, size_t rx_buffer_size)
{
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
    size_t _term_len_ = strlen(_term_);
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
    if (_data_pointers_index_ < UI_MAX_ARGS && _data_pointers_index_ < _data_pointers_index_max_)
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
        _string_pos_ = 0; //  reset output_buffer's index
        //  this maybe doesnt need to be done
        for (uint16_t i = 0; i < _output_buffer_len_; ++i)
        {
            _output_buffer_[i] = _null_; // reinit output_buffer
        }
    }
    _output_flag_ = false;
}

/*
    protected methods
*/
bool UserInput::getToken(uint8_t *data, size_t len, size_t *data_index)
{
    bool got_token = false;
    char incoming = 0;                   // cast data[data_index] to char and run tests on incoming
    bool token_flag[2] = {false, false}; // token state machine, point to a token once
    uint32_t data_length = (uint32_t)len;
    size_t delim_len = strlen(_delim_);
    #if defined(__DEBUG_GET_TOKEN__)
    UserInput::_ui_out(PSTR("UserInput::getToken(): "));
    #endif
    for (uint16_t i = *data_index; i < data_length; ++i)
    {
        incoming = (char)data[*data_index];
        #if defined(__DEBUG_GET_TOKEN__)
        char inc_buf[UI_ESCAPED_CHAR_PGM_LEN];
        UserInput::_ui_out(PSTR("%s"), (iscntrl(incoming)
                                 ? escapeCharactersSoTheyPrint(incoming, *inc_buf)
                                 : &incoming));
        #endif
        if (iscntrl(incoming)) // remove hanging control characters
        {
            _token_buffer_[*data_index] = _null_;
        }
        else if (incoming == _delim_[0]) // replace delimiter
        {
            if (delim_len == 1) // incoming is equal to _delim_[0] and the delimiter is one character in length
            {
                _token_buffer_[*data_index] = _null_;
                token_flag[0] = false;
            }
            else
            {
                bool delim_char_match = true; // error flag
                size_t idx = *data_index;
                char inc;
                for (size_t j = 1; j < (delim_len + 1); ++j)
                {
                    if ((j + i) < data_length)
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
                    for (size_t j = 1; j < (delim_len + 1); ++j)
                    {
                        (*data_index)++;
                        _token_buffer_[*data_index] = _null_;
                    }
                    token_flag[0] = false;
                }
            }
        }
        else if (incoming == *_c_str_delim_) // switch logic for c-string input
        {
            _token_buffer_[*data_index] = _null_;             // replace the c-string delimiter
            if (((uint16_t)(*data_index) + 1U) < data_length) //  don't need to do this if we're at the end of user input
            {
                bool point_to_beginning_of_c_string = true; // c-string pointer assignment flag
                (*data_index)++;
                for (uint16_t j = *data_index; j < data_length; ++j) // this for loop starts at whatever data_index is equal to and has the potential to iterate up to len
                {
                    incoming = (char)data[*data_index]; // fetch the next incoming char
                    if (incoming == *_c_str_delim_)     // if the next incoming char is a '\"'
                    {
                        _token_buffer_[*data_index] = _null_; // replace the c-string delimiter
                        (*data_index)++;                      // increment the tokenized string index
                        break;
                    }
                    _token_buffer_[*data_index] = incoming;     // else assign incoming to _token_buffer_[data_index]
                    if (point_to_beginning_of_c_string == true) // a pointer will be assigned if point_to_beginning_of_c_string == true
                    {
                        _data_pointers_[_data_pointers_index_] = &_token_buffer_[*data_index]; // point to this position in _token_buffer_
                        _data_pointers_index_++;                                               //  increment pointer index
                        point_to_beginning_of_c_string = false;                                //  only set one pointer per c-string
                        got_token = true;
                        #if defined(__DEBUG_GET_TOKEN__)
                        UserInput::_ui_out(PSTR("\n>%s$DEBUG: got the c-string token.\n"), _username_);
                        #endif
                    }
                    (*data_index)++; // increment the tokenized string index
                }
            }
        }
        else // this is a non c-string token
        {
            if (incoming == '\\' && (*data_index < data_length))
            {
                _token_buffer_[*data_index] = _null_;
                (*data_index)++; // increment buffer index
                incoming = UserInput::_combineControlCharacters((char)data[*data_index]);
            }
            _token_buffer_[*data_index] = incoming; // assign incoming to _token_buffer_ at data_index
            token_flag[0] = true;                   // set token available sentinel to true
        }

        if (token_flag[0] != token_flag[1]) // if the token state has changed
        {
            if (token_flag[0] == true) // if there's a new token
            {
                _data_pointers_[_data_pointers_index_] = &_token_buffer_[*data_index]; // assign a pointer the beginning of it
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
        if (token_flag[0] == true && (uint16_t)*data_index == (data_length - 1))
        {
            #if defined(__DEBUG_GET_TOKEN__)
            UserInput::_ui_out(PSTR("\n>%s$DEBUG: UserInput::getToken() got_token == true end of data.\n"),
                    _username_);
            #endif
            got_token = true;
        }

        if (*data_index < data_length) // if we are at the end of input data
        {
            (*data_index)++; // increment buffer index
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
    uint16_t strlen_data = strlen(_data_pointers_[_data_pointers_index_]);
    bool found_negative_sign = ((char)_data_pointers_[_data_pointers_index_][0] == _neg_) ? true : false;
    if (arg_type < (size_t)UITYPE::CHAR)
    {
        // for unsigned integers
        if (arg_type < (size_t)UITYPE::INT16_T)
        {
            if (found_negative_sign == true)
            {
                return false;
            }
            for (uint16_t j = 0; j < strlen_data; ++j)
            {
                if (isdigit(_data_pointers_[_data_pointers_index_][j]) == false)
                {
                    return false;
                }
            }
        }
        // for integer numbers
        if (arg_type == (size_t)UITYPE::INT16_T)
        {
            if (found_negative_sign == true) //  negative
            {
                for (uint16_t j = 1; j < (strlen_data - 1); ++j)
                {
                    if (isdigit(_data_pointers_[_data_pointers_index_][j]) == false)
                    {
                        return false;
                    }
                }
            }
            else //  positive
            {
                for (uint16_t j = 0; j < strlen_data; ++j)
                {
                    if (isdigit(_data_pointers_[_data_pointers_index_][j]) == false)
                    {
                        return false;
                    }
                }
            }
        }
        // for floating point numbers
        if (arg_type == (size_t)UITYPE::FLOAT)
        {
            uint8_t found_dot = 0;
            uint8_t num_digits = 0;
            if (found_negative_sign == true) //  negative
            {
                uint8_t not_digits = 0;
                /*
                    we already know there is a '-' at data[i + 1][0] because found_negative_sign is set
                    so start the for loop at an index of one
                */
                for (uint16_t j = 1; j < strlen_data; ++j)
                {
                    if (_data_pointers_[_data_pointers_index_][j] == _dot_)
                    {
                        found_dot++;
                    }
                    if (isdigit(_data_pointers_[_data_pointers_index_][j]) == true)
                    {
                        num_digits++;
                    }
                    else
                    {
                        not_digits++;
                    }
                }
                if (found_dot == 0) // if there is no fraction
                {
                    found_dot++;
                }
                /*
                    if we find one '.' and one '-' or one '-' and no '.' increment num_digits to include the sign, else type match will fail
                    this is to allow negative numbers with no decimal or fraction like "-5" and also input like "-5.0"
                */
                if ((not_digits == 2 && found_dot == 1) || (not_digits == 1 && found_dot == 1))
                {
                    num_digits++; // count the negative sign
                }
            }
            else //  positive
            {
                for (uint16_t j = 0; j < strlen_data; ++j)
                {
                    if (_data_pointers_[_data_pointers_index_][j] == _dot_)
                    {
                        found_dot++;
                    }
                    if (isdigit(_data_pointers_[_data_pointers_index_][j]) == true)
                    {
                        num_digits++;
                    }
                }
            }
            if (found_dot > 1 || (num_digits + found_dot) != strlen_data)
            {
                return false;
            }
        }
    }
    /*
        For char and c-string input.
        Types allowed are printable characters, punctuation, control characters \r\n etc, and digits 0-9
    */
    else if (arg_type == (size_t)UITYPE::CHAR)
    {
        if (strlen_data > 1)
        {
            return false;
        }
        if (isprint(_data_pointers_[_data_pointers_index_][0]) ||
            ispunct(_data_pointers_[_data_pointers_index_][0]) ||
            iscntrl(_data_pointers_[_data_pointers_index_][0]) ||
            isdigit(_data_pointers_[_data_pointers_index_][0]))
        {
        }
        else
        {
            return false;
        }
    }
    else if (arg_type == (size_t)UITYPE::C_STRING)
    {
        for (uint16_t j = 0; j < strlen_data; ++j)
        {
            if (isprint(_data_pointers_[_data_pointers_index_][j]) ||
                ispunct(_data_pointers_[_data_pointers_index_][j]) ||
                iscntrl(_data_pointers_[_data_pointers_index_][j]) ||
                isdigit(_data_pointers_[_data_pointers_index_][j]))
            {
            }
            else
            {
                return false;
            }
        }
    }
    else if (arg_type == (size_t)UITYPE::NOTYPE)
    {
        // no type validation performed
        return true;
    }
    else //  unknown types always return false
    {
        return false;
    }
    return true;
}

uint8_t UserInput::getArgType(Parameters &prm, size_t index)
{
    if (prm.argument_flag == no_args)
        return static_cast<uint8_t>(UITYPE::NO_ARGS);
    if (prm.argument_flag == one_type)
        return static_cast<uint8_t>(prm._arg_type[0]);
    if (prm.argument_flag == type_arr)
        return static_cast<uint8_t>(prm._arg_type[index]);
    return static_cast<uint8_t>(UITYPE::_LAST); // return error if no match
}

void UserInput::getArgs(size_t &tokens_received,
                        bool *input_type_match_flag,
                        Parameters &prm,
                        bool &all_arguments_valid)
{
    _rec_num_arg_strings_ = 0; // number of tokens read from data
    for (size_t i = 0; i < (tokens_received - 1); ++i)
    {
        input_type_match_flag[i] = UserInput::validateUserInput(UserInput::getArgType(prm, i),
                                                     _data_pointers_index_ + i); // validate the token
        _rec_num_arg_strings_++;
        if (input_type_match_flag[i] == false) // if the token was not valid input
        {
            all_arguments_valid = false; // set the error sentinel to true
        }
    }
}

/*
    private methods
*/
void UserInput::_ui_out(const char *fmt, ...)
{
    if (UserInput::outputIsEnabled())
    {
        va_list args;
        va_start(args, fmt);
        _string_pos_ += vsnprintf_P(_output_buffer_ + _string_pos_, _output_buffer_len_, fmt, args);
        va_end(args);
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
        // potential silent crash if _failed_on_subcommand_ > cmd->_param_array_len
        // user introduced error condition, if they enter a parameter array length that is
        // greater than the actual array length
        if (_failed_on_subcommand_ > cmd->_param_array_len) // error
        {
            memcpy_P(&prm, &(cmd->prm[0]), sizeof(prm));
            UserInput::_ui_out(PSTR("OOB Parameters array element access attempted for command %s.\n"), prm.command);
            return;
        }
        memcpy_P(&prm, &(cmd->prm[_failed_on_subcommand_]), sizeof(prm));
        UserInput::_ui_out(PSTR(">%s$Invalid input: "), _username_);
        if (command_matched == true)
        {
            // constrain err_n_args to UI_MAX_ARGS + 1
            size_t err_n_args = ((_data_pointers_index_max_ - _failed_on_subcommand_ - 1) > (UI_MAX_ARGS + 1))
                                    ? (UI_MAX_ARGS + 1)
                                    : (_data_pointers_index_max_ - _failed_on_subcommand_ - 1);
            if (err_n_args > 0)
            {
                for (size_t i = 0; i < (_failed_on_subcommand_ + 1); ++i)
                {
                    UserInput::_ui_out(PSTR("%s "), _data_pointers_[i]); // add subcommands to echo
                }
                bool print_subcmd_err = true;
                for (uint16_t i = 0; i < err_n_args; ++i)
                {
                    if (input_type_match_flag[i] == false)
                    {
                        uint8_t _type = UserInput::getArgType(prm, i);
                        char _type_char_array[UI_INPUT_TYPE_STRINGS_PGM_LEN];
                        memcpy_P(&_type_char_array, &UserInput_type_strings_pgm[_type], sizeof(_type_char_array));
                        if ((UITYPE)_type != UITYPE::NO_ARGS && _data_pointers_[1 + _failed_on_subcommand_ + i] == NULL)
                        {
                            UserInput::_ui_out(PSTR("'INPUT NOT RECEIVED'*(%s REQUIRED) "), _type_char_array);
                        }
                        else
                        {
                            if (prm.sub_commands > 0 && print_subcmd_err == true)
                            {
                                print_subcmd_err = false;
                                UserInput::_ui_out(PSTR("'%s'*(ENTER VALID SUBCOMMAND) "), _data_pointers_[1 + _failed_on_subcommand_ + i]);
                            }
                            else if ((prm.sub_commands == 0 || err_n_args > 1) && (UITYPE)_type == UITYPE::NO_ARGS)
                            {
                                UserInput::_ui_out(PSTR("'%s'*(LEAVE BLANK) "), _data_pointers_[1 + _failed_on_subcommand_ + i]);
                            }
                            else
                            {
                                UserInput::_ui_out(PSTR("'%s'*(%s) "), _data_pointers_[1 + _failed_on_subcommand_ + i], _type_char_array);
                            }
                        }
                    }
                    else
                    {
                        UserInput::_ui_out(PSTR("'%s'(OK) "), _data_pointers_[1 + _failed_on_subcommand_ + i]);
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
                                uint8_t &prm_idx,
                                size_t tokens_received)
{
    if (UserInput::outputIsEnabled())
    {
        UserInput::_ui_out(PSTR(">%s $"), _username_, _data_pointers_[0]);
        for (uint16_t i = 0; i < _data_pointers_index_max_; ++i)
        {
            if (iscntrl(*_data_pointers_[i]))
            {
                char buf[UI_ESCAPED_CHAR_PGM_LEN];
                UserInput::_ui_out(PSTR("%s "), UserInput::_escapeCharactersSoTheyPrint(*_data_pointers_[i], *buf));
            }
            else
            {
                UserInput::_ui_out(PSTR("%s "), _data_pointers_[i]);
            }
        }
        UserInput::_ui_out(PSTR("\n"));
    }
    _data_pointers_index_ = _current_search_depth_ - 1;
    #if defined(__DEBUG_LAUNCH_FUNCTION__)
    UserInput::_ui_out(PSTR("prm_idx=%d\n"), prm_idx);
    #endif

    if (prm.function != NULL)
    {
        #if defined(__DEBUG_LAUNCH_FUNCTION__)
        UserInput::_ui_out(PSTR("func ptr != NULL\n"));
        #endif
        prm.function(this);
    }
    else
    {
        #if defined(__DEBUG_LAUNCH_FUNCTION__)
        UserInput::_ui_out(PSTR("func ptr == NULL, load cmd->prm[0]\n"));
        #endif
        memcpy_P(&prm, &(cmd->prm[0]), sizeof(prm));
        if (prm.function == NULL) // silent crash guard
        {
            #if defined(__DEBUG_LAUNCH_FUNCTION__)
            UserInput::_ui_out(PSTR("ERROR! Parameters function pointer NULL for (%s), edit your source!\n"), prm.command);
            #endif
            return;
        }
        prm.function(this);
    }
}

void UserInput::_launchLogic(CommandConstructor *cmd,
                             Parameters &prm,
                             uint8_t &prm_idx,
                             size_t tokens_received,
                             bool &all_arguments_valid,
                             bool &match,
                             bool *input_type_match_flag,
                             bool &subcommand_matched)
{
    // error
    if (tokens_received > 1 &&
        prm.sub_commands == 0 &&
        prm.max_num_args == 0)
    {
        #if defined(__DEBUG_LAUNCH_LOGIC__)
        UserInput::_ui_out(PSTR(">%s$DEBUG: too many tokens (%d) for command (%s)\n"),
                _username_, tokens_received, prm.command);
        #endif
        return;
    }

    // command with no arguments
    if (subcommand_matched == false &&
        tokens_received == 1 &&
        prm.max_num_args == 0)
    {
        #if defined(__DEBUG_LAUNCH_LOGIC__)
        UserInput::_ui_out(PSTR(">%s$DEBUG: cmd w/no args, subcommand match false "
                     "tokens=0 max_args=0 launchFunction(%s)\n"),
                _username_, prm.command);
        #endif

        match = true;                                        // don't run default callback
        UserInput::_launchFunction(cmd, prm, prm_idx, tokens_received); // launch the matched command
        return;
    }

    // subcommand with no arguments
    if (tokens_received == 1 &&
        _current_search_depth_ > 1 &&
        subcommand_matched == true &&
        prm.max_num_args == 0)
    {
        #if defined(__DEBUG_LAUNCH_LOGIC__)
        UserInput::_ui_out(PSTR(">%s$DEBUG: subcmd w/no args, subcommand match true "
                     "tokens==0 max_args==0 depth>1 launchFunction(%s)\n"),
                _username_, prm.command);
        #endif
        match = true;                                        // don't run default callback
        UserInput::_launchFunction(cmd, prm, prm_idx, tokens_received); // launch the matched command
        return;
    }

    // command with arguments, potentially has subcommands but none were entered
    if ( //_current_search_depth > 1 &&
        subcommand_matched == false &&
        tokens_received > 1 &&
        prm.max_num_args > 0)
    {
        UserInput::getArgs(tokens_received, input_type_match_flag, prm, all_arguments_valid);
        if (_rec_num_arg_strings_ >= prm.num_args &&
            _rec_num_arg_strings_ <= prm.max_num_args &&
            all_arguments_valid == true)
        {
            #if defined(__DEBUG_LAUNCH_LOGIC__)
            UserInput::_ui_out(PSTR(">%s$DEBUG: cmd w/ args, no subcmd match, subcommand match false "
                         "tokens>0 max_args>0 depth>1 launchFunction(%s)\n"),
                    _username_, prm.command);
            #endif
            match = true;                                        // don't run default callback
            UserInput::_launchFunction(cmd, prm, prm_idx, tokens_received); // launch the matched command
        }
        // if !match, error
        return;
    }

    // command with arguments (max depth)
    if (_current_search_depth_ == (cmd->_tree_depth) &&
        tokens_received > 1 &&
        prm.max_num_args > 0 &&
        prm.sub_commands == 0)
    {
        UserInput::getArgs(tokens_received, input_type_match_flag, prm, all_arguments_valid);
        //  if we received at least min and less than max arguments and they are valid
        if (_rec_num_arg_strings_ >= prm.num_args &&
            _rec_num_arg_strings_ <= prm.max_num_args &&
            all_arguments_valid == true)
        {
            #if defined(__DEBUG_LAUNCH_LOGIC__)
            UserInput::_ui_out(PSTR(">%s$DEBUG: cmd w/args (max depth) launchFunction(%s)\n"), _username_, prm.command);
            #endif
            match = true;                                        // don't run default callback
            UserInput::_launchFunction(cmd, prm, prm_idx, tokens_received); // launch the matched command
        }
        // if !match, error
        return;
    }

    // subcommand search
    subcommand_matched = false;
    #if defined(__DEBUG_SUBCOMMAND_SEARCH__)
    UserInput::_ui_out(PSTR("search depth (%d)\n"), _current_search_depth);
    #endif
    if (_current_search_depth_ <= (cmd->_tree_depth)) // dig starting at depth 1
    {
        // this index starts at one because the parameter array's first element will be the root command
        for (size_t j = 1; j < (cmd->_param_array_len + 1); ++j) // through the parameter array
        {
            prm_idx = j;
            #if defined(__DEBUG_SUBCOMMAND_SEARCH__)
            UserInput::_ui_out(PSTR("match depth cmd=(%s)\ntoken=(%s)\n"),
                               prm.command, _data_pointers_[_data_pointers_index_]);
            #endif
            if (memcmp_P(_data_pointers_[0], cmd->prm[0].command, (uint16_t)pgm_read_dword(&(cmd->prm[0].command_length))) == false) // match root command
            {
                memcpy_P(&prm, &(cmd->prm[j]), sizeof(prm));
                if (prm.depth == _current_search_depth_)
                {
                    #if defined(__DEBUG_SUBCOMMAND_SEARCH__)
                    UserInput::_ui_out(PSTR("(%s) subcommand matched, (%d) subcommands, max_num_args (%d)\n"),
                                       prm.command, prm.sub_commands, prm.max_num_args);
                    #endif
                    // subcommand matched
                    if (tokens_received > 0)
                    {
                        tokens_received--; // subtract subcommand from tokens received
                        #if defined(__DEBUG_SUBCOMMAND_SEARCH__)
                        UserInput::_ui_out(PSTR("decrement tokens (%d)\n"), tokens_received);
                        #endif
                        _data_pointers_index_++;
                    }
                    subcommand_matched = true;  // subcommand matched
                    _failed_on_subcommand_ = j; // set error index
                    break;                      // break out of the loop
                }
            }
        }
        if (_current_search_depth_ < (cmd->_tree_depth))
        {
            _current_search_depth_++;
        }
    }                               // end subcommand search
    if (subcommand_matched == true) // recursion
    {
        #if defined(__DEBUG_SUBCOMMAND_SEARCH__)
        UserInput::_ui_out(PSTR("recurse\n"));
        #endif
        UserInput::_launchLogic(cmd,
                     prm,
                     prm_idx,
                     tokens_received,
                     all_arguments_valid,
                     match,
                     input_type_match_flag,
                     subcommand_matched);
    }
}

char *UserInput::_escapeCharactersSoTheyPrint(char input, char &buf)
{
    switch (input)
    {
    case '\0':
        memcpy_P(&buf, UserInput_escaped_char_pgm[0], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf;
    case '\a':
        memcpy_P(&buf, UserInput_escaped_char_pgm[1], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf;
    case '\b':
        memcpy_P(&buf, UserInput_escaped_char_pgm[2], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf;
    case '\t':
        memcpy_P(&buf, UserInput_escaped_char_pgm[3], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf;
    case '\n':
        memcpy_P(&buf, UserInput_escaped_char_pgm[4], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf;
    case '\v':
        memcpy_P(&buf, UserInput_escaped_char_pgm[5], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf;
    case '\f':
        memcpy_P(&buf, UserInput_escaped_char_pgm[6], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf;
    case '\r':
        memcpy_P(&buf, UserInput_escaped_char_pgm[7], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf;
    case '\e':
        memcpy_P(&buf, UserInput_escaped_char_pgm[8], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf;
    case '\"':
        memcpy_P(&buf, UserInput_escaped_char_pgm[9], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf;
    default:
        memcpy_P(&buf, UserInput_escaped_char_pgm[11], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf; // return er error
    }
    memcpy_P(&buf, UserInput_escaped_char_pgm[11], UI_ESCAPED_CHAR_PGM_LEN);
    return &buf; // guard return er error
}

char UserInput::_combineControlCharacters(char input)
{
    switch ((char)input)
    {
    case '0':
        return (char)'\0';
    case 'a':
        return (char)'\a';
    case 'b':
        return (char)'\b';
    case 't':
        return (char)'\t';
    case 'n':
        return (char)'\n';
    case 'v':
        return (char)'\v';
    case 'f':
        return (char)'\f';
    case 'r':
        return (char)'\r';
    case 'e':
        return (char)'\r';
    case '"':
        return (char)'\"';
    default:
        return (char)'*'; // * error
    }
}
