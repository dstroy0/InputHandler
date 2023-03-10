[![Alt text](https://github.com/dstroy0/InputHandler/blob/main/docs/img/_Logolarge.png?raw=true)](https://github.com/dstroy0/InputHandler)

# InputHandler README

[It's easy to start using](https://github.com/dstroy0/InputHandler/blob/main/examples/all_platforms/basic/GetCommandFromStream/GetCommandFromStream.ino)

Check out the [examples](https://github.com/dstroy0/InputHandler/tree/main/examples) for different use cases.

This library is meant to assist in interfacing with your hardware, either through a uint8_t buffer, or a [Stream](https://www.arduino.cc/reference/en/language/functions/communication/stream/), such as a [Serial](https://www.arduino.cc/en/reference/serial) interface object.

Class output is enabled by defining a buffer, the class methods format the buffer into useful human readable information. [ih::Input](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv4N2ih5InputE) (the input parser) will function as normal without an output buffer.

Command length has no restrictions, any printable char or control char that is not your end of line character, token delimiter, or c-string delimiter is a valid commandString. You can have up to [config.h:IH_MAX_ARGS_PER_COMMAND](https://dstroy0.github.io/InputHandler/lib/src/config/config_h_docs.html#c.IH_MAX_ARGS_PER_COMMAND) number of arguments. At runtime, [ih::Input:addCommand()](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv4N2ih5Input10addCommandER7Command) scans [ih::Parameters](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv4N2ih10ParametersE) and determines the maximum number of arguments you intend to use, it then allocates a dynamically sized array of flags (bit flags in a future feature) which lives for the duration of the process (one allocation per invocation of [ih::Input::begin()](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv4N9Input5beginEv))  

User-defined commands have a [general tree structure](https://www.cs.cmu.edu/~clo/www/CMU/DataStructures/Lessons/lesson4_1.htm), each command has its own [ih::Parameters](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv4N2ih10ParametersE) struct which is stored in non-volatile program memory ([PROGMEM on Arduino platforms](https://www.arduino.cc/reference/en/language/variables/utilities/progmem/)).  

Individual commands that do not contain a wildcard character (each call to [ih::Command](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv4N2ih7CommandE)) use 8 bytes of RAM (on avr). Commands that contain wildcards use more, how much they use depends on the placement of the wildcard characters, and the command length.  

The [ih::Command](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv4N2ih7CommandE) [ih::Parameters](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv4N2ih10ParametersE) [target function](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv4N2ih10Parameters8functionE) will not execute if the input does not match the [ih::Command](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv4N2ih7CommandE) [ih::Parameters](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv4N2ih10ParametersE) [ih::Parameters::command](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv4N2ih10Parameters7commandE), if any arguments are type-invalid, or if an unexpected amount of arguments are received.  

To make [ih::Parameters::command](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv4N2ih10Parameters7commandE) matching more performant for [ih::Parameters::command](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv4N2ih10Parameters7commandE) which contain one or more [ih::WildcardChar](https://dstroy0.github.io/InputHandler/lib/src/config/utility/namespace_h_docs.html#_CPPv4N2ih12WildcardCharE), [memcmp](https://www.cplusplus.com/reference/cstring/memcmp/) ranges are computed at runtime for each command, each memcmp range that needs to be remembered uses `((1 + (1 + 1*n_wcc_containing_prm) + 1) + n_memcmp_ranges*2)` bytes. `****`, `8***`, `*8**`, `**8*`, `***8` would compute one memcmp range `8**8` computes as two, `8888` doesn't have any wcc, so it would undergo "length of input" memcmp. Memcmp ranges are command-wide, if you have a nested command it will only have one associated [ih::CommandRuntimeCalc](https://dstroy0.github.io/InputHandler/lib/src/config/utility/namespace_h_docs.html#_CPPv4N2ih18CommandRuntimeCalcE) struct.  

InputHandler uses [C++11 Aggregate initialization](https://en.cppreference.com/w/cpp/language/aggregate_initialization) for [ih::Parameters](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv4N2ih10ParametersE) and [ih::InputParameters](https://dstroy0.github.io/InputHandler/lib/src/config/utility/namespace_h_docs.html#_CPPv4N2ih15InputParametersE) structs.  

Class output is enabled by defining a buffer, the class methods format the buffer into useful human readable information.

Default InputHandler Input constructor initialization with no output:

```cpp
/*
  InputHandler default Input constructor uses InputParameters variables defined in the namespace ihc src/config/utility/namespace.h
*/
#include <InputHandler.h>
using namespace ih;

Input inputHandler;
```

Default InputHandler Input constructor initialization with output buffer:

```cpp
/*
  InputHandler default Input constructor uses InputParameters variables defined in the namespace ihc src/config/utility/namespace.h
  This constructor will output messages into `output_buffer`, you can check to see if there's a message with ih::Input::isOutputAvailable()
*/
#include <InputHandler.h>
using namespace ih;
char output_buffer[512] = {'\0'}; //  output buffer
Input inputHandler(output_buffer, buffsz(output_buffer)); // Input constructor with output buffer and buffer length
```

Many aspects of [InputParameters](https://dstroy0.github.io/InputHandler/lib/src/config/utility/namespace_h_docs.html#_CPPv4N2ih15InputParametersE) are customizable:

```cpp
#include <InputHandler.h>
using namespace ih;

// char array typdef aliases
const PROGMEM ProcessName process_name = "_test_"; // process name
const PROGMEM EndOfLineChar process_eol = "\r\n";  // end of line characters
const PROGMEM ControlCharSeq process_ccseq = "##"; // input control character sequence
const PROGMEM WildcardChar process_wcc = "*";      // process wildcard character

// ih_auto::size_t, {ih_auto::size_t,...}, {ih_auto::char_array,...}
const PROGMEM DelimiterSequences process_delimseq = {
  1,    // number of delimiter sequences
  {1},  // delimiter sequence lens
  {" "} // delimiter sequences
};

// ih_auto::size_t, {ih_auto::size_t,...}, {ih_auto::char_array,...}
const PROGMEM StartStopSequences process_ststpseq = {
  1,           // num start stop sequence pairs
  {1, 1},      // start stop sequence lens
  {"\"", "\""} // start stop sequence pairs
};

const PROGMEM InputParameters input_prm[1] = {
  &process_name,
  &process_eol,
  &process_ccseq,
  &process_wcc,
  &process_delimseq,
  &process_ststpseq
};

char output_buffer[512] = {'\0'}; //  output buffer
Input inputHandler(input_prm, output_buffer, buffsz(output_buffer)); // Input constructor
```

A valid command string would look like this with the above [InputParameters](https://dstroy0.github.io/InputHandler/lib/src/config/utility/namespace_h_docs.html#_CPPv4N2ih15InputParametersE):

```text
your_command arg_1 arg_2 arg... "arguments enclosed with start/stop delimiter sequences can have any char value 0-255, you can memcpy these argument types directly into a recipient struct (size - 1 to remove the null terminator) as uint8_t"
your_command subcommand_1 subcommand_2 ... subcommand_N subcommand_N_arg1 subcommand_N_arg2 ...
y*ur_co***** ...
```

[ih::Input's](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv4N2ih5InputE) input methods are:

```cpp
void getCommandFromStream(Stream &stream, size_t rx_buffer_size = IH_MAX_PROC_INPUT_LEN);
```

Or, if you don't want to use a [Stream](https://www.arduino.cc/reference/en/language/functions/communication/stream/) object use this method instead:

```cpp
void readCommandFromBuffer(uint8_t *data, size_t len);
```

This method will output to any initialized stream (hardware or software Serial):

```cpp
void ih::Input::outputToStream(Stream &stream);
```

or, you can check to see if ihout output is available with:

```cpp
bool ih::Input::outputIsAvailable();
```

and then when you are done with the output buffer, it needs to be reinitialized with:

```cpp
void ih::Input::clearOutputBuffer();
```

# Bug Reporting

Please report any bugs in InputHandler/src/ using [bug_report.md](https://github.com/dstroy0/InputHandler/blob/main/src/bug_report.md) at [InputHandler/src/ bug report forum](https://github.com/dstroy0/InputHandler/discussions/60)

# Library Build Status

[![Adafruit platforms](https://github.com/dstroy0/InputHandler/actions/workflows/adafruit_platforms.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/adafruit_platforms.yml)  
[![Arduino platforms](https://github.com/dstroy0/InputHandler/actions/workflows/arduino_platforms.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/arduino_platforms.yml)  
[![ESP32 platforms](https://github.com/dstroy0/InputHandler/actions/workflows/esp32_platforms.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/esp32_platforms.yml)  
[![ESP8266 platforms](https://github.com/dstroy0/InputHandler/actions/workflows/esp8266_platforms.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/esp8266_platforms.yml)  
[![RPi platforms](https://github.com/dstroy0/InputHandler/actions/workflows/rpi_platforms.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/rpi_platforms.yml)  
[![Teensyduino platforms](https://github.com/dstroy0/InputHandler/actions/workflows/teensyduino_platforms.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/teensyduino_platforms.yml)

# Docs Build Status

[![Docs CI](https://github.com/dstroy0/InputHandler/actions/workflows/docs.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/docs.yml)

# Source Format Conformity

[![src-cpp-linter CI](https://github.com/dstroy0/InputHandler/actions/workflows/lib_cpp_linter.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/lib_cpp_linter.yml)

# Prebuilt cli_gen_tool Binaries

Made with [PyInstaller](https://pyinstaller.org/en/stable/)

[![Download for linux](https://img.shields.io/badge/Download-for%20Linux-brightgreen?style=plastic&logo=linux)](https://github.com/dstroy0/InputHandler/raw/binaries/latest/linux/cli_gen_tool.zip)[![build linux binary](https://github.com/dstroy0/InputHandler/actions/workflows/bld_tool_bin_linux_latest.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/bld_tool_bin_linux_latest.yml)  

[![Download for macos](https://img.shields.io/badge/Download-for%20macOS-brightgreen?style=plastic&logo=macos)](https://github.com/dstroy0/InputHandler/raw/binaries/latest/macos/cli_gen_tool.zip)[![build macos binary](https://github.com/dstroy0/InputHandler/actions/workflows/bld_tool_bin_macos_latest.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/bld_tool_bin_macos_latest.yml)  

[![Download for windows](https://img.shields.io/badge/Download-for%20Windows-brightgreen?style=plastic&logo=windows)](https://github.com/dstroy0/InputHandler/raw/binaries/latest/windows/cli_gen_tool.zip)[![build windows binary](https://github.com/dstroy0/InputHandler/actions/workflows/bld_tool_bin_windows_latest.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/bld_tool_bin_windows_latest.yml)

# Design Goals

Ease of use.  
Implementation and platform flexibility.  
Feature rich.  
Low memory use.  
Parse uint8_t, any value 0-255 char array.  
Inter equipment interfacing.  
Construct complex commands with subcommands, and enforce the input type.  
Nested commands with no wildcards use 8 bytes or less of sram (avr).

# News

See the releases' descriptions on
[the library's release page](https://github.com/dstroy0/InputHandler/releases) for a list of
changes.

# Supported Platforms

Not supported:  
ATTiny85 -- memory/flash  
ATMegaNG -- flash  
adafruit:samd:adafruit_neotrinkey_m0 -- doesn't build  
adafruit:samd:adafruit_pybadge_airlift_m4 -- doesn't build  
arduino:samd:nano_33_iot -- doesn't build

If your board is not listed as not supported open an issue if you'd like it added to build coverage.

NOTE: [vsnprintf](https://en.cppreference.com/w/c/io/vfprintf) and
[dtostrf](https://www.delftstack.com/howto/arduino/arduino-dtostrf/) implemented on the following platforms:  
(see: [src/config/noedit.h](https://github.com/dstroy0/InputHandler/blob/main/src/config/noedit.h) for your platform's implementation)  
SAMD,  
MBED,  
arduino DUE

Build coverage:  
[Arduino](https://github.com/dstroy0/InputHandler/blob/main/supported_boards/arduino.txt)  
[platformIO](https://github.com/dstroy0/InputHandler/blob/main/supported_boards/platformio.txt)  

# InputHandler library documentation note

The docs use a feature not supported by every browser to jump to C++ source text. Source links will still take you to the source file, but to take advantage of [url-scroll-to-text-fragment](https://caniuse.com/url-scroll-to-text-fragment) you need to use a supported browser, like chrome. Alternatively you can install an addon into firefox [auto find text fragment](https://addons.mozilla.org/en-US/firefox/addon/auto-find-text-fragment/) to enable the functionality.
