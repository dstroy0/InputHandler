/**
 * @file config.h
 * @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
 * @brief InputHandler config.h
 * @version 1.0.0
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

/***************************
 * User Configurable items *
 ***************************/

    #if !defined(IH_MAX_COMMANDS_PER_TREE)
        /**
         * @brief default is 32, total number of commands allowed per tree, including the root
         * command
         * @def IH_MAX_COMMANDS_PER_TREE
         */
        #define IH_MAX_COMMANDS_PER_TREE 32
    #endif
    #if !defined(IH_MAX_ARGS_PER_COMMAND)
        /**
         * @brief default is 32, maximum number of arguments permitted per command
         * @def IH_MAX_ARGS_PER_COMMAND
         */
        #define IH_MAX_ARGS_PER_COMMAND 32
    #endif
    #if !defined(IH_MAX_TREE_DEPTH_PER_COMMAND)
        /**
         * @brief default is 32, process-wide tree depth cap
         * @def IH_MAX_TREE_DEPTH_PER_COMMAND
         */
        #define IH_MAX_TREE_DEPTH_PER_COMMAND 32
    #endif
    #if !defined(IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT)
        /**
         * @brief default is 32, command-wide child command (including indirect subcommands) cap
         * @def IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT
         */
        #define IH_MAX_NUM_CHILD_COMMANDS_PER_ROOT 32
    #endif
    #if !defined(IH_MAX_CMD_STR_LEN)
        /**
         * @brief default is 32, process-wide commandString cap
         * @def IH_MAX_CMD_STR_LEN
         */
        #define IH_MAX_CMD_STR_LEN 32
    #endif
    #if !defined(IH_MAX_NUM_PROC_DELIM_SEQ)
        /**
         * @brief default is 5, process-wide number of ih::DelimiterSequences cap
         * @def IH_MAX_NUM_PROC_DELIM_SEQ
         */
        #define IH_MAX_NUM_PROC_DELIM_SEQ 5
    #endif
    #if !defined(IH_MAX_NUM_START_STOP_SEQ)
        /**
         * @brief default is 5, process-wide number of ih::StartStopSequences cap
         * @def IH_MAX_NUM_START_STOP_SEQ
         */
        #define IH_MAX_NUM_START_STOP_SEQ 5
    #endif
    #if !defined(IH_MAX_PROC_INPUT_LEN)
        /**
         * @brief default is 128, maximum input length (in char)
         * @def IH_MAX_PROC_INPUT_LEN
         */
        #define IH_MAX_PROC_INPUT_LEN 128
    #endif
    // maximum number of memcmp ranges per command
    #if !defined(IH_MAX_PER_ROOT_MEMCMP_RANGES)
        /**
         * @brief default is 5, per root command memcmp range array member cap
         * @def IH_MAX_PER_ROOT_MEMCMP_RANGES
         */
        #define IH_MAX_PER_ROOT_MEMCMP_RANGES 5
    #endif

