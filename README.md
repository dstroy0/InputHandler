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

To make input matching more performant, [ih::Parameters::command](https://dstroy0.github.io/InputHandler/lib/src/InputHandler_h_docs.html#_CPPv4N2ih10Parameters7commandE) that contain one or more [ih::WildcardChar](https://dstroy0.github.io/InputHandler/lib/src/config/utility/namespace_h_docs.html#_CPPv4N2ih12WildcardCharE) have their [memcmp](https://www.cplusplus.com/reference/cstring/memcmp/) ranges computed at runtime for each command containing a wildcard char, each memcmp range that needs to be remembered uses `((1 + (1 + 1*n_wcc_containing_prm) + 1) + n_memcmp_ranges*2)` bytes. `****`, `8***`, `*8**`, `**8*`, `***8` would compute one memcmp range `8**8` computes as two, `8888` doesn't have any wcc, so it would undergo "length of input" memcmp. Memcmp ranges are command-wide, if you have a nested command it will only have one associated [ih::CommandRuntimeCalc](https://dstroy0.github.io/InputHandler/lib/src/config/utility/namespace_h_docs.html#_CPPv4N2ih18CommandRuntimeCalcE) struct.  

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
&nbsp;
&nbsp;
&nbsp;
&nbsp;

# Changelog

Generated by [`auto-changelog`](https://github.com/CookPete/auto-changelog).

## [v0.0.11](https://github.com/dstroy0/InputHandler/compare/v0.0.11...v0.0.11)

## v0.0.11 - 2023-11-03

### Merged

- Lib dev [`#71`](https://github.com/dstroy0/InputHandler/pull/71)
- Create CODE_OF_CONDUCT.md [`#65`](https://github.com/dstroy0/InputHandler/pull/65)
- User input ctor overhaul [`#42`](https://github.com/dstroy0/InputHandler/pull/42)
- Ih input behavior refactor [`#18`](https://github.com/dstroy0/InputHandler/pull/18)
- User command parameters overhaul [`#15`](https://github.com/dstroy0/InputHandler/pull/15)
- fix favicon & MD linting; add docs/html to .gitignore [`#9`](https://github.com/dstroy0/InputHandler/pull/9)

### Fixed

- format [`#50`](https://github.com/dstroy0/InputHandler/issues/50)
- dynamic allocation fixes [`#50`](https://github.com/dstroy0/InputHandler/issues/50)
- fix _addCommandAbort's testing structure [`#43`](https://github.com/dstroy0/InputHandler/issues/43)

### Commits

- ci(version): library version [`de55c84`](https://github.com/dstroy0/InputHandler/commit/de55c8428252cb45e0688540c41f9b4b10470f11)
- README.md [`2289102`](https://github.com/dstroy0/InputHandler/commit/2289102191045cb12b40c652e1837ba805af689e)
- ci(version): library version [`bd7c4a1`](https://github.com/dstroy0/InputHandler/commit/bd7c4a1b28cc0521e2721f173ffe893214114f8a)
- README.md v0.0.9 [`89d16e7`](https://github.com/dstroy0/InputHandler/commit/89d16e7c1c2d30c09cb6ba970dffe5cc15c73c15)
- chore(changelog): remove vestigial changelog [`4dd1c60`](https://github.com/dstroy0/InputHandler/commit/4dd1c607846ecb2444cfec6f9524b49690a53121)
- README.md v0.0.8 [`a073c78`](https://github.com/dstroy0/InputHandler/commit/a073c7878813414aaa09921e6695c33ef7cf6b4c)
- ci(changelog): fix changelog template path [`8d221a2`](https://github.com/dstroy0/InputHandler/commit/8d221a2dcb86bb9a5a2a7ee06410ef0dc28668a5)
- ci(library.json): fix wrong path [`7d0d097`](https://github.com/dstroy0/InputHandler/commit/7d0d0972740421093d5959149bcd1a7d24cb5649)
- ci(docs.yml): remove unnecessary trigger [`6cf604d`](https://github.com/dstroy0/InputHandler/commit/6cf604d129f0fb5306eeefaff1b91a071201b8e2)
- ci(generate_changelog.yml): terminal command order [`7ca42e8`](https://github.com/dstroy0/InputHandler/commit/7ca42e82c4353e58872a9f5f59a871db02080247)
- feat(docs): add changelog to end of readme [`1f790b4`](https://github.com/dstroy0/InputHandler/commit/1f790b46ac135f832d60db6d8e6096d2d2d72dc4)
- generate changelog [`8def221`](https://github.com/dstroy0/InputHandler/commit/8def221866f32a868d9f408295576a184e390ca6)
- ci(version bump automation): auto-changelog opts [`365f8d9`](https://github.com/dstroy0/InputHandler/commit/365f8d9b5b04f087066d5fe0824bf5c67a0b6ff1)
- generate changelog [`39e7eec`](https://github.com/dstroy0/InputHandler/commit/39e7eec5c41562767fd4abd2a0dd6cafcb34b39a)
- fix(generate_changelog.yml): fetch main branch [`09c6246`](https://github.com/dstroy0/InputHandler/commit/09c62467a371c83bffef063ae31f1c37a733c267)
- generate changelog [`417009c`](https://github.com/dstroy0/InputHandler/commit/417009c6f8ba176626886b04e5246c786eb6b6a3)
- fix(generate_changelog.yml): fetch main branch [`056bdf3`](https://github.com/dstroy0/InputHandler/commit/056bdf33f6c04f930d2b062d65e2505a44370eba)
- generate changelog [`da81b57`](https://github.com/dstroy0/InputHandler/commit/da81b5707addd1bc4f813974ed358abf3fb833c8)
- chore(update library.json): add auto-changelog opts [`4806767`](https://github.com/dstroy0/InputHandler/commit/48067674844f4063a6d0b9d7eef7d23d4573d4ec)
- generate changelog [`1f5959b`](https://github.com/dstroy0/InputHandler/commit/1f5959bb03b85216090cc6ad9ceab59debd35507)
- fix(generate_changelog.yml): change commands [`90792d6`](https://github.com/dstroy0/InputHandler/commit/90792d6eff65b1b6f21b90f72943e3893b152b25)
- generate changelog [`f0e659d`](https://github.com/dstroy0/InputHandler/commit/f0e659d304da8f9a4d51a9f335b1706d1780ffcd)
- fix(generate_changelog.yml): change commands [`3c44528`](https://github.com/dstroy0/InputHandler/commit/3c4452872e60f5b0b1626fe3f0e91c85c6278e6c)
- fix(generate_changelog.yml): change commands [`895ac2a`](https://github.com/dstroy0/InputHandler/commit/895ac2a28a9835f2795bd5c13dd3f8a74e992a58)
- fix(generate_changelog.yml): change commands [`f7078b1`](https://github.com/dstroy0/InputHandler/commit/f7078b1a0bf44a6e2ec7896c5905547d0908b36f)
- fix(generate_changelog.yml): change commands [`22bc0ae`](https://github.com/dstroy0/InputHandler/commit/22bc0ae5952c04b5902bfd4368350bbff81a1737)
- fix(generate_changelog.yml): change commands [`b451ad7`](https://github.com/dstroy0/InputHandler/commit/b451ad72b1666f0b9a935c3b0592768164664a85)
- fix(generate_changelog.yml): change commands [`5e53f49`](https://github.com/dstroy0/InputHandler/commit/5e53f4941fd5ba541cae556edde6563c8f5026d2)
- fix(generate_changelog.yml): change commands [`264b563`](https://github.com/dstroy0/InputHandler/commit/264b5635ae1dde421324549b39e737c328a02cac)
- fix(generate_changelog.yml): remove symlink cmd [`70ebdb9`](https://github.com/dstroy0/InputHandler/commit/70ebdb9bd02fb7d6ce6043decf106488fd13da66)
- feat(docs.yml): build docs if changelog altered [`3e15aa8`](https://github.com/dstroy0/InputHandler/commit/3e15aa85bcb0a23d87c0076fed6f75bdf96f5cd8)
- autogenerated changelog [`21b36dc`](https://github.com/dstroy0/InputHandler/commit/21b36dc6ba2a4e17f3c20e0aa0b7a69a11495dd9)
- fix(generate_changelog.yml): testing symlink [`69bdb22`](https://github.com/dstroy0/InputHandler/commit/69bdb2285fd5d616663ebb870cabdf34b0b98521)
- autogenerated changelog [`9072774`](https://github.com/dstroy0/InputHandler/commit/9072774541d4bc47cb14280cfee5c529cee745ac)
- fix(generate_changelog.yml): add --no-git-tag-version opt [`8c4efd8`](https://github.com/dstroy0/InputHandler/commit/8c4efd82054ef2ea9b009af7ef3fee45f0b34584)
- feat(auto version bump): bump library.json version [`6cf0974`](https://github.com/dstroy0/InputHandler/commit/6cf0974224fa8dddf09fbe49a196283e91984d03)
- feat(docs changelog): add changelog to docs [`9d2f2c1`](https://github.com/dstroy0/InputHandler/commit/9d2f2c16b193d81783f914d53d42bc3c9ec289b8)
- fix(workflow): docs build requirements [`cadcf6a`](https://github.com/dstroy0/InputHandler/commit/cadcf6afd61745bb1c0b241cffc093fee788513b)
- autogenerated changelog [`b2c22ff`](https://github.com/dstroy0/InputHandler/commit/b2c22ff7d3c1721df69052c415bec963ed35ef7d)
- add changelog to docs [`440a70e`](https://github.com/dstroy0/InputHandler/commit/440a70e71017361e62f9728daade0b0e9b821df3)
- autogenerated changelog [`52ea0d8`](https://github.com/dstroy0/InputHandler/commit/52ea0d856af5370a4be8d2d39e165cff662f637f)
- auto changelog workflow [`63fa1d3`](https://github.com/dstroy0/InputHandler/commit/63fa1d3d33cea8dbb59b09cb2eb6a1bbe926813c)
- auto changelog workflow [`43642b7`](https://github.com/dstroy0/InputHandler/commit/43642b764d6937060849953e68790016eeeb7c61)
- auto changelog workflow [`25ec2da`](https://github.com/dstroy0/InputHandler/commit/25ec2da17e6079cd80d474201af91b4e1cc60835)
- auto changelog workflow [`a08b99c`](https://github.com/dstroy0/InputHandler/commit/a08b99cc0f4f91dcf6c598de5d782baacd5b3379)
- fix(generate_changelog): workflow testing [`2462937`](https://github.com/dstroy0/InputHandler/commit/24629371c3125fa74e79203f2e9c75b2555edcbd)
- fix(generate_changelog): workflow testing [`4d0856c`](https://github.com/dstroy0/InputHandler/commit/4d0856ca564bc3942a53e76f0394a3a7567857c0)
- fix(generate_changelog): workflow testing [`2531183`](https://github.com/dstroy0/InputHandler/commit/2531183ec4d47a25745d5cc0fa1aaa48db4b7d81)
- fix(generate_changelog): workflow testing [`fb08dce`](https://github.com/dstroy0/InputHandler/commit/fb08dce6bfd55693fc2c6375ea69ec75957743fa)
- fix(generate_changelog): workflow testing [`3d6150a`](https://github.com/dstroy0/InputHandler/commit/3d6150acc2e100fa8fe231329edd852326137f7d)
- fix(generate_changelog): workflow testing [`0aba2b1`](https://github.com/dstroy0/InputHandler/commit/0aba2b1fc40d6060b8b20acfe6f8c12ad8443806)
- fix(generate_changelog): workflow testing [`150f3dd`](https://github.com/dstroy0/InputHandler/commit/150f3dda4894ba070952e2ab8f3f0677a607035b)
- fix(generate_changelog): workflow testing [`e3169f2`](https://github.com/dstroy0/InputHandler/commit/e3169f23a7e488b5cbc69d52c202c59a1d4a65ad)
- fix(generate_changelog): workflow testing [`8569029`](https://github.com/dstroy0/InputHandler/commit/856902934ef0555e106401d965baf3d490802a44)
- fix(generate_changelog): workflow testing [`21cb6c4`](https://github.com/dstroy0/InputHandler/commit/21cb6c4fa17dd1aad98d4ea1695d6c4f87950f9b)
- fix(generate_changelog): workflow testing [`ee02127`](https://github.com/dstroy0/InputHandler/commit/ee02127d25b5240cda2deaaa5434aa10d265e57b)
- fix(generate_changelog): workflow testing [`7266b33`](https://github.com/dstroy0/InputHandler/commit/7266b3307981683a5b2fa54c76bf9f27b00f4f85)
- fix(generate_changelog): workflow testing [`8a1a212`](https://github.com/dstroy0/InputHandler/commit/8a1a212877ae2df8c1161027285f69d03a37b1f9)
- fix(generate_changelog): workflow testing [`e51a49f`](https://github.com/dstroy0/InputHandler/commit/e51a49f63cd6638ca41214becaf8c629b681f293)
- fix(generate_changelog): workflow testing [`315ea90`](https://github.com/dstroy0/InputHandler/commit/315ea90b0cd0a02c848bab706bcd629bcdc23b76)
- fix(generate_changelog): workflow testing [`115838c`](https://github.com/dstroy0/InputHandler/commit/115838cbb43a33dd32e96886d42e0ca552ff6801)
- fix(generate_changelog): workflow testing [`fc67bef`](https://github.com/dstroy0/InputHandler/commit/fc67bef26be16d99e0ed985a0b7bdb6d4a03e498)
- feat(library): changelog generator testing [`849fbe0`](https://github.com/dstroy0/InputHandler/commit/849fbe07cf6bd519ccee0c978122a56894883339)
- refactor(cli_gen_tool): use f string literals instead of string concatenation [`72ea79a`](https://github.com/dstroy0/InputHandler/commit/72ea79af575e2be3c051ec0f019125643c069f05)
- refactor(commandParamtersDialog): refine layout, move ui files into tool src [`ccf1c8c`](https://github.com/dstroy0/InputHandler/commit/ccf1c8c86cea1e299d4bd188d8a1fe6daf0147dd)
- feat(tool_cli): script cli improvements [`6697063`](https://github.com/dstroy0/InputHandler/commit/66970636cc6608f0ad6b5e495bdd0fb4b0ec5171)
- feat(tool_cli): add new arguments [`5b2bcd2`](https://github.com/dstroy0/InputHandler/commit/5b2bcd26bfd8613d035aae30f825d75e8cee985f)
- style(cli_gen_tool src): PEP-8 formatting [`3b04c5f`](https://github.com/dstroy0/InputHandler/commit/3b04c5f6de2000ae57081418989a94bff8b2b24f)
- docs(library): conformity [`d7e65f1`](https://github.com/dstroy0/InputHandler/commit/d7e65f17ff2a4cafe6fa62dd75774b1d5d087488)
- refactor(library): refactor config parser [`99d95b5`](https://github.com/dstroy0/InputHandler/commit/99d95b5fb55bbb99741d36f72f0df446da6f4dba)
- fix app exit errors [`5719d6c`](https://github.com/dstroy0/InputHandler/commit/5719d6c484b421349c6925e9186af054c3ee443f)
- refactor, consolidate widgets [`46a902f`](https://github.com/dstroy0/InputHandler/commit/46a902f54b79add3d1036f0fb5f41fe6abc360b9)
- gui launching w/o errors, gui closes w/ errors [`fffa68b`](https://github.com/dstroy0/InputHandler/commit/fffa68b236911945741a201e4f4b8616cd3ed11e)
- fix invalid return from MainWindow.eventFilter [`a42b01d`](https://github.com/dstroy0/InputHandler/commit/a42b01d48f31b6febfdcf7bdc472b7125d1bbd56)
- refactor, gui is launching with many errors [`2981a8e`](https://github.com/dstroy0/InputHandler/commit/2981a8ebd0ceb6cf953b58d52f5647759dcc1b5d)
- file generation/manipulation [`3b3f462`](https://github.com/dstroy0/InputHandler/commit/3b3f462118d2393c43381c7851a683a45c3c62ea)
- refactor [`0761161`](https://github.com/dstroy0/InputHandler/commit/0761161af3aac1b01608997477b420b6ed6f4aef)
- refactor, remove Qt from file manipulation [`0067547`](https://github.com/dstroy0/InputHandler/commit/006754779d459e3f9add2b19d8ff567b83d7654b)
- format, read/write consolidation [`aa5c9af`](https://github.com/dstroy0/InputHandler/commit/aa5c9af42405f9ad64d592827160d6db41a63d84)
- checkpoint [`e691d11`](https://github.com/dstroy0/InputHandler/commit/e691d111344e8131865c2ade1a0df5927eee01f7)
- Move cli_gen_tool cli to separate file [`28c95f6`](https://github.com/dstroy0/InputHandler/commit/28c95f6f7d85371194889ff4114005e7eaf3d8ce)
- contrib checkpoints [`033f47c`](https://github.com/dstroy0/InputHandler/commit/033f47c62c82959920ddb34da78c2df1902e1fe7)
- format [`7a8d03d`](https://github.com/dstroy0/InputHandler/commit/7a8d03d822f9476a3140535fa81e5bf2e46d766e)
- build workflow syntax [`dc9361d`](https://github.com/dstroy0/InputHandler/commit/dc9361dcfd66444cc7e2d78d115cde9567fef4e8)
- build workflow syntax error [`b0d9a2e`](https://github.com/dstroy0/InputHandler/commit/b0d9a2e764dc34dabc5e42b8de6bb8f66044ea64)
- build workflow syntax error [`3149afb`](https://github.com/dstroy0/InputHandler/commit/3149afb5c21306b5de72d88abf759da70975786d)
- format, linting workflows [`94b88f8`](https://github.com/dstroy0/InputHandler/commit/94b88f80c3c096d0ba229864bd4bf77719c8c747)
- src lint workflow [`be291f3`](https://github.com/dstroy0/InputHandler/commit/be291f398e746428ac6ccea60fbdc1719fa7dbfd)
- src lint workflow [`a77f6e8`](https://github.com/dstroy0/InputHandler/commit/a77f6e894e867c3ac2f3e685f10e16cfe43ea769)
- src lint workflow [`0ac9230`](https://github.com/dstroy0/InputHandler/commit/0ac92309a30e0fbaea1b4a3ea5989989a0ccc1c4)
- src lint workflow [`19fca91`](https://github.com/dstroy0/InputHandler/commit/19fca9158310ce51e5e1dae9514bcff6f4aea575)
- src lint workflow [`025d809`](https://github.com/dstroy0/InputHandler/commit/025d809d3095db5108174f2dfae45ba6d04812ef)
- src lint workflow [`4e5c079`](https://github.com/dstroy0/InputHandler/commit/4e5c0793845b579c76342e6832f36d220c035f60)
- src lint workflow [`5a7e526`](https://github.com/dstroy0/InputHandler/commit/5a7e526d6edb00102e6dc9fdbbf461d07250fdd8)
- src lint workflow [`f4cc103`](https://github.com/dstroy0/InputHandler/commit/f4cc103b41cf040b93384580232bf1bab4b5550f)
- src lint workflow [`36e1b9b`](https://github.com/dstroy0/InputHandler/commit/36e1b9b95e22a6551a2297114386649f0a99a3ac)
- src lint workflow [`06f260d`](https://github.com/dstroy0/InputHandler/commit/06f260d3d7e9623bccc6a7f9d69d148dcb7a0e4d)
- src lint workflow [`95474a9`](https://github.com/dstroy0/InputHandler/commit/95474a9238771b099ab5f16f3fb64ad561283529)
- src lint workflow [`dbba2e8`](https://github.com/dstroy0/InputHandler/commit/dbba2e847b7aafff91ed78d2787eb57c6185bf9e)
- src lint workflow [`fdf32f0`](https://github.com/dstroy0/InputHandler/commit/fdf32f003f6456368aa92883e40dcf5e3c88f81d)
