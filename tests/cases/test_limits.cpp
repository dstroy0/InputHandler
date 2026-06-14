#include "Arduino.h"
#include <cstdint>
#include "../src/InputHandler.h"
#include "../src/InputHandler.cpp"
#include <cassert>
#include <iostream>
#include <string>

using namespace ih;

static bool limit_cmd_executed = false;
static int received_args_count = 0;
static char last_arg1[64] = {0};

void limit_cb(Input* in) {
    limit_cmd_executed = true;
    received_args_count = 0;
    last_arg1[0] = '\0';
    
    char* a1 = in->getArgument(1);
    if (a1) {
        strncpy(last_arg1, a1, 63);
    }

    for (int i = 1; i <= IH_MAX_ARGS_PER_COMMAND; ++i) {
        if (in->getArgument(i) != nullptr) {
            received_args_count++;
        }
    }
}

void test_max_args() {
    std::cout << "Testing Max Args (" << IH_MAX_ARGS_PER_COMMAND << ")..." << std::endl;
    char output_buf[1024] = {0};
    Input input(nullptr, output_buf, 1024);

    Parameters p = {};
    p.function = limit_cb;
    strcpy(p.command, "MAX");
    p.command_length = 3;
    p.argument_flag = UI_ARG_HANDLING::one_type;
    p.arg_type_arr[0] = UITYPE::INT16_T;
    p.num_args = IH_MAX_ARGS_PER_COMMAND;
    p.max_num_args = IH_MAX_ARGS_PER_COMMAND;

    static const Parameters prms[1] = {p};
    Command cmd(prms, 1);
    input.addCommand(cmd);
    input.begin();

    std::string input_str = "MAX";
    for (int i = 0; i < IH_MAX_ARGS_PER_COMMAND; ++i) {
        input_str += " 1";
    }

    limit_cmd_executed = false;
    input.readCommandFromBuffer((uint8_t*)input_str.c_str(), input_str.length());
    
    if (!limit_cmd_executed) {
        std::cerr << "Max Args FAILED: Command did not execute. Output: " << output_buf << std::endl;
        exit(1);
    }
    if (received_args_count != IH_MAX_ARGS_PER_COMMAND) {
        std::cerr << "Max Args FAILED: Expected " << IH_MAX_ARGS_PER_COMMAND << " args, got " << received_args_count << std::endl;
        exit(1);
    }
    std::cout << "Max Args PASSED" << std::endl;
}

void test_max_cmd_len() {
    std::cout << "Testing Max Command Length (" << IH_MAX_CMD_STR_LEN << ")..." << std::endl;
    char output_buf[512] = {0};
    Input input(nullptr, output_buf, 512);

    std::string long_cmd_str(IH_MAX_CMD_STR_LEN, 'A');
    Parameters p = {};
    p.function = limit_cb;
    strncpy(p.command, long_cmd_str.c_str(), IH_MAX_CMD_STR_LEN);
    p.command[IH_MAX_CMD_STR_LEN] = '\0';
    p.command_length = IH_MAX_CMD_STR_LEN;
    
    static const Parameters prms[1] = {p};
    Command cmd(prms, 1);
    input.addCommand(cmd);
    input.begin();

    limit_cmd_executed = false;
    input.readCommandFromBuffer((uint8_t*)long_cmd_str.c_str(), long_cmd_str.length());
    assert(limit_cmd_executed);
    std::cout << "Max Command Length PASSED" << std::endl;
}

void test_input_overflow() {
    std::cout << "Testing Input Length Limit (" << IH_MAX_PROC_INPUT_LEN << ")..." << std::endl;
    char output_buf[512] = {0};
    Input input(nullptr, output_buf, 512);

    Parameters p = {};
    p.function = limit_cb;
    strcpy(p.command, "T");
    p.command_length = 1;
    
    static const Parameters prms[1] = {p};
    Command cmd(prms, 1);
    input.addCommand(cmd);
    input.begin();

    std::string long_input(IH_MAX_PROC_INPUT_LEN + 1, 'B');
    limit_cmd_executed = false;
    input.readCommandFromBuffer((uint8_t*)long_input.c_str(), long_input.length());
    
    // It should NOT execute because it's too long
    if (limit_cmd_executed) {
        std::cerr << "Input Overflow FAILED: Command executed despite oversized input" << std::endl;
        exit(1);
    }
    std::cout << "Input Overflow PASSED" << std::endl;
}