/****************************
 * PROGMEM length constants *
 ****************************/

    #if !defined(IH_INPUT_TYPE_STRINGS_PGM_LEN)
        /**
         * @brief default is 10, ihc::type_strings input type strings array max len
         * @def IH_INPUT_TYPE_STRINGS_PGM_LEN
         */
        #define IH_INPUT_TYPE_STRINGS_PGM_LEN 10
    #endif
    // if you edit these, some examples might break and your compiler might yell at you
    #if !defined(IH_EOL_SEQ_PGM_LEN)
        /**
         * @brief default is 5, process-wide end of line char sequence length cap
         * @def IH_EOL_SEQ_PGM_LEN
         */
        #define IH_EOL_SEQ_PGM_LEN 5
    #endif
    #if !defined(IH_DELIM_SEQ_PGM_LEN)
        /**
         * @brief default is 5, process-wide delimiter sequence length cap
         * @def IH_DELIM_SEQ_PGM_LEN
         */
        #define IH_DELIM_SEQ_PGM_LEN 5
    #endif
    #if !defined(IH_START_STOP_SEQ_PGM_LEN)
        /**
         * @brief default is 5, process-wide start-stop sequence length cap
         * @def IH_START_STOP_SEQ_PGM_LEN
         */
        #define IH_START_STOP_SEQ_PGM_LEN 5
    #endif
    #if !defined(IH_PROCESS_NAME_PGM_LEN)
        /**
         * @brief default is 12, process-wide ProcessName length cap
         * @def IH_PROCESS_NAME_PGM_LEN
         */
        #define IH_PROCESS_NAME_PGM_LEN 12
    #endif
    #if !defined(IH_INPUT_CONTROL_CHAR_SEQ_PGM_LEN)
        /**
         * @brief default is 3, process-wide input a control char sequence cap (2 char + null)
         * @def IH_INPUT_CONTROL_CHAR_SEQ_PGM_LEN
         */
        #define IH_INPUT_CONTROL_CHAR_SEQ_PGM_LEN 3
    #endif
    #if !defined(IH_WCC_SEQ_PGM_LEN)
        /**
         * @brief default is 2, process-wide WildcardChar length cap
         * @def IH_WCC_SEQ_PGM_LEN
         */
        #define IH_WCC_SEQ_PGM_LEN 2
    #endif

/********************************
 * library output customization *
 *   true == ON; false == OFF   *
 ********************************/

    #if !defined(IH_ECHO_ONLY)
        /**
         * @brief default is false, Enable this option to change the library's output to echo only.
         * It will only echo what was entered and indicate where the input error is.
         * @def IH_ECHO_ONLY
         */
        #define IH_ECHO_ONLY false
    #endif
    #if !defined(IH_VERBOSE)
        /**
         * @brief default is true, Enable this option to change the library's output to verbose.
         * Puts additional command information in the output buffer.
         * @def IH_VERBOSE
         */
        #define IH_VERBOSE true
    #endif

/********************************
 *       library debugging      *
 *   true == ON; false == OFF   *
 ********************************/

    #if !defined(DEBUG_GETCOMMANDFROMSTREAM)
        /**
         * @brief default is false, Enable this option to debug ih::Input::getCommandFromStream()
         * @def DEBUG_GETCOMMANDFROMSTREAM
         */
        #define DEBUG_GETCOMMANDFROMSTREAM false
    #endif
    #if !defined(DEBUG_READCOMMANDFROMBUFFER)
        /**
         * @brief default is false, Enable this option to debug ih::Input::readCommandFromBuffer()
         * @def DEBUG_READCOMMANDFROMBUFFER
         */
        #define DEBUG_READCOMMANDFROMBUFFER false
    #endif
    #if !defined(DEBUG_GET_TOKEN)
        /**
         * @brief default is false, Enable this option to debug ih::Input::getToken()
         * @def DEBUG_GET_TOKEN
         */
        #define DEBUG_GET_TOKEN false
    #endif
    #if !defined(DEBUG_SUBCOMMAND_SEARCH)
        /**
         * @brief default is false, Enable this option to debug Input::launchLogic subcommand
         * search; subcommand search is recursive, uses no local variables and passes a
         * ih::Input::_rcfbprm object by reference to itself.
         * @def DEBUG_SUBCOMMAND_SEARCH
         */
        #define DEBUG_SUBCOMMAND_SEARCH false
    #endif
    #if !defined(DEBUG_ADDCOMMAND)
        /**
         * @brief default is false, Enable this option to debug ih::Input::addCommand()
         * @def DEBUG_ADDCOMMAND
         */
        #define DEBUG_ADDCOMMAND false
    #endif
    #if !defined(DEBUG_LAUNCH_LOGIC)
        /**
         * @brief default is false, Enable this option to debug ih::Input::_launchLogic()
         * @def DEBUG_LAUNCH_LOGIC
         */
        #define DEBUG_LAUNCH_LOGIC false
    #endif
    #if !defined(DEBUG_LAUNCH_FUNCTION)
        /**
         * @brief default is false, Enable this option to debug ih::Input::_launchFunction()
         * @def DEBUG_LAUNCH_FUNCTION
         */
        #define DEBUG_LAUNCH_FUNCTION false
    #endif
    #if !defined(DEBUG_INCLUDE_FREERAM)
        /**
         * @brief default is false, Enable to debug src/utility/freeRam.h; only applicable if you
         * are using freeRam.
         * @def DEBUG_INCLUDE_FREERAM
         */
        #define DEBUG_INCLUDE_FREERAM false
    #endif

