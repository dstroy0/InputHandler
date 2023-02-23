/**
 * @file config.h
 * @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
 * @brief InputHandler config.h
 * @version 1.0
 * @date 2023-02-13
 *
 * @copyright Copyright (c) 2023
 */
/*
 * Copyright (c) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
 *
 * License: GNU GPL3
 * This program is free software; you can redistribute it and/or
 * modify it under the terms of the GNU General Public License
 * version 3 as published by the Free Software Foundation.
 */

#if !defined(__INPUTHANDLER_CONFIG_H__)
    #define __INPUTHANDLER_CONFIG_H__

    /*
        User Configurable items
    */
    #define IH_MAX_COMMANDS_PER_TREE 32

    #define IH_MAX_ARGS_PER_COMMAND 32

    #define IH_MAX_TREE_DEPTH_PER_COMMAND 32

    #define IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT 32

    #define IH_MAX_CMD_STR_LEN 32

    #define IH_MAX_NUM_PROC_DELIM_SEQ 5

    #define IH_MAX_NUM_START_STOP_SEQ 5

    #define IH_MAX_PROC_INPUT_LEN 128

    // maximum number of memcmp ranges per command
    #define IH_MAX_PER_ROOT_MEMCMP_RANGES 5

    /*
        fine-tune the program space needed for your implementation
    */
    // PROGMEM len constants
    #define UI_INPUT_TYPE_STRINGS_PGM_LEN 10

    // if you edit these, some examples might break and your compiler might yell at you about some
    // variables in the UserInput constants section of InputHandler.h
    #define UI_EOL_SEQ_PGM_LEN 5

    #define UI_DELIM_SEQ_PGM_LEN 5

    #define UI_START_STOP_SEQ_PGM_LEN 5

    #define UI_PROCESS_NAME_PGM_LEN 12

    #define UI_INPUT_CONTROL_CHAR_SEQ_PGM_LEN 3

    #define UI_WCC_SEQ_PGM_LEN 2

    /*
        library output
        true == ON; false == OFF
    */
    /**
     * @var UI_ECHO_ONLY
     *
     * Enable this option to change the library's output to echo only.
     * It will only echo what was entered and indicate where the input error is.
     */
    #define UI_ECHO_ONLY false

    /**
     * @var UI_VERBOSE
     *
     * Enable this option to change the library's output to verbose.
     * Puts additional command information in the output buffer.
     */
    #define UI_VERBOSE true

    /*
        DEBUGGING
        switch these on/off by commenting/uncommenting the #define
    */
    /**
     * @var DEBUG_GETCOMMANDFROMSTREAM
     *
     * Enable this option to debug UserInput::getCommandFromStream
     */
    #define DEBUG_GETCOMMANDFROMSTREAM false

    /**
     * @var DEBUG_READCOMMANDFROMBUFFER
     *
     * Enable this option to debug UserInput::readCommandFromBuffer
     */
    #define DEBUG_READCOMMANDFROMBUFFER false

    /**
     * @var DEBUG_GET_TOKEN
     *
     * Enable this option to debug UserInput::getToken
     */
    #define DEBUG_GET_TOKEN false

    /**
     * @var DEBUG_SUBCOMMAND_SEARCH
     *
     * Enable this option to debug UserInput::launchLogic subcommand search; subcommand search is
     * recursive, uses no local variables and passes a UserInput::_rcfbprm object by reference to
     * itself.
     */
    #define DEBUG_SUBCOMMAND_SEARCH false

    /**
     * @var DEBUG_ADDCOMMAND
     *
     * Enable this option to debug UserInput::addCommand
     */
    #define DEBUG_ADDCOMMAND false

    /**
     * @var DEBUG_LAUNCH_LOGIC
     *
     * Enable this option to debug UserInput::launchLogic
     */
    #define DEBUG_LAUNCH_LOGIC false

    /**
     * @var DEBUG_LAUNCH_FUNCTION
     *
     * Enable this option to debug UserInput::launchFunction
     */
    #define DEBUG_LAUNCH_FUNCTION false

    /**
     * @var DEBUG_INCLUDE_FREERAM
     *
     * Uncomment to debug src/utility/freeRam.h; only applicable if you are using freeRam.
     */
    #define DEBUG_INCLUDE_FREERAM false

    /*
        OPTIONAL METHODS
        switch these on/off by commenting/uncommenting the #define
    */
    // public methods
    /**
     * @var DISABLE_listSettings
     *
     * Enable this option to disable UserInput::listSettings()
     */
    #define DISABLE_listSettings false

    /**
     * @var DISABLE_listCommands
     *
     * Enable this option to disable UserInput::listCommands
     */
    #define DISABLE_listCommands false

    /**
     * @var DISABLE_getCommandFromStream
     *
     * Enable this option to disable UserInput::getCommandFromStream
     */
    #define DISABLE_getCommandFromStream false

    /**
     * @var DISABLE_nextArgument
     *
     * Enable this option to disable UserInput::nextArgument, either this or UserInput::getArgument
     * are required to retrieve arguments.
     */
    #define DISABLE_nextArgument false

    /**
     * @var DISABLE_getArgument
     *
     * Enable this option to disable UserInput::getArgument method, either this or
     * UserInput::nextArgument need to be enabled to retrieve arguments.
     */
    #define DISABLE_getArgument false

    /**
     * @var DISABLE_outputIsAvailable
     *
     * Enable this option to disable the output available flag.
     */
    #define DISABLE_outputIsAvailable false

    /**
     * @var DISABLE_outputIsEnabled
     *
     * Enable this option to disable UserInput::outputIsEnabled
     */
    #define DISABLE_outputIsEnabled false

    /**
     * @var DISABLE_outputToStream
     *
     * Enable this option to reduce codesize if you are only using
     * UserInput::readCommandFromBuffer. Default is false.
     */
    #define DISABLE_outputToStream false

    /**
     * @var DISABLE_clearOutputBuffer
     *
     * Only disable this method if you have already disabled output.
     * Enable this option to disable UserInput::clearOutputBuffer()
     * Default is false.
     */
    #define DISABLE_clearOutputBuffer false

    // private methods
    /**
     * @var DISABLE_readCommandFromBufferErrorOutput
     *
     * Enable this option to disable the library's error output.
     * Default is false.
     */
    #define DISABLE_readCommandFromBufferErrorOutput false

    /**
     * @var DISABLE_ui_out
     *
     * Enable this option to completely remove output functionality at buildtime from the library.
     * Default is false.
     */
    #define DISABLE_ui_out false

#endif // end include guard
// end of file
