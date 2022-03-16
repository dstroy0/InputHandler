/**
   @file InputHandler.cpp
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief InputHandler library cpp file
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

#include "InputHandler.h"

/*
    public methods
*/
char *UserInput::NextArgument()
{
    // return NULL if there are no more arguments
    if (data_pointers_index < UI_MAX_ARGS && data_pointers_index < rec_num_arg_strings)
    {
        data_pointers_index++;
        return data_pointers[data_pointers_index];
    }
    else
    {
        return NULL;
    }
    return NULL; // guard return
}

void UserInput::AddCommand(CommandConstructor &command)
{
    CommandConstructor **cmd_head = &commands_head_;
    CommandConstructor **cmd_tail = &commands_tail_;
    size_t *cmd_count = &commands_count_;
    command.next_command_parameters = NULL;
    if (*cmd_head == NULL)
    {
        *cmd_head = *cmd_tail = &command;
    }
    else
    {
        (*cmd_tail)->next_command_parameters = &command;
        *cmd_tail = &command;
    }
    (*cmd_count)++;
}

void UserInput::ReadCommandFromBuffer(uint8_t *data, size_t len)
{
    // error checking
    if (len > (UI_MAX_IN_LEN - 2)) // 65535 - 1(index align) - 1(space for null '\0')
    {
        _ui_out(PSTR(">%s $ERROR: input is too long.\n"), _username_);
        return;
    }

    // this is declared here to test if token_buffer == nullptr (error condition)
    token_buffer = new char[len + 1](); // place to chop up the input
    if (token_buffer == nullptr)        // if there was an error allocating the memory
    {
        _ui_out(PSTR(">%s $ERROR: cannot allocate ram for token_buffer.\n"), _username_);
        return;
    }
    // end error checking

    // reinit data_pointers
    for (size_t i = 0; i < (UI_MAX_ARGS + 1); ++i)
    {
        data_pointers[i] = NULL;
    }

    uint8_t tokens_received = 0;  // amount of delimiter separated tokens
    size_t data_index = 0;        // data iterator
    data_pointers_index = 0;      // token buffer pointers    
    rec_num_arg_strings = 0;      // number of tokens read from data
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
        if (getToken(token_buffer, data, len, &data_index) == true)
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
    data_pointers_index_max = tokens_received;    
    // error condition
    if (tokens_received == 0)
    {
        _ui_out(PSTR(">%s $ERROR: No tokens retrieved.\n"), _username_);
        delete[] token_buffer;
        return;
    }
    // end error condition

    bool input_type_match_flag[UI_MAX_ARGS] = {false};
    bool all_arguments_valid = true; // error sentinel

    for (cmd = commands_head_; cmd != NULL; cmd = cmd->next_command_parameters) // iterate through user commands
    {
        // &(cmd->prm[0]) points to the first parameters struct for this cmd
        memcpy_P(&prm, &(cmd->prm[0]), sizeof(prm)); // move working variables to ram
        // if the first test is false, the strcmp test is not evaluated
        if (strcmp(data_pointers[0], prm.command) == 0) // match root command
        {
            _current_search_depth = 1; // start searching for subcommands at depth 1
            data_pointers_index = 1;   // index 1 of data_pointers is the token after the root command            
            command_matched = true;          // root command match flag
            failed_on_subcommand = 0;        // subcommand error index
            bool subcommand_matched = false; // subcommand match flag
            uint8_t prm_idx = 0;
            // see if command has any subcommands, validate input types, try to launch function
            launchLogic(cmd,                   // CommandConstructor pointer, contains target function pointer
                        prm,                   // ReadCommandFromBuffer Parameters structure reference
                        prm_idx,               // Parameters array index
                        tokens_received,       // how many tokens were retrieved
                        all_arguments_valid,   // type error sentinel
                        match,                 // function launch sentinel
                        input_type_match_flag, // type error flag array
                        subcommand_matched);   // subcommand match flag            
            break;                             // break command iterator for loop
        }                                      // end command logic
    }                                          // end root command for loop
    if (!match && default_function_ != NULL) // if there was no command match and a default function is configured
    {
        _ReadCommandFromBufferErrorOutput(cmd,
                                          prm,
                                          command_matched,                                          
                                          input_type_match_flag,
                                          all_arguments_valid,
                                          data);
        (*default_function_)(this); // run the default function
    }
    delete[] token_buffer;
}

