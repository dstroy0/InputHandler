#ifndef USER_INPUT_HANDLER_H_
#define USER_INPUT_HANDLER_H_

#include <Arduino.h>

#define _NE(x) (sizeof(x) / sizeof((x)[0U]))

#define USER_INPUT_TYPE_UINT8_T 0U  // 8-bit unsigned integer 0-255
#define USER_INPUT_TYPE_UINT16_T 1U // 16-bit unsigned integer 0-65534
#define USER_INPUT_TYPE_UINT32_T 2U // 32-bit unsigned integer 0-4294967295
#define USER_INPUT_TYPE_INT16_T 3U  // 16-bit signed integer -32768-32767
#define USER_INPUT_TYPE_FLOAT 4U    // 32-bit signed floating point number -3.4028235E+38 - 3.4028235E+38
#define USER_INPUT_TYPE_CHAR 5U     // 8-bit char
#define USER_INPUT_TYPE_C_STRING 6U // any printable char are allowed

#ifndef USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS
#define USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS 32U
#endif

#ifndef UINT16_MAX
#define UINT16_MAX 65535
#endif

#ifndef USER_INPUT_MAX_INPUT_LENGTH
#define USER_INPUT_MAX_INPUT_LENGTH UINT16_MAX
#endif

// arg_type[argument] = {argument_type 0-5, UINT8_T, ... STRING}

class UserInput;

class UserCallbackFunctionParameters
{
public:
    UserCallbackFunctionParameters(const char *user_defined_command_to_match,
                                   void (*user_defined_function_to_call)(UserInput *),
                                   uint8_t expected_number_of_function_arguments = 0,
                                   const uint8_t *function_argument_type_array = {0})
        : command(user_defined_command_to_match),
          function(user_defined_function_to_call),
          num_args(expected_number_of_function_arguments),
          arg_type(function_argument_type_array),
          command_length(0),
          next_callback_function_parameters(NULL)
    {
    }
    const char *command;
    uint16_t command_length = strlen(command);
    void (*function)(UserInput *);
    uint8_t num_args;
    const uint8_t *arg_type; // array
    UserCallbackFunctionParameters *next_callback_function_parameters;
};

class UserInput
{
public:
    UserInput(char *output_buffer,
              uint16_t *output_buffer_string_pos,
              uint16_t output_buffer_len,
              const char *username = _default_username,
              const char *end_of_line_character = _default_end_of_line_character,
              const char *token_delimiter = _default_token_delimiter,
              const char *c_string_delimiter = _default_c_string_delimiter)
        : _output_buffer(output_buffer),
          _string_pos(output_buffer_string_pos),
          _output_buffer_len(output_buffer_len),
          _username(username),
          term_(end_of_line_character),
          delim_(token_delimiter),
          c_str_delim_(c_string_delimiter),
          default_handler_(NULL),
          commands_head_(NULL),
          commands_tail_(NULL),
          commands_count_(0)
    {
    }

    char *NextArgument();

    void AddUserCommand(UserCallbackFunctionParameters *command);

    void ReadCommand(uint8_t *data, size_t len);

    void GetCommandFromStream(Stream &stream, uint16_t rx_buffer_size = 128, const char *end_of_line_character = _default_end_of_line_character);

    void ListUserCommands();

    void ListUserInputSettings(UserInput *inputprocess);

    void SetDefaultHandler(void (*function)(UserInput *));

    bool OutputIsAvailable();

    bool EnableDebugOutput = false;

protected:
    bool getToken(char *token_buffer, uint8_t *data, size_t len, uint16_t *data_index);
    bool validateUserInput(UserCallbackFunctionParameters *cmd, uint8_t arg_type, uint16_t data_pointers_index);
    void launchFunction(UserCallbackFunctionParameters *cmd);

private:
    const char *_username;
    const char *term_;
    const char *delim_;
    const char *c_str_delim_;

    static constexpr const PROGMEM char *null_ = "\0";
    static constexpr const PROGMEM char *_default_username = "user";
    static constexpr const PROGMEM char *_default_end_of_line_character = "\r\n";
    static constexpr const PROGMEM char *_default_token_delimiter = " ";
    static constexpr const PROGMEM char *_default_c_string_delimiter = "\"";

    char *_output_buffer;
    uint16_t *_string_pos;
    uint16_t _output_buffer_len;
    bool _output_flag = false;

    void (*default_handler_)(UserInput *);
    UserCallbackFunctionParameters *commands_head_;
    UserCallbackFunctionParameters *commands_tail_;
    uint16_t commands_count_;

    boolean serial_buffer_allocated = false;
    uint8_t *data = NULL;
    boolean new_data = false;
    uint16_t data_index = 0;
    char *data_pointers[USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS] = {0};
    uint16_t data_pointers_index = 0;
    uint16_t rec_num_arg_strings = 0;
    const char *USER_INPUT_TYPE_STRING_LITERAL_ARRAY[7] = {"uint8_t", "uint16_t", "uint32_t", "int16_t", "float", "char", "c-string"};
};

#endif
