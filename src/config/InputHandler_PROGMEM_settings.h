#if !defined(__INPUTHANDLER_PROGMEM_SETTINGS_H__)
#define __INPUTHANDLER_PROGMEM_SETTINGS_H__

// PROGMEM width constants
#define UI_INPUT_TYPE_STRINGS_PGM_LEN     10 // UserInput_type_strings_pgm width in bytes 
#define UI_EOL_SEQ_PGM_LEN                5  // IH_eol width in bytes
#define UI_DELIM_SEQ_PGM_LEN              5  // InputProcessDelimiterSequences::delimiter_sequences[a][b] b width in bytes
#define UI_START_STOP_SEQ_PGM_LEN         5  // InputProcessStartStopSequences::start_stop_sequence_pairs[a][b] b width in bytes
#define UI_PROCESS_NAME_PGM_LEN           12 // IH_pname width in bytes
#define UI_INPUT_CONTROL_CHAR_SEQ_PGM_LEN 3  // IH_input_cc width in bytes

#endif // include guard
// end of file