/********************************
 *   optional library methods   *
 *   true == ON; false == OFF   *
 ********************************/
/**** public methods ****/
    #if !defined(DISABLE_listSettings)
        /**
         * @brief default is false, Enable this option to disable ih::Input::listSettings()
         * @def DISABLE_listSettings
         */
        #define DISABLE_listSettings false
    #endif
    #if !defined(DISABLE_listCommands)
        /**
         * @brief default is false, Enable this option to disable ih::Input::listCommands()
         * @def DISABLE_listCommands
         */
        #define DISABLE_listCommands false
    #endif
    #if !defined(DISABLE_getCommandFromStream)
        /**
         * @brief default is false, Enable this option to disable ih::Input::getCommandFromStream()
         * @def DISABLE_getCommandFromStream
         */
        #define DISABLE_getCommandFromStream false
    #endif
    #if !defined(DISABLE_nextArgument)
        /**
         * @brief default is false, Enable this option to disable ih::Input::nextArgument(), either
         * this method or ih::Input::getArgument()) are required to retrieve arguments.
         * @def DISABLE_nextArgument
         */
        #define DISABLE_nextArgument false
    #endif
    #if !defined(DISABLE_getArgument)
        /**
         * @brief default is false, Enable this option to disable ih::Input::getArgument(), either
         * this method or ih::Input::nextArgument() need to be enabled to retrieve arguments.
         * @def DISABLE_getArgument
         */
        #define DISABLE_getArgument false
    #endif
    #if !defined(DISABLE_outputIsAvailable)
        /**
         * @brief default is false, Enable this option to disable ih::Input::outputIsAvailable().
         * @def DISABLE_outputIsAvailable
         */
        #define DISABLE_outputIsAvailable false
    #endif
    #if !defined(DISABLE_outputIsEnabled)
        /**
         * @brief default is false, Enable this option to disable ih::Input::outputIsEnabled()
         * @def DISABLE_outputIsEnabled
         */
        #define DISABLE_outputIsEnabled false
    #endif
    #if !defined(DISABLE_outputToStream)
        /**
         * @brief default is false, Enable this option to reduce codesize if you are only using
         * ih::Input::readCommandFromBuffer().
         * @def DISABLE_outputToStream
         */
        #define DISABLE_outputToStream false
    #endif
    #if !defined(DISABLE_clearOutputBuffer)
        /**
         * @brief default is false, Only disable this method if you have already disabled output.
         * Enable this option to disable Input::clearOutputBuffer()
         * @def DISABLE_clearOutputBuffer
         */
        #define DISABLE_clearOutputBuffer false
    #endif
/**** private methods ****/
    #if !defined(DISABLE_readCommandFromBufferErrorOutput)
        /**
         * @brief default is false, Enable this option to disable the library's error output.
         * @def DISABLE_readCommandFromBufferErrorOutput
         */
        #define DISABLE_readCommandFromBufferErrorOutput false
    #endif

/**** global library output ****/
    #if !defined(DISABLE_ihout)
        /**
         * @brief default is false, Enable this option to completely remove output functionality at
         * buildtime from the library.
         * @def DISABLE_ihout
         */
        #define DISABLE_ihout false
    #endif
#endif // end include guard
// end of file
