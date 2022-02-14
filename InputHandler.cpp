#include "InputHandler.h"

char* UserInput::NextArgument()
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

void UserInput::AddUserCommand(UserCallbackFunctionParameters* command)
{
    UserCallbackFunctionParameters** cmd_head = &commands_head_;
    UserCallbackFunctionParameters** cmd_tail = &commands_tail_;
    uint8_t* cmd_count = &commands_count_;
    command->next_callback_function_parameters = NULL;
    if (*cmd_head == NULL)
    {
        *cmd_head = *cmd_tail = command;
    }
    else
    {
        (*cmd_tail)->next_callback_function_parameters = command;
        *cmd_tail = command;
    }
    (*cmd_count)++;
}

bool UserInput::getToken(char* token_buffer, uint8_t* data, size_t len, uint16_t* data_index)
{
    bool got_token = false;
    char incoming = 0;                   // cast data[data_index] to char and run tests on incoming
    bool token_flag[2] = {false, false}; // token state machine, point to a token once
    for (uint16_t i = *data_index; i < len; ++i)
    {
        if (got_token == true)
        {
            if (EnableDebugOutput == true)
            {
                (*_string_pos) += snprintf_P(_output_buffer + (*_string_pos), _output_buffer_len,
                                             PSTR(">%s $DEBUG: got the token at the beginning of the for loop.\n"), (char*)_username);
            }
            break;
        }
        incoming = (char)data[*data_index];
        if (EnableDebugOutput == true)
        {
            (*_string_pos) += snprintf_P(_output_buffer + (*_string_pos), _output_buffer_len,
                                         PSTR(">%s $DEBUG: incoming char '%c' data_index = %lu.\n"),
                                         (char*)_username,
                                         incoming,
                                         (uint16_t)*data_index);
        }
        //  remove control characters that are not in a c-string argument, usually CRLF '\r' '\n'
        //  replace delimiter
        if (iscntrl(incoming) == true || incoming == (char)delim_[0])
        {
            token_buffer[*data_index] = (char)null_[0];
            token_flag[0] = false;
        }
        else if (incoming == (char)c_str_delim_[0]) // switch logic for c-string input
        {
            token_buffer[*data_index] = (char)null_[0]; // replace the c-string delimiter
            if (((*data_index) + 1) < len)              //  don't need to do this if we're at the end of user input
            {
                bool point_to_beginning_of_c_string = true; // c-string pointer assignment flag
                (*data_index)++;
                for (uint16_t j = *data_index; j < len; ++j) // this for loop starts at whatever data_index is equal to and has the potential to iterate up to len
                {
                    incoming = (char)data[*data_index];    // fetch the next incoming char
                    if (incoming == (char)c_str_delim_[0]) // if the next incoming char is a '\"'
                    {
                        token_buffer[*data_index] = (char)null_[0]; // replace the c-string delimiter
                        (*data_index)++;                            // increment the tokenized string index
                        break;
                    }
                    token_buffer[*data_index] = incoming;       // else assign incoming to token_buffer[data_index]
                    if (point_to_beginning_of_c_string == true) // a pointer will be assigned if point_to_beginning_of_c_string == true
                    {
                        data_pointers[data_pointers_index] = &token_buffer[*data_index]; // point to this position in token_buffer
                        data_pointers_index++;                                           //  increment pointer index
                        point_to_beginning_of_c_string = false;                          //  only set one pointer per c-string
                        got_token = true;
                        if (EnableDebugOutput == true)
                        {
                            (*_string_pos) += snprintf_P(_output_buffer + (*_string_pos), _output_buffer_len,
                                                         PSTR(">%s $DEBUG: got the c-string token.\n"), (char*)_username);
                        }
                    }
                    (*data_index)++; // increment the tokenized string index
                }
            }
        }
        else // this is a non c-string token
        {
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
                if (EnableDebugOutput == true)
                {
                    (*_string_pos) += snprintf_P(_output_buffer + (*_string_pos), _output_buffer_len,
                                                 PSTR(">%s $DEBUG: got the token token_flag[0] == false.\n"), (char*)_username);
                }
                got_token = true;
            }
            token_flag[1] = token_flag[0]; // track the state
        }
        if (token_flag[0] == true && (uint16_t)*data_index == (uint16_t)(len - 1))
        {
            if (EnableDebugOutput == true)
            {
                (*_string_pos) += snprintf_P(_output_buffer + (*_string_pos), _output_buffer_len,
                                             PSTR(">%s $DEBUG: got the token token_flag[0] == true && data_index == len - 1.\n"), (char*)_username);
            }
            got_token = true;
        }

        if (*data_index < len) // if we are at the end of input data
        {
            (*data_index)++; // increment buffer index
        }
    }
    return got_token;
}

