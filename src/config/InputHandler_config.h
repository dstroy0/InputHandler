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

//  uncomment to debug
//#define _DEBUG_USER_INPUT
#define _DEBUG_SUBCOMMAND_SEARCH

#define UI_INPUT_TYPE_STRINGS_MAX_LEN 14
#define UI_DEFAULT_STRINGS_MAX_LEN 14

//  maximum number of arguments per command
#ifndef USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS
#define USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS 32U
#endif

//  max value of a sixteen bit unsigned integer
#ifndef UINT16_MAX
#define UINT16_MAX 65535
#endif

//  max value of an eight bit unsigned integer
#ifndef UINT8_MAX
#define UINT8_MAX 255
#endif

//  maximum command length
#ifndef USER_INPUT_MAX_COMMAND_LENGTH
#define USER_INPUT_MAX_COMMAND_LENGTH 32
#endif

//  maximum user input length
#ifndef USER_INPUT_MAX_INPUT_LENGTH
#define USER_INPUT_MAX_INPUT_LENGTH UINT16_MAX
#endif

//  portability directives
#define UI_DEREFERENCE &
#define UI_PGM_READ_DWORD(x) pgm_read_dword(x)
#define UI_PGM_READ_BYTE(x) pgm_read_byte(x)
#define UI_SNPRINTF_P(s_, sz_, f_, ...) snprintf_P(s_, sz_, f_, ##__VA_ARGS__)
#define _N_ARGS(x) (sizeof(x) / sizeof((x)[0])) // gets the number of elements in an array

#if defined(ARDUINO_SAMD_VARIANT_COMPLIANCE)
#include <avr/dtostrf.h>
#endif

#if defined(__MBED_CONFIG_DATA__)
#include <avr/dtostrf.h>
#undef UI_DEREFERENCE
#define UI_DEREFERENCE
#undef UI_PGM_READ_DWORD
#define UI_PGM_READ_DWORD
#undef UI_SNPRINTF_P
#define UI_SNPRINTF_P(s_, sz_, f_, ...) snprintf(s_, sz_, f_, ##__VA_ARGS__)
#endif

#if defined(ARDUINO_SAM_DUE)
#undef UI_DEREFERENCE
#define UI_DEREFERENCE
#undef UI_PGM_READ_DWORD
#define UI_PGM_READ_DWORD
#undef UI_PGM_READ_BYTE
#define UI_PGM_READ_BYTE
#undef UI_SNPRINTF_P
#define UI_SNPRINTF_P(s_, sz_, f_, ...) snprintf(s_, sz_, f_, ##__VA_ARGS__)
#include <avr/dtostrf.h>
#endif

#endif