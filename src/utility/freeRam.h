#if !defined(__FREERAM_H__)
#define __FREERAM_H__

#include <Arduino.h>

int freeRam () 
{
  extern int __heap_start, *__brkval;
  int v;
  return (int) &v - (__brkval == 0 ? (int) &__heap_start : (int) __brkval);
}

#endif

// end of file
