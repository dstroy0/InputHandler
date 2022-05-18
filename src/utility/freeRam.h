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

    // not esp32 or esp8266 freeRam()
    // https://forum.arduino.cc/t/how-much-static-ram-is-used/84286/8
    #if !defined(ESP32) || !defined(ESP8266)
        int freeRam()
        {
          extern int __heap_start, *__brkval;
          int v;
          return (int)&v - (__brkval == 0 ? (int)&__heap_start : (int)__brkval);
        }
    #endif

    // esp "freeRam" built-in ESP.getFreeHeap()
    #if defined(ESP32) || defined(ESP8266)
        #define freeRam() ESP.getFreeHeap()
    #endif

#endif

// end of file
