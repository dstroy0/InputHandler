/**
 *  @file InputHandler.cpp
 *  @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
 *  @brief InputHandler library cpp file
 *  @version 1.1
 *  @date 2022-05-28
 *
 *  @copyright Copyright (c) 2022
 */
/*
 *   Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
 *
 *   This program is free software; you can redistribute it and/or
 *   modify it under the terms of the GNU General Public License
 *   version 3 as published by the Free Software Foundation.
 */

#include "InputHandler.h"

/*
 *   public methods
 */

void UserInput::defaultFunction(void (*function)(UserInput*))
{
    _default_function_ = function;
} // end defaultFunction

void UserInput::addCommand(CommandConstructor& command)
{
    size_t max_depth_found = 0; // for _data_pointers_ array sizing
    size_t max_args_found = 0;  // for _data_pointers_ array sizing
    CommandParameters prm; // this CommandParameters struct is referenced by the helper function
                           // _addCommandAbort()
    size_t wc_containing_prm_found = 0;
    IH::memcmp_idx_t
        wc_containing_prm_index_arr[UI_MAX_COMMANDS_IN_TREE] {}; // max possible amount of
                                                                 // subcommands + root command
    bool err = false; // CommandParameters struct error sentinel
    /*
        the reason we run through the whole CommandParameters array instead of breaking
        on error is to give users clues as to what might be wrong with their
        command CommandParameters
    */
    for (size_t i = 0; i < command.param_array_len; ++i)
    {
        memcpy_P(&prm, &(command.prm[i]), sizeof(prm));
        if (!UserInput::_addCommandAbort(command, prm)) // input CommandParameters error checking
        {
            err = true;
        }
        else
        {
            max_depth_found =
                (command.tree_depth > max_depth_found) ? command.tree_depth : max_depth_found;
            max_args_found =
                (prm.max_num_args > max_args_found) ? prm.max_num_args : max_args_found;
            if (prm.has_wildcards == true)
            {
                wc_containing_prm_index_arr[wc_containing_prm_found] = i;
                wc_containing_prm_found++;
            }
        }
    }
    if (!err) // if no error
    {
        if (wc_containing_prm_found
            > 0) // if the number of wildcard containing CommandParameters is greater than zero
        {
            command.calc = (struct CommandRuntimeCalc*)calloc(1, sizeof(struct CommandRuntimeCalc));
            command.calc->num_prm_with_wc = (IH::memcmp_idx_t)wc_containing_prm_found;
            command.calc->idx_of_prm_with_wc =
                (IH::memcmp_idx_t*)calloc(wc_containing_prm_found, sizeof(IH::memcmp_idx_t));
            command.calc->num_memcmp_ranges_this_row = (IH::ui_max_per_cmd_memcmp_ranges_t*)calloc(
                wc_containing_prm_found, sizeof(IH::ui_max_per_cmd_memcmp_ranges_t));
            command.calc->memcmp_ranges_arr = (IH::ui_max_per_cmd_memcmp_ranges_t**)calloc(
                wc_containing_prm_found, sizeof(IH::ui_max_per_cmd_memcmp_ranges_t*));
            memcpy(command.calc->idx_of_prm_with_wc, wc_containing_prm_index_arr,
                wc_containing_prm_found);
            for (size_t i = 0; i < wc_containing_prm_found; ++i)
            {
                IH::ui_max_per_cmd_memcmp_ranges_t memcmp_ranges[UI_MAX_PER_CMD_MEMCMP_RANGES] {};
                IH::ui_max_per_cmd_memcmp_ranges_t memcmp_ranges_idx = 0;
                memcpy_P(&prm, &(command.prm[wc_containing_prm_index_arr[i]]), sizeof(prm));
                UserInput::_calcCmdMemcmpRanges(
                    command, prm, wc_containing_prm_index_arr[i], memcmp_ranges_idx, memcmp_ranges);
                command.calc->num_memcmp_ranges_this_row[i] = memcmp_ranges_idx;
                command.calc->memcmp_ranges_arr[i] = (IH::ui_max_per_cmd_memcmp_ranges_t*)calloc(
                    memcmp_ranges_idx, sizeof(IH::ui_max_per_cmd_memcmp_ranges_t));
                memcpy(command.calc->memcmp_ranges_arr[i], &memcmp_ranges, memcmp_ranges_idx);
#if defined(__DEBUG_ADDCOMMAND__) && defined(ENABLE_ui_out)
                UserInput::_ui_out(
                    PSTR("cmd %s memcmp_ranges_arr num elements: %d\nmemcmp ranges: \n"),
                    prm.command, memcmp_ranges_idx);
                for (size_t j = 0; j < memcmp_ranges_idx; ++j)
                {
                    if (j % 2 == 0)
                    {
                        UserInput::_ui_out(
                            PSTR("%d, "), (uint8_t)command.calc->memcmp_ranges_arr[i][j]);
                    }
                    else
                    {
                        UserInput::_ui_out(
                            PSTR("%d\n"), (uint8_t)command.calc->memcmp_ranges_arr[i][j]);
                    }
                }
#endif
            }
        }
        else
        {
            // CommandConstructor sets this pointer null, this is here for clarity
            command.calc = NULL;
        }
        _commands_count_++;
        _max_depth_ = (max_depth_found > _max_depth_) ? max_depth_found : _max_depth_;
        _max_args_ = (max_args_found > _max_args_) ? max_args_found : _max_args_;

        if (_commands_head_ == NULL) // the linked-list is empty
        {
            _commands_head_ = _commands_tail_ =
                &command; // (this) is the beginning of the linked-list
        }
        else
        {
            _commands_tail_->next_command = &command; // single linked-list (next only)
            _commands_tail_ = &command;               // move the tail to (this)
        }
    }
} // end addCommand

bool UserInput::begin()
{
    _p_num_ptrs_ = 1U + _max_depth_
        + _max_args_; // root + max depth found + max args found (in UserInput::addCommand())
    if (_max_args_ != 0)
    {
        _input_type_match_flags_ = (IH::input_type_match_flags_type*)calloc(_max_args_,
            sizeof(
                IH::input_type_match_flags_type)); // this array lives the lifetime of the process
    }
    if (_input_type_match_flags_ == NULL && _max_args_ != 0)
    {
#if defined(UI_VERBOSE) && defined(ENABLE_ui_out)
        UserInput::_ui_out(
            PSTR("ERROR! Cannot allocate ram for UserInput::_input_type_match_flags_\n"));
#endif
        _begin_ = false;
        return _begin_;
    }
    _data_pointers_ = (char**)calloc(_p_num_ptrs_, sizeof(char*)); // as does this array of pointers
    if (_data_pointers_ == NULL)
    {
#if defined(UI_VERBOSE) && defined(ENABLE_ui_out)
        UserInput::_ui_out(PSTR("ERROR! Cannot allocate ram for UserInput::_data_pointers_\n"));
#endif
        _begin_ = false;
        free(_input_type_match_flags_);
        return _begin_;
    }
    _begin_ = true;
    return _begin_;
} // end begin

