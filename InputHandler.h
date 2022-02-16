#ifndef USER_INPUT_HANDLER_H_
#define USER_INPUT_HANDLER_H_

#include <Arduino.h>

enum USER_INPUT_TYPES
{
    USER_INPUT_TYPE_UINT8_T,
    USER_INPUT_TYPE_UINT16_T,
    USER_INPUT_TYPE_UINT32_T,
    USER_INPUT_TYPE_INT16_T,
    USER_INPUT_TYPE_FLOAT,
    USER_INPUT_TYPE_CHAR,
    USER_INPUT_TYPE_C_STRING,
    _LAST_USER_INPUT_TYPES_enum
};

#ifndef USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS
#define USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS 32U
#endif

#ifndef UINT16_MAX
#define UINT16_MAX 65535
#endif

#ifndef UINT8_MAX
#define UINT8_MAX 255
#endif

#ifndef USER_INPUT_MAX_INPUT_LENGTH
#define USER_INPUT_MAX_INPUT_LENGTH UINT16_MAX
#endif

#ifdef DEBUG_USER_INPUT
#define _DEBUG_USER_INPUT
#endif

static constexpr const PROGMEM char *_default_username = "user";
static constexpr const PROGMEM char *_default_end_of_line_characters = "\r\n";
static constexpr const PROGMEM char *_default_token_delimiter = " ";
static constexpr const PROGMEM char *_default_c_string_delimiter = "\"";
static constexpr const PROGMEM char *null_ = "\0";

static constexpr const PROGMEM char *_input_type_strings[] = {
    "uint8_t",
    "uint16_t",
    "uint32_t",
    "int16_t",
    "float",
    "char",
    "c-string"};
static constexpr const PROGMEM char *_negative_sign = "-";
static constexpr const PROGMEM char *_dot = ".";
static constexpr const PROGMEM char *error = "error";

class UserInput;

class UserCallbackFunctionParameters
{
public:
    uint16_t num_args;
    const uint8_t *_arg_type;
    const char *command;
    uint16_t command_length;
    void (*function)(UserInput *);
    UserCallbackFunctionParameters *next_callback_function_parameters;

    template <typename... Arguments>
    UserCallbackFunctionParameters(const char *user_defined_command_to_match,
                                   void (*user_defined_function_to_call)(UserInput *),
                                   const Arguments &...args)
        : command(user_defined_command_to_match),
          function(user_defined_function_to_call),
          command_length(strlen_P(command)),
          next_callback_function_parameters(NULL),
          num_args(sizeof...(Arguments))
    {
        static const uint8_t _arg[] = {static_cast<uint8_t>(args)...};
        _arg_type = _arg;
    }
};

class UserInput
{
public:
    UserInput(char *output_buffer,
              uint16_t *output_buffer_string_pos,
              uint16_t output_buffer_len,
              const char *username = _default_username,
              const char *end_of_line_characters = _default_end_of_line_characters,
              const char *token_delimiter = _default_token_delimiter,
              const char *c_string_delimiter = _default_c_string_delimiter)
        : _output_buffer(output_buffer),
          _string_pos(output_buffer_string_pos),
          _output_buffer_len(output_buffer_len),
          _username_(username),
          _term_(end_of_line_characters),
          _delim_(token_delimiter),
          _c_str_delim_(c_string_delimiter),
          _null_(null_),
          default_handler_(NULL),
          commands_head_(NULL),
          commands_tail_(NULL),
          commands_count_(0)
    {
    }

    char *NextArgument();

    void AddUserCommand(UserCallbackFunctionParameters *command);

    void ReadCommand(uint8_t *data, size_t len);

    void GetCommandFromStream(Stream &stream,
                              uint16_t rx_buffer_size = 128,
                              const char *end_of_line_character = _default_end_of_line_characters);

    void ListUserCommands();

    void ListUserInputSettings(UserInput *inputprocess);

    void SetDefaultHandler(void (*function)(UserInput *));

    bool OutputIsAvailable();

#ifdef _DEBUG_USER_INPUT
    bool EnableDebugOutput = false;
#endif

protected:
    bool getToken(char *token_buffer, uint8_t *data, size_t len, uint16_t *data_index);
    bool validateUserInput(UserCallbackFunctionParameters *cmd, uint8_t arg_type, uint16_t data_pointers_index);
    void launchFunction(UserCallbackFunctionParameters *cmd);
    void escapeCharactersSoTheyPrint(const char *input, char *output);

private:
    const char *_username_;
    const char *_term_;
    const char *_delim_;
    const char *_c_str_delim_;
    const char *_null_;

    char *_output_buffer;
    uint16_t *_string_pos;
    uint16_t _output_buffer_len;
    bool _output_flag = false;

    void (*default_handler_)(UserInput *);
    UserCallbackFunctionParameters *commands_head_;
    UserCallbackFunctionParameters *commands_tail_;
    uint16_t commands_count_;

    char *token_buffer = NULL;
    boolean serial_buffer_allocated = false;
    uint8_t *serial_data = NULL;
    boolean new_serial_data = false;
    uint16_t serial_data_index = 0;
    char *data_pointers[USER_INPUT_MAX_NUMBER_OF_COMMAND_ARGUMENTS] = {0};
    uint16_t data_pointers_index = 0;
    uint16_t rec_num_arg_strings = 0;
};

#endif
