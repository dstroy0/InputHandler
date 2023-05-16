import os
import json


class NoDialogFileManipulation(object):
    def __init__(self) -> None:
        super(NoDialogFileManipulation, self).__init__()
    
    def setup_logging(self):
        NoDialogFileManipulation.logger = self.get_child_logger(__name__)

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

        path = os.path.abspath(self.cli_gen_tool_json_path)
        size = self.write_json(self.session, path)
        if size > 0:
            NoDialogFileManipulation.logger.info("session json saved")
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
        file = open(os.path.abspath(path), "w")
        file_name = os.path.abspath(path).split("/")[-1]
        if not file:
            file.close()
            NoDialogFileManipulation.logger.info("Save " + file_name + " error.")
            return -1  # file error
        output_json = json.dumps(dict_to_serialize, indent=2, sort_keys=False)
        out = bytearray(output_json)
        size = file.write(out)
        if size != -1:
            NoDialogFileManipulation.logger.info(
                "wrote " + str(size) + " bytes to " + file_name
            )
            if dict_to_serialize["type"] != "session" and not self.headless:
                self.write_cli_gen_tool_json()
        else:
            NoDialogFileManipulation.logger.info("Write " + file_name + " error.")
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
            NoDialogFileManipulation.logger.info("file does not exist")
            return [-2, {}]  # file doesn't exist
        file = open(abs_path, "r", encoding="utf-8")
        if not file:
            file.close()
            NoDialogFileManipulation.logger.warning("File access error.")
            return [-3, {}]  # access error
        data_in = file.read()
        file.close()
        try:
            read_json = json.loads(data_in)
            if "type" in read_json:
                json_type = read_json["type"]
                NoDialogFileManipulation.logger.info(f"loaded json: {json_type}")
                return [len(data_in), read_json]
            elif len(read_json) == 0:
                return [-4, {}]
            else:
                NoDialogFileManipulation.logger.info("invalid json type")
                NoDialogFileManipulation.logger.debug(
                    "json.loads():\n" + str(json.dumps(read_json, indent=2))
                )
                return [-4, {}]
        except Exception as e:
            NoDialogFileManipulation.logger.warning(str(e))
            return [-4, {}]
    def load_cli_gen_tool_json(self, path):
        """load session json

        Args:
            path (str): path to json

        Returns:
            int: filesize
        """        
        read_json_result = self.read_json(path)
        error = read_json_result[0]
        _json = read_json_result[1]
        if error == -2:  # file not exists
            NoDialogFileManipulation.logger.info(
                "cli_gen_tool.json doesn't exist, using default options"
            )
            _json = self.defaultGuiOpt
            _json["opt"]["inputhandler_config_file_path"] = self.default_lib_config_path
            return _json
        if error == -3:            
            NoDialogFileManipulation.logger.warning(
                "open cli_gen_tool.json error; using default options"
            )
            _json = self.defaultGuiOpt
            _json["opt"]["inputhandler_config_file_path"] = self.default_lib_config_path
            return _json
        return _json