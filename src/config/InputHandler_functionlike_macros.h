#if !defined(__INPUTHANDLER_FUNCTIONLIKE_MACROS_H__)
#define __INPUTHANDLER_FUNCTIONLIKE_MACROS_H__

// function-like macros
#define nprms(x)  (sizeof(x) / sizeof((x)[0])) // gets the number of elements in an array
#define buffsz(x) nprms(x)                     // gets the number of elements in an array
#define nelems(x) nprms(x)                     // gets the number of elements in an array

#endif // include guard
// end of file