void UserInput::GetCommandFromStream(Stream &stream, size_t rx_buffer_size)
{
    if (stream_buffer_allocated == false)
    {
        stream_data = new uint8_t[rx_buffer_size]; // an array to store the received data
        if (stream_data == nullptr)                // if there was an error allocating the memory
        {
            _ui_out(PSTR(">%s $ERROR: cannot allocate ram for stream_data\n"), _username_);
            return;
        }
        stream_buffer_allocated = true;
        _term_index_ = 0;
    }
    char *rc = (char *)stream_data; // point rc to allocated memory
    size_t _term_len_ = strlen(_term_);
    while (stream.available() > 0 && new_stream_data == false)
    {
        rc[stream_data_index] = stream.read();
        if (rc[stream_data_index] == _term_[_term_index_])
        {
            stream_data[stream_data_index] = _null_;
            if (_term_index_ < _term_len_)
            {
                _term_index_++;
            }
            if (_term_index_ == _term_len_)
            {
                new_stream_data = true;
            }
        }
        if (stream_data_index < rx_buffer_size)
        {
            stream_data_index++;
        }
    }
    if (new_stream_data == true)
    {
        UserInput::ReadCommandFromBuffer(stream_data, stream_data_index);
        stream_data_index = 0;
        new_stream_data = false;
        delete[] stream_data;
        stream_buffer_allocated = false;
    }
}

void UserInput::ListCommands()
{
    CommandConstructor *cmd;
    _ui_out(PSTR("Commands available to %s:\n"), _username_);
    uint8_t i = 1;
    for (cmd = commands_head_; cmd != NULL; cmd = cmd->next_command_parameters)
    {
        char buffer[UI_MAX_CMD_LEN];
        memcpy_P(&buffer, cmd->prm->command, sizeof(buffer));
        _ui_out(PSTR(" %02u. <%s>\n"), i, buffer);
        i++;
    }
}

void UserInput::ListSettings(UserInput *inputprocess)
{
    
    _ui_out(PSTR("username = \"%s\"\n"), _username_);

    _ui_out(PSTR("end_of_line_characters = \""));
    char term_buf[strlen(_term_)][UI_ESCAPED_CHAR_PGM_LEN];
    for (size_t i = 0; i < strlen(_term_); ++i)
    {
        _ui_out(PSTR("%s"), (iscntrl(_term_[i])
                                 ? escapeCharactersSoTheyPrint(_term_[i], *term_buf[i])
                                 : &_term_[i]));
    }
    _ui_out(PSTR("\"\n"));
    
    _ui_out(PSTR("token_delimiter = \"")); 
    char delim_buf[strlen(_delim_)][UI_ESCAPED_CHAR_PGM_LEN];
    for (size_t i = 0; i < strlen(_delim_); ++i)
    {
        _ui_out(PSTR("%s"), (iscntrl(_delim_[i])
                                 ? escapeCharactersSoTheyPrint(_delim_[i], *delim_buf[i])
                                 : &_delim_[i]));
    }
    _ui_out(PSTR("\"\n"));

    _ui_out(PSTR("c_string_delimiter = \"")); 
    char _c_str_delim_buf[strlen(_c_str_delim_)][UI_ESCAPED_CHAR_PGM_LEN];
    for (size_t i = 0; i < strlen(_c_str_delim_); ++i)
    {
        _ui_out(PSTR("%s"), (iscntrl(_c_str_delim_[i])
                                 ? escapeCharactersSoTheyPrint(_c_str_delim_[i], *_c_str_delim_buf[i])
                                 : &_c_str_delim_[i]));
    }
    _ui_out(PSTR("\"\n"));
}

