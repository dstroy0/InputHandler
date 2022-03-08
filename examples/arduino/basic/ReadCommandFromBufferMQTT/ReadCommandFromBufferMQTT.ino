/**
   @file basicReadCommandFromBufferMQTTarduino.ino
   @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
   @brief An example that uses ReadCommandFromBuffer and MQTT
   @version 0.1
   @date 2022-03-01

   @copyright Copyright (c) 2022
*/

#include <SPI.h>
#include <WiFiNINA.h>
#include <PubSubClient.h>
#include <InputHandler.h>

const char* ssid = "REPLACE_WITH_YOUR_SSID";
const char* password = "REPLACE_WITH_YOUR_PASSWORD";
const char* mqtt_server = "YOUR_MQTT_BROKER_IP_ADDRESS";

WiFiClient arduinoClient;
PubSubClient client(arduinoClient);
char msg[50]; // command rx buffer

/*
  this output buffer is formatted by UserInput's methods
  you have to empty it out yourself with
  ClearOutputBuffer()
*/
char output_buffer[512] = {'\0'}; //  output buffer

/*
  UserInput constructor
*/
UserInput inputHandler(
  /* UserInput's output buffer */ output_buffer,
  /* size of UserInput's output buffer */ 512,
  /* username */ "arduino",
  /* end of line characters */ "\r\n",
  /* token delimiter */ " ",
  /* c-string delimiter */ "\""
);

/*
   default function, called if nothing matches or if there is an error
*/
void uc_unrecognized(UserInput* inputProcess)
{
  // do your error output here
  if (inputHandler->OutputIsAvailable())
  {
    client.publish("esp/output", output_buffer);
    inputHandler->ClearOutputBuffer();
  }
}
/*
   lists the settings passed to UserInput's constructor, or default parameters
*/
void uc_settings(UserInput* inputProcess)
{
  inputProcess->ListSettings(inputProcess);
}

/*
   lists commands available to the user
*/
void uc_help(UserInput* inputProcess)
{
  inputProcess->ListCommands();
}
void uc_help(UserInput& inputProcess)
{
  inputProcess.ListCommands();
}

/*
   test all available input types
*/
void uc_test_input_types(UserInput* inputProcess)
{
  inputProcess->OutputToStream(Serial);                                             // class output, doesn't have to output to the input stream
  char* str_ptr = inputProcess->NextArgument();                                     //  init str_ptr and point it at the next argument input by the user
  char* strtoul_ptr = 0;                                                            //  this is for strtoul
  uint32_t strtoul_result = strtoul(str_ptr, &strtoul_ptr, 10);                     // get the result in base10
  uint8_t eight_bit = (strtoul_result <= UINT8_MAX) ? (uint8_t)strtoul_result : 0U; // if the result is less than UINT8_MAX then set eight_bit, else eight_bit = 0

  str_ptr = inputProcess->NextArgument();
  strtoul_ptr = 0;
  strtoul_result = strtoul(str_ptr, &strtoul_ptr, 10);
  uint16_t sixteen_bit = (strtoul_result <= UINT16_MAX) ? (uint16_t)strtoul_result : 0U;

  str_ptr = inputProcess->NextArgument();
  strtoul_ptr = 0;
  uint32_t thirtytwo_bit = strtoul(str_ptr, &strtoul_ptr, 10);

  str_ptr = inputProcess->NextArgument();
  int sixteen_bit_int = atoi(str_ptr);

  str_ptr = inputProcess->NextArgument();
  float thirtytwo_bit_float = (float)atof(str_ptr);

  str_ptr = inputProcess->NextArgument();
  char _char = *str_ptr;

  str_ptr = inputProcess->NextArgument();
  char c_string[64] = {'\0'};
  snprintf_P(c_string, 64, PSTR("%s"), str_ptr);

  char float_buffer[32] = {'\0'}; //  dtostrf buffer
  char out[128] = {'\0'};         //  function output buffer
  uint16_t string_pos = 0;        // function output buffer index

  /*
       format out[] with all of the arguments received
  */
  string_pos += snprintf_P(out + string_pos, 128,
                           PSTR("Test user input types:\n"
                                "uint8_t %u\nuint16_t %u\nuint32_t %lu\nint %d\nfloat %s\nchar %c\nc-string %s\n"),
                           eight_bit,
                           sixteen_bit,
                           thirtytwo_bit,
                           sixteen_bit_int,
                           dtostrf(thirtytwo_bit_float, 2, 3, float_buffer),
                           _char,
                           c_string);

  memcpy(output_buffer, out, ((sizeof(out) < sizeof(output_buffer)) ? sizeof(out) : sizeof(output_buffer - 1)));
}

const CommandParameters help_param PROGMEM =
{
  uc_help,      // function name
  "help",       // command string
  4,            // command string characters
  no_arguments, // argument handling
  0,                // minimum expected number of arguments
  0,                // maximum expected number of arguments
  /*
    UITYPE arguments
  */
  {
    UITYPE::NO_ARGS // use NO_ARGS if the function expects no arguments
  }
};
CommandConstructor uc_help_(&help_param); //  uc_help_ has a command string, and function specified

const CommandParameters settings_param PROGMEM =
{
  uc_settings,      // function name
  "inputSettings",  // command string
  13,               // command string characters
  no_arguments,     // argument handling
  0,                // minimum expected number of arguments
  0,                // maximum expected number of arguments
  /*
    UITYPE arguments
  */
  {
    UITYPE::NO_ARGS // use NO_ARGS if the function expects no arguments
  }
};
CommandConstructor uc_settings_(&settings_param); // uc_settings_ has a command string, and function specified

const CommandParameters type_test_param PROGMEM =
{
  uc_test_input_types, // function name
  "test",              // command string
  4,                   // string length
  argument_type_array, // argument handling
  8,                   // minimum expected number of arguments
  8,                   // maximum expected number of arguments
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
CommandConstructor uc_test_(&type_test_param);

void setup_wifi()
{
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
  }
}

void reconnect_mqtt()
{
  // Loop until we're reconnected
  while (!client.connected())
  {
    if (client.connect("ArduinoClient"))
    {
      // Subscribe
      client.subscribe("arduino/command");
    }
    else
    {
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

// incoming command
void mqtt_callback(char* topic, byte* message, unsigned int length)
{
  inputHandler.ReadCommandFromBuffer(message, length);
}

void setup()
{
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(mqtt_callback);

  inputHandler.DefaultFunction(uc_unrecognized); // set default function, called when user input has no match or is not valid
  inputHandler.AddCommand(uc_help_);             // lists commands available to the user
  inputHandler.AddCommand(uc_settings_);         // lists UserInput class settings
  inputHandler.AddCommand(uc_test_);             // input type test

  uc_help(inputHandler); // formats output_buffer with the command list
}

void loop()
{
  // keep connecting to MQTT
  if (!client.connected())
  {
    reconnect_mqtt();
  }
  client.loop();

  if (inputHandler.OutputIsAvailable())
  {
    client.publish("arduino/output", output_buffer);
    inputHandler.ClearOutputBuffer();
  }
}
