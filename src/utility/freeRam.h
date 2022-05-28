/**
 * @file freeRam.h
 * @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
 * @brief cross platform freeRam()
 * @version 1.0
 * @date 2022-05-18
 *
 * @copyright Copyright (c) 2022
 */
/*
 Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 version 3 as published by the Free Software Foundation.
 */

#if !defined(__CROSS_PLATFORM_FREERAM_H__)
    #define __CROSS_PLATFORM_FREERAM_H__

    #include <Arduino.h>

    // avr
    // https://forum.arduino.cc/t/how-much-static-ram-is-used/84286/8
    #if defined(ARDUINO_ARCH_AVR)
        int freeRam()
        {
            extern int __heap_start, *__brkval;
            int v;
            return (int)&v - (__brkval == 0 ? (int)&__heap_start : (int)__brkval);
        }

    // esp "freeRam" built-in ESP.getFreeHeap()
    #elif defined(ESP32) || defined(ESP8266)
        #define freeRam() ESP.getFreeHeap()

    // teensy 4.x freeram()
    // Paul Stoffregen - https://forum.pjrc.com/threads/62104-Teensy-4-and-4-1-pre-processor-defines
    // Paul Stoffregen - https://forum.pjrc.com/threads/33443-How-to-display-free-ram
    #elif defined(DARDUINO_TEENSY41) || defined(DARDUINO_TEENSY4)
        extern unsigned long _heap_start;
        extern unsigned long _heap_end;
        extern char* __brkval;
        int freeRam()
        {
            return (char*)&_heap_end - __brkval;
        }

    // SAM, teensy3.x
    // Paul Stoffregen - https://forum.pjrc.com/threads/62104-Teensy-4-and-4-1-pre-processor-defines
    #elif (defined(__arm__) || defined(__ARM__)) && defined(DARDUINO_TEENSY31) || defined(DARDUINO_TEENSY32) || defined(DARDUINO_TEENSY35) || defined(DARDUINO_TEENSY36) || (ARDUINO > 103 && ARDUINO != 151) // arduino and teensy model macros
        #if defined(__arm__)
            extern "C" char* sbrk(int incr);
        #else
            extern char* __brkval;
        #endif
            int freeRam()
            {
                char top;
            #if defined(__arm__)
                return &top - reinterpret_cast<char*>(sbrk(0));
            #elif defined(DARDUINO_TEENSY31) || defined(DARDUINO_TEENSY32) || defined(DARDUINO_TEENSY35) || defined(DARDUINO_TEENSY36) || (ARDUINO > 103 && ARDUINO != 151) // arduino and teensy model macros
                return &top - __brkval;
            #else
                return __brkval ? &top - __brkval : &top - __malloc_heap_start;
            #endif
            }

    // add support
    #else
        #define freeRam() 0
    #endif

#endif

// end of file
