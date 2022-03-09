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

char *UserInput::NextArgument()
{
    // wrap the index just in case this is called too many times
    if (data_pointers_index < USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS && data_pointers_index < rec_num_arg_strings)
    {
        data_pointers_index++;
    }
    else
    {
        data_pointers_index = 0;
    }
    return data_pointers[data_pointers_index];
}

void UserInput::AddCommand(CommandConstructor &command)
{
    CommandConstructor **cmd_head = &commands_head_;
    CommandConstructor **cmd_tail = &commands_tail_;
    size_t *cmd_count = &commands_count_;
    size_t *arg_count = &max_num_user_defined_args;
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
    //CommandParameters cmdprm;
    uint8_t max_args;
    //memcpy_P(&cmdprm, &(command.cmdprm), sizeof(cmdprm));
    memcpy_P(&max_args, &(command.prm->max_num_args), sizeof(max_args));
    if (*arg_count < max_args)
    {
        *arg_count = max_args;
    }
}

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
            #if defined(_DEBUG_USER_INPUT)
            if (UserInput::OutputIsEnabled())
            {
                _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                             PSTR(">%s $DEBUG: got the token at the beginning of the for loop.\n"),
                                             _username_);
                _output_flag = true;
            }
            #endif
            break;
        }
        incoming = (char)data[*data_index];
        #if defined(_DEBUG_USER_INPUT)
        if (UserInput::OutputIsEnabled())
        {
            _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                         PSTR(">%s $DEBUG: incoming char '%c' data_index = %lu.\n"),
                                         _username_,
                                         incoming,
                                         (uint16_t)*data_index);
            _output_flag = true;
        }
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
            token_buffer[*data_index] = _null_;              // replace the c-string delimiter
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
                        (*data_index)++;                     // increment the tokenized string index
                        break;
                    }
                    token_buffer[*data_index] = incoming;       // else assign incoming to token_buffer[data_index]
                    if (point_to_beginning_of_c_string == true) // a pointer will be assigned if point_to_beginning_of_c_string == true
                    {
                        data_pointers[data_pointers_index] = &token_buffer[*data_index]; // point to this position in token_buffer
                        data_pointers_index++;                                           //  increment pointer index
                        point_to_beginning_of_c_string = false;                          //  only set one pointer per c-string
                        got_token = true;
                        #if defined(_DEBUG_USER_INPUT)
                        if (UserInput::OutputIsEnabled())
                        {
                            _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                                         PSTR(">%s $DEBUG: got the c-string token.\n"),
                                                         _username_);
                            _output_flag = true;
                        }
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
                #if defined(_DEBUG_USER_INPUT)
                if (UserInput::OutputIsEnabled())
                {
                    _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                                 PSTR(">%s $DEBUG: got the token token_flag[0] == false.\n"),
                                                 _username_);
                    _output_flag = true;
                }
                #endif
                got_token = true;
            }
            token_flag[1] = token_flag[0]; // track the state
        }
        if (token_flag[0] == true && (uint16_t)*data_index == (data_length - 1U))
        {
            #if defined(_DEBUG_USER_INPUT)
            if (UserInput::OutputIsEnabled())
            {
                _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                             PSTR(">%s $DEBUG: got the token token_flag[0] == true && data_index == len - 1.\n"),
                                             _username_);
                _output_flag = true;
            }
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

void UserInput::launchFunction(const CommandConstructor *parameters)
{
    if (UserInput::OutputIsEnabled())
    {
        _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len, PSTR(">%s $%s"),
                                     _username_,
                                     data_pointers[0]);
        for (uint16_t i = 0; i < rec_num_arg_strings; ++i)
        {
            if (iscntrl(*data_pointers[i + 1]))
            {
                char temp_buffer[13] = {'\0'};
                UserInput::escapeCharactersSoTheyPrint(data_pointers[i + 1], temp_buffer);
                _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len, PSTR(" %s"), temp_buffer);
            }
            else
            {
                _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len, PSTR(" %s"), data_pointers[i + 1]);
            }
        }
        _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len, PSTR("\n"));
        _output_flag = true;
    }
    data_pointers_index = 0;
    parameters->function(this);
}

