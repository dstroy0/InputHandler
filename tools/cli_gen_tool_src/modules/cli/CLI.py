##
# @file CLI.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief CodePreview/file generation external methods
# @version 1.0
# @date 2023-01-08
# @copyright Copyright (c) 2022
# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.

import os
import glob


class cliH(object):
    """CLI.h generator

    Args:
        object (object): base object specialization
    """

    def __init__(self) -> None:
        """the constructor"""
        super(cliH, self).__init__()
        self.cliopt = self.cliOpt
        self.command_index = self.cliopt["commands"]["index"]

    def cli_h(self, item_string: str, place_cursor: bool = False) -> None:
        """generates the CLI.h file component of the InputHandler
        autogenerated CLI

        Args:
            item_string (str): code to highlight
            place_cursor (bool, optional): move cursor to highlighted code. Defaults to False.
        """

        def sequence_string_helper(seq: str) -> list:
            """make part of a valid C++11 array

            Args:
                seq (str): The sequence of characters to encode

            Returns:
                list: number of sequences, sequence char lens, sequence string
            """
            control_char = [
                "0",
                "a",
                "b",
                "t",
                "n",
                "v",
                "f",
                "r",
                '"',
            ]
            num_seq = len(seq)
            seq_lens_string = "{"
            seqs_string = "{"
            seq_lens = []
            seqs = []
            for key in seq:
                delim_str_len = 0
                delim_str = str(seq[key]).replace("'", "").strip()
                p = 0
                for i in range(len(delim_str)):
                    if delim_str[p] == "\\":
                        if len(delim_str) > 1 and delim_str[p + 1] in control_char:
                            delim_str_len += 1
                            p += 2
                        else:
                            delim_str_len += 1
                            p += 1
                    else:
                        delim_str_len += 1
                        p += 1
                    if p >= len(delim_str):
                        break
                seq_lens.append(delim_str_len)
                seqs.append(seq[key])

            for i in range(len(seq_lens)):
                seq_lens_string = seq_lens_string + str(seq_lens[i])
                seqs_string = (
                    seqs_string
                    + '"'
                    + str(repr(seqs[i])).strip("'").replace("\\\\", "\\")
                    + '"'
                )
                if i != len(seq_lens) - 1:
                    seq_lens_string = seq_lens_string + ", "
                    seqs_string = seqs_string + ", "
            seq_lens_string = seq_lens_string + "}"
            seqs_string = seqs_string + "}"
            return [num_seq, seq_lens_string, seqs_string]

        setup_function_entry_string = "Setting up InputHandler..."
        setup_function_exit_string = "InputHandler setup complete."

        # process output
        output_buffer_name = "InputHandler_output_buffer"
        buffer_size = self.cliOpt["process output"]["var"]["buffer size"]
        buffer_char = "{'\\0'}"
        object_name = "inputHandler"
        output_buffer = self.fsdb["CLI"]["h"]["filestring components"][
            "outputbuffer"
        ].format(
            outputbuffername=output_buffer_name,
            buffersize=buffer_size,
            bufferchar=buffer_char,
        )
        class_output = self.fsdb["CLI"]["h"]["filestring components"][
            "classoutput"
        ].format(input_prm="input_prm", outputbuffer="InputHandler_output_buffer")

        class_constructor = self.fsdb["CLI"]["h"]["filestring components"][
            "constructor"
        ].format(objectname=object_name, classoutput=class_output)
        if buffer_size == "":
            buffer_size = 0
        if int(buffer_size) == 0:
            output_buffer = ""
            class_constructor = self.fsdb["CLI"]["h"]["filestring components"][
                "constructor"
            ].format(objectname=object_name, classoutput="")

        # process parameters
        pprm = self.cliOpt["process parameters"]["var"]
        process_name = pprm["process name"]
        process_eol = (
            str(repr(pprm["end of line characters"])).strip("'").replace("\\\\", "\\")
        )
        process_ipcc = (
            str(repr(pprm["input control char sequence"]))
            .strip("'")
            .replace("\\\\", "\\")
        )
        process_wcc = str(repr(pprm["wildcard char"])).strip("'").replace("\\\\", "\\")
        delim_seq = pprm["data delimiter sequences"]
        ststp_seq = pprm["start stop data delimiter sequences"]

        result = sequence_string_helper(delim_seq)
        num_delim_seq = result[0]
        delim_seq_lens_string = result[1]
        delim_seqs_string = result[2]

        result = sequence_string_helper(ststp_seq)
        num_ststp_pairs = int(result[0] / 2)
        ststp_seq_lens_string = result[1]
        ststp_seqs_string = result[2]

        stream_string = self.cliOpt["process output"]["var"]["output stream"]
        command_list_string = ""

        for root_command_index in self.command_index:
            # addCommand root commands only
            if int(self.command_index[root_command_index]["root index key"]) == int(
                self.command_index[root_command_index]["parameters key"]
            ):
                command_parameters_name = (
                    str(
                        self.cliOpt["commands"]["parameters"][
                            self.command_index[root_command_index]["parameters key"]
                        ]["functionName"]
                    )
                    + "_"
                )
                command_list_string += self.fsdb["CLI"]["h"]["filestring components"][
                    "addCommand"
                ]["call"].format(
                    objectname=object_name,
                    commandparametersname=command_parameters_name,
                )

        buffer_size = self.cliOpt["process output"]["var"]["buffer size"]
        setup_function_entry = ""
        setup_function_exit = ""
        stream_string = self.cliOpt["process output"]["var"]["output stream"]

        _lc = ""
        if self.cliopt["builtin methods"]["var"]["listCommands"]:
            _lc = f"\n  {object_name}.listCommands(); // prints commands available to user"
        _ls = ""
        if self.cliopt["builtin methods"]["var"]["listSettings"]:
            _ls = f"\n  {object_name}.listSettings(); // prints InputHandler settings"

        if stream_string != "" and stream_string != None and int(buffer_size) != 0:
            setup_function_entry = self.fsdb["CLI"]["h"]["filestring components"][
                "setup function output"
            ]["stream"]["entry"].format(
                stream=stream_string,
                outputstring=setup_function_entry_string,
                ls=_ls,
                lc=_lc,
            )
            setup_function_exit = self.fsdb["CLI"]["h"]["filestring components"][
                "setup function output"
            ]["stream"]["exit"].format(
                stream=stream_string,
                outputstring=setup_function_exit_string,
                objectname = object_name,
                ls=_ls,
                lc=_lc,
            )

        elif stream_string == "" or stream_string == None and int(buffer_size) != 0:
            setup_function_entry = self.fsdb["CLI"]["h"]["filestring components"][
                "setup function output"
            ]["buffer"]["entry"].format(
                outputbuffer=output_buffer_name,
                outputstring=setup_function_entry_string,
                ls=_ls,
                lc=_lc,
            )
            setup_function_exit = self.fsdb["CLI"]["h"]["filestring components"][
                "setup function output"
            ]["buffer"]["exit"].format(
                outputbuffer=output_buffer_name,
                outputstring=setup_function_exit_string,
                ls=_ls,
                lc=_lc,
            )

        default_function_string = ""
        if self.cliOpt["builtin methods"]["var"]["defaultFunction"] == True:
            default_function_string = self.fsdb["CLI"]["h"]["filestring components"][
                "defaultFunction"
            ]["call"].format(objectname=object_name, defaultfunctionname="unrecognized")

        begin_string = self.fsdb["CLI"]["h"]["filestring components"]["begin"][
            "call"
        ].format(objectname=object_name)

        options_string = ""

        setup_function = self.fsdb["CLI"]["h"]["filestring components"][
            "setup function"
        ].format(
            setupfunctionentry=setup_function_entry,
            defaultfunction=default_function_string,
            commandlist=command_list_string,
            begin=begin_string,
            options=options_string,
            setupfunctionexit=setup_function_exit,
        )

        loop_function = ""
        if (
            self.cliOpt["builtin methods"]["var"]["outputToStream"] == True
            and stream_string != ""
            and stream_string != None
        ):
            loop_statements = self.fsdb["CLI"]["h"]["filestring components"][
                "getCommandFromStream"
            ]["call"].format(objectname=object_name, stream=stream_string)
            loop_statements += self.fsdb["CLI"]["h"]["filestring components"][
                "outputToStream"
            ]["call"].format(objectname=object_name, stream=stream_string)

            loop_function = self.fsdb["CLI"]["h"]["filestring components"][
                "loop function"
            ].format(loopstatements=loop_statements)

        # arduino compatibility
        compatibility = ""
        project_path = self.session["opt"]["cli_output_dir"]
        if project_path:
            file_structure = glob.glob(os.path.join(project_path, "*.ino"))
            if file_structure:
                compatibility = '\n    #include "InputHandler.cpp"'

        setup_h = self.fsdb["CLI"]["h"]["filestring"].format(
            arduino_compatibility=compatibility,
            objectname=object_name,
            outputbuffer=output_buffer,
            constructor=class_constructor,
            processname=process_name,
            processeol=process_eol,
            processinputcontrolchar=process_ipcc,
            processwildcardchar=process_wcc,
            numdelimseq=num_delim_seq,
            delimseqlens=delim_seq_lens_string,
            delimseqs=delim_seqs_string,
            numstartstoppairs=num_ststp_pairs,
            startstopseqlens=ststp_seq_lens_string,
            startstopseqs=ststp_seqs_string,
            setupfunction=setup_function,
            loopfunction=loop_function,
        )

        self.code_preview_dict["files"]["CLI.h"]["file_lines_list"] = []
        docstring = self.generate_docstring_list_for_filename(
            "CLI.h", "InputHandler autogenerated CLI.h"
        )
        code_string = self.list_to_code_string(docstring)
        code_string = code_string + setup_h
        self.code_preview_dict["files"]["CLI.h"]["file_lines_list"] = code_string.split(
            "\n"
        )
        self.code_preview_dict["files"]["CLI.h"]["file_string"] = code_string
        self.set_code_string("CLI.h", code_string, item_string, place_cursor)


# end of file
