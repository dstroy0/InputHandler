##
# @file no_dialog_file_manipulation.py
# @author Douglas Quigg (dstroy0 dquigg123@gmail.com)
# @brief no dialog file manipulation
# @version 1.0
# @date 2023-05-17
# @copyright Copyright (c) 2023
# Copyright (C) 2023 Douglas Quigg (dstroy0) <dquigg123@gmail.com>
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# version 3 as published by the Free Software Foundation.


from __future__ import absolute_import
import os
import glob
import json
import shutil
from modules.data_models import DataModels
from modules.pathing import Pathing


class FileManipulation(object):
    def __init__(self) -> None:
        super().__init__()
        FileManipulation.logger = self.get_child_logger(__name__)

    def write_cli_gen_tool_json(self):
        """writes session json

        Returns:
            int: filesize
        """
        if (
            self.session["opt"]["save_file_path"]
            not in self.session["opt"]["recent_files"]["paths"]
        ):
            self.session["opt"]["recent_files"]["paths"].append(
                self.session["opt"]["save_file_path"]
            )
        if len(self.session["opt"]["recent_files"]["paths"]) > int(
            self.session["opt"]["recent_files"]["num_paths_to_keep"]
        ):
            self.session["opt"]["recent_files"]["paths"].pop(0)

        size = self.write_json(self.session, Pathing.cli_gen_tool_json_path)
        if size > 0:
            FileManipulation.logger.info("session json saved")
        return size

    def write_json(self, dict_to_serialize: dict, path: str):
        """writes a json to disk

        Args:
            dict_to_serialize (dict): make this dict serializable
            path (str): the file to write
            create_error_dialog (bool, optional): create dialog on error if True. Defaults to False.

        Returns:
            int: -1 on error or filesize
        """
        file = open(path, "w", encoding="utf-8")
        file_name = os.path.abspath(path).split("/")[-1]
        if not file:
            file.close()
            FileManipulation.logger.info("Save " + file_name + " error.")
            return -1  # file error
        output_json = json.dumps(dict_to_serialize, indent=2, sort_keys=False)
        size = file.write(output_json)
        if size != -1:
            FileManipulation.logger.info(
                "wrote " + str(size) + " bytes to " + file_name
            )
            if dict_to_serialize["type"] != "session" and not self.headless:
                self.write_cli_gen_tool_json()
        else:
            FileManipulation.logger.info("Write " + file_name + " error.")
        file.close()
        return size

    def read_json(self, path: str):
        """reads json from disk

        Args:
            path (str): json path
            create_error_dialog (bool, optional): create dialog on error if True. Defaults to False.

        Returns:
            int: -2 if file doesnt exist, -3 on access error, -4 on zero filesize or invalid json or exception,
        """
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            FileManipulation.logger.info("file does not exist")
            return [-2, {}]  # file doesn't exist
        file = open(abs_path, "r", encoding="utf-8")
        if not file:
            file.close()
            FileManipulation.logger.warning("File access error.")
            return [-3, {}]  # access error
        data_in = file.read()
        file.close()
        try:
            read_json = json.loads(data_in)
            if "type" in read_json:
                json_type = read_json["type"]
                FileManipulation.logger.info(f"loaded json: {json_type}")
                return [len(data_in), read_json]
            elif len(read_json) == 0:
                return [-4, {}]
            else:
                FileManipulation.logger.info("invalid json type")
                FileManipulation.logger.debug(
                    "json.loads():\n" + str(json.dumps(read_json, indent=2))
                )
                return [-4, {}]
        except Exception as e:
            FileManipulation.logger.warning(str(e))
            return [-4, {}]

    def load_cli_gen_tool_json(self, path):
        """load session json

        Args:
            path (str): path to json

        Returns:
            int: filesize
        """
        read_json_result = self.read_json(
            os.path.abspath(os.path.join(path, "cli_gen_tool.json"))
        )
        error = read_json_result[0]
        _json = read_json_result[1]
        if error == -2:  # file not exists
            FileManipulation.logger.info(
                "cli_gen_tool.json doesn't exist, using default options"
            )
            _json = self.defaultGuiOpt
            _json["opt"]["inputhandler_config_file_path"] = self.default_config_path
            return _json
        if error == -3:
            FileManipulation.logger.warning(
                "open cli_gen_tool.json error; using default options"
            )
            _json = self.defaultGuiOpt
            _json["opt"]["inputhandler_config_file_path"] = self.default_config_path
            return _json
        return _json

    # TODO detect file structure as defined in DataModels
    def detect_output_type(self, project_path):
        pio_structure = DataModels.pio_structure
        arduino_structure = DataModels.arduino_structure
        if project_path == None:
            project_path = ""
        ino_search = glob.glob(os.path.join(project_path, "*.ino"))
        arduino_compatibility = False
        if bool(ino_search):
            # ino file detected
            arduino_compatibility = True
        if project_path.find("sketch") != -1:
            # empty sketch folder case
            arduino_compatibility = True
        if arduino_compatibility:
            FileManipulation.logger.info("detected arduino file structure")
        else:
            FileManipulation.logger.info("detected platformio file structure")
        return arduino_compatibility

    # TODO revert on fail
    def generate_cli(self, project_path: str = None) -> int:
        """generates the platform appropriate CLI in `project_path`
           set in preferences

        Args:
            project_path (str, optional): valid os path. Defaults to None.

        Returns:
            int: -1 invalid output directory, -2 invalid library directory, -3 create directory error,
                 -4 file write error
        """
        # require output directory
        if project_path == None or project_path == "":
            FileManipulation.logger.info("Output directory not set")
            return -1

        # get inputhandler src/ path
        src = os.path.abspath(os.path.join(self.lib_root_path, "/src/"))
        if os.path.exists(os.path.abspath(os.path.join(src, "InputHandler.h"))):
            FileManipulation.logger.info("found library")
        else:
            FileManipulation.logger.info("couldn't find library; aborting!")
            return -2
        src_path = os.path.abspath(src)

        # check destination path
        dst = os.path.abspath(project_path)
        if os.path.exists(dst):
            FileManipulation.logger.info("found project dir")
        else:
            os.mkdir(dst)
            if os.path.exists(dst):
                FileManipulation.logger.info("created project dir")
            else:
                FileManipulation.logger.info("couldn't make project directory!")
            return -1

        # detect output type
        if self.detect_output_type(project_path):
            # arduino
            cli_path = os.path.join(project_path, "CLI")
            cli_src_path = os.path.join(cli_path, "src")
            cli_config_h_path = os.path.join(cli_src_path, "config/config.h")
        else:
            # platformio
            cli_path = os.path.join(project_path, "lib", "CLI")
            cli_src_path = cli_path  # os.path.join(cli_path, "src")
            cli_config_h_path = os.path.join(cli_src_path, "config/config.h")

        # Create CLI file structure
        # Create in project dir
        # /CLI/
        # copy /InputHandler/src/ to project_path/CLI/src/
        # remove original config.h
        if not os.path.exists(cli_path):
            FileManipulation.logger.info(
                "creating dir <CLI> in <" + str(project_path) + ">"
            )
            shutil.copytree(src_path, cli_src_path)
            os.remove(cli_config_h_path)
            if os.path.exists(cli_src_path):
                FileManipulation.logger.info(
                    "dir <CLI> created in <" + str(project_path) + ">"
                )
            else:
                FileManipulation.logger.info(
                    "Error creating dir <CLI> in <"
                    + str(project_path)
                    + "> aborting generation!"
                )
                return -3
        else:
            FileManipulation.logger.info(
                "dir <CLI> already exists in <" + str(project_path) + ">"
            )
            shutil.rmtree(cli_path)
            shutil.copytree(src_path, cli_src_path)
            os.remove(cli_config_h_path)

        # update code
        self.code_preview_dict["files"]["README.md"]["file_string"] = self.readme_md()
        self.code_preview_dict["files"]["config.h"]["file_string"] = self.config_h()
        self.code_preview_dict["files"]["CLI.h"]["file_string"] = self.cli_h()
        self.code_preview_dict["files"]["parameters.h"][
            "file_string"
        ] = self.parameters_h()
        self.code_preview_dict["files"]["functions.h"][
            "file_string"
        ] = self.functions_h()

        # write library.properties to cli_path
        path = os.path.join(cli_path, "library.properties")
        file_string = self.fsdb["library"]["properties"]["filestring"].format(
            lib_version=self.lib_version
        )
        size = self.write_cli_file(path, file_string)
        if size == -1:
            FileManipulation.logger.warning(
                f"couldnt write library.properties, removing directory:\n{cli_path}"
            )
            os.rmtree(cli_path)
            return -4

        # write cli files to cli_path
        files = self.code_preview_dict["files"].keys()
        for filename in files:
            file_string = self.code_preview_dict["files"][filename]["file_string"]
            if filename == "README.md":
                path = os.path.join(project_path, "CLI_" + filename)
            elif filename == "config.h":
                path = cli_config_h_path
            else:
                path = os.path.join(cli_src_path, filename)
            size = self.write_cli_file(path, file_string)
            if size == -1:
                FileManipulation.logger.warning(
                    f"couldnt write {filename}, removing directory:\n{cli_path}"
                )
                os.rmtree(cli_path)
                return -4

    def write_cli_file(self, path: str, string_to_write: str) -> int:
        """writes a cli file with UTF-8 encoding
        Args:
            path (str): path to file
            file_to_write (str): file string
        Returns:
            int: the number of bytes written if successful else -1
        """
        file = open(path, "w", encoding="utf-8")
        filename = os.path.basename(os.path.abspath(path))
        if not file:
            FileManipulation.logger.info(f"Save {filename} error.")
            file.close()
            return -1  # file error
        # file object
        out = bytearray(string_to_write)
        size = file.write(out)
        if size != -1:
            FileManipulation.logger.info(f"wrote {size} bytes to {filename}")
        else:
            FileManipulation.logger.info(f"Write {filename} error.")
            file.close()
            return -1
        file.close()
        return size
