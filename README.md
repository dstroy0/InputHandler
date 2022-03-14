<!-- markdownlint-disable MD041 -->
[![Arduino CLI CI](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_cli.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_cli.yml) [![PlatformIO arduino CI](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_pio.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_pio.yml) [![PlatformIO esp CI](https://github.com/dstroy0/InputHandler/actions/workflows/build_esp_pio.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/build_esp_pio.yml)  

[![Doxygen CI](https://github.com/dstroy0/InputHandler/actions/workflows/doxygen.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/doxygen.yml) [![src-cpp-linter CI](https://github.com/dstroy0/InputHandler/actions/workflows/lib_cpp_linter.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/lib_cpp_linter.yml)  

# InputHandler

Arduino user input handler:  
Executes arbitrary functions by matching user input command strings.  Feature rich, low memory use.  Each CommandConstructor uses just 6 bytes of RAM (avr).

Check out the examples for different use cases.  You can use this library to build a remote cli for your equipment.  

Commands are simple to setup, command length does not matter, any printable char or control char that is not your end of line character, token delimiter, or c-string delimiter is a valid command.  You can have as many (up to `UI_MAX_ARGS`) or as few arguments (`0` minimum) as you wish.

A command string looks like:  

```text
your_command arg1 arg... "c-string args can have spaces and are enclosed with quotes"
your_command subcommand1 subcommand2 ... subcommandN subcommand_arg1 subcommand_arg2 ...
```

The classes' input methods are:  

```cpp
void GetCommandFromStream(Stream &stream, size_t rx_buffer_size = 32);
```

OR if you don't want to use a [Stream](https://www.arduino.cc/reference/en/language/functions/communication/stream/) object use:  

```cpp
void ReadCommandFromBuffer(uint8_t *data, size_t len);
```

InputHandler uses [Aggregate initialization](https://en.cppreference.com/w/cpp/language/aggregate_initialization) for `Parameters` struct objects:  
```cpp  
struct Parameters
{
    void (*function)(UserInput *);
    char command[UI_MAX_CMD_LEN];
    uint16_t command_length;
    uint8_t depth;
    uint8_t sub_commands;
    UI_ARGUMENT_FLAG_ENUM argument_flag;
    uint8_t num_args;
    uint8_t max_num_args;
    UITYPE _arg_type[UI_MAX_ARGS];
};
```  

Easily enforce input argument types and construct complex commands with subcommands:  

```cpp
// no arguments
const Parameters no_args_prm[1] PROGMEM =
    {   // func ptr
        func,         // this is allowed to be NULL, if this is NULL and the terminating subcommand function ptr is also NULL nothing will launch (error)
        "cmd_str",    // command string
        7,            // command string characters
        0,            // command depth
        0,            // subcommands
        no_arguments, // argument handling
        0,            // minimum expected number of arguments
        0,            // maximum expected number of arguments
        /*
          UITYPE arguments
        */
        {
            UITYPE::NO_ARGS // use NO_ARGS if the function expects no arguments
        }
    };
CommandConstructor your_command(no_args_prm);

// single argument type
const Parameters single_type_args_prm[1] PROGMEM =
    {   // func ptr
        func,                 // this is allowed to be NULL, if this is NULL and the terminating subcommand function ptr is also NULL nothing will launch (error)
        "cmd_str",            // command string
        7,                    // command string characters
        0,                    // command depth
        0,                    // subcommands
        single_type_argument, // argument handling
        1,                    // minimum expected number of arguments
        1,                    // maximum expected number of arguments
        /*
          UITYPE arguments
        */
        {   // any type except for NO_ARGS is allowed
            UITYPE::NOTYPE // NOTYPE is a special type that performs no type validation
        }
    };
CommandConstructor your_command(single_type_args_prm);

// argument array
const Parameters argument_type_array_prm[1] PROGMEM =
    {   // func ptr
        func,         // this is allowed to be NULL, if this is NULL and the terminating subcommand function ptr is also NULL nothing will launch (error)
        "cmd_str",    // command string
        7,            // command string characters
        0,            // command depth
        0,            // subcommands
        no_arguments, // argument handling
        8,            // minimum expected number of arguments
        8,            // maximum expected number of arguments
        /*
          UITYPE arguments
        */
        {
            UITYPE::UINT8_T,    // 8-bit  uint
            UITYPE::UINT16_T,   // 16-bit uint
            UITYPE::UINT32_T,   // 32-bit uint
            UITYPE::INT16_T,    // 16-bit int
            UITYPE::FLOAT,      // 32-bit float
            UITYPE::CHAR,       // char
            UITYPE::C_STRING,   // c-string, pass without quotes if there are no spaces, or pass with quotes if there are
            UITYPE::NOTYPE      // special type, no type validation performed
        }
    };
CommandConstructor your_command(argument_type_array_prm);

// nested parameters
const Parameters nested_cmd_prms_tree_depth_n[n] PROGMEM =
{
  any_prm_with_function_pointer,  // nested command parameters index zero needs a function pointer, else error
  any_prm_with_NULL_func_ptr_or_its_own_func_ptr_tree_depth_1,  // NULL func ptr defaults to element zero func ptr, or point this subcommand to its own func
  ...
};
CommandConstructor your_command(nested_cmd_prms, _N_prms(nested_cmd_prms), tree_depth);
```

Each call to CommandConstructor uses 6 bytes of RAM (avr).  It doesn't matter how many parameters it contains, the Parameters structures are stored in PROGMEM and read by UserInput's methods.

`NOTYPE` is a special argument type that doesn't perform any type-validation.  
`NO_ARGS` is a special argument type that explicitly states you wish to pass no arguments.  
`_N_prms(x)` is a macro which expands to `(sizeof(x) / sizeof((x)[0]))` it returns the number of elements in an array.  

Class output is enabled by defining a buffer, the class methods format the buffer into useful human readable information.  

This method will output to any stream (hardware or software Serial):  

```cpp
void OutputToStream(Stream &stream);
```

or, you can check to see if output is available with:  

```cpp
bool OutputIsAvailable();
```

and then when you are done with the output buffer, it needs to be reinitialized with:  

```cpp
void ClearOutputBuffer();
```

The input process will continue to function even if you do not define an output buffer.  

Target function will not execute if the command string does not match, or any arguments are type-invalid.  

# Supported Platforms

Not supported:  
ATTiny85 -- memory/flash  
ATMegaNG -- flash  

If your board is not listed as not supported open an issue if you'd like it added to build coverage.  

NOTE: vsnprintf and dtostrf implemented on the following platforms:  
(see: src/config/InputHandler_config.h portability directives subsection)  
SAMD,  
MBED,  
arduino DUE  

Build coverage:  

nano rp2040 connect  
teensy 3.1  
teensy 3.5  
teensy 3.6  
teensy 4.0  
teensy 4.1  
Espressif esp32dev generic ESP32  
Espressif Adafruit esp8266 huzzah  
yun  
uno  
diecimila  
nano  
mega  
megaADK  
leonardo  
micro  
esplora  
mini  
ethernet  
fio  
bt
LilyPadUSB  
pro 
robotControl  
robotMotor  
circuitplay32u4cat  
yunmini  
chiwawa  
one  
unowifi  
nano33ble  
mkr1000  
mkrzero  
mkrwifi1010  
nano_33_iot  
mkrfox1200  
mkrwan1300  
mkrwan1310  
mkrgsm1400  
mkrnb1500  
mkrvidor4000  
adafruit_circuitplayground_m0  
mzero_pro_bl  
mzero_bl  
tian  
uno2018  
due  
