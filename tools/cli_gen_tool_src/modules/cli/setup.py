##
# @file setup.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief CodePreview/file generation external methods
# @version 1.0
# @date 2022-07-29
# @copyright Copyright (c) 2022
# Copyright (C) 2022 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.


class cliSetup(object):
    def __init__(self) -> None:
        super(cliSetup, self).__init__()

    def setup_h(self, item_string, place_cursor=False):
        def sequence_string_helper(seq):
            num_seq = len(seq)
            seq_lens_string = "{"
            seqs_string = "{"
            seq_lens = []
            seqs = []
            for key in seq:
                delim_str = str(seq[key]).strip("'")
                delim_str_len = len(delim_str)

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

        # process output
        output_buffer_name = "InputHandler_output_buffer"
        buffer_size = self.cliOpt["process output"]["var"]["buffer size"]
        buffer_char = "{'\\0'}"
        object_name = "inputHandler"
        output_buffer = self.fsdb["setup"]["h"]["filestring components"][
            "outputbuffer"
        ].format(
            outputbuffername=output_buffer_name,
            buffersize=buffer_size,
            bufferchar=buffer_char,
        )
        class_output = self.fsdb["setup"]["h"]["filestring components"][
            "classoutput"
        ].format(input_prm="input_prm", outputbuffer="InputHandler_output_buffer")

        class_constructor = self.fsdb["setup"]["h"]["filestring components"][
            "constructor"
        ].format(objectname=object_name, classoutput=class_output)
        if buffer_size == "":
            buffer_size = 0
        if int(buffer_size) == 0:
            output_buffer = ""
            class_constructor = self.fsdb["setup"]["h"]["filestring components"][
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

        loop_prototype = ""
        stream_string = self.cliOpt["process output"]["var"]["output stream"]
        if (
            self.cliOpt["builtin methods"]["var"]["outputToStream"] == True
            and stream_string != ""
            and stream_string != None
        ):
            loop_prototype = self.fsdb["setup"]["h"]["filestring components"][
                "prototypes"
            ]["loop"]

        setup_prototype = self.fsdb["setup"]["h"]["filestring components"][
            "prototypes"
        ]["setup"]

        setup_h = self.fsdb["setup"]["h"]["filestring"].format(
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
            setupprototype=setup_prototype,
            loopprototype=loop_prototype,
        )

        self.code_preview_dict["files"]["setup.h"]["file_lines_list"] = []
        docstring = self.generate_docstring_list_for_filename(
            "setup.h", "InputHandler autogenerated setup.h"
        )
        code_string = self.list_to_code_string(docstring)
        code_string = code_string + setup_h
        self.code_preview_dict["files"]["setup.h"][
            "file_lines_list"
        ] = code_string.split("\n")
        self.code_preview_dict["files"]["setup.h"][
            "file_string"
        ] = code_string
        self.set_code_string("setup.h", code_string, item_string, place_cursor)

    def setup_cpp(self, item_string, place_cursor=False):
        output_buffer_name = "InputHandler_output_buffer"
        setup_function_entry_string = "Setting up InputHandler..."
        object_name = "inputHandler"

        stream_string = self.cliOpt["process output"]["var"]["output stream"]

        command_list_string = ""
        for key in self.cliOpt["commands"]["parameters"]:
            # iterate through list
            command_parameters_name = (
                str(self.cliOpt["commands"]["parameters"][key]["functionName"]) + "_"
            )
            command_list_string += self.fsdb["setup"]["cpp"]["filestring components"][
                "addCommand"
            ]["call"].format(
                objectname=object_name, commandparametersname=command_parameters_name
            )

        buffer_size = self.cliOpt["process output"]["var"]["buffer size"]
        setup_function_entry = ""
        stream_string = self.cliOpt["process output"]["var"]["output stream"]
        if stream_string != "" and stream_string != None and int(buffer_size) != 0:
            setup_function_entry = self.fsdb["setup"]["cpp"]["filestring components"][
                "setup function output"
            ]["stream"].format(
                stream=self.cliOpt["process output"]["var"]["output stream"],
                setupstring=setup_function_entry_string,
            )
        elif stream_string == "" or stream_string == None and int(buffer_size) != 0:
            setup_function_entry = self.fsdb["setup"]["cpp"]["filestring components"][
                "setup function output"
            ]["buffer"].format(
                outputbuffer=output_buffer_name,
                setupstring=setup_function_entry_string,
            )

        default_function_string = ""
        if self.cliOpt["builtin methods"]["var"]["defaultFunction"] == True:
            default_function_string = self.fsdb["setup"]["cpp"][
                "filestring components"
            ]["defaultFunction"]["call"].format(
                objectname=object_name, defaultfunctionname="unrecognized"
            )

        begin_string = self.fsdb["setup"]["cpp"]["filestring components"]["begin"][
            "call"
        ].format(objectname=object_name)

        options_string = ""

        setup_function = self.fsdb["setup"]["cpp"]["filestring components"][
            "setup function"
        ].format(
            setupfunctionentry=setup_function_entry,
            defaultfunction=default_function_string,
            commandlist=command_list_string,
            begin=begin_string,
            options=options_string,
        )

        loop_function = ""
        if (
            self.cliOpt["builtin methods"]["var"]["outputToStream"] == True
            and stream_string != ""
            and stream_string != None
        ):
            loop_statements = self.fsdb["setup"]["cpp"]["filestring components"][
                "outputToStream"
            ]["call"].format(objectname=object_name, stream=stream_string)
            loop_function = self.fsdb["setup"]["cpp"]["filestring components"][
                "loop function"
            ].format(loopstatements=loop_statements)

        setup_cpp = self.fsdb["setup"]["cpp"]["filestring"].format(
            setupfunction=setup_function, loopfunction=loop_function
        )

        self.code_preview_dict["files"]["setup.cpp"]["file_lines_list"] = []
        docstring = self.generate_docstring_list_for_filename(
            "setup.cpp", "InputHandler autogenerated setup.cpp"
        )
        code_string = self.list_to_code_string(docstring)
        code_string = code_string + setup_cpp
        self.code_preview_dict["files"]["setup.cpp"][
            "file_lines_list"
        ] = code_string.split("\n")
        self.code_preview_dict["files"]["setup.cpp"][
            "file_string"
        ] = code_string
        self.set_code_string(
            "setup.cpp", code_string, "InputHandler_setup", place_cursor
        )


# end of file
