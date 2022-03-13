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
    // return null if there are no more arguments
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
    if (len > (UI_MAX_IN_LEN - 2)) // 65535 - 1(index align) - 1(space for null)
    {
        _ui_out(PSTR(">%s $ERROR: input is greater than USER_INPUT_MAX_INPUT_LENGTH.\n"), _username_);
        return;
    }

    // this is declared here to test if token_buffer == nullptr (error condition)
    token_buffer = new char[len + 1](); // place to chop up the input
    if (token_buffer == nullptr)        // if there was an error allocating the memory
    {
        _ui_out(PSTR(">%s $ERROR: not enough free ram to allocate the token buffer.\n"), _username_);
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
    while ((getToken(token_buffer, data, len, &data_index) == true) // if there was a token
           && (tokens_received < (UI_MAX_ARGS + 1)))
    {
        tokens_received++;                        // increment tokens_received
        if (tokens_received == (UI_MAX_ARGS + 1)) // while sentinel
        {
            break;
        }
    }

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
            // tokens_received--;                  // subtract root command from remaining tokens
            command_matched = true;          // root command match flag
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
        // format a string with useful information
        if (UserInput::OutputIsEnabled())
        {
            memcpy_P(&prm, &(cmd->prm[failed_on_subcommand]), sizeof(prm));
            if (failed_on_subcommand > 0)
            {
                _ui_out(PSTR(">%s $Invalid input: %s "), _username_, data_pointers[0]);
                for (size_t i = 0; i < (failed_on_subcommand - 1); ++i)
                {
                    _ui_out(PSTR("%s "), data_pointers[i + 1]);
                }
            }
            else
            {
                _ui_out(PSTR(">%s $Invalid input: %s "), _username_, data_pointers[0]);
            }
            if (command_matched == true)
            {
                uint16_t err_n_args = (prm.max_num_args > rec_num_arg_strings) ? rec_num_arg_strings : prm.max_num_args;
                if (err_n_args > 0)
                {
                    for (uint16_t i = 0; i < err_n_args; ++i)
                    {
                        if (failed_on_subcommand > 0)
                        {
                            if (input_type_match_flag[i] == false)
                            {
                                _ui_out(PSTR("%s* "), data_pointers[failed_on_subcommand + i]);
                            }
                            else
                            {
                                _ui_out(PSTR("%s "), data_pointers[failed_on_subcommand + i]);
                            }
                        }
                        else
                        {
                            if (input_type_match_flag[i] == false)
                            {
                                _ui_out(PSTR("%s* "), data_pointers[i + 1]);
                            }
                            else
                            {
                                _ui_out(PSTR("%s "), data_pointers[i + 1]);
                            }
                        }
                    }
                    _ui_out(PSTR("\n"));
                }
            }
            if (!command_matched)
            {
                _ui_out(PSTR("Command <%s> unknown.\n"), data_pointers[0]);
            }
            if (command_matched && all_arguments_valid == false)
            {
                uint16_t err_n_args = (prm.max_num_args > rec_num_arg_strings) ? rec_num_arg_strings : prm.max_num_args;
                for (uint8_t i = 0; i < err_n_args; ++i)
                {
                    if (failed_on_subcommand > 0)
                    {
                        if (input_type_match_flag[i] == false)
                        {
                            char _type[UI_INPUT_TYPE_STRINGS_MAX_LEN];
                            memcpy_P(&_type, &ui_input_type_strings[UserInput::getArgType(prm, i)], sizeof(_type));
                            _ui_out(PSTR(" > arg(%u) should be %s; received \"%s\".\n"), i + 1, _type,
                                    data_pointers[failed_on_subcommand + i]);
                        }
                    }
                    else
                    {
                        if (input_type_match_flag[i] == false)
                        {
                            char _type[UI_INPUT_TYPE_STRINGS_MAX_LEN];
                            memcpy_P(&_type, &ui_input_type_strings[UserInput::getArgType(prm, i)], sizeof(_type));
                            _ui_out(PSTR(" > arg(%u) should be %s; received \"%s\".\n"), i + 1, _type,
                                    data_pointers[i + 1]);
                        }
                    }
                }
            }
            if (command_matched && ((rec_num_arg_strings < prm.num_args) || (rec_num_arg_strings > prm.max_num_args)))
            {
                if (prm.num_args == prm.max_num_args) // fixed amount of args
                {
                    if (failed_on_subcommand > 0)
                    {
                        _ui_out(PSTR(" subcommand \"%s\" received <%02u> arguments; %s expects <%02u> arguments.\n"),
                                prm.command, (rec_num_arg_strings), prm.command, prm.num_args);
                    }
                    else
                    {
                        _ui_out(PSTR(" command \"%s\" received <%02u> arguments; %s expects <%02u> arguments.\n"),
                                prm.command, (rec_num_arg_strings), prm.command, prm.num_args);
                    }
                }
                else // variable number of args
                {
                    if (failed_on_subcommand > 0)
                    {
                        _ui_out(PSTR(" subcommand \"%s\" received <%02u> arguments; %s expects between <%02u> and <%02u> arguments.\n"),
                                prm.command, (rec_num_arg_strings), prm.command, prm.num_args, prm.max_num_args);
                    }
                    else
                    {
                        _ui_out(PSTR(" command \"%s\" received <%02u> arguments; %s expects between <%02u> and <%02u> arguments.\n"),
                                prm.command, (rec_num_arg_strings), prm.command, prm.num_args, prm.max_num_args);
                    }
                }
            }
        }
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
            _ui_out(PSTR(">%s $ERROR: not enough memory for stream rx buffer\n"), _username_);
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
    char temp_settings[3][8] = {'\0'};
    inputprocess->escapeCharactersSoTheyPrint(_term_, temp_settings[0]);
    inputprocess->escapeCharactersSoTheyPrint(_delim_, temp_settings[1]);
    inputprocess->escapeCharactersSoTheyPrint(_c_str_delim_, temp_settings[2]);
    _ui_out(PSTR("username = \"%s\"\n"
                 "end_of_line_characters = \"%s\"\n"
                 "token_delimiter = \"%s\"\n"
                 "c_string_delimiter = \"%s\"\n"),
            _username_,
            (char *)temp_settings[0],
            (char *)temp_settings[1],
            (char *)temp_settings[2]);
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
    for (uint16_t i = *data_index; i < data_length; ++i)
    {
        if (got_token == true)
        {
#if defined(__DEBUG_GET_TOKEN__)
            _ui_out(PSTR(">%s $DEBUG: got the token at the beginning of the for loop.\n"), _username_);
#endif
            break;
        }
        incoming = (char)data[*data_index];
#if defined(__DEBUG_GET_TOKEN__)
        _ui_out(PSTR(">%s $DEBUG: incoming char '%c' data_index = %lu.\n"),
                _username_, incoming, (uint16_t)*data_index);
#endif
        //  remove control characters that are not in a c-string argument, usually CRLF '\r' '\n'
        //  replace delimiter
        if (iscntrl(incoming) == true || incoming == (char)_delim_[0])
        {
            token_buffer[*data_index] = _null_;
            token_flag[0] = false;
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
                        _ui_out(PSTR(">%s $DEBUG: got the c-string token.\n"), _username_);
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
                token_buffer[*data_index] = '\0';
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
                _ui_out(PSTR(">%s $DEBUG: got the token token_flag[0] == false.\n"),
                        _username_);
#endif
                got_token = true;
            }
            token_flag[1] = token_flag[0]; // track the state
        }
        if (token_flag[0] == true && (uint16_t)*data_index == (data_length - 1U))
        {
#if defined(__DEBUG_GET_TOKEN__)
            _ui_out(PSTR(">%s $DEBUG: got the token token_flag[0] == true && data_index == len - 1.\n"),
                    _username_);
#endif
            got_token = true;
        }

        if (*data_index < data_length) // if we are at the end of input data
        {
            (*data_index)++; // increment buffer index
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
                               Parameters &prm, uint8_t &prm_idx, size_t tokens_received)
{
    if (UserInput::OutputIsEnabled())
    {
        _ui_out(PSTR(">%s $%s"), _username_, data_pointers[0]);
        for (uint16_t i = 0; i < (tokens_received - 1); ++i)
        {
            if (iscntrl(*data_pointers[i + 1]))
            {
                char temp_buffer[13] = {'\0'};
                UserInput::escapeCharactersSoTheyPrint(data_pointers[i + 1], temp_buffer);
                _ui_out(PSTR(" %s"), temp_buffer);
            }
            else
            {
                _ui_out(PSTR(" %s"), data_pointers[i + 1]);
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
    if (tokens_received > 1 && prm.sub_commands == 0 && prm.max_num_args == 0)
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
    if (_current_search_depth > 1 &&
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
    failed_on_subcommand = 0;
    subcommand_matched = false;
    #if defined(__DEBUG_SUBCOMMAND_SEARCH__)
    _ui_out(PSTR("search depth (%d)\n"), _current_search_depth);
    #endif
    if (_current_search_depth <= (cmd->_tree_depth)) // dig starting at depth 1
    {
        // this index starts at one because the parameter array's first element will be the root command
        for (size_t j = 1; j < cmd->_param_array_len; ++j) // through the parameter array
        {
            memcpy_P(&prm, &(cmd->prm[j]), sizeof(prm));
            failed_on_subcommand = j;
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
                    break;                     // break out of the loop
                }
            }
        }
        if (_current_search_depth < (cmd->_tree_depth))
        {
            _current_search_depth++;
        }
    } // end subcommand search

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

void UserInput::escapeCharactersSoTheyPrint(const char *input, char *output)
{
    uint16_t len = strlen(input);
    for (uint16_t i = 0; i < len; ++i)
    {
        switch ((char)input[i])
        {
        case '\a':
            strcat_P(output, PSTR("\\a"));
            break;
        case '\b':
            strcat_P(output, PSTR("\\b"));
            break;
        case '\f':
            strcat_P(output, PSTR("\\f"));
            break;
        case '\n':
            strcat_P(output, PSTR("\\n"));
            break;
        case '\r':
            strcat_P(output, PSTR("\\r"));
            break;
        case '\t':
            strcat_P(output, PSTR("\\t"));
            break;
        case '\v':
            strcat_P(output, PSTR("\\v"));
            break;
        case '\"':
            strcat_P(output, PSTR("\\\""));
            break;
        default:
            strcat(output, input);
            break;
        }
    }
}

char UserInput::combineControlCharacters(char input)
{
    switch ((char)input)
    {
    case 'a':
        return (char)'\a';
    case 'b':
        return (char)'\b';
    case 'f':
        return (char)'\f';
    case 'n':
        return (char)'\n';
    case 'r':
        return (char)'\r';
    case 't':
        return (char)'\t';
    case 'v':
        return (char)'\v';
    case '"':
        return (char)'\"';
    default:
        return input;
    }
}

uint8_t UserInput::getArgType(Parameters &opt, size_t index)
{
    if (opt.argument_flag == no_arguments)
        return static_cast<uint8_t>(UITYPE::NOTYPE);
    if (opt.argument_flag == single_type_argument)
        return static_cast<uint8_t>(opt._arg_type[0]);
    if (opt.argument_flag == argument_type_array)
        return static_cast<uint8_t>(opt._arg_type[index]);
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
