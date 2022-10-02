/**
   @file config.h
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief InputHandler library user configurable items
   @version 1.1
   @date 2022-05-28

   @copyright Copyright (c) 2022
*/
/*
 Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 version 3 as published by the Free Software Foundation.
 */

#if !defined(__INPUTHANDLER_CONFIG_H__)
    #define __INPUTHANDLER_CONFIG_H__

/*
    User Configurable items
*/
// maxumum number of tree commands including root
    #define UI_MAX_COMMANDS_IN_TREE 32

//  maximum number of arguments per command
    #define UI_MAX_ARGS_PER_COMMAND 32

//  maximum command tree depth
    #define UI_MAX_TREE_DEPTH_PER_COMMAND 32

//  maximum number of child commands that any command can branch to
    #define UI_MAX_NUM_CHILD_COMMANDS 32

//  maximum command/subcommand char length
    #define UI_MAX_CMD_LEN 32

// maximum number of delimiter sequences
    #define UI_MAX_NUM_DELIM_SEQ 5

// maximum number of start stop sequence len
    #define UI_MAX_NUM_START_STOP_SEQ 5

//  maximum user input length
    #define UI_MAX_INPUT_LEN 255

// maximum number of memcmp ranges per command
    #define UI_MAX_PER_CMD_MEMCMP_RANGES 5 /*< UserInput::addCommand array sizing macro (soft limit, typeof container is max) */

/*
    fine-tune the program space needed for your implementation
*/
// PROGMEM width constants
    #define UI_INPUT_TYPE_STRINGS_PGM_LEN 10 /*< ihconst::type_strings width in bytes, don't change this unless you also edit the members of ihconst::type_strings src/InputHandler.h:105  */

    // if you edit these, some examples might break and your compiler might yell at you about some variables in the UserInput constants section of InputHandler.h
    #define UI_EOL_SEQ_PGM_LEN 5 /*< IH_eol width in bytes */

    #define UI_DELIM_SEQ_PGM_LEN 5 /*< InputProcessDelimiterSequences::delimiter_sequences[a][b] b width in bytes */

    #define UI_START_STOP_SEQ_PGM_LEN 5 /*< InputProcessStartStopSequences::start_stop_sequence_pairs[a][b] b width in bytes */

    #define UI_PROCESS_NAME_PGM_LEN 12 /*< IH_pname width in bytes */

    #define UI_INPUT_CONTROL_CHAR_SEQ_PGM_LEN 3 /*< IH_input_cc width in bytes */

/*
    library output
    switch this on/off by commenting/uncommenting the #define
*/    
    // #define UI_ECHO_ONLY

/*
    DEBUGGING
    switch these on/off by commenting/uncommenting the #define
*/
    // #define DEBUG_GETCOMMANDFROMSTREAM
    // #define DEBUG_READCOMMANDFROMBUFFER
    // #define DEBUG_GET_TOKEN
    // #define DEBUG_SUBCOMMAND_SEARCH
    // #define DEBUG_ADDCOMMAND
    // #define DEBUG_LAUNCH_LOGIC
    // #define DEBUG_LAUNCH_FUNCTION
    // #define DEBUG_INCLUDE_FREERAM

/*
    OPTIONAL METHODS
    switch these on/off by commenting/uncommenting the #define
*/
    // public methods
    // #define DISABLE_listSettings
    // #define DISABLE_listCommands
    // #define DISABLE_getCommandFromStream
    // #define DISABLE_nextArgument
    // #define DISABLE_getArgument
    // #define DISABLE_outputIsAvailable
    // #define DISABLE_outputIsEnabled
    // #define DISABLE_outputToStream
    // #define DISABLE_clearOutputBuffer
    
    // private methods
    // #define DISABLE_readCommandFromBufferErrorOutput
    // #define DISABLE_ui_out

#endif // end include guard
// end of file
