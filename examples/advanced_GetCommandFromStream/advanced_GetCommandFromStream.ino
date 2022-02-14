#include <InputHandler.h>

const uint16_t output_buffer_size = 128;
char output_buffer[output_buffer_size] = {'\0'};
uint16_t string_pos = 0;
UserInput inputHandler(output_buffer, &string_pos, 128);

void uc_unrecognized(UserInput* inputProcess)
{
  Serial.println(F("made it to uc_unrecognized"));
}

void uc_settings(UserInput* inputProcess)
{
  //inputHandler->ListUserInputSettings(inputHandler);
}

void uc_help(UserInput* inputProcess)
{
  inputProcess->ListUserCommands();
}

PGM_P const PROGMEM CMD_HELP = "help";
PGM_P const PROGMEM CMD_INPUT_SETTINGS = "inputSettings";

UserCallbackFunctionParameters uc_help_(CMD_HELP, uc_help, 0, 0);
UserCallbackFunctionParameters uc_settings_(CMD_INPUT_SETTINGS, uc_settings, 0, 0);

void setup() {
  Serial.begin(115200); //  set up Serial0

  inputHandler.SetDefaultHandler(uc_unrecognized);  // set default function, called when user input has no match or is not valid
  inputHandler.AddUserCommand(&uc_help_); // lists commands available to the user
  inputHandler.AddUserCommand(&uc_settings_); // lists UserInput class settings
  
}

void loop() {
  // put your main code here, to run repeatedly:
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
