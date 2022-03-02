[![Arduino CLI Build](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_cli.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_cli.yml)  

[![PlatformIO arduino CI](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_pio.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/build_arduino_pio.yml)  

[![PlatformIO esp CI](https://github.com/dstroy0/InputHandler/actions/workflows/build_esp_pio.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/build_esp_pio.yml)  

[![Doxygen CI](https://github.com/dstroy0/InputHandler/actions/workflows/doxygen.yml/badge.svg)](https://github.com/dstroy0/InputHandler/actions/workflows/doxygen.yml)  

# InputHandler
Arduino user input handler :  
Executes arbitrary functions by matching user input command strings.

The classes' input methods are:

```
void GetCommandFromStream(Stream &stream, uint16_t rx_buffer_size = 32);
```
and
```
void ReadCommandFromBuffer(uint8_t *data, size_t len);
```

Easily enforce input argument type with:
```
const UITYPE your_arguments_in_order[] = {UITYPE::UINT8_T,
                                          UITYPE::UINT16_T,
                                          UITYPE::UINT32_T,
                                          UITYPE::INT16_T,
                                          UITYPE::FLOAT,
                                          UITYPE::CHAR,
                                          UITYPE::C_STRING
                                         };
UserCommandParameters your_command_object_("your_input_to_match",    // your command string
                                           your_function_to_launch,  // the function you want to launch 
                                           _N_ARGS(your_arguments_in_order), // a macro that gets the number of arguments in your argument array
                                           your_arguments_in_order  // your argument array
                                          );                           
```


Target function will not execute if the command string does not match, or any arguments are type-invalid.

ATTiny85 not supported  

If your board is not listed as not supported open an issue if you'd like it added to build coverage.  
  
Build coverage:  
  
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
