/**
 * @file vsnprintf.h
 * @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
 * @brief InputHandler vsnprintf support
 * @version 1.0
 * @date 2022-10-05
 *
 * @copyright Copyright (c) 2022
 *
 */
/*
 Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 version 3 as published by the Free Software Foundation.
 */

#if !defined(__USER_INPUT_VSNPRINTF__)
    #define __USER_INPUT_VSNPRINTF__

    #if !defined(__va_list__)
typedef __gnuc_va_list va_list;
    #endif /* not __va_list__ */

    #if !defined(__VALIST)
        #ifdef __GNUC__
            #define __VALIST __gnuc_va_list
        #else
            #define __VALIST char*
        #endif
    #endif

    #define va_start(v, l) __builtin_va_start(v, l)
    #define va_end(v) __builtin_va_end(v)
    #define va_arg(v, l) __builtin_va_arg(v, l)

/**
 * @brief InputHandler vsnprintf
 * 
 * C99 vsnprintf
 * 
 *     int vsnprintf( char *restrict buffer, size_t bufsz,
 *         const char *restrict format, va_list vlist);
 * 
 * This variadic function writes to a predefined buffer.
 * 
 * [vsnprintf ref](https://cplusplus.com/reference/cstdio/vsnprintf/)
 * 
 */
int vsnprintf(char* __restrict, size_t, const char* __restrict, __VALIST)
    _ATTRIBUTE((__format__(__printf__, 3, 0)));

#endif

// end of file
