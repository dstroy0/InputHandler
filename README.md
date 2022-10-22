<!-- markdownlint-disable MD041 -->
![Alt text](https://github.com/dstroy0/InputHandler/blob/main/docs/img/_Logolarge.png?raw=true)  
[![Arduino CLI CI](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_cli.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_cli.yml) [![PlatformIO arduino CI](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_pio.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_pio.yml) [![PlatformIO esp CI](https://github.com/dstroy0/InputHandler/actions/workflows/build_esp_pio.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/build_esp_pio.yml)  [![src/ cpp linter](https://github.com/dstroy0/InputHandler/actions/workflows/lib_cpp_linter.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/lib_cpp_linter.yml)  

[![Docs CI](https://github.com/dstroy0/InputHandler/actions/workflows/docs.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/docs.yml) [![src-cpp-linter CI](https://github.com/dstroy0/InputHandler/actions/workflows/lib_cpp_linter.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/lib_cpp_linter.yml)  

# Bug reporting
Please report any bugs in InputHandler/src/ using [bug_report.md](https://github.com/dstroy0/InputHandler/blob/main/src/bug_report.md) at [InputHandler/src/ bug report forum](https://github.com/dstroy0/InputHandler/discussions/60)

# InputHandler README  

This library is meant to assist in interfacing with your hardware, either through a uint8_t buffer, or a [Stream](https://www.arduino.cc/reference/en/language/functions/communication/stream/), like a [Serial](https://www.arduino.cc/en/reference/serial) object.  
User-defined commands have a [general tree structure](https://www.cs.cmu.edu/~clo/www/CMU/DataStructures/Lessons/lesson4_1.htm), each command has its own [CommandParameters](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv417CommandParameters) struct which is stored in non-volatile program memory ([PROGMEM](https://www.arduino.cc/reference/en/language/variables/utilities/progmem/)).  

Individual commands that do not contain a wildcard character (each call to [CommandConstructor](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv418CommandConstructor)) use 8 bytes of RAM (avr).  Commands that contain wildcards use more, how much they use depends on the placement of the wildcard characters, and the command length.  

To make matching more performant, [memcmp](https://www.cplusplus.com/reference/cstring/memcmp/) ranges are computed at runtime for each command, each memcmp range that needs to be remembered uses `((1 + (1 + 1*n_wcc_containing_prm) + 1) + n_memcmp_ranges*2)` bytes.  `****`, `8***`, `*8**`, `**8*`, `***8` would compute one memcmp range `8**8` computes as two, `8888` doesn't have any wcc, so it would undergo "length of input" memcmp.  Memcmp ranges are command-wide, if you have a nested command it will only have one associated [CommandRuntimeCalc](https://dstroy0.github.io/InputHandler/dc/d3d/struct_command_runtime_calc.html) struct.  

Command length does not matter, any printable char or control char that is not your end of line character, token delimiter, or c-string delimiter is a valid command.  You can have up to [UI_MAX_ARGS_PER_COMMAND](https://dstroy0.github.io/InputHandler/lib/src/config/config_h_docs.html#c.UI_MAX_ARGS_PER_COMMAND) number of arguments.  At runtime, UserInput scans your input [CommandParameters](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv417CommandParameters) and determines the maximum number of arguments you intend to use, it then allocates a dynamically sized array of flags (bit flags in a future feature) which lives for the duration of the process (one allocation per invocation of [UserInput::begin()](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv4N9UserInput5beginEv))  

[This library is easy to start using](https://github.com/dstroy0/InputHandler/blob/main/examples/all_platforms/basic/GetCommandFromStream/GetCommandFromStream.ino)  

Check out the [examples](https://github.com/dstroy0/InputHandler/tree/main/examples) for different use cases.  

Default InputHandler UserInput constructor initialization with no output:  
```cpp
/*
  InputHandler UserInput constructor
*/
UserInput inputHandler;
```

Default InputHandler UserInput constructor initialization with output buffer:
```cpp
/*
  InputHandler UserInput constructor
*/
char output_buffer[650] = {'\0'}; //  output buffer
UserInput inputHandler(output_buffer, buffsz(output_buffer));
```

A valid (default-settings) command string would look something like:  
```text
your_command arg_1 arg_2 arg... "arguments enclosed with start/stop delimiter sequences can have any char value 0-255, you can memcpy these argument types directly into a recipient struct (size - 1 to remove the null terminator) as uint8_t"
your_command subcommand_1 subcommand_2 ... subcommand_N subcommand_N_arg1 subcommand_N_arg2 ...
```  

You can also customize many aspects of input characteristics:  
```cpp
/*
  InputHandler UserInput constructor
*/
char output_buffer[650] = {'\0'}; //  output buffer

const PROGMEM IH_pname pname = "_test_";   // process name
const PROGMEM IH_eol peol = "\r\n";        // end of line characters
const PROGMEM IH_input_cc pinputcc = "##"; // input control character sequence
const PROGMEM IH_wcc pwcc = "*";           // process wildcard character

const PROGMEM InputProcessDelimiterSequences pipdelimseq = {
  1,    // number of delimiter sequences
  {1},  // delimiter sequence lens
  {" "} // delimiter sequences
};

const PROGMEM InputProcessStartStopSequences pststpseq = {
  1,           // num start stop sequence pairs
  {1, 1},      // start stop sequence lens
  {"\"", "\""} // start stop sequence pairs
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
```

The classes' input methods are:  

```cpp
void getCommandFromStream(Stream &stream, size_t rx_buffer_size = 32);
```

Or, if you don't want to use a [Stream](https://www.arduino.cc/reference/en/language/functions/communication/stream/) object use:  

```cpp
void readCommandFromBuffer(uint8_t *data, size_t len);
```

InputHandler uses [C++11 Aggregate initialization](https://en.cppreference.com/w/cpp/language/aggregate_initialization) for [CommandParameters](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv417CommandParameters) struct objects.

Easily construct complex commands with subcommands, and enforce input type. Nested commands with no wildcards use 8 bytes of sram (avr). 

[NOTYPE](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv4N6UITYPE6NOTYPEE) is a special argument type that doesn't perform any type-validation (input any char!).  
[NO_ARGS](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv4N6UITYPE7NO_ARGSE) is a special argument type that explicitly states you wish to pass no arguments.  
[nprms(x)](https://dstroy0.github.io/InputHandler/lib/src/config/noedit_h_docs.html#c.nprms), [buffsz(x)](https://dstroy0.github.io/InputHandler/lib/src/config/noedit_h_docs.html#c.buffsz), and [nelems(x)](https://dstroy0.github.io/InputHandler/lib/src/config/noedit_h_docs.html#c.nelems) are macros which return the number of elements in an array.  

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

# Design Goals
Implementation flexibility.  
Low memory use, feature rich.  
Ease of use.  
It satisfies some advanced interfacing requirements.  
It can parse uint8_t, unsigned char, any value 0-255 char strings.  
It can be used to interface your project with other equipment, programs, and sensors.  

# News

See the releases' descriptions on
[the library's release page](https://github.com/dstroy0/InputHandler/releases) for a list of
changes.

# Supported Platforms

Not supported:  
ATTiny85 -- memory/flash  
ATMegaNG -- flash  

If your board is not listed as not supported open an issue if you'd like it added to build coverage.  

NOTE: [vsnprintf](https://en.cppreference.com/w/c/io/vfprintf) and 
[dtostrf](https://www.delftstack.com/howto/arduino/arduino-dtostrf/) implemented on the following platforms:  
(see: [src/config/noedit.h](https://github.com/dstroy0/InputHandler/blob/main/src/config/noedit.h) for your platform's implementation)  
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

# Docs note
The docs use a feature not supported by every browser to jump to C++ source text.  Source links will still take you to the source file, but to take advantage of [url-scroll-to-text-fragment](https://caniuse.com/url-scroll-to-text-fragment) you need to use a supported browser, like chrome.  Alternatively you can install an addon into firefox [auto find text fragment](https://addons.mozilla.org/en-US/firefox/addon/auto-find-text-fragment/) to enable the functionality.