void UserInput::DefaultFunction(void (*function)(UserInput *))
{
    default_function_ = function;
}

bool UserInput::OutputIsAvailable()
{
    return _output_flag;
}

bool UserInput::OutputIsEnabled()
{
    return _output_enabled;
}

void UserInput::OutputToStream(Stream &stream)
{
    if (UserInput::OutputIsAvailable()) // if there's something to print
    {
        stream.println(_output_buffer); // print output_buffer, which is formatted into a string by UserInput's methods
        UserInput::ClearOutputBuffer();
    }
}

void UserInput::ClearOutputBuffer()
{
    if (UserInput::OutputIsEnabled())
    {
        _string_pos = 0; //  reset output_buffer's index
        //  this maybe doesnt need to be done
        for (uint16_t i = 0; i < _output_buffer_len; ++i)
        {
            _output_buffer[i] = _null_; // reinit output_buffer
        }
    }
    _output_flag = false;
}

/*
    protected methods
*/
bool UserInput::getToken(char *token_buffer, uint8_t *data, size_t len, size_t *data_index)
{
    bool got_token = false;
    char incoming = 0;                   // cast data[data_index] to char and run tests on incoming
    bool token_flag[2] = {false, false}; // token state machine, point to a token once
    uint32_t data_length = (uint32_t)len;
    size_t delim_len = strlen(_delim_);
    #if defined(__DEBUG_GET_TOKEN__)
    _ui_out(PSTR("getToken(): "));
    #endif
    for (uint16_t i = *data_index; i < data_length; ++i)
    {        
        incoming = (char)data[*data_index];
        #if defined(__DEBUG_GET_TOKEN__)
        char inc_buf[UI_ESCAPED_CHAR_PGM_LEN];
        _ui_out(PSTR("%s"), (iscntrl(incoming)
                                 ? escapeCharactersSoTheyPrint(incoming, *inc_buf)
                                 : &incoming));
        #endif        
        if (iscntrl(incoming))  // remove hanging control characters
        {
            token_buffer[*data_index] = _null_;
        }
        else if (incoming == _delim_[0])    // replace delimiter
        {
            if (delim_len == 1) // incoming is equal to _delim_[0] and the delimiter is one character in length
            {
                token_buffer[*data_index] = _null_;                
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
                        token_buffer[*data_index] = _null_;
                    }
                    token_flag[0] = false;
                }
            }
        }
        else if (incoming == *_c_str_delim_) // switch logic for c-string input
        {
            token_buffer[*data_index] = _null_;               // replace the c-string delimiter
            if (((uint16_t)(*data_index) + 1U) < data_length) //  don't need to do this if we're at the end of user input
            {
                bool point_to_beginning_of_c_string = true; // c-string pointer assignment flag
                (*data_index)++;
                for (uint16_t j = *data_index; j < data_length; ++j) // this for loop starts at whatever data_index is equal to and has the potential to iterate up to len
                {
                    incoming = (char)data[*data_index]; // fetch the next incoming char
                    if (incoming == *_c_str_delim_)     // if the next incoming char is a '\"'
                    {
                        token_buffer[*data_index] = _null_; // replace the c-string delimiter
                        (*data_index)++;                    // increment the tokenized string index
                        break;
                    }
                    token_buffer[*data_index] = incoming;       // else assign incoming to token_buffer[data_index]
                    if (point_to_beginning_of_c_string == true) // a pointer will be assigned if point_to_beginning_of_c_string == true
                    {
                        data_pointers[data_pointers_index] = &token_buffer[*data_index]; // point to this position in token_buffer
                        data_pointers_index++;                                           //  increment pointer index
                        point_to_beginning_of_c_string = false;                          //  only set one pointer per c-string
                        got_token = true;
                        #if defined(__DEBUG_GET_TOKEN__)
                        _ui_out(PSTR("\n>%s $DEBUG: got the c-string token.\n"), _username_);
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
                token_buffer[*data_index] = _null_;
                (*data_index)++; // increment buffer index
                incoming = combineControlCharacters((char)data[*data_index]);
            }
            token_buffer[*data_index] = incoming; // assign incoming to token_buffer at data_index
            token_flag[0] = true;                 // set token available sentinel to true
        }

        if (token_flag[0] != token_flag[1]) // if the token state has changed
        {
            if (token_flag[0] == true) // if there's a new token
            {
                data_pointers[data_pointers_index] = &token_buffer[*data_index]; // assign a pointer the beginning of it
                data_pointers_index++;                                           // and increment the pointer index
            }
            else
            {
                #if defined(__DEBUG_GET_TOKEN__)
                _ui_out(PSTR("\n>%s $DEBUG: getToken got_token == true token state machine.\n"),
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
            _ui_out(PSTR("\n>%s $DEBUG: getToken() got_token == true end of data.\n"),
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
            _ui_out(PSTR("\n>%s $DEBUG: getToken() break for loop.\n"), _username_);
            #endif
            break;
        }
    }
    return got_token;
}

bool UserInput::validateUserInput(uint8_t arg_type, size_t data_pointers_index)
{
    uint16_t strlen_data = strlen(data_pointers[data_pointers_index]);
    bool found_negative_sign = ((char)data_pointers[data_pointers_index][0] == _neg_) ? true : false;
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
                if (isdigit(data_pointers[data_pointers_index][j]) == false)
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
                    if (isdigit(data_pointers[data_pointers_index][j]) == false)
                    {
                        return false;
                    }
                }
            }
            else //  positive
            {
                for (uint16_t j = 0; j < strlen_data; ++j)
                {
                    if (isdigit(data_pointers[data_pointers_index][j]) == false)
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
                    if (data_pointers[data_pointers_index][j] == _dot_)
                    {
                        found_dot++;
                    }
                    if (isdigit(data_pointers[data_pointers_index][j]) == true)
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
                    if (data_pointers[data_pointers_index][j] == _dot_)
                    {
                        found_dot++;
                    }
                    if (isdigit(data_pointers[data_pointers_index][j]) == true)
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
        if (isprint(data_pointers[data_pointers_index][0]) ||
            ispunct(data_pointers[data_pointers_index][0]) ||
            iscntrl(data_pointers[data_pointers_index][0]) ||
            isdigit(data_pointers[data_pointers_index][0]))
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
            if (isprint(data_pointers[data_pointers_index][j]) ||
                ispunct(data_pointers[data_pointers_index][j]) ||
                iscntrl(data_pointers[data_pointers_index][j]) ||
                isdigit(data_pointers[data_pointers_index][j]))
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

void UserInput::launchFunction(CommandConstructor *cmd,
                               Parameters &prm, 
                               uint8_t &prm_idx, 
                               size_t tokens_received)
{    
    if (UserInput::OutputIsEnabled())
    {
        _ui_out(PSTR(">%s $"), _username_, data_pointers[0]);
        for (uint16_t i = 0; i < data_pointers_index_max; ++i)
        {
            if (iscntrl(*data_pointers[i]))
            { 
                char buf[UI_ESCAPED_CHAR_PGM_LEN];               
                _ui_out(PSTR("%s "), escapeCharactersSoTheyPrint(*data_pointers[i], *buf));
            }
            else
            {
                _ui_out(PSTR("%s "), data_pointers[i]);
            }
        }
        _ui_out(PSTR("\n"));
    }
    data_pointers_index = 0;
    #if defined(__DEBUG_LAUNCH_FUNCTION__)
    _ui_out(PSTR("prm_idx=%d\n"), prm_idx);
    #endif

    if (prm.function != NULL)
    {
        #if defined(__DEBUG_LAUNCH_FUNCTION__)
        _ui_out(PSTR("func ptr != NULL\n"));
        #endif
        prm.function(this);
    }
    else
    {
        #if defined(__DEBUG_LAUNCH_FUNCTION__)
        _ui_out(PSTR("func ptr == NULL, load cmd->prm[0]\n"));
        #endif
        memcpy_P(&prm, &(cmd->prm[0]), sizeof(prm));
        if (prm.function == NULL) // silent crash guard
        {
            #if defined(__DEBUG_LAUNCH_FUNCTION__)
            _ui_out(PSTR("ERROR! Parameters function pointer NULL for (%s), edit your source!\n"), prm.command);
            #endif
            return;
        }
        prm.function(this);
    }
}

void UserInput::launchLogic(CommandConstructor *cmd,
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
        _ui_out(PSTR(">%s $DEBUG: too many tokens (%d) for command (%s)\n"),
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
        _ui_out(PSTR(">%s $DEBUG: cmd w/no args, subcommand match false "
                     "tokens=0 max_args=0 launchFunction(%s)\n"),
                _username_, prm.command);
        #endif

        match = true;                                       // don't run default callback
        launchFunction(cmd, prm, prm_idx, tokens_received); // launch the matched command
        return;
    }

    // subcommand with no arguments
    if (tokens_received == 1 &&
        _current_search_depth > 1 &&
        subcommand_matched == true &&
        prm.max_num_args == 0)
    {
        #if defined(__DEBUG_LAUNCH_LOGIC__)
        _ui_out(PSTR(">%s $DEBUG: subcmd w/no args, subcommand match true "
                     "tokens==0 max_args==0 depth>1 launchFunction(%s)\n"),
                _username_, prm.command);
        #endif
        match = true;                                       // don't run default callback
        launchFunction(cmd, prm, prm_idx, tokens_received); // launch the matched command
        return;
    }

    // command with arguments, potentially has subcommands but none were entered
    if (//_current_search_depth > 1 &&
        subcommand_matched == false &&
        tokens_received > 1 &&
        prm.max_num_args > 0)
    {        
        getArgs(tokens_received, input_type_match_flag, prm, all_arguments_valid);
        if (rec_num_arg_strings >= prm.num_args && 
            rec_num_arg_strings <= prm.max_num_args && 
            all_arguments_valid == true)
        {
            #if defined(__DEBUG_LAUNCH_LOGIC__)
            _ui_out(PSTR(">%s $DEBUG: cmd w/ args, no subcmd match, subcommand match false "
                         "tokens>0 max_args>0 depth>1 launchFunction(%s)\n"),
                    _username_, prm.command);
            #endif
            match = true;                                       // don't run default callback
            launchFunction(cmd, prm, prm_idx, tokens_received); // launch the matched command
        }
        // if !match, error
        return;
    }

    // command with arguments (max depth)
    if (_current_search_depth == (cmd->_tree_depth) && 
        tokens_received > 1 && 
        prm.max_num_args > 0 && 
        prm.sub_commands == 0)
    {
        getArgs(tokens_received, input_type_match_flag, prm, all_arguments_valid);
        //  if we received at least min and less than max arguments and they are valid
        if (rec_num_arg_strings >= prm.num_args && 
            rec_num_arg_strings <= prm.max_num_args && 
            all_arguments_valid == true)
        {
            #if defined(__DEBUG_LAUNCH_LOGIC__)
            _ui_out(PSTR(">%s $DEBUG: cmd w/args (max depth) launchFunction(%s)\n"), _username_, prm.command);
            #endif
            match = true;                                       // don't run default callback
            launchFunction(cmd, prm, prm_idx, tokens_received); // launch the matched command
        }
        // if !match, error
        return;
    }

    // subcommand search    
    subcommand_matched = false;
    #if defined(__DEBUG_SUBCOMMAND_SEARCH__)
    _ui_out(PSTR("search depth (%d)\n"), _current_search_depth);
    #endif
    if (_current_search_depth <= (cmd->_tree_depth)) // dig starting at depth 1
    {
        // this index starts at one because the parameter array's first element will be the root command
        for (size_t j = 1; j < (cmd->_param_array_len + 1); ++j) // through the parameter array
        {
            memcpy_P(&prm, &(cmd->prm[j]), sizeof(prm));            
            prm_idx = j;  
            if (prm.depth == _current_search_depth)
            {
                #if defined(__DEBUG_SUBCOMMAND_SEARCH__)
                _ui_out(PSTR("match depth cmd=(%s)\ntoken=(%s)\n"), 
                        prm.command, data_pointers[data_pointers_index]);
                #endif
                if (strcmp(data_pointers[data_pointers_index], prm.command) == 0)
                {
                    #if defined(__DEBUG_SUBCOMMAND_SEARCH__)
                    _ui_out(PSTR("(%s) subcommand matched, (%d) subcommands, max_num_args (%d)\n"),
                            prm.command, prm.sub_commands, prm.max_num_args);
                    #endif
                    // subcommand matched                    
                    if (tokens_received > 0)
                    {
                        tokens_received--; // subtract subcommand from tokens received
                        #if defined(__DEBUG_SUBCOMMAND_SEARCH__)
                        _ui_out(PSTR("decrement tokens (%d)\n"), tokens_received);
                        #endif
                        data_pointers_index++;
                    }
                    subcommand_matched = true; // subcommand matched
                    failed_on_subcommand = j;  // set error index
                    break;                     // break out of the loop
                }
            }
        }
        if (_current_search_depth < (cmd->_tree_depth))
        {
            _current_search_depth++;
        }
    }                               // end subcommand search    
    if (subcommand_matched == true) // recursion
    {
        #if defined(__DEBUG_SUBCOMMAND_SEARCH__)
        _ui_out(PSTR("recurse\n"));
        #endif
        launchLogic(cmd,
                    prm,
                    prm_idx,
                    tokens_received,
                    all_arguments_valid,
                    match,
                    input_type_match_flag,
                    subcommand_matched);
    }
}

char* UserInput::escapeCharactersSoTheyPrint(char input, char& buf)
{
    switch (input)
    {
    case '\0':
        memcpy_P(&buf, ui_escaped_char_pgm[0], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf;
    case '\a':
        memcpy_P(&buf, ui_escaped_char_pgm[1], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf;
    case '\b':
        memcpy_P(&buf, ui_escaped_char_pgm[2], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf;
    case '\t':
        memcpy_P(&buf, ui_escaped_char_pgm[3], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf;
    case '\n':
        memcpy_P(&buf, ui_escaped_char_pgm[4], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf;
    case '\v':
        memcpy_P(&buf, ui_escaped_char_pgm[5], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf;
    case '\f':
        memcpy_P(&buf, ui_escaped_char_pgm[6], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf;
    case '\r':
        memcpy_P(&buf, ui_escaped_char_pgm[7], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf;
    case '\e':
        memcpy_P(&buf, ui_escaped_char_pgm[8], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf;
    case '\"':
        memcpy_P(&buf, ui_escaped_char_pgm[9], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf;    
    default:
        memcpy_P(&buf, ui_escaped_char_pgm[11], UI_ESCAPED_CHAR_PGM_LEN);
        return &buf;    // return er error
    }
    memcpy_P(&buf, ui_escaped_char_pgm[11], UI_ESCAPED_CHAR_PGM_LEN);
    return &buf;    // guard return er error
}

char UserInput::combineControlCharacters(char input)
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
        return (char)'*';   // * error
    }
}

uint8_t UserInput::getArgType(Parameters &prm, size_t index)
{
    if (prm.argument_flag == no_arguments)
        return static_cast<uint8_t>(UITYPE::NO_ARGS);
    if (prm.argument_flag == single_type_argument)
        return static_cast<uint8_t>(prm._arg_type[0]);
    if (prm.argument_flag == argument_type_array)
        return static_cast<uint8_t>(prm._arg_type[index]);
    return static_cast<uint8_t>(UITYPE::_LAST); // return error if no match
}

void UserInput::getArgs(size_t &tokens_received,
                        bool *input_type_match_flag,
                        Parameters &prm,
                        bool &all_arguments_valid)
{
    rec_num_arg_strings = 0; // number of tokens read from data
    for (size_t i = 0; i < (tokens_received - 1); ++i)
    {
        input_type_match_flag[i] = validateUserInput(UserInput::getArgType(prm, i),
                                                     data_pointers_index + i); // validate the token
        rec_num_arg_strings++;
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
    if (UserInput::OutputIsEnabled())
    {
        va_list args;
        va_start(args, fmt);
        _string_pos += vsnprintf_P(_output_buffer + _string_pos, _output_buffer_len, fmt, args);
        va_end(args);
        _output_flag = true;
    }
}

void UserInput::_ReadCommandFromBufferErrorOutput(CommandConstructor *cmd,
                                                  Parameters &prm,
                                                  bool &command_matched,
                                                  bool *input_type_match_flag,
                                                  bool &all_arguments_valid,
                                                  uint8_t *data)
{
    // format a string with useful information
    if (UserInput::OutputIsEnabled())
    {
        // potential silent crash if failed_on_subcommand > cmd->_param_array_len
        // user introduced error condition, if they enter a parameter array length that is
        // greater than the actual array length
        if (failed_on_subcommand > cmd->_param_array_len) // error
        {
            memcpy_P(&prm, &(cmd->prm[0]), sizeof(prm));
            _ui_out(PSTR("OOB Parameters array element access attempted for command %s.\n"), prm.command);
            return;
        }        
        memcpy_P(&prm, &(cmd->prm[failed_on_subcommand]), sizeof(prm));
        _ui_out(PSTR(">%s $Invalid input: "), _username_);
        if (command_matched == true)
        {
            uint16_t err_n_args = (prm.max_num_args > (data_pointers_index_max - _current_search_depth))
                                      ? (data_pointers_index_max - _current_search_depth)
                                      : prm.max_num_args;
            if (err_n_args > 0)
            {
                for (size_t i = 0; i < (_current_search_depth + 1); ++i)
                {
                    _ui_out(PSTR("%s "), data_pointers[i]); // add subcommands to echo
                }
                for (uint16_t i = 0; i < err_n_args; ++i)
                {
                    if (input_type_match_flag[i] == false)
                    {
                        char _type[UI_INPUT_TYPE_STRINGS_PGM_LEN];
                        memcpy_P(&_type, &ui_input_type_strings[UserInput::getArgType(prm, i)], sizeof(_type));
                        if (data_pointers[1 + _current_search_depth + i] == NULL)
                        {
                            _ui_out(PSTR("'REQUIRED'*(%s) "), _type);
                        }
                        else
                        {
                            _ui_out(PSTR("'%s'*(%s) "), data_pointers[1 + _current_search_depth + i], _type);
                        }
                    }
                    else
                    {
                        _ui_out(PSTR("'%s'(OK) "), data_pointers[1 + _current_search_depth + i]);
                    }
                }
                _ui_out(PSTR("\n"));
                return;
            }
            _ui_out(PSTR("%s\n"), (char *)data);
            return;
        }
        else // command not matched
        {
            _ui_out(PSTR("%s\n"), (char *)data);
            _ui_out(PSTR("\n >Command <%s> unknown.\n"), data_pointers[0]);
        }
    }
}