bool UserInput::validateUserInput(UserCallbackFunctionParameters* cmd, uint8_t arg_type, uint16_t data_pointers_index)
{
    bool input_is_valid = true;

    const char* _negative_sign = PSTR("-");
    const char* _dot = PSTR(".");

    uint16_t strlen_data = strlen((char*)data_pointers[data_pointers_index]);
    bool found_negative_sign = ((char)data_pointers[data_pointers_index][0] == (char)_negative_sign[0]) ? true : false;

    if (arg_type < USER_INPUT_TYPE_CHAR && ((isdigit(data_pointers[data_pointers_index][0]) == true) || found_negative_sign == true))
    {
        // for numbers that are not floating point
        if (arg_type < USER_INPUT_TYPE_INT16_T && found_negative_sign == false)
        {
            for (uint16_t j = 0; j < strlen_data; ++j)
            {
                if (isdigit(data_pointers[data_pointers_index][j]) == false)
                {
                    input_is_valid = false;
                    break;
                }
            }
        }
        // for integer numbers
        if (arg_type == USER_INPUT_TYPE_INT16_T)
        {
            if (found_negative_sign == true)
            {
                for (uint16_t j = 1; j < (strlen_data - 1); ++j)
                {
                    if (isdigit(data_pointers[data_pointers_index][j]) == false)
                    {
                        input_is_valid = false;
                        break;
                    }
                }
            }
            else
            {
                for (uint16_t j = 0; j < strlen_data; ++j)
                {
                    if (isdigit(data_pointers[data_pointers_index][j]) == false)
                    {
                        input_is_valid = false;
                        break;
                    }
                }
            }
        }
        // for floating point numbers
        if (arg_type == USER_INPUT_TYPE_FLOAT)
        {
            uint8_t found_dot = 0;
            uint8_t num_digits = 0;
            if (found_negative_sign == true)
            {
                uint8_t not_digits = 0;
                /*
                    we already know there is a '-' at data[i + 1][0] because found_negative_sign is set
                    so start the for loop at an index of one
                */
                for (uint16_t j = 1; j < strlen_data; ++j)
                {
                    if (data_pointers[data_pointers_index][j] == (char)_dot[0])
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
            else
            {
                for (uint16_t j = 0; j < strlen_data; ++j)
                {
                    if (data_pointers[data_pointers_index][j] == (char)_dot[0])
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
                input_is_valid = false;
            }
        }
    }
    /*
        For char or c-string input.
        Types allowed are printable characters, punctuation, control characters \r\n etc, and digits 0-9
    */
    else if (arg_type == USER_INPUT_TYPE_CHAR || arg_type == USER_INPUT_TYPE_C_STRING)
    {
        for (uint16_t j = 0; j < strlen_data; ++j)
        {
            if (isprint(data_pointers[data_pointers_index][j])
                || ispunct(data_pointers[data_pointers_index][j])
                || iscntrl(data_pointers[data_pointers_index][j])
                || isdigit(data_pointers[data_pointers_index][j]))
            {
            }
            else
            {
                input_is_valid = false;
                break;
            }
        }
    }
    else
    {
        input_is_valid = false;
    }

    return input_is_valid;
}

void UserInput::launchFunction(UserCallbackFunctionParameters* cmd)
{
    (*_string_pos) += snprintf_P(_output_buffer + (*_string_pos), _output_buffer_len, PSTR(">%s $%s"), (char*)_username, (char*)data_pointers[0]);
    for (uint16_t i = 0; i < rec_num_arg_strings; ++i)
    {
        (*_string_pos) += snprintf_P(_output_buffer + (*_string_pos), _output_buffer_len, PSTR(" %s"), (char*)data_pointers[i + 1]);
    }
    (*_string_pos) += snprintf_P(_output_buffer + (*_string_pos), _output_buffer_len, PSTR("\n"));
    data_pointers_index = 0;
    cmd->function(this);
}

void UserInput::ReadCommand(uint8_t* data, size_t len)
{
    if (len > USER_INPUT_MAX_INPUT_LENGTH)
    {
        (*_string_pos) += snprintf_P(_output_buffer + (*_string_pos), _output_buffer_len,
                                     PSTR(">%s $ERROR: user input exceeds max allowed (UINT16_MAX) input length.\n"), (char*)_username);
        return;
    }
    uint16_t data_index = 0; // data iterator

    //  should maybe see if there is enough memory to allocate the token buffer
    char token_buffer[len + 1] = {'\0'}; // place to chop up the input
    data_pointers_index = 0;             // token buffer pointers
    rec_num_arg_strings = 0;             // number of tokens read from data
    bool match = false;
    UserCallbackFunctionParameters* cmd;

    /*
        this tokenizes an input buffer, it should work with any 8 bit input type that represents char
        char tokenized_string[] = "A\0Tokenized\0C-string\0"
        char non_tokenized_string[] = "A Non Tokenized C-string" <-- still has a \0 at the end of the string to terminate it
    */
    if (getToken(token_buffer, data, len, &data_index) == true) // if there was a token
    {
        bool input_type_match_flag[USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS] = {false};
        bool all_arguments_valid = true;                                                      // error sentinel
        bool command_matched = false;                                                         // error sentinel
        for (cmd = commands_head_; cmd != NULL; cmd = cmd->next_callback_function_parameters) // iterate through user commands
        {
            if (strcmp(data_pointers[0], cmd->command) == 0) // match
            {
                command_matched = true;
                if (cmd->num_args == 0) // command with no arguments
                {
                    if (EnableDebugOutput == true)
                    {
                        (*_string_pos) += snprintf_P(_output_buffer + (*_string_pos), _output_buffer_len,
                                                     PSTR(">%s $DEBUG: match zero argument command \"%s\".\n"),
                                                     (char*)_username,
                                                     (char*)cmd->command);
                    }
                    match = true;        // don't run default callback
                    launchFunction(cmd); // launch the matched command
                    break;               // break out of the for loop
                }
                else if (cmd->num_args > 0) // cmd->num_args > 0
                {
                    for (uint16_t i = 0; i < cmd->num_args; ++i) // iterate through all command arguments
                    {
                        if (getToken(token_buffer, data, len, &data_index) == true) //  see if there is a token
                        {
                            rec_num_arg_strings++;                                                                                              // if there is a token, increment the token counter
                            input_type_match_flag[i] = validateUserInput(cmd, cmd->arg_type[rec_num_arg_strings - 1], data_pointers_index - 1); // validate the token
                            if (input_type_match_flag[i] == false)                                                                              // if the token was not valid input
                            {
                                all_arguments_valid = false; // set the error sentinel to true
                            }
                            if (rec_num_arg_strings == cmd->num_args && all_arguments_valid == true) //  if we received the expected amount of arguments and all of them are valid
                            {
                                if (EnableDebugOutput == true)
                                {
                                    (*_string_pos) += snprintf_P(_output_buffer + (*_string_pos), _output_buffer_len,
                                                                 PSTR(">%s $DEBUG: match command \"%s\".\n"),
                                                                 (char*)_username,
                                                                 (char*)cmd->command);
                                }
                                match = true;        // don't run default callback
                                launchFunction(cmd); // launch the matched command
                                break;               // break out of the for loop
                            }
                        }
                        else
                        {
                            break;
                        }
                    }
                    break; // guard break
                }
                break;
            }
        }
        if (!match && default_handler_ != NULL) // if there was no command match and a default handler is configured
        {
            // format a string with useful information
            char data_char_buffer[len + 1] = {'\0'};
            for (uint16_t i = 0; i < len; ++i)
            {
                data_char_buffer[i] = (char)data[i];
            }
            (*_string_pos) += snprintf_P(_output_buffer + (*_string_pos), _output_buffer_len,
                                         PSTR(">%s $ERROR: %s\n"),
                                         (char*)_username,
                                         (char*)data_char_buffer);
            if (!command_matched)
            {
                (*_string_pos) += snprintf_P(_output_buffer + (*_string_pos), _output_buffer_len,
                                             PSTR("User command \"%s\" unknown.\n"),
                                             (char*)data_pointers[0]);
            }
            if (all_arguments_valid == false)
            {
                for (int i = 0; i < rec_num_arg_strings; ++i)
                {
                    if (input_type_match_flag[i] == false)
                    {
                        (*_string_pos) += snprintf_P(_output_buffer + (*_string_pos), _output_buffer_len,
                                                     PSTR("User command \"%s\" argument %lu error; Type mismatch, expected a %s; received \"%s\".\n"),
                                                     cmd->command, i + 1,
                                                     (char*)USER_INPUT_TYPE_STRING_LITERAL_ARRAY[cmd->arg_type[i]],
                                                     (char*)data_pointers[i + 1]);
                    }
                }
            }
            if (rec_num_arg_strings != cmd->num_args)
            {
                (*_string_pos) += snprintf_P(_output_buffer + (*_string_pos), _output_buffer_len,
                                             PSTR("User command \"%s\" received %02d arguments; \"%s\" expects %02d arguments.\n"),
                                             cmd->command, (rec_num_arg_strings), cmd->command, cmd->num_args);
            }
            (*default_handler_)(this); // run the default handler
        }
    }
    else
    {
        return;
    }
}

void UserInput::GetCommandFromStream(Stream& stream, uint16_t rx_buffer_size, const char* end_of_line_char)
{
    uint8_t data[rx_buffer_size + 1U] = {'\0'}; // an array to store the received data
    static boolean new_data = false;
    static uint16_t data_index = 0;
    char rc = 0;

    while (stream.available() > 0 && new_data == false)
    {
        rc = stream.read();
        if (rc != (char)end_of_line_char[0])
        {
            data[data_index] = (uint8_t)rc;
            data_index++;
            if (data_index >= rx_buffer_size)
            {
                data_index = rx_buffer_size - 1;
                data[data_index] = '\0'; // terminate the string
                new_data = true;
            }
        }
        else
        {
            data[data_index] = '\0'; // terminate the string
            data_index = 0;
            new_data = true;
        }
    }
    if (new_data == true)
    {
        UserInput::ReadCommand(data, data_index);
        new_data = false;
    }
}

void UserInput::ListUserCommands()
{
    UserCallbackFunctionParameters* cmd;
    (*_string_pos) += snprintf_P(_output_buffer + (*_string_pos), _output_buffer_len, PSTR("There are %lu commands available to user '%s':\n"), commands_count_, (char*)_username);
    for (cmd = commands_head_; cmd != NULL; cmd = cmd->next_callback_function_parameters)
    {
        (*_string_pos) += snprintf_P(_output_buffer + (*_string_pos), _output_buffer_len, PSTR("%s\n"), cmd->command);
    }
    (*_string_pos) += snprintf_P(_output_buffer + (*_string_pos), _output_buffer_len, PSTR("\n"));
}

void UserInput::ListUserInputSettings(UserInput* inputprocess)
{
    (*_string_pos) += snprintf_P(_output_buffer + (*_string_pos), _output_buffer_len, PSTR("end of line character \"%s\""), (char*)inputprocess->term_);
}

void UserInput::SetDefaultHandler(void (*function)(UserInput*))
{
    default_handler_ = function;
}