void test_zdc() {
    std::cout << "Testing Zero Delimiter Command (ZDC)..." << std::endl;
    char output_buf[512] = {0};
    Input input(nullptr, output_buf, 512);

    Parameters p = {};
    p.function = limit_cb;
    strcpy(p.command, "Z");
    p.command_length = 1;
    p.argument_flag = UI_ARG_HANDLING::one_type;
    p.arg_type_arr[0] = UITYPE::INT16_T;
    p.num_args = 1;
    p.max_num_args = 1;
    
    static const Parameters prms[1] = {p};
    Command cmd(prms, 1);
    input.addCommand(cmd);
    input.begin();

    const Parameters* zdc_prms[1] = { &prms[0] };
    uint8_t data[] = "Z123";
    
    limit_cmd_executed = false;
    received_args_count = 0;
    last_arg1[0] = '\0';
    input.readCommandFromBuffer(data, 4, 1, zdc_prms);
    
    if (!limit_cmd_executed) {
        std::cerr << "ZDC FAILED: Command did not execute." << std::endl;
        exit(1);
    }
    if (strcmp(last_arg1, "123") != 0) {
        std::cerr << "ZDC FAILED: Expected argument '123', got '" << last_arg1 << "'" << std::endl;
        exit(1);
    }
    std::cout << "ZDC PASSED" << std::endl;
}

static int last_executed_id = 0;
void cb_lvl1(Input* in) { last_executed_id = 1; }
void cb_lvl2(Input* in) { 
    last_executed_id = 2; 
    char* a1 = in->getArgument(2); // Level 2 command is token 1, arg is token 2
    if (a1) strncpy(last_arg1, a1, 63);
}
void cb_lvl3(Input* in) { 
    last_executed_id = 3; 
    char* a1 = in->getArgument(3); // Level 3 command is token 2, args are token 3, 4
    if (a1) strncpy(last_arg1, a1, 63);
}

Parameters create_limit_params(void (*func)(Input*), const char* cmd, uint8_t id, uint8_t parent = root, uint8_t depth = 0) {
    Parameters p = {};
    p.function = func;
    p.has_wildcards = false;
    strncpy(p.command, cmd, IH_MAX_CMD_STR_LEN);
    p.command_length = strlen(cmd);
    p.parent_command_id = parent;
    p.command_id = id;
    p.depth = depth;
    p.sub_commands = 0;
    p.argument_flag = UI_ARG_HANDLING::no_args;
    p.num_args = 0;
    p.max_num_args = 0;
    return p;
}

void test_complex_nesting() {
    std::cout << "Testing Complex Nesting..." << std::endl;
    char output_buf[512] = {0};
    Input input(nullptr, output_buf, 512);

    static Parameters prms[3];
    prms[0] = create_limit_params(cb_lvl1, "L1", 10, root, 0);
    prms[0].sub_commands = 1;
    
    prms[1] = create_limit_params(cb_lvl2, "L2", 20, 10, 1);
    prms[1].sub_commands = 1;
    
    prms[2] = create_limit_params(cb_lvl3, "L3", 30, 20, 2);
    prms[2].argument_flag = UI_ARG_HANDLING::one_type;
    prms[2].arg_type_arr[0] = UITYPE::INT16_T;
    prms[2].num_args = 2;
    prms[2].max_num_args = 2;

    Command cmd(prms, 3, 2);
    input.addCommand(cmd);
    input.begin();

    uint8_t d1[] = "L1 L2 L3 200 300";
    last_executed_id = 0;
    input.readCommandFromBuffer(d1, strlen((char*)d1));
    
    if (last_executed_id != 3) {
        std::cerr << "Complex Nesting FAILED: Expected ID 3, got " << last_executed_id << std::endl;
        exit(1);
    }
    std::cout << "Complex Nesting PASSED" << std::endl;
}

int main() {
    test_max_args();
    test_max_cmd_len();
    test_input_overflow();
    test_zdc();
    test_complex_nesting();
    std::cout << "All limit tests passed!" << std::endl;
    return 0;
}