void UserInput::launchLogic(CommandConstructor *cmd,
                            Parameters &prm,
                            uint8_t *data,
                            size_t len,
                            bool &all_arguments_valid,
                            size_t &data_index,
                            bool &match,
                            bool *input_type_match_flag)
{
    if (prm.num_args == 0 && prm.max_num_args == 0) // command with no arguments
    {
        while (getToken(token_buffer, data, len, &data_index) == true && rec_num_arg_strings < USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS)
        {
            rec_num_arg_strings++;
            if (rec_num_arg_strings > 0)
            {
                break;
            }
        }
        #if defined(_DEBUG_USER_INPUT)
        if (UserInput::OutputIsEnabled())
        {
            _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                         PSTR(">%s $DEBUG: match zero argument command <%s>.\n"),
                                         _username_,
                                         cmd->command);
            _output_flag = true;
        }
        #endif
        match = true;        // don't run default callback
        launchFunction(cmd); // launch the matched command
        return;
    }
    else if (prm.num_args > 0 || prm.max_num_args > 0) // command has arguments
    {
        while (getToken(token_buffer, data, len, &data_index) == true && rec_num_arg_strings < USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS)
        {
            input_type_match_flag[rec_num_arg_strings] = validateUserInput(UserInput::getArgType(prm, rec_num_arg_strings), data_pointers_index - 1); // validate the token
            if (input_type_match_flag[rec_num_arg_strings] == false)                                                                                  // if the token was not valid input
            {
                all_arguments_valid = false; // set the error sentinel to true
            }
            rec_num_arg_strings++;
        }
        if (rec_num_arg_strings >= prm.num_args && rec_num_arg_strings <= prm.max_num_args && all_arguments_valid == true) //  if we received at least min and less than max arguments
        {
            #if defined(_DEBUG_USER_INPUT)
            if (UserInput::OutputIsEnabled())
            {
                _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                             PSTR(">%s $DEBUG: match command <%s>.\n"),
                                             _username_,
                                             cmd->command);
                _output_flag = true;
            }
            #endif
            match = true;        // don't run default callback
            launchFunction(cmd); // launch the matched command
        }
    }
}

