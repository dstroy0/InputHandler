/**
   @file advanced_config.h
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief InputHandler library advanced user settings
   @version 1.0
   @date 2022-05-16

   @copyright Copyright (c) 2022
*/
/*
 Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 version 3 as published by the Free Software Foundation.
 */

#if !defined(__INPUTHANDLER_ADVANCED_CONFIG_H__)
    #define __INPUTHANDLER_ADVANCED_CONFIG_H__

    // uncomment to enable debug
    //#define __DEBUG_USER_INPUT__

    // then uncomment which method(s) to debug
    #if defined(__DEBUG_USER_INPUT__)
    //#define __DEBUG_GETCOMMANDFROMSTREAM__
    //#define __DEBUG_READCOMMANDFROMBUFFER__
    //#define __DEBUG_GET_TOKEN__
    //#define __DEBUG_SUBCOMMAND_SEARCH__
    //#define __DEBUG_ADDCOMMAND__
    //#define __DEBUG_LAUNCH_LOGIC__
    //#define __DEBUG_LAUNCH_FUNCTION__
    #endif // debug section

    /*
        OPTIONAL METHODS

        comment out to DISABLE and save some program space
        for your implementation, disabling these methods will break some examples
        some of these methods depend on other methods, 
    */
    
    //  public methods
    #define ENABLE_listSettings
    #define ENABLE_listCommands
    #define ENABLE_getCommandFromStream
    #define ENABLE_nextArgument
    #define ENABLE_getArgument
    #define ENABLE_outputIsAvailable
    #define ENABLE_outputIsEnabled
    #define ENABLE_outputToStream
    #define ENABLE_clearOutputBuffer
    // private methods
    #define ENABLE_readCommandFromBufferErrorOutput

    /*
        fine-tune the program space needed for your implementation
    */
    // PROGMEM width constants
    #define UI_INPUT_TYPE_STRINGS_PGM_LEN 10    ///< UserInput_type_strings_pgm width in bytes
    #define UI_EOL_SEQ_PGM_LEN 5                ///< IH_eol width in bytes
    #define UI_DELIM_SEQ_PGM_LEN 5              ///< InputProcessDelimiterSequences::delimiter_sequences[a][b] b width in bytes
    #define UI_START_STOP_SEQ_PGM_LEN 5         ///< InputProcessStartStopSequences::start_stop_sequence_pairs[a][b] b width in bytes
    #define UI_PROCESS_NAME_PGM_LEN 12          ///< IH_pname width in bytes
    #define UI_INPUT_CONTROL_CHAR_SEQ_PGM_LEN 3 ///< IH_input_cc width in bytes

#endif // include guard
// end of file