#if defined(ENABLE_listSettings) && defined(UI_VERBOSE) && defined(ENABLE_ui_out)
void UserInput::listSettings(UserInput* inputProcess)
{
    if (!_begin_)
    {
        UserInput::_ui_out(PSTR("UserInput::begin() not declared.\n"));
        return;
    }
    IH_pname process_name;
    memcpy_P(&process_name, _input_prm_.process_name, sizeof(process_name));
    IH_eol eol;
    memcpy_P(&eol, _input_prm_.eol_char, sizeof(eol));
    IH_input_cc input_control_char_sequence;
    memcpy_P(&input_control_char_sequence, _input_prm_.input_control_char_sequence,
        sizeof(input_control_char_sequence));
    InputProcessDelimiterSequences delimseqs;
    memcpy_P(&delimseqs, _input_prm_.delimiter_sequences, sizeof(delimseqs));
    InputProcessStartStopSequences ststpseqs;
    memcpy_P(&ststpseqs, _input_prm_.start_stop_sequences, sizeof(ststpseqs));
    size_t buf_sz = strlen((char*)eol) + strlen((char*)input_control_char_sequence) + 2U;

    // should loop through and strlen everything
    for (size_t i = 0;
         i < ((delimseqs.num_seq > ststpseqs.num_seq) ? delimseqs.num_seq : ststpseqs.num_seq); ++i)
    {
        if (i < delimseqs.num_seq)
        {
            buf_sz += delimseqs.delimiter_lens[i];
            buf_sz++;
        }
        if (i < ststpseqs.num_seq)
        {
            buf_sz += ststpseqs.start_stop_sequence_lens[i];
            buf_sz++;
        }
    }
    char* buf = (char*)calloc(buf_sz * UI_ESCAPED_CHAR_STRLEN,
        sizeof(
            char)); // allocate char buffer large enough to print these potential control characters
    if (buf == NULL)
    {
        UserInput::_ui_out(PSTR("ERROR: listSettings() cannot allocate ram to escape control char "
                                "so they will print.\n"));
        return;
    }
    size_t idx = 0;
    UserInput::_ui_out(
        PSTR("src/config/InputHandler_config.h:\n"
             "UI_MAX_ARGS_PER_COMMAND %lu max allowed arguments per unique command_id\n"
             "UI_MAX_CMD_LEN (root command) %lu characters\n"
             "UI_MAX_IN_LEN %lu bytes\n"
             "\nUserInput constructor:\n"
             "output buffer size in bytes = %lu\n"
             "process_name = \"%s\"\n"
             "_data_pointers_[root(1) + _max_depth_ + _max_args_] == [%02lu]\n"
             "_max_depth_ (found from input CommandParameters) = %lu\n"
             "_max_args_ (found from input CommandParameters) = %lu\n"
             "\nEscaped for display:\n"
             "input_control_char_sequence = \"%s\"\n"
             "peol = \"%s\"\n"),
        (uint32_t)UI_MAX_ARGS_PER_COMMAND, (uint32_t)UI_MAX_CMD_LEN, (uint32_t)UI_MAX_INPUT_LEN,
        (uint32_t)_output_buffer_len_, (char*)process_name, (uint32_t)_p_num_ptrs_,
        (uint32_t)_max_depth_, (uint32_t)_max_args_,
        _addEscapedControlCharToBuffer(buf, idx, (char*)input_control_char_sequence,
            strlen((char*)input_control_char_sequence)),
        _addEscapedControlCharToBuffer(buf, idx, (char*)eol, strlen((char*)eol)));
    UserInput::_ui_out(PSTR("pdelimseqs = delim<\"\">\n"));
    for (size_t i = 0; i < delimseqs.num_seq; ++i)
    {
        UserInput::_ui_out(PSTR("<\"%s\">%c"),
            UserInput::_addEscapedControlCharToBuffer(buf, idx, delimseqs.delimiter_sequences[i],
                strlen(delimseqs.delimiter_sequences[i])),
            (((delimseqs.num_seq > 1) && (i % 5U != 0))
                    ? '|'
                    : ((i % 5U == 0) ? '\n' : '\n'))); // separate <> with a pipe | and start a
                                                       // newline every 5 sequences
    }
    UserInput::_ui_out(PSTR("pststpseqs = start<\"\">|stop<\"\">\n"));
    for (size_t i = 0; i < ststpseqs.num_seq; i += 2)
    {
        UserInput::_ui_out(PSTR("<\"%s\">|<\"%s\">\n"),
            UserInput::_addEscapedControlCharToBuffer(buf, idx,
                ststpseqs.start_stop_sequence_pairs[i],
                strlen(ststpseqs.start_stop_sequence_pairs[i])),
            UserInput::_addEscapedControlCharToBuffer(buf, idx,
                ststpseqs.start_stop_sequence_pairs[i + 1],
                strlen(ststpseqs.start_stop_sequence_pairs[i + 1])));
    }
    free(buf); // cleanup
} // end listSettings
#endif // end ENABLE_listSettings

#if defined(ENABLE_listCommands) && defined(UI_VERBOSE) && defined(ENABLE_ui_out)

int UserInput::_linearSearch(_searchStruct& s)
{
    s.lsize--;
    if (s.lsize < 0)
    {
        return -1; // element not present
    }
    if (*s.sorted_ptr[s.lsize] == s.ls_value)
    {
        return s.lsize; // idx of value
    }
    return _linearSearch(s);
}

int UserInput::_linearMatrixSearch(_searchStruct& s, int& lmsize, uint8_t* lms_values)
{
    lmsize--;
    if (lmsize < 0)
    {
        return -1; // element not present
    }
    if (s.sort_array[mIndex(5, lmsize, 0)] == lms_values[0]
        && s.sort_array[mIndex(5, lmsize, 2)] == lms_values[1])
    {
        return lmsize; // idx of value
    }
    return _linearMatrixSearch(s, lmsize, lms_values);
}

bool UserInput::_sortSubcommands(_searchStruct& s, int& lmsize, uint8_t* lms_values)
{
    int _lmsize = lmsize;
    int sortidx = _linearMatrixSearch(s, _lmsize, lms_values);
    if (sortidx != -1)
    {
        s.ls_value = sortidx;
        s.lsize = s.sorted_idx;
        if (_linearSearch(s) != -1 && s.sorted_idx > 0) // load index already in sorted
        {
            if (sortidx > 0)
            {
                _lmsize = sortidx;
            }
            return _sortSubcommands(s, _lmsize, lms_values);
        }

        s.sorted_ptr[s.sorted_idx] = &s.sort_array[mIndex(5, sortidx, 4)];
        s.sorted_idx++;
        if (s.sort_array[mIndex(5, sortidx, 3)] > 0)
        {
            uint8_t lms_values[2] = {uint8_t(s.sort_array[mIndex(5, sortidx, 1)]),
                uint8_t(s.sort_array[mIndex(5, sortidx, 2)] + 1)};
            uint8_t sc_num = 1;

            while (sc_num < (s.sort_array[mIndex(5, sortidx, 3)]) + 1U)
            {
                _lmsize = s.cmd->param_array_len;
                sc_num++;
                _sortSubcommands(s, _lmsize, lms_values);
            }
            _lmsize = s.cmd->param_array_len;
            return _sortSubcommands(s, _lmsize, lms_values);
        }
        if (s.sorted_idx < s.cmd->param_array_len)
        {
            return _sortSubcommands(s, _lmsize, lms_values);
        }
    }
    if (s.sorted_idx >= s.cmd->param_array_len) // all sorted
    {
        return true;
    }
    else
    {
        return false;
    }
}

void UserInput::_printCommand(_searchStruct& s, uint8_t index)
{
    memcpy_P(&s.prm, &(s.cmd->prm[index]), sizeof(CommandParameters));
    if (s.prm.depth > 0)
    {
        if (s.prm.depth == s.prev_dp)
        {
            s.sc_num++;
        }
        else
        {
            s.prev_dp = s.prm.depth;
            s.sc_num = 1;
        }
        char indent[s.prm.depth + 1] = {'\0'};
        for (int j = 0; j < (nelems(indent)) - 1; ++j)
        {
            indent[j] = ' ';
        }
        UserInput::_ui_out(
            PSTR("    %s%02u> dp:%02u>.<%s>"), &indent, s.sc_num, s.prm.depth, &s.prm.command);
    }
    else
    {
        UserInput::_ui_out(PSTR("rt.<%s>"), &s.prm.command);
    }

    if (s.prm.max_num_args > 0)
    {
        UserInput::_ui_out(PSTR(".MIN_ARGS:%02u.<"), s.prm.num_args);
        for (uint8_t j = 0; j < s.prm.max_num_args; ++j)
        {
            char type_buffer[UI_INPUT_TYPE_STRINGS_PGM_LEN + 1] = {'\0'};
            memcpy_P(&type_buffer, &ihconst::type_strings[int(s.prm.arg_type_arr[j])],
                sizeof(type_buffer));
            UserInput::_ui_out(PSTR("%s"), &type_buffer);
            if (j < s.prm.max_num_args - 1)
            {
                UserInput::_ui_out(PSTR(", "));
            }
        }
        UserInput::_ui_out(PSTR(">\n"));
    }
    else
    {
        UserInput::_ui_out(PSTR(".<NO_ARGS>\n"));
    }
}

#endif

