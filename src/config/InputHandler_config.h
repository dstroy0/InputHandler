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

//  uncomment to debug functions
//#define __DEBUG_USER_INPUT__
#if defined(__DEBUG_USER_INPUT__)
//#define __DEBUG_GET_TOKEN__
#define __DEBUG_SUBCOMMAND_SEARCH__
#define __DEBUG_LAUNCH_LOGIC__
#define __DEBUG_LAUNCH_FUNCTION__
#endif

//  maximum number of arguments per command
#if !defined(UI_MAX_ARGS)
#define UI_MAX_ARGS 32
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
#define UI_MAX_IN_LEN UINT16_MAX
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
#endif

#if defined(ARDUINO_SAM_DUE)
#include <avr/dtostrf.h>
#include "utility/vsnprintf.h"
#define vsnprintf_P vsnprintf
#endif

// PROGMEM width constants
#define UI_INPUT_TYPE_STRINGS_MAX_LEN 14
#define UI_DEFAULT_STRINGS_MAX_LEN 14

#endif