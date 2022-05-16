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

    /*
        DEBUGGING

        switch these on/off by using #define before including the library
    */

    #if defined(DEBUG_GETCOMMANDFROMSTREAM)
        #define __DEBUG_GETCOMMANDFROMSTREAM__
    #endif
    #if defined(DEBUG_READCOMMANDFROMBUFFER)
        #define __DEBUG_READCOMMANDFROMBUFFER__
    #endif
    #if defined(DEBUG_GET_TOKEN)
        #define __DEBUG_GET_TOKEN__
    #endif
    #if defined(DEBUG_SUBCOMMAND_SEARCH)
        #define __DEBUG_SUBCOMMAND_SEARCH__
    #endif
    #if defined(DEBUG_ADDCOMMAND)
        #define __DEBUG_ADDCOMMAND__
    #endif
    #if defined(DEBUG_LAUNCH_LOGIC)
        #define __DEBUG_LAUNCH_LOGIC__
    #endif
    #if defined(DEBUG_LAUNCH_FUNCTION)
        #define __DEBUG_LAUNCH_FUNCTION__
    #endif

    /*
        OPTIONAL METHODS

        switch these on/off by using #define DISABLE_<method> before including the library        
    */
    
    //  public methods
    #if !defined(DISABLE_listSettings)
        #define ENABLE_listSettings
    #endif
    #if !defined(DISABLE_listCommands)
        #define ENABLE_listCommands
    #endif
    #if !defined(DISABLE_getCommandFromStream)
        #define ENABLE_getCommandFromStream
    #endif
    #if !defined(DISABLE_nextArgument)
        #define ENABLE_nextArgument
    #endif
    #if !defined(DISABLE_getArgument)
        #define ENABLE_getArgument
    #endif
    #if !defined(DISABLE_outputIsAvailable)
        #define ENABLE_outputIsAvailable
    #endif
    #if !defined(DISABLE_outputIsEnabled)
        #define ENABLE_outputIsEnabled
    #endif
    #if !defined(DISABLE_outputToStream)
        #define ENABLE_outputToStream
    #endif
    #if !defined(DISABLE_clearOutputBuffer)
        #define ENABLE_clearOutputBuffer
    #endif
    // private methods
    #if !defined(DISABLE_readCommandFromBufferErrorOutput)
        #define ENABLE_readCommandFromBufferErrorOutput
    #endif

    /*
        fine-tune the program space needed for your implementation
    */
   
    // PROGMEM width constants
    #if !defined(UI_INPUT_TYPE_STRINGS_PGM_LEN)
        #define UI_INPUT_TYPE_STRINGS_PGM_LEN 10    ///< UserInput_type_strings_pgm width in bytes
    #endif
    
    #if !defined(UI_EOL_SEQ_PGM_LEN)
        #define UI_EOL_SEQ_PGM_LEN 5                ///< IH_eol width in bytes
    #endif
    
    #if !defined(UI_DELIM_SEQ_PGM_LEN)
        #define UI_DELIM_SEQ_PGM_LEN 5              ///< InputProcessDelimiterSequences::delimiter_sequences[a][b] b width in bytes
    #endif
    
    #if !defined(UI_START_STOP_SEQ_PGM_LEN)
        #define UI_START_STOP_SEQ_PGM_LEN 5         ///< InputProcessStartStopSequences::start_stop_sequence_pairs[a][b] b width in bytes
    #endif
    
    #if !defined(UI_PROCESS_NAME_PGM_LEN)
        #define UI_PROCESS_NAME_PGM_LEN 12          ///< IH_pname width in bytes
    #endif
    
    #if !defined(UI_INPUT_CONTROL_CHAR_SEQ_PGM_LEN)
        #define UI_INPUT_CONTROL_CHAR_SEQ_PGM_LEN 3 ///< IH_input_cc width in bytes
    #endif
#endif // include guard
// end of file