#if defined(ENABLE_listCommands) && defined(UI_VERBOSE) && defined(ENABLE_ui_out)
void UserInput::listCommands()
{
    if (!_begin_)
    {
        UserInput::_ui_out(PSTR("UserInput::begin() not declared.\n"));
        return;
    }
    IH_pname process_name;
    memcpy_P(&process_name, _input_prm_.process_name, sizeof(process_name));
    if (process_name[0] == _null_)
    {
        UserInput::_ui_out(PSTR("Commands available:\n"));
    }
    else
    {
        UserInput::_ui_out(PSTR("Commands available to %s:\n"), process_name);
    }
    CommandConstructor* cmd; // linked-list pointer
    // traverse linked list
    uint8_t i = 1;
    for (cmd = _commands_head_; cmd != NULL; cmd = cmd->next_command, ++i)
    {
        CommandParameters prm;
        uint8_t* sort_array = (uint8_t*)calloc((cmd->param_array_len * 5) + 1, sizeof(uint8_t));
        uint8_t** sorted_ptr = (uint8_t**)calloc(cmd->param_array_len + 1, sizeof(uint8_t*));
        uint8_t sorted_idx = 0;
        uint8_t ls_value = 0;
        uint8_t lms_values[2] = {0, 0};
        int lsize = 0;
        uint8_t prev_dp = 0;
        uint8_t sc_num = 0;
        _searchStruct s = {
            &(*cmd), prm, sort_array, sorted_ptr, sorted_idx, ls_value, lsize, prev_dp, sc_num};

        // load unsorted partial commands into array to be sorted
        for (uint8_t i = 0; i < cmd->param_array_len; ++i)
        {
            memcpy_P(&prm, &(cmd->prm[i]), sizeof(CommandParameters));
            sort_array[mIndex(5, i, 0)] = prm.parent_command_id;
            sort_array[mIndex(5, i, 1)] = prm.command_id;
            sort_array[mIndex(5, i, 2)] = prm.depth;
            sort_array[mIndex(5, i, 3)] = prm.sub_commands;
            sort_array[mIndex(5, i, 4)] = i;
        }

        // sort subcommands
        int lmsize = cmd->param_array_len;
        if (_sortSubcommands(s, lmsize, lms_values))
        {
            // print root and its subcommands
            UserInput::_ui_out(PSTR(" %02u> "), i);
            for (uint8_t i = 0; i < sorted_idx; ++i)
            {
                _printCommand(s, *s.sorted_ptr[i]);
            }
            UserInput::_ui_out(PSTR("\n"));
        }
        else
        {
            // print root
            UserInput::_ui_out(PSTR(" %02u> "), i);
            _printCommand(s, 0);
            if (s.prm.sub_commands > 0)
            {
                // warn user
                UserInput::_ui_out(PSTR("    Couldn't sort subcommands\n"));
            }
            else
            {
                UserInput::_ui_out(PSTR("\n"));
            }
        }
        free(sorted_ptr);
        free(sort_array);
    }

    UserInput::_ui_out(PSTR("end listCommands\n"));
} // end listCommands
#endif // end ENABLE_listCommands

void UserInput::readCommandFromBuffer(
    uint8_t* data, size_t len, const size_t num_zdc, const CommandParameters** zdc)
{
    // error checking
    if (!_begin_) // begin not set; allocation or implementation error
    {
        return;
    }
    if (len > UI_MAX_INPUT_LEN) // increase UI_MAX_INPUT_LEN error
    {
#if defined(__DEBUG_READCOMMANDFROMBUFFER__) && defined(ENABLE_ui_out)
        UserInput::_ui_out(PSTR(">%s$ERROR: input is too long.\n"),
            (char*)pgm_read_dword(_input_prm_.process_name));
#endif
        return;
    }
    _rcfbprm rprm; // this is passed by reference to child functions
    // initial settings
    rprm.launch_attempted = false;   // made it to launchFunction if true
    rprm.command_matched = false;    // error sentinel, true if error
    rprm.all_arguments_valid = true; // error sentinel, false if error
    rprm.subcommand_matched = false; // subcommand match flag, true on match
    rprm.cmd = NULL;                 // command parameters pointer (for loop linked-list iterator)
    rprm.all_wcc_cmd = NULL;         // all wcc cmd ptr, NULL if no all wcc cmd
    rprm.result = no_match;          // the result of UserInput::_compareCommandToString
    rprm.command_id = root;          // 16-bit command id starts at root
    rprm.idx = 0;                    // CommandParameters index
    rprm.all_wcc_idx = 0;            // index of all wcc CommandParameters
    rprm.input_len = len;            // input_len can change, len cannot
    rprm.token_buffer_len =
        rprm.input_len + 1U;  // the token buffer will always be at least one larger than input
    rprm.tokens_received = 0; // amount of delimiter separated tokens
    rprm.input_data = data;   // working pointer, can point at data or split_input
    rprm.split_input = NULL;  // split input will be NULL unless there are zero delim commands

    if (UserInput::_splitZDC(rprm, num_zdc, zdc))
    {
        rprm.input_data = rprm.split_input; // the input command and data have been split
    }

    _token_buffer_ = (char*)calloc(
        rprm.token_buffer_len, sizeof(char)); // place to chop up the input into tokens
    if (_token_buffer_ == NULL)               // if there was an error allocating the memory
    {
#if defined(__DEBUG_READCOMMANDFROMBUFFER__) && defined(ENABLE_ui_out)
        UserInput::_ui_out(PSTR(">%s$ERROR: cannot allocate ram for _token_buffer_.\n"),
            (char*)pgm_read_dword(_input_prm_.process_name));
#endif
        if (rprm.split_input != NULL) // error
        {
            free(rprm.split_input);
            rprm.split_input = NULL;
        }
        return;
    }
    // end error checking

    // getTokens parameters
    getTokensParam gtprm = {
        rprm.input_data,       // input data uint8_t array
        rprm.input_len,        // input len
        0,                     // data_pos
        _token_buffer_,        // pointer to char array, size of len + 1
        rprm.token_buffer_len, // the size of token_buffer
        0,                     // token_buffer_index
        _p_num_ptrs_,          // _data_pointers_[MAX], _data_pointers_index_[MAX]
        _data_pointers_index_, // index of token_buffer pointer array
        _data_pointers_,       // token_buffer pointers
        true,                  // point_to_beginning_of_token
        _null_,                // token_buffer sep char, _null_ == '\0'
    };
    // tokenize the input
    rprm.tokens_received = UserInput::getTokens(gtprm, _input_prm_);
    _data_pointers_index_max_ = rprm.tokens_received; // set index max to tokens received
    if (rprm.tokens_received == 0)                    // error condition
    {
        if (rprm.split_input != NULL)
        {
            free(rprm.split_input);
            rprm.split_input = NULL;
        }
        if (_token_buffer_ != NULL)
        {
            free(_token_buffer_);
            _token_buffer_ = NULL;
        }
#if defined(__DEBUG_READCOMMANDFROMBUFFER__) && defined(ENABLE_ui_out)
        UserInput::_ui_out(PSTR(">%s$ERROR: No tokens retrieved.\n"),
            (char*)pgm_read_dword(_input_prm_.process_name));
#endif
        return;
    } // end error condition

    for (rprm.cmd = _commands_head_; rprm.cmd != NULL;
         rprm.cmd = rprm.cmd->next_command) // iterate through CommandConstructor linked-list
    {
        rprm.result = UserInput::_compareCommandToString(
            rprm.cmd, 0, _data_pointers_[0]); // compare the root command to the first token
        if (rprm.result == match)
        {
            break; // break command iterator for loop
        }
        if (rprm.all_wcc_cmd == NULL
            && rprm.result == match_all_wcc_cmd) // remember first all wcc cmd
        {
            rprm.all_wcc_cmd = rprm.cmd;
        }
    } // end root command for loop

    if (rprm.result != match
        && rprm.all_wcc_cmd
            != NULL) // if there was not a "match" but we found an all wcc command (this makes all
                     // wcc commands lower priority than a regular match)
    {
        rprm.result = match_all_wcc_cmd; // set result to all wcc
        rprm.cmd = rprm.all_wcc_cmd;     // point to the all wcc CommandConstructor
    }

    if (rprm.result >= match_all_wcc_cmd) // match root command
    {
        memcpy_P(&rprm.prm, &(rprm.cmd->prm[0]),
            sizeof(rprm.prm)); // move CommandParameters variables from PROGMEM to sram for work
        _current_search_depth_ = 1; // start searching for subcommands at depth 1
        _data_pointers_index_ = 1; // index 1 of _data_pointers_ is the token after the root command
        rprm.command_matched = true; // root command match flag
        _failed_on_subcommand_ = 0;  // subcommand error index
        rprm.result = no_match;      // UI_COMPARE input/command compare result
        rprm.all_wcc_cmd = NULL;

        UserInput::_launchLogic(rprm); // see if command has any subcommands, validate input types,
                                       // try to launch function
    }                                  // end command logic

    if (!rprm.launch_attempted
        && _default_function_
            != NULL) // if there was no command match and a default function is configured
    {
#if defined(ENABLE_readCommandFromBufferErrorOutput)
        UserInput::_readCommandFromBufferErrorOutput(rprm); // error output function
#endif                               // end ENABLE_readCommandFromBufferErrorOutput
        (*_default_function_)(this); // run the default function
    }

    // cleanup
    for (size_t i = 0; i < _p_num_ptrs_; ++i)
    {
        _data_pointers_[i] = NULL; // reinit _data_pointers_
    }
    if (rprm.split_input != NULL)
    {
        free(rprm.split_input);
        rprm.split_input = NULL;
    }
    if (_token_buffer_ != NULL)
    {
        free(_token_buffer_);
        _token_buffer_ = NULL;
    }
} // end readCommandFromBuffer

