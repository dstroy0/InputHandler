/* Generated by cli_gen_tool version <1.0>; using InputHandler version <0.9a> */
/**
* @file functions.h
* @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
* @brief InputHandler autogenerated functions.h
* @version 1.0
* @date 2023-02-12
*
* @copyright Copyright (c) 2023
*/
/*
* Copyright (c) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
*
* License: GNU GPL3
* This program is free software; you can redistribute it and/or
* modify it under the terms of the GNU General Public License
* version 3 as published by the Free Software Foundation.
*/


#if !defined(__FUNCTIONS_H__)
    #define __FUNCTIONS_H__
    #include "InputHandler.h"    


/* InputHandler user return function prototypes */

extern void test(UserInput* _inputHandler);
extern void testa(UserInput* _inputHandler);
extern void testb(UserInput* _inputHandler);
extern void testc(UserInput* _inputHandler);
extern void testd(UserInput* _inputHandler);
extern void teste(UserInput* _inputHandler);
extern void testf(UserInput* _inputHandler);
extern void testg(UserInput* _inputHandler);

/* InputHandler builtin functions */

void unrecognized(UserInput* _inputHandler){ _inputHandler->outputToStream(Serial);}
void listCommands(UserInput* _inputHandler){ _inputHandler->listCommands();}
void listSettings(UserInput* _inputHandler){ _inputHandler->listSettings(_inputHandler);}

/* InputHandler user defined functions */

void test_2(UserInput* _inputHandler){test(_inputHandler);}
void testa_3(UserInput* _inputHandler){testa(_inputHandler);}
void testb_4(UserInput* _inputHandler){testb(_inputHandler);}
void testc_5(UserInput* _inputHandler){testc(_inputHandler);}
void testd_6(UserInput* _inputHandler){testd(_inputHandler);}
void teste_7(UserInput* _inputHandler){teste(_inputHandler);}
void testf_8(UserInput* _inputHandler){testf(_inputHandler);}
void testg_9(UserInput* _inputHandler){testg(_inputHandler);}

#endif

// end of file
