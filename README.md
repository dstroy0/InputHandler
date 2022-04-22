<!-- markdownlint-disable MD041 -->
[![Arduino CLI CI](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_cli.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_cli.yml) [![PlatformIO arduino CI](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_pio.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_pio.yml) [![PlatformIO esp CI](https://github.com/dstroy0/InputHandler/actions/workflows/build_esp_pio.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/build_esp_pio.yml)  

[![Doxygen CI](https://github.com/dstroy0/InputHandler/actions/workflows/doxygen.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/doxygen.yml) [![src-cpp-linter CI](https://github.com/dstroy0/InputHandler/actions/workflows/lib_cpp_linter.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/lib_cpp_linter.yml)  

## WARNING
This library is in the prerelease stage. It is being updated frequently, none of the examples are guaranteed to work and the API may undergo drastic changes without warning.  It is a work in progress nearing completion.

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

# InputHandler

This library is meant to assist in interfacing with hardware, either through a buffer, or a [Stream](https://www.arduino.cc/reference/en/language/functions/communication/stream/).  
Commands have a [general tree structure](https://www.cs.cmu.edu/~clo/www/CMU/DataStructures/Lessons/lesson4_1.htm), each command has its own [Parameters](https://dstroy0.github.io/InputHandler/html/d0/dbf/struct_parameters.html) container that holds all pertinient command information, subcommands, and argument-types which are stored in PROGMEM.  

Individual commands that do not contain a wildcard character (each call to [CommandConstructor](https://dstroy0.github.io/InputHandler/html/df/d68/class_command_constructor.html)) use 8 bytes of RAM (avr).  Commands that contain wildcards use more, how much they use depends on the placement of the wildcard characters, and the command length.  

To make matching more performant, [memcmp](https://www.cplusplus.com/reference/cstring/memcmp/) ranges are computed at runtime for each command, each memcmp range that needs to be remembered uses `command((1 + (1 + 1*n_wcc_containing_prm) + 1) + n_memcmp_ranges*2)` bytes.  `****`, `8***`, `*8**`, `**8*`, `***8` would compute one memcmp range `8**8` computes as two, `8888` doesn't have any wcc, so it would undergo "length of input" memcmp.  Memcmp ranges are command-wide, if you have a nested command it will only have one associated `CommandRuntimeCalc` struct.

Check out the [examples](https://github.com/dstroy0/InputHandler/tree/main/examples) for different use cases.    

[This library is easy to start using](https://github.com/dstroy0/InputHandler/blob/main/examples/arduino/basic/GetCommandFromStream/GetCommandFromStream.ino), command length does not matter, any printable char or control char that is not your end of line character, token delimiter, or c-string delimiter is a valid command.  You can have as many (up to [UI_MAX_ARGS](https://dstroy0.github.io/InputHandler/html/dd/d4e/_input_handler__config_8h.html#a72f41b83365fd2261e5ddfacd27bb8a5)) or as few arguments (`0` minimum) as you wish.  

A valid (default-settings) command string would look something like:  

```text
your_command arg1 arg... "c-string args can have spaces and are enclosed with quotes"
your_command subcommand1 subcommand2 ... subcommandN subcommand_arg1 subcommand_arg2 ...
```

The first library object that needs to be initialized is the constructor for the [UserInput](https://dstroy0.github.io/InputHandler/html/dc/d4b/class_user_input.html#a62df272305fd09fc81023c316c7002e1) class:  
```cpp
/*
  UserInput constructor
*/
char output_buffer[650] = {'\0'}; //  output buffer

const PROGMEM IH_pname pname = "_test_";   ///< default process name
const PROGMEM IH_eol peol = "\r\n";        ///< default process eol characters
const PROGMEM IH_input_cc pinputcc = "##"; ///< default input control character sequence
const PROGMEM IH_wcc pwcc = "*";           ///< default process wildcard character

const PROGMEM InputProcessDelimiterSequences pipdelimseq = {
  1,    ///< number of delimiter sequences
  {1},  ///< delimiter sequence lens
  {" "} ///< delimiter sequences
};

const PROGMEM InputProcessStartStopSequences pststpseq = {
  1,           ///< num start stop sequence pairs
  {1, 1},      ///< start stop sequence lens
  {"\"", "\""} ///< start stop sequence pairs
};

const PROGMEM InputProcessParameters input_prm[1] = {
  &pname,
  &peol,
  &pinputcc,
  &pwcc,
  &pipdelimseq,
  &pststpseq
};
UserInput inputHandler(output_buffer, buffsz(output_buffer), input_prm);

// or use default input parameters and define your output buffer
UserInput inputHandler(output_buffer, buffsz(output_buffer));

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

InputHandler uses [C++11 Aggregate initialization](https://en.cppreference.com/w/cpp/language/aggregate_initialization) for [Parameters](https://dstroy0.github.io/InputHandler/html/db/d11/struct_command_parameters.html) struct objects:  
```cpp  
struct CommandParameters
{
    void (*function)(UserInput*);      ///< void function pointer with UserInput class pointer parameter, void your_function(UserInput *inputProcess)
    bool has_wildcards;                ///< if true this command has one or more wildcard char
    char command[UI_MAX_CMD_LEN + 1U]; ///< command string + '\0'
    uint16_t command_length;           ///< command length in characters
    uint16_t parent_command_id;        ///< parent command's unique id root-65535
    uint16_t command_id;               ///< this command's unique id root-65535
    uint8_t depth;                     ///< command tree depth root-255
    uint8_t sub_commands;              ///< how many subcommands does this command have 0 - UI_MAX_SUBCOMMANDS
    UI_ARG_HANDLING argument_flag;     ///< argument handling flag
    uint8_t num_args;                  ///< minimum number of arguments this command expects 0 - UI_MAX_ARGS
    uint8_t max_num_args;              ///< maximum number of arguments this command expects 0 - UI_MAX_ARGS, cannot be less than num_args
    UITYPE arg_type_arr[UI_MAX_ARGS];  ///< argument UITYPE array
};
```  

Easily construct complex commands with subcommands, and enforce input type. Nested commands still only use 6 bytes of sram (avr):  

```cpp
/**
   @brief CommandParameters struct for help_

*/
const PROGMEM CommandParameters help_param[1] = {
  help,                  // this is allowed to be NULL, if this is NULL and the terminating subcommand function ptr is also NULL nothing will launch (error)
  no_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
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
CommandConstructor help_(help_param); //  help_ has a command string, and function specified

/**
   @brief CommandParameters struct for settings_

*/
const PROGMEM CommandParameters settings_param[1] = {
  settings,              // function ptr
  no_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
  "inputSettings",          // command string
  13,                       // command string characters
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
CommandConstructor settings_(settings_param); // settings_ has a command string, and function specified

/**
   @brief CommandParameters struct for test_

*/
const PROGMEM CommandParameters type_test_param[1] = {
  test_input_types,       // function ptr
  no_wildcards,              // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
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
    UITYPE::UINT8_T,    // 8-bit  uint
    UITYPE::UINT16_T,   // 16-bit uint
    UITYPE::UINT32_T,   // 32-bit uint
    UITYPE::INT16_T,    // 16-bit int
    UITYPE::FLOAT,      // 32-bit float
    UITYPE::CHAR,       // char
    UITYPE::START_STOP, // regex-like start stop char sequences
    UITYPE::NOTYPE      // special type, no type validation performed
  }
};
CommandConstructor test_(type_test_param);

// nest parameters like this

const PROGMEM CommandParameters nested_prms[3] =
{
  { // root command
    unrecognized,             // root command not allowed to be NULL
    no_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "launch",                 // command string
    6,                        // command string characters
    root,                     // parent id
    root,                     // this command id
    root,                     // command depth
    2,                        // subcommands
    UI_ARG_HANDLING::no_args, // argument handling
    0,                        // minimum expected number of arguments
    0,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NO_ARGS} // use NO_ARGS if the function expects no arguments  
  },
  { // subcommand depth one
    nest_one,                 // unique function
    no_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "one",                    // command string
    3,                        // command string characters
    root,                     // parent id
    1,                        // this command id
    1,                        // command depth
    0,                        // subcommands
    UI_ARG_HANDLING::no_args, // argument handling
    0,                        // minimum expected number of arguments
    0,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NO_ARGS} // use NO_ARGS if the function expects no arguments  
  },
  { // subcommand depth one
    nest_two,                 // unique function
    no_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "two",                    // command string
    3,                        // command string characters
    root,                     // parent id
    2,                        // this command id
    1,                        // command depth
    0,                        // subcommands
    UI_ARG_HANDLING::no_args, // argument handling
    0,                        // minimum expected number of arguments
    0,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NO_ARGS} // use NO_ARGS if the function expects no arguments    
  }
};
CommandConstructor nested_example_(nested_prms, nprms(nested_prms), 1);

// or this

const PROGMEM CommandParameters nest_one_[1] =
{ // subcommand depth one
    nest_one,                 // unique function
    no_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "one",                    // command string
    3,                        // command string characters
    root,                     // parent id
    1,                        // this command id
    1,                        // command depth
    0,                        // subcommands
    UI_ARG_HANDLING::no_args, // argument handling
    0,                        // minimum expected number of arguments
    0,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NO_ARGS} // use NO_ARGS if the function expects no arguments  
};

const PROGMEM CommandParameters nest_two_[1] =
{ // subcommand depth one
    nest_two,                 // unique function
    no_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "two",                    // command string
    3,                        // command string characters
    root,                     // parent id
    2,                        // this command id
    1,                        // command depth
    0,                        // subcommands
    UI_ARG_HANDLING::no_args, // argument handling
    0,                        // minimum expected number of arguments
    0,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NO_ARGS} // use NO_ARGS if the function expects no arguments    
};

const PROGMEM CommandParameters nested_prms[3] =
{
  { // root command
    unrecognized,             // root command not allowed to be NULL
    no_wildcards,             // no_wildcards or has_wildcards, default WildCard Character (wcc) is '*'
    "launch",                 // command string
    6,                        // command string characters
    root,                     // parent id
    root,                     // this command id
    root,                     // command depth
    2,                        // subcommands
    UI_ARG_HANDLING::no_args, // argument handling
    0,                        // minimum expected number of arguments
    0,                        // maximum expected number of arguments
    /* UITYPE arguments */
    {UITYPE::NO_ARGS} // use NO_ARGS if the function expects no arguments  
  },
  *nest_one_,
  *nest_two_
};
CommandConstructor nested_example_(nested_prms, nprms(nested_prms), 1);

```  

[NOTYPE](https://dstroy0.github.io/InputHandler/html/de/d8a/group___user_input.html#gga70e7c464dbd2c5c26fa63684d9dfdd70a0323d2829f046f18b7dbcc0f58f941bc) is a special argument type that doesn't perform any type-validation.  
[NO_ARGS](https://dstroy0.github.io/InputHandler/html/de/d8a/group___user_input.html#gga70e7c464dbd2c5c26fa63684d9dfdd70acd158bf723602ecc6429b5771682a716) is a special argument type that explicitly states you wish to pass no arguments.  
[nprms(x)](https://dstroy0.github.io/InputHandler/html/dd/d4e/_input_handler__config_8h.html#a478361b897ab0ecfafbf38dc51ca3586), [buffsz(x)](https://dstroy0.github.io/InputHandler/html/dd/d4e/_input_handler__config_8h.html#abd56e27b6e10765f411acdc3ef1b2178), and [nelems(x)](https://dstroy0.github.io/InputHandler/html/dd/d4e/_input_handler__config_8h.html#a2cecc0de5f5f7dbca96aff3cedf1a83a) are macros which return the number of elements in an array.  

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