#if defined(ENABLE_getCommandFromStream)
void UserInput::getCommandFromStream(
    Stream& stream, size_t rx_buffer_size, const size_t num_zdc, const CommandParameters** zdc)
{
    if (!_begin_) // error
    {
        return;
    }
    if (_stream_buffer_allocated_ == false)
    {
        _stream_data_ = (uint8_t*)calloc(
            rx_buffer_size, sizeof(uint8_t)); // an array to store the received data
        if (_stream_data_ == NULL)            // if there was an error allocating the memory
        {
    #if defined(__DEBUG_GETCOMMANDFROMSTREAM__) && defined(ENABLE_ui_out)
            UserInput::_ui_out(PSTR(">%s$ERROR: _stream_data_ alloc fail\n"),
                (char*)pgm_read_dword(_input_prm_.process_name));
    #endif
            return;
        }
        _stream_buffer_allocated_ = true;
        _term_index_ = 0;
    }
    char* rc = (char*)_stream_data_; // point rc to allocated memory
    while (stream.available() > 0 && _new_stream_data_ == false)
    {
        IH_eol eol;
        memcpy_P(&eol, _input_prm_.eol_char, sizeof(eol));
        rc[_stream_data_index_] = stream.read();
        if (rc[_stream_data_index_] == eol[_term_index_])
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
        UserInput::readCommandFromBuffer(_stream_data_, _stream_data_index_, num_zdc, zdc);
        _stream_data_index_ = 0;
        _new_stream_data_ = false;
        free(_stream_data_);
        _stream_buffer_allocated_ = false;
    }
} // end getCommandFromStream
#endif // end ENABLE_getCommandFromStream

#if defined(ENABLE_nextArgument)
char* UserInput::nextArgument()
{
    if (_data_pointers_index_ < (_max_depth_ + _max_args_)
        && _data_pointers_index_ < _data_pointers_index_max_)
    {
        _data_pointers_index_++;
        return _data_pointers_[_data_pointers_index_];
    }
    return NULL; // else return NULL
} // end nextArgument
#endif // end ENABLE_nextArgument

#if defined(ENABLE_getArgument)
char* UserInput::getArgument(size_t argument_number)
{
    if (argument_number < (_max_depth_ + _max_args_) && argument_number < _data_pointers_index_max_)
    {
        return _data_pointers_[argument_number];
    }
    return NULL; // else return NULL
} // end getArgument
#endif // end ENABLE_getArgument

#if defined(ENABLE_outputIsAvailable)
size_t UserInput::outputIsAvailable()
{
    return _output_buffer_len_ - _output_buffer_bytes_left_;
} // end outputIsAvailable
#endif // end ENABLE_outputIsAvailable

#if defined(ENABLE_outputIsEnabled)
inline bool UserInput::outputIsEnabled() { return _output_enabled_; } // end outputIsEnabled
#endif                                                                // end ENABLE_outputIsEnabled

#if defined(ENABLE_outputToStream)
void UserInput::outputToStream(Stream& stream)
{
    if (_output_flag_) // if there's something to print
    {
        stream.println(_output_buffer_); // print output_buffer, which is formatted into a string by
                                         // UserInput's methods
        UserInput::clearOutputBuffer();
    }
} // end outputToStream
#endif // end ENABLE_outputToStream

#if defined(ENABLE_clearOutputBuffer)
inline void UserInput::clearOutputBuffer(bool overwrite_contents)
{
    if (_output_enabled_)
    {
        _output_buffer_bytes_left_ = _output_buffer_len_; //  reset output_buffer's index
        if (!overwrite_contents)
        {
            _output_buffer_[0] = _null_; // soft reinit _output_buffer_
        }
        else
        {
            for (size_t i = 0; i < _output_buffer_len_; ++i)
            {
                _output_buffer_[i] = _null_; // overwrite buffer contents
            }
        }
    }
    _output_flag_ = false;
} // end clearOutputBuffer
#endif // end ENABLE_clearOutputBuffer

size_t UserInput::getTokens(getTokensParam& gtprm, const InputProcessParameters& input_prm)
{
    gtprm.token_pointer_index = 0; // and the token pointer index to zero

    while (gtprm.data_pos < gtprm.len)
    {
        UserInput::_getTokensDelimiters(gtprm, input_prm);
        UserInput::_getTokensStartStop(gtprm, input_prm);
        UserInput::_getTokensChar(gtprm, input_prm);
    }
    return gtprm.token_pointer_index;
} // end getTokens

inline bool UserInput::validateNullSepInput(validateNullSepInputParam& vprm)
{
    size_t strlen_data = strlen(vprm.token_pointers[vprm.token_pointer_index]);
    size_t start =
        ((char)vprm.token_pointers[vprm.token_pointer_index][0] == vprm.neg_sign) ? 1 : 0;
    if (vprm.arg_type
        <= UITYPE::FLOAT) // for unsigned integers, integers, and floating point numbers
    {
        size_t found_dot = 0;
        size_t num_digits = 0;
        size_t not_digits = 0;
        if (vprm.arg_type < UITYPE::INT16_T && start == 1) // error
        {
            return false; // uint cannot be negative
        }
        for (size_t j = start; j < strlen_data; ++j)
        {
            if (vprm.token_pointers[vprm.token_pointer_index][j] == vprm.float_sep)
            {
                found_dot++;
            }
            else if (isdigit(vprm.token_pointers[vprm.token_pointer_index][j]) == true)
            {
                num_digits++;
            }
            else
            {
                not_digits++;
            }
        }
        // int/uint error test
        if (vprm.arg_type <= UITYPE::INT16_T
            && (found_dot > 0U || not_digits > 0U || (num_digits + start) != strlen_data))
        {
            return false;
        }
        // float error test
        if (vprm.arg_type == UITYPE::FLOAT
            && (found_dot > 1U || not_digits > 0U
                || (num_digits + found_dot + start) != strlen_data))
        {
            return false;
        }
        return true; // no errors
    }

    if (vprm.arg_type == UITYPE::CHAR || vprm.arg_type == UITYPE::START_STOP) // char and start/stop
    {
        if (vprm.arg_type == UITYPE::CHAR && strlen_data > 1) // error
        {
            return false; // looking for a single char value, not a c-string
        }
        for (size_t j = 0; j < strlen_data; ++j)
        { // if we encounter anything that isn't one of these four things, something isn't right
            int test_bool[4] = {isprint(vprm.token_pointers[vprm.token_pointer_index][j]),
                ispunct(vprm.token_pointers[vprm.token_pointer_index][j]),
                iscntrl(vprm.token_pointers[vprm.token_pointer_index][j]),
                isdigit(vprm.token_pointers[vprm.token_pointer_index][j])};
            if (test_bool[0] == 0 && test_bool[1] == 0 && test_bool[2] == 0
                && test_bool[3] == 0) // no match
            {
                return false;
            }
        }
        return true;
    }

    // no type specified
    if (vprm.arg_type == UITYPE::NOTYPE)
    {
        return true; // no type validation performed
    }

    return false; // error, unknown type
} // end validateNullSepInput

/*
    private methods
*/
#if defined(ENABLE_ui_out)
void UserInput::_ui_out(const char* fmt, ...)
{
    if (_output_enabled_)
    {
        va_list args;        // ... parameter pack list
        va_start(args, fmt); // set the parameter pack list index here
        int err = vsnprintf_P(
            _output_buffer_ + abs((int)_output_buffer_bytes_left_ - (int)_output_buffer_len_),
            _output_buffer_bytes_left_, fmt, args);
        va_end(args);                               // we are done with the parameter pack
        if (err > (long)_output_buffer_bytes_left_) // overflow condition
        {
            UserInput::clearOutputBuffer(true);
            // attempt warn
            snprintf_P(_output_buffer_, _output_buffer_len_,
                PSTR("Increase output buffer to %d bytes.\n"),
                (abs(err - (int)_output_buffer_bytes_left_) + (int)_output_buffer_len_));
            _output_flag_ = true;
            return;
        }
        else if (err < 0) // encoding error
        {
            UserInput::clearOutputBuffer(true);
            // attempt warn
            snprintf_P(_output_buffer_, _output_buffer_len_, PSTR("Encoding error.\n"));
            _output_flag_ = true;
            return;
        }
        else // normal condition
        {
            _output_buffer_bytes_left_ -= err; // decrement amount of bytes left in buffer
        }
        _output_flag_ = true; // output is available
    }
} // end _ui_out
#endif

