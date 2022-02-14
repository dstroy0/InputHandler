#include <InputHandler.h>

const uint16_t output_buffer_size = 128;
char output_buffer[output_buffer_size] = {'\0'};
uint16_t string_pos = 0; 
UserInput inputHandler(output_buffer, &string_pos, 128);

void uc_unrecognized(UserInput* inputProcess)
{
  Serial.println(F("made it to uc_unrecognized"));  
}

void uc_help(UserInput* inputProcess)
{
  inputProcess->ListUserCommands();
}

UserCallbackFunctionParameters uc_help_("help", uc_help);


void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);

  inputHandler.SetDefaultHandler(uc_unrecognized);
  inputHandler.AddUserCommand(&uc_help_);
}

void loop() {
  // put your main code here, to run repeatedly:
  inputHandler.GetCommandFromStream(Serial);
  Serial.println(output_buffer);
  string_pos = 0;
  for(uint16_t i = 0; i < output_buffer_size; ++i)
  {
    output_buffer[i] = '\0';
  }
}