void UserInput::ReadCommandFromBuffer(uint8_t* data, size_t len)
{
    // error checking
    if (len > USER_INPUT_MAX_INPUT_LENGTH)
    {
        if (UserInput::OutputIsEnabled())
        {
            _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                         PSTR(">%s $ERROR: input is greater than USER_INPUT_MAX_INPUT_LENGTH.\n"),
                                         _username_);
            _output_flag = true;
        }
        return;
    }    
    
    // this is declared here to test if token_buffer == nullptr (error condition)
    token_buffer = new char[len + 1](); // place to chop up the input
    if (token_buffer == nullptr)        // if there was an error allocating the memory
    {
        if (UserInput::OutputIsEnabled())
        {
            _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                         PSTR(">%s $ERROR: not enough free ram to allocate the token buffer.\n"),
                                         _username_);
            _output_flag = true;
        }
        return;
    }
    // end error checking

    size_t data_index = 0;              // data iterator
    data_pointers_index = 0;            // token buffer pointers
    rec_num_arg_strings = 0;            // number of tokens read from data
    bool match = false;                 // command string match
    bool command_matched = false;       // error sentinel
    bool subcommand_matched = false;    // error sentinel
    uint8_t failed_on_subcommand = 0;   // error index
    CommandConstructor* cmd;            // command parameters pointer        
    Parameters prm;

    /*
        this tokenizes an input buffer, it should work with any 8 bit input type that represents char
        char tokenized_string[] = "A\0Tokenized\0C-string\0"
        char non_tokenized_string[] = "A Non Tokenized C-string" <-- still has a \0 at the end of the string to terminate it
    */
    if (getToken(token_buffer, data, len, &data_index) == true) // if there was a token
    {
        bool input_type_match_flag[USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS] = {false};
        bool all_arguments_valid = true;                                            // error sentinel
        for (cmd = commands_head_; cmd != NULL; cmd = cmd->next_command_parameters) // iterate through user commands
        {            
            memcpy_P(&prm, cmd->prm, sizeof(prm));  // move working variables to ram         
            // if the first test is false, the strcmp test is not evaluated
            if (cmd->sub_commands == 0 && (strcmp(data_pointers[0], prm.command) == 0)) // match command with no subcommands
            {
                command_matched = true; // base command matched
                // try to launch target function
                launchLogic(cmd,
                            prm,
                            data,
                            len,
                            all_arguments_valid,
                            data_index,
                            match,
                            input_type_match_flag);
                break;
            }   // end regular command logic
            if (cmd->sub_commands > 0 && (strcmp(data_pointers[0], prm.command) == 0)) // match command with subcommands
            {
                command_matched = true; // base command matched (base command with subcommands)
                bool got_token = getToken(token_buffer, data, len, &data_index);    // see if there's a token
                if ((prm.num_args == 0) && got_token == false)  // if the base command accepts no args and there are no tokens
                {   
                    // try to launch target function
                    launchLogic(cmd,
                                prm,
                                data,
                                len,
                                all_arguments_valid,
                                data_index,
                                match,
                                input_type_match_flag);
                    break;  // break out of cmd iterator for loop
                }
                for (size_t j = 0; j < cmd->sub_commands; ++j)
                {                    
                    memcpy_P(&prm, &(cmd->prm[j + 1]), sizeof(prm));    // move working subcommand variables into ram
                    if (strcmp(data_pointers[1], prm.command) == 0) // if the subcommand matched
                    {                        
                        subcommand_matched = true;  // clear subcommand match error                                                                        
                        // try to launch target function
                        launchLogic(cmd,
                                    prm,
                                    data,
                                    len,
                                    all_arguments_valid,
                                    data_index,
                                    match,
                                    input_type_match_flag);
                        failed_on_subcommand = j + 1;   // set error index
                        break;
                    }                    
                }
                break;  // guard break
            }   // end subcommand logic
        } // end base command for loop

        if (!match && default_function_ != NULL) // if there was no command match and a default function is configured
        {
            // format a string with useful information
            if (UserInput::OutputIsEnabled())
            {                
                memcpy_P(&prm, &(cmd->prm[failed_on_subcommand]), sizeof(prm));
                if (failed_on_subcommand > 0)
                {
                    _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                                 PSTR(">%s $Invalid input: %s %s "),
                                                 _username_,
                                                 data_pointers[0], data_pointers[failed_on_subcommand]);
                }
                else
                {
                    _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                                 PSTR(">%s $Invalid input: %s "),
                                                 _username_,
                                                 data_pointers[0]);
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
                                    _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                                                 PSTR("%s* "),
                                                                 data_pointers[failed_on_subcommand + i + 1]);
                                }
                                else
                                {
                                    _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                                                 PSTR("%s "),
                                                                 data_pointers[failed_on_subcommand + i + 1]);
                                }
                            }
                            else
                            {
                                if (input_type_match_flag[i] == false)
                                {
                                    _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                                                 PSTR("%s* "),
                                                                 data_pointers[i + 1]);
                                }
                                else
                                {
                                    _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                                                 PSTR("%s "),
                                                                 data_pointers[i + 1]);
                                }
                            }
                        }
                    }
                }
                _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                             PSTR("\n"));
                if (!command_matched)
                {
                    _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                                 PSTR("Command <%s> unknown.\n"),
                                                 data_pointers[0]);
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
                                _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                                             PSTR(" > arg(%u) should be %s; received \"%s\".\n"),
                                                             i + 1,
                                                             _type,
                                                             data_pointers[failed_on_subcommand + i + 1]);
                            }
                        }
                        else
                        {
                            if (input_type_match_flag[i] == false)
                            {
                                char _type[UI_INPUT_TYPE_STRINGS_MAX_LEN];
                                memcpy_P(&_type, &ui_input_type_strings[UserInput::getArgType(prm, i)], sizeof(_type));
                                _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                                             PSTR(" > arg(%u) should be %s; received \"%s\".\n"),
                                                             i + 1,
                                                             _type,
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
                            _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                                         PSTR(" subcommand \"%s\" received <%02u> arguments; %s expects <%02u> arguments.\n"),
                                                         prm.command, (rec_num_arg_strings), prm.command, prm.num_args);
                        }
                        else
                        {
                            _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                                         PSTR(" command \"%s\" received <%02u> arguments; %s expects <%02u> arguments.\n"),
                                                         prm.command, (rec_num_arg_strings), prm.command, prm.num_args);
                        }
                    }
                    else // variable number of args
                    {
                        if (failed_on_subcommand > 0)
                        {
                            _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                                         PSTR(" subcommand \"%s\" received <%02u> arguments; %s expects between <%02u> and <%02u> arguments.\n"),
                                                         prm.command, (rec_num_arg_strings), prm.command, prm.num_args, prm.max_num_args);
                        }
                        else
                        {
                            _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                                         PSTR(" command \"%s\" received <%02u> arguments; %s expects between <%02u> and <%02u> arguments.\n"),
                                                         prm.command, (rec_num_arg_strings), prm.command, prm.num_args, prm.max_num_args);
                        }
                    }
                }
                _output_flag = true;
            }
            (*default_function_)(this); // run the default function
        }
    }
    else
    {
        if (UserInput::OutputIsEnabled() && len > 0)
        {
            _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                         PSTR(">%s $ERROR: No tokens retrieved.\n"),
                                         _username_);
            _output_flag = true;
        }
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
            if (UserInput::OutputIsEnabled())
            {
                _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                             PSTR(">%s $ERROR: not enough memory for stream rx buffer\n"),
                                             _username_);
                _output_flag = true;
            }
            return;
        }
        stream_buffer_allocated = true;
    }
    char *rc = (char *)stream_data;

    while (stream.available() > 0 && new_stream_data == false)
    {
        rc[stream_data_index] = stream.read();
        if (rc[stream_data_index] == _term_[0] || rc[stream_data_index] == _term_[1])
        {
            stream_data[stream_data_index] = '\0';
            new_stream_data = true;
        }
        else if (stream_data_index < (rx_buffer_size - 1))
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
    if (UserInput::OutputIsEnabled())
    {
        CommandConstructor *cmd;                      
        _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                     PSTR("Commands available to %s:\n"),
                                     _username_);
        uint8_t i = 1;
        for (cmd = commands_head_; cmd != NULL; cmd = cmd->next_command_parameters)
        {            
            char buffer[USER_INPUT_MAX_COMMAND_LENGTH];
            memcpy_P(&buffer, cmd->prm->command, sizeof(buffer));
            _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len, PSTR(" %02u. <%s>\n"),
                                         i, buffer);
            i++;
        }
        _output_flag = true;
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
            if (i == len)
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

