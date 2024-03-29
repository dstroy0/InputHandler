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

    /**
     * @def va_start
     * @brief initializes va_list variable used with vsnprintf.h::va_arg and vsnprintf.h::va_end
     *
     * [va_start ref](https://www.tutorialspoint.com/c_standard_library/c_macro_va_start.htm)
     */
    #define va_start(v, l) __builtin_va_start(v, l)
    /**
     * @def va_end
     * @brief allows a function with arguments that used va_start to return.
     *
     * If va_end is not called after using va_start before returning from
     * the function, the result is undefined.
     *
     * [va_end ref](https://www.tutorialspoint.com/c_standard_library/c_macro_va_end.htm)
     */
    #define va_end(v) __builtin_va_end(v)
    /**
     * @def va_arg
     * @brief retrieves the next argument in the parameter list (va_list)
     *
     * No indication when reaching the tail of arguments passed.
     *
     * [va_arg ref](https://www.tutorialspoint.com/c_standard_library/c_macro_va_arg.htm)
     */
    #define va_arg(v, l) __builtin_va_arg(v, l)

    /**
     * @brief InputHandler vsnprintf
     *
     * InputHandler vsnprintf [vsnprintf ref](https://cplusplus.com/reference/cstdio/vsnprintf/)
     *
     * @code{.c}
     * int vsnprintf(char* __restrict, size_t, const char* __restrict, __VALIST)
     *     _ATTRIBUTE((__format__(__printf__, 3, 0)));
     * @endcode
     *
     * @param[in] str pointer to a buffer where the C-string is stored
     * @param[in] size maximum number of bytes to write into the buffer
     * @param[in] format C string that contains a format string which follows the same
     * specifications as `format` in `printf` [printf
     * ref](https://cplusplus.com/reference/cstdio/printf/)
     * @param[in] args the argument list (va_list)
     * @returns The number of bytes written to str
     */
    #if defined(DOXYGEN_XML_BUILD)
int vsnprintf(char* str, size_t size, const char* format, va_list args);
    #else
/** @cond */
int vsnprintf(char* __restrict, size_t, const char* __restrict, __VALIST)
    _ATTRIBUTE((__format__(__printf__, 3, 0)));

    /** @endcond */
    #endif
#endif

// end of file
