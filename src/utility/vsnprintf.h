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

#define va_start(v,l)	__builtin_va_start(v,l)
#define va_end(v)	__builtin_va_end(v)
#define va_arg(v,l)	__builtin_va_arg(v,l)

int	vsnprintf (char *__restrict, size_t, const char *__restrict, __VALIST)
               _ATTRIBUTE ((__format__ (__printf__, 3, 0)));

#endif

// end of file