void UserInput::ListSettings(UserInput *inputprocess)
{
    if (UserInput::OutputIsEnabled())
    {
        char temp_settings[3][13] = {'\0'};
        inputprocess->escapeCharactersSoTheyPrint(_term_, temp_settings[0]);
        inputprocess->escapeCharactersSoTheyPrint(_delim_, temp_settings[1]);
        inputprocess->escapeCharactersSoTheyPrint(_c_str_delim_, temp_settings[2]);
        _string_pos += UI_SNPRINTF_P(_output_buffer + _string_pos, _output_buffer_len,
                                     PSTR("username = \"%s\"\n"
                                          "end_of_line_characters = \"%s\"\n"
                                          "token_delimiter = \"%s\"\n"
                                          "c_string_delimiter = \"%s\"\n"),
                                     _username_,
                                     (char *)temp_settings[0],
                                     (char *)temp_settings[1],
                                     (char *)temp_settings[2]);
        _output_flag = true;
    }
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
            _output_buffer[i] = '\0'; // reinit output_buffer
        }
    }
    _output_flag = false;
}

uint8_t UserInput::getArgType(Parameters &opt, size_t index)
{
    if (opt.argument_flag == no_arguments) return static_cast<uint8_t>(UITYPE::NOTYPE);
    if (opt.argument_flag == single_type_argument) return static_cast<uint8_t>(opt._arg_type[0]);
    if (opt.argument_flag == argument_type_array) return static_cast<uint8_t>(opt._arg_type[index]);    
    return static_cast<uint8_t>(UITYPE::_LAST);    // return error if no match
}