#if defined(ENABLE_readCommandFromBufferErrorOutput) && defined(ENABLE_ui_out)
void UserInput::_readCommandFromBufferErrorOutput(_rcfbprm& rprm)
{
    #if defined(UI_VERBOSE)
    if (_output_enabled_) // format a string with useful information
    {
        IH_pname process_name;
        memcpy_P(&process_name, _input_prm_.process_name, sizeof(process_name));
        UserInput::_ui_out(PSTR(">%s$Invalid input: "), process_name);
        if (rprm.command_matched == true)
        {
            memcpy_P(&rprm.prm, &(rprm.cmd->prm[_failed_on_subcommand_]),
                sizeof(rprm.prm)); // only load if a command matched
            // constrain err_n_args to UI_MAX_ARGS + 1
            size_t err_n_args = ((_data_pointers_index_max_ - _failed_on_subcommand_ - 1U)
                                    > (UI_MAX_ARGS_PER_COMMAND + 1))
                ? (UI_MAX_ARGS_PER_COMMAND + 1)
                : (_data_pointers_index_max_ - _failed_on_subcommand_ - 1U);
            err_n_args = (err_n_args == 0 && rprm.prm.num_args > 0) ? 1 : err_n_args;
            if (err_n_args > 0)
            {
                for (size_t i = 0; i < (_failed_on_subcommand_ + 1U); ++i)
                {
                    UserInput::_ui_out(PSTR("%s "), _data_pointers_[i]); // add subcommands to echo
                }
                UserInput::_ui_out(PSTR("\n"));
                bool print_subcmd_err = true;
                for (size_t i = 0; i < rprm.prm.max_num_args; ++i)
                {
                    if (_input_type_match_flags_[i] == false
                        || _data_pointers_[1 + _failed_on_subcommand_ + i] == NULL)
                    {
                        uint8_t _type = (uint8_t)UserInput::_getArgType(rprm.prm, i);
                        char _type_char_array[UI_INPUT_TYPE_STRINGS_PGM_LEN];
                        memcpy_P(&_type_char_array, &ihconst::type_strings[_type],
                            sizeof(_type_char_array));
                        if ((UITYPE)_type != UITYPE::NO_ARGS
                            && _data_pointers_[1 + _failed_on_subcommand_ + i] == NULL)
                        {
                            UserInput::_ui_out(
                                PSTR(" 'INPUT NOT RECEIVED'*(%s REQUIRED)\n"), _type_char_array);
                        }
                        else
                        {
                            if (rprm.prm.sub_commands > 0 && print_subcmd_err == true)
                            {
                                print_subcmd_err = false;
                                UserInput::_ui_out(PSTR(" '%s'*(ENTER VALID SUBCOMMAND)\n"),
                                    _data_pointers_[1 + _failed_on_subcommand_ + i]);
                            }
                            else if ((rprm.prm.sub_commands == 0 || err_n_args > 1)
                                && (UITYPE)_type == UITYPE::NO_ARGS)
                            {
                                UserInput::_ui_out(PSTR(" '%s'*(LEAVE BLANK)\n"),
                                    _data_pointers_[1 + _failed_on_subcommand_ + i]);
                            }
                            else
                            {
                                UserInput::_ui_out(PSTR(" '%s'*(%s)\n"),
                                    _data_pointers_[1 + _failed_on_subcommand_ + i],
                                    _type_char_array);
                            }
                        }
                    }
                    else
                    {
                        UserInput::_ui_out(PSTR(" '"));
                        size_t strlen_data =
                            strlen(_data_pointers_[1 + _failed_on_subcommand_ + i]);
                        for (size_t j = 0; j < strlen_data; ++j)
                        {
                            if (iscntrl(_data_pointers_[1 + _failed_on_subcommand_ + i]
                                                       [j])) // format buffer with escaped char
                            {
                                char buf[UI_ESCAPED_CHAR_STRLEN] {};
                                UserInput::_ui_out(PSTR("%s"),
                                    UserInput::_escapeCharactersSoTheyPrint(
                                        _data_pointers_[1 + _failed_on_subcommand_ + i][j], buf));
                            }
                            else
                            {
                                UserInput::_ui_out(PSTR("%c"),
                                    _data_pointers_[1 + _failed_on_subcommand_ + i]
                                                   [j]); // single char
                            }
                        }
                        UserInput::_ui_out(PSTR("'(OK)\n"));
                    }
                }
                return;
            }
    #endif // end UI_VERBOSE
           // this is the library output with UI_ECHO_ONLY defined
            UserInput::_ui_out(PSTR("%s\n"), (char*)rprm.input_data);
    #if defined(UI_VERBOSE)
            return;
        }
        else // command not matched
        {
            UserInput::_ui_out(
                PSTR("%s\n command <%s> unknown\n"), (char*)rprm.input_data, _data_pointers_[0]);
        }
    }
    #endif // end UI_VERBOSE
} // end _readCommandFromBufferErrorOutput
#endif // end ENABLE_readCommandFromBufferErrorOutput

// clang-format off
inline void UserInput::_launchFunction(_rcfbprm& rprm, const IH_pname& process_name)
{   
    #if defined(UI_VERBOSE)
    if (_output_enabled_)
    {
        #if defined(ENABLE_ui_out)
        UserInput::_ui_out(PSTR(">%s$"), process_name);
        #endif
        for (size_t i = 0; i < _data_pointers_index_max_; ++i)
        {
            size_t strlen_data = strlen(_data_pointers_[i]);
            for (size_t j = 0; j < strlen_data; ++j)
            {
                if (iscntrl(_data_pointers_[i][j])) // format buffer with escaped char
                {
                    char buf[UI_ESCAPED_CHAR_STRLEN] {};
                    #if defined(ENABLE_ui_out)
                    UserInput::_ui_out(PSTR("%s"), UserInput::_escapeCharactersSoTheyPrint(_data_pointers_[i][j], buf));
                    #endif
                }
                else
                {
                    #if defined(ENABLE_ui_out)
                    UserInput::_ui_out(PSTR("%c"), _data_pointers_[i][j]); // single char
                    #endif
                }
            }
            #if defined(ENABLE_ui_out)
            UserInput::_ui_out(PSTR(" ")); // add a space
            #endif
        }
        #if defined(ENABLE_ui_out)
        UserInput::_ui_out(PSTR("\n"));
        #endif
    }
    #endif // UI_VERBOSE
    _data_pointers_index_ = _current_search_depth_ - 1;

    if (rprm.prm.function != NULL)
    {
        #if defined(__DEBUG_LAUNCH_FUNCTION__) && defined(ENABLE_ui_out)
        UserInput::_ui_out(PSTR(">%s$_launchFunction: launch command_id %u\n"), process_name, rprm.prm.command_id);
        #endif
        rprm.prm.function(this);
    }
    else
    {
        memcpy_P(&rprm.prm, &(rprm.cmd->prm[0]), sizeof(rprm.prm));
        #if defined(__DEBUG_LAUNCH_FUNCTION__) && defined(ENABLE_ui_out)
        UserInput::_ui_out(PSTR(">%s$_launchFunction: launch command_id %u\n"), process_name, rprm.prm.command_id);
        #endif
        rprm.prm.function(this);
    }
} // end _launchFunction

