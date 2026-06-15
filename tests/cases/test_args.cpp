#include "../src/InputHandler.cpp"
#include "../src/InputHandler.h"
#include "Arduino.h"
#include <cassert>
#include <cstdint>
#include <iostream>

using namespace ih;

static int val1 = 0;
static float val2 = 0.0f;

void arg_cb(Input *in)
{
    char *a1 = in->getArgument(1);
    char *a2 = in->getArgument(2);
    if (a1)
        val1 = atoi(a1);
    if (a2)
        val2 = atof(a2);
}

void test_args()
{
    std::cout << "Running test_args..." << std::endl;
    char output_buf[512] = {0};
    Input input(nullptr, output_buf, 512);

    Parameters p = {};
    p.function = arg_cb;
    strcpy(p.command, "VAL");
    p.command_length = 3;
    p.argument_flag = UI_ARG_HANDLING::type_arr;
    p.num_args = 2;
    p.max_num_args = 2;
    p.arg_type_arr[0] = UITYPE::INT16_T;
    p.arg_type_arr[1] = UITYPE::FLOAT;

    static const Parameters prms[1] = {p};
    Command cmd(prms, 1);
    input.addCommand(cmd);
    input.begin();

    val1 = 0;
    val2 = 0.0f;
    uint8_t d1[] = "VAL -42 3.14";
    input.readCommandFromBuffer(d1, 12);
    assert(val1 == -42);
    assert(val2 > 3.13f && val2 < 3.15f);

    std::cout << "test_args passed." << std::endl;
}

int main()
{
    test_args();
    return 0;
}
