##
# @file generate_workflow_matrix.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief generates json to use as build workflow matrix
# @version 1.0
# @date 2023-03-20
# @copyright Copyright (c) 2022
# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

import os
import sys
import argparse

exclude = "#" # lines starting with # are ignored
platforms = {
    "arduino": ["adafruit", "esp32", "esp8266", "teensyduino", "arduino", "rpi"],
    "platformio": [
        "atmelavr",
        "atmelmegaavr",
        "atmelsam",
        "esp32",
        "esp8266",
        "nordicnrf51",
        "nordicnrf52",
        "rpi",
        "ststm32",
        "ststm8",
        "teensyduino",
    ],
}


def open_supported_boards_file(compiler: str) -> list:
    file_name = ""
    if compiler == "arduino":
        file_name = os.path.join(os.getcwd(), "supported_boards", "arduino.txt")
    elif compiler == "platformio":
        file_name = os.path.join(os.getcwd(), "supported_boards", "platformio.txt")
    else:
        return []  # error
    with open(file_name) as file:
        raw_file_text = file.readlines()
    return raw_file_text


def get_boards_for_platform(file_text: list, platform: str) -> list:
    platform = platform.strip()
    ret_list = list()
    if file_text == [] or platform == "":
        return f"get boards error!\nfile_text:\n{file_text}\n\nplatform: {platform}\n"
    for line_num in range(len(file_text)):
        line_text = file_text[line_num].lower().strip()
        if ("boards" in line_text or "fqbn" in line_text) and platform in line_text:
            line_num += 1
            while file_text[line_num] != "\n":
                ret_list.append(file_text[line_num].strip())
                line_num += 1
                if line_num >= len(file_text):
                    break
                if file_text[line_num] == "\n":
                    break
            break
    if not bool(ret_list):
        return f"platform not found or no boards are supported for this platform: {platform}"
    return ret_list


def generate_workflow_matrix(board_list: list) -> str:
    if not isinstance(board_list, list):
        print(board_list)
        sys.exit(1)
    matrix_text = '{"boards":['
    for item in board_list:
        ignore = False
        for ex in exclude:
            if ex in item:
                ignore = True
        if not ignore:
            line = '"' + item.strip()
            if item != board_list[-1]:
                line += '", '
            else:
                line += '"'
            matrix_text += line
    matrix_text += "]}"
    return matrix_text


def cli() -> list:
    parser = argparse.ArgumentParser(
        prog=os.path.basename(__file__),
        description="generates board matrices for CI/CD workflows",
    )
    parser.add_argument(
        "-c",
        "--compiler",
        nargs=1,
        type=str,
        required=True,
        help="-c <compiler type>",
        metavar="",
    )
    parser.add_argument(
        "-p",
        "--platform",
        nargs=1,
        type=str,
        required=True,
        help="-p <platform>",
        metavar="",
    )
    args = parser.parse_args(sys.argv[1:])

    ret_list = list()
    if bool(args.compiler):
        if str(args.compiler[0]).lower() in platforms:
            ret_list.append(str(args.compiler[0]).lower().strip())
        else:
            print(f"acceptable compilers and platforms are: {platforms}")
            sys.exit(1)
    if bool(args.platform) and bool(ret_list):
        if args.platform[0].lower().strip() in platforms[ret_list[0]]:
            ret_list.append(str(args.platform[0]).lower().strip())
        else:
            print(
                f"compiler: {ret_list[0]}\nplatform unknown: {args.platform[0].lower().strip()}"
            )
    if len(ret_list) < 2:  # fatal error
        parser.print_help()
        sys.exit(1)
    return ret_list


def main():
    opts = cli()
    file_text = open_supported_boards_file(opts[0])
    board_list = get_boards_for_platform(file_text, opts[1])
    matrix_text = generate_workflow_matrix(board_list)
    print(matrix_text)


if __name__ == "__main__":
    main()
