/**
   @file InputHandler_functionlike_macros.h
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief InputHandler library function-like macros
   @version 1.0
   @date 2022-05-10

   @copyright Copyright (c) 2022
*/
/*
 Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>

 This program is free software; you can redistribute it and/or
 modify it under the terms of the GNU General Public License
 version 3 as published by the Free Software Foundation.
 */

#if !defined(__INPUTHANDLER_FUNCTIONLIKE_MACROS_H__)
    #define __INPUTHANDLER_FUNCTIONLIKE_MACROS_H__

    // function-like macros
    #define nprms(x) (sizeof(x) / sizeof((x)[0])) // gets the number of elements in an array
    #define buffsz(x) nprms(x)                    // gets the number of elements in an array
    #define nelems(x) nprms(x)                    // gets the number of elements in an array

#endif // include guard
// end of file
