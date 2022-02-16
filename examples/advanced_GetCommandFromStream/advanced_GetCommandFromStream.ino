#include <InputHandler.h>

const uint16_t output_buffer_size = 512;
char output_buffer[output_buffer_size] = {'\0'};
uint16_t string_pos = 0;
UserInput inputHandler(output_buffer, &string_pos, 512);

void uc_unrecognized(UserInput* inputProcess)
{
  Serial.println(F("made it to uc_unrecognized"));
}

void uc_settings(UserInput* inputProcess)
{
  inputProcess->ListUserInputSettings(inputProcess);
}

void uc_help(UserInput* inputProcess)
{
  inputProcess->ListUserCommands();
}

void uc_test_input_types(UserInput* inputProcess)
{
  char* str_ptr = inputProcess->NextArgument();
  char* strtoul_ptr = 0;
  uint32_t strtoul_result = strtoul(str_ptr, &strtoul_ptr, 10);
  uint8_t eight_bit = (strtoul_result <= UINT8_MAX) ? (uint8_t)strtoul_result : 0U;

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

  char float_buffer[32] = {'\0'};
  char out[128] = {'\0'};
  uint16_t string_pos = 0;
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

  Serial.print(out);
}

PGM_P const PROGMEM CMD_HELP = "help";  //  "help" command, lists commands
PGM_P const PROGMEM CMD_INPUT_SETTINGS = "inputSettings"; //  lists UserInput settings
PGM_P const PROGMEM CMD_TEST = "test";  // test input types

UserCallbackFunctionParameters uc_help_(CMD_HELP, uc_help);
UserCallbackFunctionParameters uc_settings_(CMD_INPUT_SETTINGS, uc_settings);
UserCallbackFunctionParameters uc_test_(CMD_TEST, uc_test_input_types,
                                        USER_INPUT_TYPE_UINT8_T,
                                        USER_INPUT_TYPE_UINT16_T,
                                        USER_INPUT_TYPE_UINT32_T,
                                        USER_INPUT_TYPE_INT16_T,
                                        USER_INPUT_TYPE_FLOAT,
                                        USER_INPUT_TYPE_CHAR,
                                        USER_INPUT_TYPE_C_STRING);

void setup() {
  Serial.begin(115200); //  set up Serial0

  inputHandler.SetDefaultHandler(uc_unrecognized);  // set default function, called when user input has no match or is not valid
  inputHandler.AddUserCommand(&uc_help_); // lists commands available to the user
  inputHandler.AddUserCommand(&uc_settings_); // lists UserInput class settings
  inputHandler.AddUserCommand(&uc_test_); // input type test
  inputHandler.ListUserCommands();
}

void loop() {

  inputHandler.GetCommandFromStream(Serial);
  if (inputHandler.OutputIsAvailable() == true)
  {
    Serial.println(output_buffer);
    string_pos = 0;
    for (uint16_t i = 0; i < output_buffer_size; ++i)
    {
      output_buffer[i] = '\0';
    }
  }
}
