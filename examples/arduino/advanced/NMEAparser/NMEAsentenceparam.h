#if !defined(__NMEAsentenceparam_H__)
    #define __NMEAsentenceparam_H__

    #include <InputHandler.h>

/**
 * @brief Parameters struct with NMEA sentence types
 *
 */

extern void uc_unrecognized(UserInput* inputProcess);
extern void NMEA_parse_test(UserInput* inputProcess);

const PROGMEM Parameters GPAAM[1] = {
    NMEA_parse_test,           // function ptr
    "GPAAM",                   // command string
    5,                         // string length
    root,                      // parent id
    1,                         // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPAPA[1] = {
    NMEA_parse_test,           // function ptr
    "GPAPA",                   // command string
    5,                         // string length
    root,                      // parent id
    2,                         // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPAPB[1] = {
    NMEA_parse_test,           // function ptr
    "GPAPB",                   // command string
    5,                         // string length
    root,                      // parent id
    3,                         // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPBOD[1] = {
    NMEA_parse_test,           // function ptr
    "GPBOD",                   // command string
    5,                         // string length
    root,                      // parent id
    4,                         // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPBWC[1] = {
    NMEA_parse_test,           // function ptr
    "GPBWC",                   // command string
    5,                         // string length
    root,                      // parent id
    5,                         // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPBWR[1] = {
    NMEA_parse_test,           // function ptr
    "GPBWR",                   // command string
    5,                         // string length
    root,                      // parent id
    6,                         // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPDBT[1] = {
    NMEA_parse_test,           // function ptr
    "GPDBT",                   // command string
    5,                         // string length
    root,                      // parent id
    7,                         // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPDPT[1] = {
    NMEA_parse_test,           // function ptr
    "GPDPT",                   // command string
    5,                         // string length
    root,                      // parent id
    8,                         // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPGGA[1] = {
    NMEA_parse_test,           // function ptr
    "GPGGA",                   // command string
    5,                         // string length
    root,                      // parent id
    9,                         // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPGLL[1] = {
    NMEA_parse_test,           // function ptr
    "GPGLL",                   // command string
    5,                         // string length
    root,                      // parent id
    10,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPGSA[1] = {
    NMEA_parse_test,           // function ptr
    "GPGSA",                   // command string
    5,                         // string length
    root,                      // parent id
    11,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPGSV[1] = {
    NMEA_parse_test,           // function ptr
    "GPGSV",                   // command string
    5,                         // string length
    root,                      // parent id
    12,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPHDM[1] = {
    NMEA_parse_test,           // function ptr
    "GPHDM",                   // command string
    5,                         // string length
    root,                      // parent id
    13,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPHDT[1] = {
    NMEA_parse_test,           // function ptr
    "GPHDT",                   // command string
    5,                         // string length
    root,                      // parent id
    14,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPHSC[1] = {
    NMEA_parse_test,           // function ptr
    "GPHSC",                   // command string
    5,                         // string length
    root,                      // parent id
    15,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPMTW[1] = {
    NMEA_parse_test,           // function ptr
    "GPMTW",                   // command string
    5,                         // string length
    root,                      // parent id
    16,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPRMB[1] = {
    NMEA_parse_test,           // function ptr
    "GPRMB",                   // command string
    5,                         // string length
    root,                      // parent id
    17,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPRMC[1] = {
    NMEA_parse_test,           // function ptr
    "GPRMC",                   // command string
    5,                         // string length
    root,                      // parent id
    18,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPVTG[1] = {
    NMEA_parse_test,           // function ptr
    "GPVTG",                   // command string
    5,                         // string length
    root,                      // parent id
    19,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPWCV[1] = {
    NMEA_parse_test,           // function ptr
    "GPWCV",                   // command string
    5,                         // string length
    root,                      // parent id
    20,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPWPL[1] = {
    NMEA_parse_test,           // function ptr
    "GPWPL",                   // command string
    5,                         // string length
    root,                      // parent id
    21,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPXTE[1] = {
    NMEA_parse_test,           // function ptr
    "GPXTE",                   // command string
    5,                         // string length
    root,                      // parent id
    22,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

const PROGMEM Parameters GPXTR[1] = {
    NMEA_parse_test,           // function ptr
    "GPXTR",                   // command string
    5,                         // string length
    root,                      // parent id
    23,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
        UITYPE::NOTYPE // special type, no type validation performed
    }};

/**
   @brief Parameters struct for NMEA sentence
*/
const PROGMEM Parameters sentence_param[24] = {
    {uc_unrecognized,          // function ptr
     "$",                      // command string
     1,                        // string length
     root,                     // parent id
     root,                     // this command id
     root,                     // command depth
     23,                       // subcommands
     UI_ARG_HANDLING::no_args, // argument handling
     0,                        // minimum expected number of arguments
     0,                        // maximum expected number of arguments
     /*
       UITYPE arguments
     */
     {
         UITYPE::NOTYPE // special type, no type validation performed
     }},
    *GPAAM,
    *GPAPA,
    *GPAPB,
    *GPBOD,
    *GPBWC,
    *GPBWR,
    *GPDBT,
    *GPDPT,
    *GPGGA,
    *GPGLL,
    *GPGSA,
    *GPGSV,
    *GPHDM,
    *GPHDT,
    *GPHSC,
    *GPMTW,
    *GPRMB,
    *GPRMC,
    *GPVTG,
    *GPWCV,
    *GPWPL,
    *GPXTE,
    *GPXTR};

/**
   @brief Parameters struct for NMEA sentence error

*/
const PROGMEM Parameters sentence_error_param[24] = {
    {uc_unrecognized,          // function ptr
     "!",                      // command string
     1,                        // string length
     root,                     // parent id
     root,                     // this command id
     root,                     // command depth
     23,                       // subcommands
     UI_ARG_HANDLING::no_args, // argument handling
     0,                        // minimum expected number of arguments
     0,                        // maximum expected number of arguments
     /*
       UITYPE arguments
     */
     {
         UITYPE::NO_ARGS}},
    *GPAAM,
    *GPAPA,
    *GPAPB,
    *GPBOD,
    *GPBWC,
    *GPBWR,
    *GPDBT,
    *GPDPT,
    *GPGGA,
    *GPGLL,
    *GPGSA,
    *GPGSV,
    *GPHDM,
    *GPHDT,
    *GPHSC,
    *GPMTW,
    *GPRMB,
    *GPRMC,
    *GPVTG,
    *GPWCV,
    *GPWPL,
    *GPXTE,
    *GPXTR};
#endif