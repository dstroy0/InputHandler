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
    #define UI_MAX_COMMANDS_IN_TREE 32 ///< maxumum number of tree commands including root; default is 32

    #define UI_MAX_ARGS_PER_COMMAND 32 ///< maximum number of arguments per command; default is 32

    #define UI_MAX_TREE_DEPTH_PER_COMMAND 32 ///<  maximum command tree depth; default is 32

    #define UI_MAX_NUM_CHILD_COMMANDS 32 ///< maximum number of child commands that any command can branch to; default is 32

    #define UI_MAX_CMD_LEN 32 ///<  maximum command/subcommand char length; default is 32

    #define UI_MAX_NUM_DELIM_SEQ 5 ///< maximum number of delimiter sequences; default is 5

    #define UI_MAX_NUM_START_STOP_SEQ 5 ///< maximum number of start stop sequences; default is 5

    #define UI_MAX_INPUT_LEN 255 ///<  maximum user input length (total number of single char); default is 255

// maximum number of memcmp ranges per command
    #define UI_MAX_PER_CMD_MEMCMP_RANGES 5 ///< UserInput::addCommand array sizing macro (soft limit, typeof container is max) 

/*
    fine-tune the program space needed for your implementation
*/
// PROGMEM width constants
    #define UI_INPUT_TYPE_STRINGS_PGM_LEN 10 ///< ihconst::type_strings MAX len of members in ihconst::type_strings src/InputHandler.h:105; default is 10

    // if you edit these, some examples might break and your compiler might yell at you about some variables in the UserInput constants section of InputHandler.h
    #define UI_EOL_SEQ_PGM_LEN 5 ///< IH_eol MAX len in char; default is 5

    #define UI_DELIM_SEQ_PGM_LEN 5 ///< InputProcessDelimiterSequences::delimiter_sequences[a][b] b MAX len in char; default is 5

    #define UI_START_STOP_SEQ_PGM_LEN 5 ///< InputProcessStartStopSequences::start_stop_sequence_pairs[a][b] b MAX len in char; default is 5

    #define UI_PROCESS_NAME_PGM_LEN 12 ///< IH_pname MAX len in char; default is 12

    #define UI_INPUT_CONTROL_CHAR_SEQ_PGM_LEN 3 ///< IH_input_cc MAX len in char; default is 3

/*
    library output
    switch this on/off by commenting/uncommenting the #define
*/
    /**
     * @def UI_ECHO_ONLY
     *
     * Uncomment this line to change the library's output to echo only.
     */  
    // #define UI_ECHO_ONLY

/*
    DEBUGGING
    switch these on/off by commenting/uncommenting the #define
*/
    /**
     * @def DEBUG_GETCOMMANDFROMSTREAM
     *
     * Uncomment to debug UserInput::getCommandFromStream
     */
    // #define DEBUG_GETCOMMANDFROMSTREAM

    /**
     * @def DEBUG_READCOMMANDFROMBUFFER
     *
     * Uncomment to debug UserInput::readCommandFromBuffer
     */
    // #define DEBUG_READCOMMANDFROMBUFFER
    
    /**
     * @def DEBUG_GET_TOKEN
     *
     * Uncomment to debug UserInput::getToken
     */
    // #define DEBUG_GET_TOKEN
    
    /**
     * @def DEBUG_SUBCOMMAND_SEARCH
     *
     * Uncomment to debug UserInput::launchLogic subcommand search; subcommand search is recursive, uses no local variables and passes a UserInput::_rcfbprm object by reference to itself. 
     */
    // #define DEBUG_SUBCOMMAND_SEARCH
    
    /**
     * @def DEBUG_ADDCOMMAND
     *
     * Uncomment to debug UserInput::addCommand
     */
    // #define DEBUG_ADDCOMMAND
    
    /**
     * @def DEBUG_LAUNCH_LOGIC
     *
     * Uncomment to debug UserInput::launchLogic
     */
    // #define DEBUG_LAUNCH_LOGIC
    
    /**
     * @def DEBUG_LAUNCH_FUNCTION
     *
     * Uncomment to debug UserInput::launchFunction
     */
    // #define DEBUG_LAUNCH_FUNCTION
    
    /**
     * @def DEBUG_INCLUDE_FREERAM
     *
     * Uncomment to debug src/utility/freeRam.h; only applicable if you are using freeRam.
     */
    // #define DEBUG_INCLUDE_FREERAM

/*
    OPTIONAL METHODS
    switch these on/off by commenting/uncommenting the #define
*/    
    // public methods
    /**
     * @def DISABLE_listSettings
     *
     * Disables UserInput::listSettings
     */    
    // #define DISABLE_listSettings
    
    /**
     * @def DISABLE_listCommands
     *
     * Disables UserInput::listCommands
     */
    // #define DISABLE_listCommands
    
    /**
     * @def DISABLE_getCommandFromStream
     *
     * Disables UserInput::getCommandFromStream
     */
    // #define DISABLE_getCommandFromStream
    
    /**
     * @def DISABLE_nextArgument
     *
     * Disables UserInput::nextArgument, either this or UserInput::getArgument are required to retrieve arguments.
     */
    // #define DISABLE_nextArgument
    
    /**
     * @def DISABLE_getArgument
     *
     * Disables UserInput::getArgument method, either this or UserInput::nextArgument need to be enabled to retrieve arguments.
     */
    // #define DISABLE_getArgument
    
    /**
     * @def DISABLE_outputIsAvailable
     *
     * Disables the output available flag.
     */
    // #define DISABLE_outputIsAvailable
    
    /**
     * @def DISABLE_outputIsEnabled
     *
     * Disable UserInput::outputIsEnabled
     */
    // #define DISABLE_outputIsEnabled
    
    /**
     * @def DISABLE_outputToStream
     *
     * You can disable this to reduce codesize if you are only using readCommandFromBuffer.
     */
    // #define DISABLE_outputToStream
    
    /**
     * @def DISABLE_clearOutputBuffer
     *
     * Only disable this method if you have already disabled output.
     */
    // #define DISABLE_clearOutputBuffer
    
    // private methods
    /**
     * @def DISABLE_readCommandFromBufferErrorOutput
     *
     * Uncomment this line to disable the library's error output.
     */
    // #define DISABLE_readCommandFromBufferErrorOutput
    
    /**
     * @def DISABLE_ui_out
     *
     * Uncomment this line to completely remove output functionality at buildtime from the library.
     */
    // #define DISABLE_ui_out

#endif // end include guard
// end of file
