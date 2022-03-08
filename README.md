<!-- markdownlint-disable MD041 -->
[![Arduino CLI CI](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_cli.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_cli.yml) [![PlatformIO arduino CI](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_pio.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_pio.yml) [![PlatformIO esp CI](https://github.com/dstroy0/InputHandler/actions/workflows/build_esp_pio.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/build_esp_pio.yml)  

[![Doxygen CI](https://github.com/dstroy0/InputHandler/actions/workflows/doxygen.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/doxygen.yml) [![src-cpp-linter CI](https://github.com/dstroy0/InputHandler/actions/workflows/lib_cpp_linter.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/lib_cpp_linter.yml)  

# InputHandler

Arduino user input handler:  
Executes arbitrary functions by matching user input command strings.  

Check out the examples for different use cases.  You can use this library to build a remote cli for your equipment.  

Commands are simple to setup, command length does not matter, any printable char or control char that is not your end of line character, token delimiter, or c-string delimiter is a valid command.  You can have as many or as few arguments as you wish.

A command string looks like:  

```text
your_command arg1 arg... "c-string args can have spaces and are enclosed with quotes"
```

The classes' input methods are:  

```cpp
void GetCommandFromStream(Stream &stream, size_t rx_buffer_size = 32);
```

OR if you don't want to use a [Stream](https://www.arduino.cc/reference/en/language/functions/communication/stream/) object use:  

```cpp
void ReadCommandFromBuffer(uint8_t *data, size_t len);
```

Easily enforce input argument types:  

```cpp
const CommandParameters your_command_parameters PROGMEM =
{
  your_function,       // function name
  "cmd_str",           // command string
  7,                   // command string length
  argument_type_array, // argument handling (no_arguments, single_argument_type, or argument_type_array)
  8,                   // expected number of arguments (set to zero if no arguments)
  /*
    UITYPE arguments, fill with arguments you want to send in order
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
CommandConstructor your_command(&your_command_parameters);                       
```

`NOTYPE` is a special argument type that doesn't perform any type-validation.  
`NO_ARGS` is a special argument type that explicitly states you wish to pass no arguments.  

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

ATTiny85 not supported  

If your board is not listed as not supported open an issue if you'd like it added to build coverage.  
  
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
atmegang  
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