void UserInput::_launchLogic(_rcfbprm& rprm)
{
    IH_pname process_name;
    memcpy_P(&process_name, _input_prm_.process_name, sizeof(process_name));        
    if (rprm.tokens_received > 1 && rprm.prm.sub_commands == 0 && rprm.prm.max_num_args == 0) // error
    {
        #if defined(__DEBUG_LAUNCH_LOGIC__) && defined(ENABLE_ui_out)        
        UserInput::_ui_out(PSTR(">%s$launchLogic: too many tokens for command_id %u\n"), process_name, rprm.prm.command_id);
        #endif
        return;
    }            
    if ((rprm.subcommand_matched == false && rprm.tokens_received == 1 && rprm.prm.max_num_args == 0) // command with no arguments
        || (rprm.tokens_received == 1 && _current_search_depth_ > 1 && rprm.subcommand_matched == true && rprm.prm.max_num_args == 0)) // subcommand with no arguments
    {
        #if defined(__DEBUG_LAUNCH_LOGIC__) && defined(ENABLE_ui_out)
        UserInput::_ui_out(PSTR(">%s$launchLogic: launchFunction command_id %u\n"), process_name, rprm.prm.command_id);
        #endif

        rprm.launch_attempted = true; // don't run default callback
        UserInput::_launchFunction(rprm, process_name); // launch the matched command
        return;
    }    

    if ((rprm.subcommand_matched == false && rprm.tokens_received > 1 && rprm.prm.max_num_args > 0) // command with arguments, potentially has subcommands but none were entered
        || (_current_search_depth_ == (rprm.prm.depth + 1) && rprm.tokens_received > 1 && rprm.prm.max_num_args > 0 && rprm.prm.sub_commands == 0)) // command with arguments (max depth)
    {
        UserInput::_getArgs(rprm);
        if (_rec_num_arg_strings_ >= rprm.prm.num_args && _rec_num_arg_strings_ <= rprm.prm.max_num_args && rprm.all_arguments_valid == true)
        {
            #if defined(__DEBUG_LAUNCH_LOGIC__) && defined(ENABLE_ui_out)
            UserInput::_ui_out(PSTR(">%s$launchLogic: launchFunction command_id %u\n"), process_name, rprm.prm.command_id);
            #endif
            rprm.launch_attempted = true;                                                      // don't run default callback
            UserInput::_launchFunction(rprm, process_name); // launch the matched command
        }
        return; // if !match, error
    }    

    // subcommand search
    rprm.subcommand_matched = false;       
    if (_current_search_depth_ <= (rprm.cmd->tree_depth))             // dig starting at depth 1
    {                                                                  // this index starts at one because the parameter array's first element will be the root command        
        #if defined(__DEBUG_SUBCOMMAND_SEARCH__) && defined(ENABLE_ui_out)
        UserInput::_ui_out(PSTR(">%s$launchLogic: search depth (%d)\n"), process_name, _current_search_depth_);
        #endif
        rprm.result = no_match;
        rprm.all_wcc_cmd = NULL;
        rprm.idx = 0;
        rprm.all_wcc_idx = 0;        
        for (size_t j = 1; j < (rprm.cmd->param_array_len + 1U); ++j) // through the parameter array
        {
            if (rprm.tokens_received == 1) // pointer index protection
            {
                break;
            }
            
            rprm.result = UserInput::_compareCommandToString(rprm.cmd, j, _data_pointers_[_data_pointers_index_]);
            if (rprm.result == match)
            {
                rprm.idx = j;
                break; // break command iterator for loop
            }
            if (rprm.all_wcc_cmd == NULL && rprm.result == match_all_wcc_cmd)
            {
                rprm.all_wcc_idx = j;
                rprm.all_wcc_cmd = rprm.cmd;
            }
        }        

        if (rprm.result != match && rprm.all_wcc_cmd != NULL)
        {
            rprm.result = match_all_wcc_cmd;
            rprm.cmd = rprm.all_wcc_cmd;
            rprm.idx = rprm.all_wcc_idx;
        }
            
        if (rprm.result >= match_all_wcc_cmd) // match subcommand string
        {                
            memcpy_P(&rprm.prm, &(rprm.cmd->prm[rprm.idx]), sizeof(rprm.prm));
            if (rprm.prm.depth == _current_search_depth_ && rprm.prm.parent_command_id == rprm.command_id)
            {
                #if defined(__DEBUG_SUBCOMMAND_SEARCH__) && defined(ENABLE_ui_out)
                UserInput::_ui_out(PSTR(">%s$launchLogic: subcommand (%s) match, command_id (%u), (%d) subcommands, max_num_args (%d)\n"), process_name, rprm.prm.command, rprm.prm.command_id, rprm.prm.sub_commands, rprm.prm.max_num_args);
                #endif
                if (rprm.tokens_received > 0) // subcommand matched
                {
                    rprm.tokens_received--; // subtract subcommand from tokens received
                    _data_pointers_index_++; // increment to the next token
                }
                rprm.command_id = rprm.prm.command_id; // set command_id to matched subcommand
                rprm.subcommand_matched = true;         // subcommand matched
                _failed_on_subcommand_ = rprm.idx;      // set error index                
            }
        }
        
        if (_current_search_depth_ < (rprm.cmd->tree_depth))
        {
            _current_search_depth_++;
        }
    }                                     // end subcommand search
    if (rprm.subcommand_matched == true) // recursion
    {
        #if defined(__DEBUG_SUBCOMMAND_SEARCH__) && defined(ENABLE_ui_out)
        UserInput::_ui_out(PSTR(">%s$launchLogic: launchLogic recurse, command_id (%u)\n"), process_name, rprm.prm.command_id);
        #endif
        UserInput::_launchLogic(rprm);
    }
} // end _launchLogic

inline char *UserInput::_escapeCharactersSoTheyPrint(char input, char *buf)
{
    if (input < (char)32 || input == (char)34)
    {
        buf[0] = (char)92; // (char)92 == '\\'
        switch (input)
        {
            case (char)'\0':{buf[1] = '0'; break;}
            case (char)'\a':{buf[1] = 'a'; break;}
            case (char)'\b':{buf[1] = 'b'; break;}
            case (char)'\t':{buf[1] = 't'; break;}
            case (char)'\n':{buf[1] = 'n'; break;}
            case (char)'\v':{buf[1] = 'v'; break;}
            case (char)'\f':{buf[1] = 'f'; break;}
            case (char)'\r':{buf[1] = 'r'; break;}
            case (char)'\e':{buf[1] = 'e'; break;}
            case (char)'\"':{buf[1] = '"'; break;}
            default: break;
        }
        buf[2] = _null_; // terminate
        return buf;
    }
    buf[0] = input;  // pass through input
    buf[1] = _null_; // terminate the string
    return buf;      // not a control char
} // end _escapeCharactersSoTheyPrint

inline char UserInput::_combineControlCharacters(char input)
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
} // end _combineControlCharacters
// clang-format on

bool UserInput::_addCommandAbort(CommandConstructor& cmd, CommandParameters& prm)
{
    bool error_not = true;
    size_t cmd_len = strlen(prm.command);

    if (prm.function == NULL && prm.depth == 0)
    {
#if defined(ENABLE_ui_out) && defined(UI_VERBOSE)
        UserInput::_ui_out(
            PSTR("command <%s> root command function pointer cannot be NULL\n"), prm.command);
#endif
        error_not = false;
    }

    if (prm.has_wildcards == true)
    {
        size_t num_wcc = 0;
        IH_wcc wcc;
        memcpy_P(&wcc, _input_prm_.wildcard_char, sizeof(wcc));
        for (size_t i = 0; i < cmd_len; ++i)
        {
            if (prm.command[i] == wcc[0])
            {
                num_wcc++;
            }
        }
        if (num_wcc == 0)
        {
#if defined(ENABLE_ui_out) && defined(UI_VERBOSE)
            UserInput::_ui_out(PSTR("command <%s> has_wildcard is set, but no wildcards were found "
                                    "in the command\n"),
                prm.command);
#endif
            error_not = false;
        }
    }

    if (cmd_len > UI_MAX_CMD_LEN)
    {
#if defined(ENABLE_ui_out) && defined(UI_VERBOSE)
        UserInput::_ui_out(PSTR("command <%s> command too long, increase UI_MAX_CMD_LEN or reduce "
                                "command length.\n"),
            prm.command);
#endif
        error_not = false;
    }
    if (cmd_len != prm.command_length)
    {
        if (cmd_len > prm.command_length)
        {
#if defined(ENABLE_ui_out) && defined(UI_VERBOSE)
            UserInput::_ui_out(
                PSTR("command <%s> command_length too large for command\n"), prm.command);
#endif
        }
        else
        {
#if defined(ENABLE_ui_out) && defined(UI_VERBOSE)
            UserInput::_ui_out(
                PSTR("command <%s> command_length too small for command\n"), prm.command);
#endif
        }
        error_not = false;
    }
    if (prm.depth > UI_MAX_TREE_DEPTH_PER_COMMAND)
    {
#if defined(ENABLE_ui_out) && defined(UI_VERBOSE)
        UserInput::_ui_out(PSTR("command <%s> depth exceeds UI_MAX_DEPTH\n"), prm.command);
#endif
        error_not = false;
    }
    if (prm.sub_commands > UI_MAX_NUM_CHILD_COMMANDS)
    {
#if defined(ENABLE_ui_out) && defined(UI_VERBOSE)
        UserInput::_ui_out(
            PSTR("command <%s> sub_commands exceeds UI_MAX_SUBCOMMANDS\n"), prm.command);
#endif
        error_not = false;
    }
    if (prm.num_args > UI_MAX_ARGS_PER_COMMAND)
    {
#if defined(ENABLE_ui_out) && defined(UI_VERBOSE)
        UserInput::_ui_out(PSTR("command <%s> num_args exceeds UI_MAX_ARGS\n"), prm.command);
#endif
        error_not = false;
    }
    if (prm.max_num_args > UI_MAX_ARGS_PER_COMMAND)
    {
#if defined(ENABLE_ui_out) && defined(UI_VERBOSE)
        UserInput::_ui_out(PSTR("command <%s> max_num_args exceeds UI_MAX_ARGS\n"), prm.command);
#endif
        error_not = false;
    }
    if (prm.num_args > prm.max_num_args)
    {
#if defined(ENABLE_ui_out) && defined(UI_VERBOSE)
        UserInput::_ui_out(
            PSTR("command <%s> num_args must be less than max_num_args\n"), prm.command);
#endif
        error_not = false;
    }
    if (error_not == false) // error condition
    {
#if defined(ENABLE_ui_out) && defined(UI_VERBOSE)
        UserInput::_ui_out(PSTR("<%s> CommandParameters error! Root <%s> command tree rejected!\n"),
            prm.command, prm.command);
#endif
    }
    return error_not;
} // end _addCommandAbort

