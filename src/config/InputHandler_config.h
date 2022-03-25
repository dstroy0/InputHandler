/**
   @file InputHandler_config.h
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief InputHandler library configuration file
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

#include <Arduino.h>

//  uncomment to debug functions (ensure you have a large enough output buffer)
//#define __DEBUG_USER_INPUT__
#if defined(__DEBUG_USER_INPUT__)
//#define __DEBUG_GET_TOKEN__
//#define __DEBUG_SUBCOMMAND_SEARCH__
#define __DEBUG_LAUNCH_LOGIC__
#define __DEBUG_LAUNCH_FUNCTION__
#endif

//  maximum number of arguments per command
#if !defined(UI_MAX_ARGS)
/*
  max is 255, 
  change to uint16_t
  _max_args_
  _data_pointers_index_
  _data_pointers_index_max_
  _rec_num_arg_strings_
  to increase max to 65535
*/
#define UI_MAX_ARGS 32  
#endif

//  maximum tree depth
#if !defined(UI_MAX_DEPTH)
/*
   max is 255,
   change to uint16_t
   _max_depth_
   _current_search_depth_
   to increase max to 65535
*/
#define UI_MAX_DEPTH 32
#endif

//  maximum number of subcommands
#if !defined(UI_MAX_SUBCOMMANDS)
/*
   max is 255,
   change to uint16_t
   _data_pointers_index_
   _data_pointers_index_max_
   _failed_on_subcommand_
   to increase max to 65535
*/
#define UI_MAX_SUBCOMMANDS 32
#endif

//  max value of a sixteen bit unsigned integer
#if !defined(UINT16_MAX)
#define UINT16_MAX 65535
#endif

//  max value of an eight bit unsigned integer
#if !defined(UINT8_MAX)
#define UINT8_MAX 255
#endif

//  maximum command length
#if !defined(UI_MAX_CMD_LEN)
#define UI_MAX_CMD_LEN 32
#endif

//  maximum user input length
#if !defined(UI_MAX_IN_LEN)
/*
   max is 65535 - 2
   change to (UINT32_MAX - 2) POTENTIALLY LOTS OF RAM!!!
   to increase UI_MAX_IN_LEN (2^32) - 2 
*/
#define UI_MAX_IN_LEN (UINT16_MAX - 2U)
#endif

#define _N_prms(x) (sizeof(x) / sizeof((x)[0])) // gets the number of elements in an array

// portability directives

#if defined(ARDUINO_SAMD_VARIANT_COMPLIANCE)
#include <avr/dtostrf.h>
#include "utility/vsnprintf.h"
#define vsnprintf_P vsnprintf
#endif

#if defined(__MBED_CONFIG_DATA__)
#include <avr/dtostrf.h>
#include "utility/vsnprintf.h"
#define vsnprintf_P vsnprintf
#undef pgm_read_dword
#define pgm_read_dword(addr) ({ \
  typeof(addr) _addr = (addr); \
  *(const unsigned long *)(_addr); \
})
#endif

#if defined(ARDUINO_SAM_DUE)
#include <avr/dtostrf.h>
#include "utility/vsnprintf.h"
#define vsnprintf_P vsnprintf
#undef pgm_read_dword
#define pgm_read_dword(addr) ({ \
  typeof(addr) _addr = (addr); \
  *(const unsigned long *)(_addr); \
})
#endif

#if defined(TEENSYDUINO)
// pgm/ram section type conflict fix
#define QUO(x) #x
#define QLINE(x,y) QUO(x)QUO(y)
#define PFIX QLINE(.progmem.variable, __COUNTER__)
#undef PROGMEM
#define PROGMEM __attribute__((section(PFIX)))
#endif

// PROGMEM width constants
#define UI_INPUT_TYPE_STRINGS_PGM_LEN 9
#define UI_ESCAPED_CHAR_PGM_LEN 3

#endif