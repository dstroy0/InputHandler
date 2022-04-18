/**
   @file NMEAsentenceparam.h
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief NMEA 0183 sentence CommandParameters structs
   @version 1.0
   @date 2022-04-02

   @copyright Copyright (c) 2022
*/

#if !defined(__NMEAsentenceparam_H__)
    #define __NMEAsentenceparam_H__

    #include <InputHandler.h>
    #include "NMEAsentencefunc.h"

extern void uc_unrecognized(UserInput* inputProcess);
extern void NMEA_parse_test(UserInput* inputProcess);

/**
   @brief AAM NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters AAM[1] = {
    NMEA_0183_AAM,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**AAM",                   // command string
    5,                         // string length
    root,                      // parent id
    1,                         // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief APA NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters APA[1] = {
    NMEA_0183_APA,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**APA",                   // command string
    5,                         // string length
    root,                      // parent id
    2,                         // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief APB NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters APB[1] = {
    NMEA_0183_APB,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**APB",                   // command string
    5,                         // string length
    root,                      // parent id
    3,                         // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief BOD NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters BOD[1] = {
    NMEA_0183_BOD,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**BOD",                   // command string
    5,                         // string length
    root,                      // parent id
    4,                         // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief BWC NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters BWC[1] = {
    NMEA_0183_BWC,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**BWC",                   // command string
    5,                         // string length
    root,                      // parent id
    5,                         // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief BWR NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters BWR[1] = {
    NMEA_0183_BWR,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**BWR",                   // command string
    5,                         // string length
    root,                      // parent id
    6,                         // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief DBT NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters DBT[1] = {
    NMEA_0183_DBT,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**DBT",                   // command string
    5,                         // string length
    root,                      // parent id
    7,                         // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief DPT NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters DPT[1] = {
    NMEA_0183_DPT,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**DPT",                   // command string
    5,                         // string length
    root,                      // parent id
    8,                         // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief GGA NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters GGA[1] = {
    NMEA_0183_GGA,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**GGA",                   // command string
    5,                         // string length
    root,                      // parent id
    9,                         // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief GLL NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters GLL[1] = {
    NMEA_0183_GLL,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**GLL",                   // command string
    5,                         // string length
    root,                      // parent id
    10,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief GSA NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters GSA[1] = {
    NMEA_0183_GSA,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**GSA",                   // command string
    5,                         // string length
    root,                      // parent id
    11,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief GSV NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters GSV[1] = {
    NMEA_0183_GSV,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**GSV",                   // command string
    5,                         // string length
    root,                      // parent id
    12,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief HDM NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters HDM[1] = {
    NMEA_0183_HDM,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**HDM",                   // command string
    5,                         // string length
    root,                      // parent id
    13,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief HDT NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters HDT[1] = {
    NMEA_0183_HDT,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**HDT",                   // command string
    5,                         // string length
    root,                      // parent id
    14,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief HSC NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters HSC[1] = {
    NMEA_0183_HSC,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**HSC",                   // command string
    5,                         // string length
    root,                      // parent id
    15,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief MTW NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters MTW[1] = {
    NMEA_0183_MTW,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**MTW",                   // command string
    5,                         // string length
    root,                      // parent id
    16,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief RMB NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters RMB[1] = {
    NMEA_0183_RMB,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**RMB",                   // command string
    5,                         // string length
    root,                      // parent id
    17,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief RMC NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters RMC[1] = {
    NMEA_0183_RMC,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**RMC",                   // command string
    5,                         // string length
    root,                      // parent id
    18,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief VTG NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters VTG[1] = {
    NMEA_0183_VTG,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**VTG",                   // command string
    5,                         // string length
    root,                      // parent id
    19,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief WCV NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters WCV[1] = {
    NMEA_0183_WCV,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**WCV",                   // command string
    5,                         // string length
    root,                      // parent id
    20,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief WPL NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters WPL[1] = {
    NMEA_0183_WPL,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**WPL",                   // command string
    5,                         // string length
    root,                      // parent id
    21,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief XTE NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters XTE[1] = {
    NMEA_0183_XTE,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**XTE",                   // command string
    5,                         // string length
    root,                      // parent id
    22,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    0,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief XTR NMEA 0183 sentence command setup

*/
const PROGMEM CommandParameters XTR[1] = {
    NMEA_0183_XTR,             // function ptr
    has_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "**XTR",                   // command string
    5,                         // string length
    root,                      // parent id
    23,                        // this command id
    1,                         // command depth
    0,                         // subcommands
    UI_ARG_HANDLING::one_type, // argument handling
    1,                         // minimum expected number of arguments
    32,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NOTYPE} // special type, no type validation performed
};

/**
   @brief CommandParameters struct for NMEA sentence
*/
const PROGMEM CommandParameters sentence_param[24] = {
    {uc_unrecognized,          // function ptr
     no_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
     "$",                      // command string
     1,                        // string length
     root,                     // parent id
     root,                     // this command id
     root,                     // command depth
     23,                       // subcommands
     UI_ARG_HANDLING::no_args, // argument handling
     0,                        // minimum expected number of arguments
     0,                        // maximum expected number of arguments
     /* UITYPE arguments */
     {UITYPE::NO_ARGS}},
    *AAM,
    *APA,
    *APB,
    *BOD,
    *BWC,
    *BWR,
    *DBT,
    *DPT,
    *GGA,
    *GLL,
    *GSA,
    *GSV,
    *HDM,
    *HDT,
    *HSC,
    *MTW,
    *RMB,
    *RMC,
    *VTG,
    *WCV,
    *WPL,
    *XTE,
    *XTR};

/**
   @brief CommandParameters struct for NMEA sentence error
*/
const PROGMEM CommandParameters sentence_error_param[24] = {
    {uc_unrecognized,          // function ptr
     no_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
     "!",                      // command string
     1,                        // string length
     root,                     // parent id
     root,                     // this command id
     root,                     // command depth
     23,                       // subcommands
     UI_ARG_HANDLING::no_args, // argument handling
     0,                        // minimum expected number of arguments
     0,                        // maximum expected number of arguments
     /* UITYPE arguments */
     {UITYPE::NO_ARGS}},
    *AAM,
    *APA,
    *APB,
    *BOD,
    *BWC,
    *BWR,
    *DBT,
    *DPT,
    *GGA,
    *GLL,
    *GSA,
    *GSV,
    *HDM,
    *HDT,
    *HSC,
    *MTW,
    *RMB,
    *RMC,
    *VTG,
    *WCV,
    *WPL,
    *XTE,
    *XTR};
#endif