// clang-format off
inline UITYPE UserInput::_getArgType(CommandParameters &prm, size_t index)
{
    if (prm.argument_flag == UI_ARG_HANDLING::no_args) return UITYPE::NO_ARGS;
    if (prm.argument_flag == UI_ARG_HANDLING::one_type) return prm.arg_type_arr[0];
    if (prm.argument_flag == UI_ARG_HANDLING::type_arr) return prm.arg_type_arr[index];

    return UITYPE::_LAST; // return error if no match
} // end _getArgType
// clang-format on

void UserInput::_getArgs(_rcfbprm& rprm)
{
    _rec_num_arg_strings_ = 0; // number of tokens read from data
    for (size_t i = 0; i < (rprm.tokens_received - 1U); ++i)
    {
        validateNullSepInputParam vprm = {UserInput::_getArgType(rprm.prm, i), _data_pointers_,
            _data_pointers_index_ + i, _neg_, _dot_};
        _input_type_match_flags_[i] = UserInput::validateNullSepInput(vprm); // validate the token
        _rec_num_arg_strings_++;
        if (_input_type_match_flags_[i] == false) // if the token was not valid input
        {
            rprm.all_arguments_valid = false; // set the error sentinel
        }
    }
} // end _getArgs

char* UserInput::_addEscapedControlCharToBuffer(
    char* buf, size_t& idx, const char* input, size_t input_len)
{
    char* start = &buf[idx];
    char tmp_esc_chr[UI_ESCAPED_CHAR_STRLEN] {};
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
} // end _addEscapedControlCharToBuffer

inline void UserInput::_getTokensDelimiters(
    getTokensParam& gtprm, const InputProcessParameters& input_prm)
{
    InputProcessDelimiterSequences delimseq;
    memcpy_P(&delimseq, input_prm.delimiter_sequences, sizeof(delimseq));
    bool found_delimiter_sequence = false;
    bool match = false; // match delimiter sequence sentinel
    do                  // skip over delimiters; do-while loops iterate at least once
    {
        match = false;
        for (size_t i = 0; i < delimseq.num_seq; ++i)
        {
            if (delimseq.delimiter_sequences[i][0] == (char)gtprm.data[gtprm.data_pos])
            {
                if (delimseq.delimiter_lens[i] > 1U)
                {
                    char* ptr = (char*)&gtprm.data[gtprm.data_pos];
                    if (memcmp(ptr, delimseq.delimiter_sequences[i], delimseq.delimiter_lens[i])
                        == 0) // match
                    {
                        gtprm.data_pos += delimseq.delimiter_lens[i] + 1U;
                        match = true;
                        break;
                    }
                }
                else // match
                {
                    gtprm.data_pos++;
                    match = true;
                    break; // break for loop
                }
            }
        }
        if (match == true)
        {
            found_delimiter_sequence = true;
        }
    } while (match == true); // end do-while loop
    if (found_delimiter_sequence == true && (gtprm.data_pos + _term_len_ < gtprm.len))
    {
        gtprm.point_to_beginning_of_token = true;
        gtprm.token_buffer[gtprm.token_buffer_index] = gtprm.token_buffer_sep;
        gtprm.token_buffer_index++;
    }
} // end _getTokensDelimiters

inline void UserInput::_getTokensStartStop(
    getTokensParam& gtprm, const InputProcessParameters& input_prm)
{
    InputProcessStartStopSequences start_stop_sequences {};
    memcpy_P(&start_stop_sequences, input_prm.start_stop_sequences, sizeof(start_stop_sequences));
    if (start_stop_sequences.start_stop_sequence_pairs[0] != NULL
        && start_stop_sequences.start_stop_sequence_pairs[0][0] == (char)gtprm.data[gtprm.data_pos])
    {
        for (size_t i = 0; i < start_stop_sequences.num_seq; ++i)
        {
            if (start_stop_sequences.start_stop_sequence_lens[i] > 1U
                || start_stop_sequences.start_stop_sequence_lens[i + 1] > 1U)
            {
                char* ptr = (char*)&gtprm.data[gtprm.data_pos];
                if (memcmp(ptr, start_stop_sequences.start_stop_sequence_pairs[i],
                        start_stop_sequences.start_stop_sequence_lens[i])
                    == 0) // match
                {
                    gtprm.data_pos += start_stop_sequences.start_stop_sequence_lens[i] + 1U;
                    ptr = (char*)&gtprm.data[gtprm.data_pos]; // point to beginning of c-string
                    char* end_ptr =
                        (char*)memchr(ptr, start_stop_sequences.start_stop_sequence_pairs[i + 1][0],
                            (gtprm.len - gtprm.data_pos)); // search for next c-string delimiter
                    while (end_ptr != NULL || gtprm.data_pos < gtprm.len)
                    {
                        if (memcmp(end_ptr, start_stop_sequences.start_stop_sequence_pairs[i + 1],
                                start_stop_sequences.start_stop_sequence_lens[i + 1])
                            == 0) // match end sequence
                        {
                            size_t size = ((end_ptr - (char*)gtprm.data)
                                - (ptr - (char*)gtprm.data)); // memcpy c-string to token buffer
                            if ((size + 1U) < (gtprm.len - gtprm.data_pos))
                            {
                                memcpy(gtprm.token_buffer + gtprm.token_buffer_index, ptr, size);
                                gtprm.token_pointers[gtprm.token_pointer_index] =
                                    &gtprm.token_buffer[gtprm.token_buffer_index];
                                gtprm.token_pointer_index++;
                                gtprm.token_buffer_index += size + 1U;
                                gtprm.token_buffer[gtprm.token_buffer_index] =
                                    gtprm.token_buffer_sep;
                                gtprm.token_buffer_index++;
                                gtprm.data_pos += size + 1U;
                            }
                            break;
                        }
                        else
                        {
                            end_ptr = (char*)memchr(end_ptr,
                                start_stop_sequences.start_stop_sequence_pairs[i + 1][0],
                                (gtprm.len - gtprm.data_pos));
                            gtprm.data_pos += end_ptr - (char*)gtprm.data;
                        }
                    }
                }
            }
            else // match
            {
                gtprm.data_pos++;
                char* ptr = (char*)&gtprm.data[gtprm.data_pos]; // point to beginning of c-string
                char* end_ptr =
                    (char*)memchr(ptr, start_stop_sequences.start_stop_sequence_pairs[i + 1][0],
                        (gtprm.len - gtprm.data_pos)); // search for next c-string delimiter
                if (end_ptr != NULL)                   // memcpy
                {
                    size_t size = ((end_ptr - (char*)gtprm.data) - (ptr - (char*)gtprm.data));
                    if ((size + 1U) < (gtprm.len - gtprm.data_pos))
                    {
                        memcpy(gtprm.token_buffer + gtprm.token_buffer_index, ptr, size);
                        gtprm.token_pointers[gtprm.token_pointer_index] =
                            &gtprm.token_buffer[gtprm.token_buffer_index];
                        gtprm.token_pointer_index++;
                        gtprm.token_buffer_index += size + 1U;
                        gtprm.token_buffer[gtprm.token_buffer_index] = gtprm.token_buffer_sep;
                        gtprm.token_buffer_index++;
                        gtprm.data_pos += size + 1U;
                    }
                }
            }
        }
    }
} // end _getTokensStartStop

void UserInput::_getTokensChar(getTokensParam& gtprm, const InputProcessParameters& input_prm)
{
    IH_input_cc input_control_char_sequence;
    memcpy_P(&input_control_char_sequence, input_prm.input_control_char_sequence,
        sizeof(input_control_char_sequence));
    if ((char)gtprm.data[gtprm.data_pos] == input_control_char_sequence[0]
        && (char)gtprm.data[gtprm.data_pos + 1U] == input_control_char_sequence[1]
        && (gtprm.data_pos + 3U < gtprm.len))
    {
        if (gtprm.point_to_beginning_of_token)
        {
            gtprm.token_pointers[gtprm.token_pointer_index] =
                &gtprm.token_buffer[gtprm.token_buffer_index];
            gtprm.token_pointer_index++;
            gtprm.point_to_beginning_of_token = false;
        }
        if (UserInput::_combineControlCharacters((char)gtprm.data[gtprm.data_pos + 2U])
            == '*') // error
        {
            gtprm.token_buffer[gtprm.token_buffer_index] = input_control_char_sequence[0];
            gtprm.token_buffer[gtprm.token_buffer_index + 1] = input_control_char_sequence[1];
            gtprm.token_buffer[gtprm.token_buffer_index + 2] =
                UserInput::_combineControlCharacters((char)gtprm.data[gtprm.data_pos + 2U]);
            gtprm.token_buffer_index = gtprm.token_buffer_index + 3U;
            gtprm.data_pos = gtprm.data_pos + 3U;
            return;
        }
        else
        {
            gtprm.token_buffer[gtprm.token_buffer_index] =
                UserInput::_combineControlCharacters((char)gtprm.data[gtprm.data_pos + 2U]);
        }
        gtprm.token_buffer_index++;
        gtprm.data_pos = gtprm.data_pos + 3U;
    }
    else
    {
        gtprm.token_buffer[gtprm.token_buffer_index] = gtprm.data[gtprm.data_pos];
        if (gtprm.point_to_beginning_of_token)
        {
            gtprm.token_pointers[gtprm.token_pointer_index] =
                &gtprm.token_buffer[gtprm.token_buffer_index];
            gtprm.token_pointer_index++;
            gtprm.point_to_beginning_of_token = false;
        }
        gtprm.token_buffer_index++;
        gtprm.data_pos++;
    }
} // end _getTokensChar

