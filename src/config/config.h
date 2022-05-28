/**
   @file config.h
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief InputHandler library user configurable items
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

#ifndef __USER_INPUT_HANDLER_CONFIG_H__
    #define __USER_INPUT_HANDLER_CONFIG_H__

/*
    User Configurable items
*/
// maxumum number of root commands
    #define UI_MAX_COMMANDS 256

//  maximum number of arguments per command
    #define UI_MAX_ARGS 32

//  maximum tree depth
    #define UI_MAX_DEPTH 32

//  maximum number of subcommands that a command can branch to
    #define UI_MAX_SUBCOMMANDS 32

//  maximum command/subcommand char length
    #define UI_MAX_CMD_LEN 32

// maximum number of delimiter sequences
    #define UI_MAX_DELIM_SEQ 5

// maximum number of start stop sequence len
    #define UI_MAX_START_STOP_SEQ 5

//  maximum user input length
    #define UI_MAX_IN_LEN 65533

// maximum number of memcmp ranges per command
    #define UI_MAX_PER_CMD_MEMCMP_RANGES 5 ///< UserInput::addCommand array sizing macro (soft limit, typeof container is max)

/*
    fine-tune the program space needed for your implementation
*/
// PROGMEM width constants
    #define UI_INPUT_TYPE_STRINGS_PGM_LEN 10 ///< UserInput_type_strings_pgm width in bytes

    #define UI_EOL_SEQ_PGM_LEN 5 ///< IH_eol width in bytes

    #define UI_DELIM_SEQ_PGM_LEN 5 ///< InputProcessDelimiterSequences::delimiter_sequences[a][b] b width in bytes

    #define UI_START_STOP_SEQ_PGM_LEN 5 ///< InputProcessStartStopSequences::start_stop_sequence_pairs[a][b] b width in bytes

    #define UI_PROCESS_NAME_PGM_LEN 12 ///< IH_pname width in bytes

    #define UI_INPUT_CONTROL_CHAR_SEQ_PGM_LEN 3 ///< IH_input_cc width in bytes

#endif // end include guard
// end of file
