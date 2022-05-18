#if !defined(__FREERAM_H__)
    #define __FREERAM_H__

    #include <Arduino.h>

    // not esp32 or esp8266 freeRam()
    #if !defined(ESP32) || !defined(ESP8266)
        int freeRam()
        {
          extern int __heap_start, *__brkval;
          int v;
          return (int)&v - (__brkval == 0 ? (int)&__heap_start : (int)__brkval);
        }
    #endif

    // esp "freeRam" built-in ESP.getFreeHeap
    #if defined(ESP32) || defined(ESP8266)
        #define freeRam() ESP.getFreeHeap()
    #endif

#endif

// end of file