inline bool UserInput::_splitZDC(
    _rcfbprm& rprm, const size_t num_zdc, const CommandParameters** zdc)
{
    if (num_zdc != 0) // if there are zero delim commands
    {
        InputProcessDelimiterSequences delimiter_sequences;
        uint8_t delim_len = pgm_read_byte(&_input_prm_.delimiter_sequences->delimiter_lens[0]);
        size_t split_input_len = rprm.input_len + delim_len + 1U;

        rprm.split_input = (uint8_t*)calloc(split_input_len, sizeof(uint8_t));
        if (rprm.split_input == NULL) // if there was an error allocating the memory
        {
#if defined(__DEBUG_READCOMMANDFROMBUFFER__) && defined(ENABLE_ui_out)
            UserInput::_ui_out(
                PSTR(">%s$ERROR: cannot allocate ram to split input for zero delim command.\n"),
                (char*)pgm_read_dword(_input_prm_.process_name));
#endif
            return false;
        }
        memcpy_P(
            &delimiter_sequences, _input_prm_.delimiter_sequences, sizeof(delimiter_sequences));
        for (size_t i = 0; i < num_zdc;
             ++i) // look for zero delim commands and put a delimiter between the command and data
        {
            size_t cmd_len_pgm = pgm_read_dword(
                &(zdc[i]->command_length)); // read command len from CommandParameters object
            if (memcmp_P(rprm.input_data, zdc[i]->command, cmd_len_pgm) == false) // match zdc
            {
                char* ptr = (char*)rprm.split_input;
                memcpy(rprm.split_input, rprm.input_data,
                    cmd_len_pgm); // copy the command into token buffer
                ptr = (char*)rprm.split_input + cmd_len_pgm;
                memcpy(ptr, delimiter_sequences.delimiter_sequences[0],
                    delimiter_sequences.delimiter_lens[0]); // copy the delimiter into token buffer
                                                            // after the command
                ptr = (char*)rprm.split_input + cmd_len_pgm + delimiter_sequences.delimiter_lens[0];
                char* src = (char*)rprm.input_data + cmd_len_pgm;
                memcpy(ptr, src, (rprm.input_len - cmd_len_pgm)); // copy the data after the command
                                                                  // and delimiter into token buffer
                rprm.token_buffer_len++;
                rprm.input_len = split_input_len;
                return true;
            }
        } // end for loop
    }
    return false;
} // end _splitZDC

void UserInput::_calcCmdMemcmpRanges(CommandConstructor& command, CommandParameters& prm,
    size_t prm_idx, IH::memcmp_idx_t& memcmp_ranges_idx,
    IH::ui_max_per_cmd_memcmp_ranges_t* memcmp_ranges)
{
    // this function is only used inside of UserInput::addCommand() and is not iterated over in
    // loop()
    if (prm.has_wildcards == true) // if this command has wildcards
    {
        IH_wcc wcc;                     // char array to hold WildCard Character (wcc)
        size_t cmd_str_pos = 0;         // prm.command char array index
        bool start_memcmp_range = true; // sentinel
        memcpy_P(
            &wcc, _input_prm_.wildcard_char, sizeof(wcc)); // copy WildCard Character (wcc) to ram
        for (size_t i = 0; i < prm.command_length; ++i)
        {
            if (prm.command[i] == wcc[0]) // detect wildcard char
            {
                cmd_str_pos++; // use cmd_str_pos as temp counter
            }
        }
        if (cmd_str_pos
            == strlen(
                prm.command)) // all wildcard char command, strlen is safe to use on prm.command
        {
            memcmp_ranges[0] = UI_ALL_WCC_CMD;
            memcmp_ranges[1] = UI_ALL_WCC_CMD;
            memcmp_ranges_idx = 2;
        }
        else
        {
            cmd_str_pos = 0;
            while (cmd_str_pos < prm.command_length) // iterate over whole command len
            {
                if (prm.command[cmd_str_pos] == wcc[0])
                {
                    cmd_str_pos++;
                }
                if (prm.command[cmd_str_pos] != wcc[0]
                    && start_memcmp_range == true) // start memcmp range
                {
                    memcmp_ranges[memcmp_ranges_idx] = cmd_str_pos;
                    memcmp_ranges_idx++;
                    start_memcmp_range = false;
                }
                if (prm.command[cmd_str_pos] == wcc[0]
                    && prm.command[cmd_str_pos - 1] != wcc[0]) // end memcmp range
                {
                    memcmp_ranges[memcmp_ranges_idx] = cmd_str_pos - 1;
                    memcmp_ranges_idx++;
                    start_memcmp_range = true;
                }
                cmd_str_pos++; // increment char array index
            }
            if (memcmp_ranges_idx % 2 != 0) // memcmp ranges needs to be / 2
            {
                memcmp_ranges[memcmp_ranges_idx] = cmd_str_pos; // remember the end of the array
                memcmp_ranges_idx++;
            }
        }
    }
} // end _calcCmdMemcmpRanges

inline UI_COMPARE UserInput::_compareCommandToString(
    CommandConstructor* cmd, size_t prm_idx, char* str)
{
    size_t cmd_len_pgm = 0; // the length of the command in PROGMEM
    memcpy_P(&cmd_len_pgm, &cmd->prm[prm_idx].command_length, sizeof(IH::ui_max_cmd_len_t));
    size_t input_len = strlen(str); // the length of the input, str is a token in _token_buffer_ it
                                    // is safe to assume it is null terminated

#if defined(__DEBUG_SUBCOMMAND_SEARCH__)
    char buf[32] = {};
    strcpy_P(buf, cmd->prm[prm_idx].command);
    UserInput::_ui_out(PSTR("_compareCommandToString()\n"));
    UserInput::_ui_out(PSTR("command: <%s> len: %d\n"), buf, cmd_len_pgm);
    UserInput::_ui_out(PSTR("user input: <%s> len: %d\n"), str, input_len);
#endif
    if (input_len != cmd_len_pgm) // no match (length different)
    {
        return no_match;
    }

    UI_COMPARE retval = no_match;

    if (!(bool)pgm_read_byte(&cmd->prm[prm_idx].has_wildcards)) // no wildcards
    {
        if (memcmp_P(str, cmd->prm[prm_idx].command, cmd_len_pgm) != 0) // doesn't match
        {
            retval = no_match;
        }
        else
        {
            retval = match;
        }
    }
    else // has wildcards
    {
        if (cmd->calc->memcmp_ranges_arr[prm_idx][0] != UI_ALL_WCC_CMD
            && cmd->calc->memcmp_ranges_arr[prm_idx][1]
                != UI_ALL_WCC_CMD) // but is not an all wcc cmd
        {
            for (size_t i = 0; i < cmd->calc->num_memcmp_ranges_this_row[prm_idx];
                 i = i + 2) // iterate through memcmp range sets
            {
                long result = (int)cmd->calc->memcmp_ranges_arr[prm_idx][i + 1]
                    - (int)cmd->calc->memcmp_ranges_arr[prm_idx][i];
                result = abs(result); // remove the sign
                size_t size = ((size_t)result == 0) ? 1 : (size_t)result;
                char* cmp_ptr = &str[cmd->calc->memcmp_ranges_arr[prm_idx][i]];
                if (memcmp_P(cmp_ptr,
                        &(cmd->prm[prm_idx].command[cmd->calc->memcmp_ranges_arr[prm_idx][i]]),
                        size)
                    != 0) // doesn't match
                {
                    retval = no_match;
                }
                else
                {
                    retval = match;
                }
            }
        }
        else if (cmd_len_pgm == input_len
            && cmd->calc->memcmp_ranges_arr[prm_idx][0] == UI_ALL_WCC_CMD
            && cmd->calc->memcmp_ranges_arr[prm_idx][1] == UI_ALL_WCC_CMD) // all wcc
        {
            retval = match_all_wcc_cmd;
        }
    }
    return retval;
} // end _compareCommandToString()

// end of file
