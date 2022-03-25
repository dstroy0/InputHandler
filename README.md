<!-- markdownlint-disable MD041 -->
[![Arduino CLI CI](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_cli.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_cli.yml) [![PlatformIO arduino CI](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_pio.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_pio.yml) [![PlatformIO esp CI](https://github.com/dstroy0/InputHandler/actions/workflows/build_esp_pio.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/build_esp_pio.yml)  

[![Doxygen CI](https://github.com/dstroy0/InputHandler/actions/workflows/doxygen.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/doxygen.yml) [![src-cpp-linter CI](https://github.com/dstroy0/InputHandler/actions/workflows/lib_cpp_linter.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/lib_cpp_linter.yml)  

## Design Goals
Low memory use, feature rich.  
InputHandler should be easy to use for beginners.  
It should satisfy some more advanced interfacing requirements.  
It should be able to parse uint8_t.  
It should be able to be used to interface with other equipment, programs, or sensors that output ASCII or uint8_t.  

## News

See the releases' descriptions on
[the library's release page](https://github.com/dstroy0/InputHandler/releases) for a list of
changes.

## InputHandler

This library is meant to assist in interfacing with hardware, either through a buffer, or a [Stream](https://www.arduino.cc/reference/en/language/functions/communication/stream/).  
Commands have a tree structure, each command has its own [Parameters](https://dstroy0.github.io/InputHandler/html/d0/dbf/struct_parameters.html) container that holds all pertinient command information, subcommands, and argument-types which are stored in PROGMEM.  

Individual commands (each call to CommandConstructor) use just 6 bytes of RAM (avr).  

Check out the examples for different use cases.    

Commands are simple to set up, command length does not matter, any printable char or control char that is not your end of line character, token delimiter, or c-string delimiter is a valid command.  You can have as many (up to [UI_MAX_ARGS](https://dstroy0.github.io/InputHandler/html/dd/d4e/_input_handler__config_8h.html#a72f41b83365fd2261e5ddfacd27bb8a5)) or as few arguments (`0` minimum) as you wish.  

A valid (default-settings) command string would look something like:  

```text
your_command arg1 arg... "c-string args can have spaces and are enclosed with quotes"
your_command subcommand1 subcommand2 ... subcommandN subcommand_arg1 subcommand_arg2 ...
```

The first library object that needs to be initialized is the constructor for the UserInput class:  
```cpp
/*
  UserInput constructor
*/
char output_buffer[512] = {'\0'};
UserInput inputHandler
(   /* UserInput's output buffer */ output_buffer,
    /* size of UserInput's output buffer */ buffSZ(output_buffer),
    /* username */ "",
    /* end of line characters */ "\r\n",
    /* token delimiter */ " ",
    /* c-string delimiter */ "\""
);
```

or, default-init with no output:  

```cpp
/*
  UserInput constructor
*/
UserInput inputHandler;
```

The classes' input methods are:  

```cpp
void getCommandFromStream(Stream &stream, size_t rx_buffer_size = 32);
```

OR if you don't want to use a [Stream](https://www.arduino.cc/reference/en/language/functions/communication/stream/) object use:  

```cpp
void readCommandFromBuffer(uint8_t *data, size_t len);
```

InputHandler uses [C++11 Aggregate initialization](https://en.cppreference.com/w/cpp/language/aggregate_initialization) for [Parameters](https://dstroy0.github.io/InputHandler/html/d0/dbf/struct_parameters.html) struct objects:  
```cpp  
struct Parameters
{
    void (*function)(UserInput *);    ///< function pointer
    char command[UI_MAX_CMD_LEN + 1]; ///< command string + '\0'
    uint16_t command_length;          ///< command length in characters
    uint8_t depth;                    ///< command tree depth
    uint8_t sub_commands;             ///< how many subcommands does this command have
    UI_ARG_HANDLING argument_flag;    ///< argument handling flag
    uint8_t num_args;                 ///< minimum number of arguments this command expects
    uint8_t max_num_args;             ///< maximum number of arguments this command expects
    UITYPE arg_type_arr[UI_MAX_ARGS]; ///< argument type array
};
```  

Easily construct complex commands with subcommands, and enforce input type. Nested commands still only use 6 bytes of sram (avr):  

```cpp
const PROGMEM Parameters help_param[1] =
{ 
  uc_help,                  // function pointer
  "help",                   // command string
  4,                        // command string characters
  root,                     // parent id
  root,                     // this command id
  root,                     // command depth
  0,                        // subcommands
  UI_ARG_HANDLING::no_args, // argument handling
  0,                        // minimum expected number of arguments
  0,                        // maximum expected number of arguments
  /*
    UITYPE arguments
  */
  {
    UITYPE::NO_ARGS // use NO_ARGS if the function expects no arguments
  }
};
CommandConstructor uc_help_(help_param); 

const PROGMEM Parameters settings_param[1] =
{
  uc_settings,     // function ptr
  "inputSettings", // command string
  13,              // command string characters
  root,            // parent id
  root,            // this command id
  root,            // command depth
  0,                        // subcommands
  UI_ARG_HANDLING::no_args, // argument handling
  0,                        // minimum expected number of arguments
  0,                        // maximum expected number of arguments
  /*
    UITYPE arguments
  */
  {
    UITYPE::NO_ARGS // use NO_ARGS if the function expects no arguments
  }
};
CommandConstructor uc_settings_(settings_param);

const PROGMEM Parameters type_test_param[1] = {
  uc_test_input_types,       // function ptr
  "test",                    // command string
  4,                         // string length
  root,                      // parent id
  root,                      // this command id
  root,                      // command depth
  0,                         // subcommands
  UI_ARG_HANDLING::type_arr, // argument handling
  8,                         // minimum expected number of arguments
  8,                         // maximum expected number of arguments
  /*
    UITYPE arguments
  */
  {
    UITYPE::UINT8_T,  // 8-bit  uint
    UITYPE::UINT16_T, // 16-bit uint
    UITYPE::UINT32_T, // 32-bit uint
    UITYPE::INT16_T,  // 16-bit int
    UITYPE::FLOAT,    // 32-bit float
    UITYPE::CHAR,     // char
    UITYPE::C_STRING, // c-string, pass without quotes if there are no spaces, or pass with quotes if there are
    UITYPE::NOTYPE    // special type, no type validation performed
  }
};
CommandConstructor uc_test_(type_test_param);

// nested parameters
const PROGMEM Parameters nested_prms[3] =
{
  { // root command
    uc_unrecognized,          // root command not allowed to be NULL
    "launch",                 // command string
    6,                        // command string characters
    root,                     // parent id
    root,                     // this command id
    root,                     // command depth
    2,                        // subcommands
    UI_ARG_HANDLING::no_args, // argument handling
    0,                        // minimum expected number of arguments
    0,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
      UITYPE::NO_ARGS // use NO_ARGS if the function expects no arguments
    }
  }, // end root
  { // command "launch" subcommand "one"
    uc_nest_one,              // function ptr (if NULL, root function is launched)
    "one",                    // command string
    3,                        // command string characters
    root,                     // parent id
    1,                        // this command id
    1,                        // command depth
    0,                        // subcommands
    UI_ARG_HANDLING::no_args, // argument handling
    0,                        // minimum expected number of arguments
    0,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
      UITYPE::NO_ARGS // use NO_ARGS if the function expects no arguments
    }
  },
  { // command "launch" subcommand "two"
    uc_nest_two,              // function ptr (if NULL, root function is launched)
    "two",                    // command string
    3,                        // command string characters
    root,                     // parent id
    2,                        // this command id
    1,                        // command depth
    0,                        // subcommands
    UI_ARG_HANDLING::no_args, // argument handling
    0,                        // minimum expected number of arguments
    0,                        // maximum expected number of arguments
    /*
      UITYPE arguments
    */
    {
      UITYPE::NO_ARGS // use NO_ARGS if the function expects no arguments
    }
  }
};
CommandConstructor uc_nested_example_(nested_prms, _N_prms(nested_prms), 1); // 
```

Each call to CommandConstructor uses 6 bytes of RAM (avr).  It doesn't matter how many parameters it contains, the Parameters structures are stored in PROGMEM and read by UserInput's methods (ultimately [memcpy_P](https://www.nongnu.org/avr-libc/user-manual/group__avr__pgmspace.html#gad92fa2ebe26e65fa424051047d21a0eb)).  

[NOTYPE](https://dstroy0.github.io/InputHandler/html/de/d8a/group___user_input.html#ga70e7c464dbd2c5c26fa63684d9dfdd70) is a special argument type that doesn't perform any type-validation.  
[NO_ARGS](https://dstroy0.github.io/InputHandler/html/de/d8a/group___user_input.html#ga70e7c464dbd2c5c26fa63684d9dfdd70) is a special argument type that explicitly states you wish to pass no arguments.  
[_N_prms(x)](https://dstroy0.github.io/InputHandler/html/dd/d4e/_input_handler__config_8h.html#acedaeea0ea767f43653abdf77453de79) is a macro which returns the number of elements in an array.  

Class output is enabled by defining a buffer, the class methods format the buffer into useful human readable information.  

This method will output to any stream (hardware or software Serial):  

```cpp
void outputToStream(Stream &stream);
```

or, you can check to see if output is available with:  

```cpp
bool outputIsAvailable();
```

and then when you are done with the output buffer, it needs to be reinitialized with:  

```cpp
void clearOutputBuffer();
```

The input process will continue to function even if you do not define an output buffer.  

Target function will not execute if the command string does not match, any arguments are type-invalid, or an unexpected amount of arguments are received.  

# Supported Platforms

Not supported:  
ATTiny85 -- memory/flash  
ATMegaNG -- flash  

If your board is not listed as not supported open an issue if you'd like it added to build coverage.  

NOTE: [vsnprintf](https://en.cppreference.com/w/c/io/vfprintf) and 
[dtostrf](https://www.delftstack.com/howto/arduino/arduino-dtostrf/) implemented on the following platforms:  
(see: [src/config/InputHandler_config.h](https://github.com/dstroy0/InputHandler/blob/main/src/config/InputHandler_config.h) portability directives subsection)  
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
