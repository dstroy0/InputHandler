#include "../src/InputHandler.cpp"
#include "../src/InputHandler.h"
#include "Arduino.h"
#include <cassert>
#include <cstdint>
#include <iostream>

using namespace ih;

Parameters create_params(void (*func)(Input *), const char *cmd, uint8_t id, uint8_t parent = root, uint8_t depth = 0)
{
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

static int last_id = -1;
void cmd_root_cb(Input *in)
{
    last_id = 1;
}
void cmd_sub_cb(Input *in)
{
    last_id = 2;
}
void cmd_subsub_cb(Input *in)
{
    last_id = 3;
}

void test_nested_commands()
{
    std::cout << "Running test_nested_commands..." << std::endl;
    char output_buf[512] = {0};
    Input input(nullptr, output_buf, 512);

    static Parameters prms[3];
    prms[0] = create_params(cmd_root_cb, "LED", 1, root, 0);
    prms[0].sub_commands = 1;
    prms[1] = create_params(cmd_sub_cb, "ON", 2, 1, 1);
    prms[1].sub_commands = 1;
    prms[2] = create_params(cmd_subsub_cb, "RED", 3, 2, 2);

    // tree_depth should be 2 (max depth)
    Command cmd(prms, 3, 2);
    input.addCommand(cmd);
    input.begin();

    last_id = -1;
    uint8_t d1[] = "LED ON RED";
    input.readCommandFromBuffer(d1, 10);
    if (last_id != 3)
    {
        std::cerr << "Nested match FAILED. Expected 3, got " << last_id << std::endl;
        exit(1);
    }

    last_id = -1;
    uint8_t d2[] = "LED ON";
    input.readCommandFromBuffer(d2, 6);
    if (last_id != 2)
    {
        std::cerr << "Partial nested match FAILED. Expected 2, got " << last_id << std::endl;
        exit(1);
    }

    std::cout << "test_nested_commands passed." << std::endl;
}

int main()
{
    test_nested_commands();
    return 0;
}
