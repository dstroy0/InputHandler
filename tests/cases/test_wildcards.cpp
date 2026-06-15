#include "Arduino.h"
#include <cstdint>
#include "../src/InputHandler.h"
#include "../src/InputHandler.cpp"
#include <cassert>
#include <iostream>

using namespace ih;

Parameters create_params(void (*func)(Input *), const char *cmd, uint8_t id)
{
    Parameters p = {};
    p.function = func;
    p.has_wildcards = false;
    strncpy(p.command, cmd, IH_MAX_CMD_STR_LEN);
    p.command_length = strlen(cmd);
    p.parent_command_id = root;
    p.command_id = id;
    p.depth = 0;
    p.sub_commands = 0;
    p.argument_flag = UI_ARG_HANDLING::no_args;
    p.num_args = 0;
    p.max_num_args = 0;
    return p;
}

static bool cmd_executed = false;
void cmd_callback(Input *input)
{
    cmd_executed = true;
}

void test_wildcards()
{
    std::cout << "Running test_wildcards (S*T)..." << std::endl;
    char output_buf[512] = {0};
    Input input(nullptr, output_buf, 512);

    Parameters p = create_params(cmd_callback, "S*T", 3);
    p.has_wildcards = true;

    static const Parameters wc_cmd_prm[1] = {p};
    Command wc_cmd(wc_cmd_prm, 1);
    input.addCommand(wc_cmd);
    input.begin();

    const char *matches[] = {"SET", "SOT", "SAT", "S-T", "S1T"};
    for (const char *m : matches)
    {
        cmd_executed = false;
        uint8_t data[10];
        strcpy((char *)data, m);
        input.readCommandFromBuffer(data, strlen(m));
        if (!cmd_executed)
        {
            std::cerr << "Wildcard FAILED to match: " << m << std::endl;
            exit(1);
        }
    }

    const char *non_matches[] = {"SEET", "ST", "SETT", "SEA"};
    for (const char *nm : non_matches)
    {
        cmd_executed = false;
        uint8_t data[10];
        strcpy((char *)data, nm);
        input.readCommandFromBuffer(data, strlen(nm));
        if (cmd_executed)
        {
            std::cerr << "Wildcard INCORRECTLY matched: " << nm << std::endl;
            exit(1);
        }
    }

    std::cout << "test_wildcards passed." << std::endl;
}

int main()
{
    test_wildcards();
    return 0;
}
