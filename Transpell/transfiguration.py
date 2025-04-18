import json
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import pandas
import re
import os
import ast

from global_env import *
from .expression_transformer import ExpressionTransformer


class Transfiguration:
    _TEMPLATE_PATH = os.path.join(os.getcwd(), "Template") # system default template path

    def __init__(self):
        self._configure_file_name = None
        self._configure_handler = None
        self._targets = None
        self._target_name = None
        self._database = None
        self._template_output = None
        self._global_dict = {}
        self._env = Environment(loader=FileSystemLoader([Transfiguration._TEMPLATE_PATH, os.getcwd()]))

    def process(self, configure_file: str):
        """
        Process the JSON configuration file and render the template files.

        1. Opens the JSON configuration file
        2. Depends on the JSON configuration file database and targets, initialize expression handler, registe the function and database route
        3. Processes its content with AST
        4. Traverses the JSON structure recursively to handle nested structures
        5. Renders the template files using Jinja2 with the processed JSON data
        6. Returns the rendered template outputs

        :param configure_file: The path to the JSON configuration file.
        :return: A list of rendered template outputs.
        """


        self._configure_file_name = configure_file
        with open(self._configure_file_name, "r", encoding="utf-8") as f:
            configure_json = json.load(f)
            self._configure_handler = configure_json
            # Get the target name and it is a list
            self._targets = configure_json['Target_Name']
            # Get database path
            self._database_filter(configure_json['Datebase'])
            # preprocess

        self.expression_handler = ExpressionTransformer(self._database)

        self._template_output = self._traverse_recursive("", configure_json)

        print("Global: ", self._global_dict)

        print(self._template_output)

        # json_out = []

        # for _target in self._targets:
        #     self._template_output["Target_Name"] = _target
        #     self._target_name = _target
        #     t_path = Path(os.path.normpath(os.path.join(os.path.dirname(self._configure_file_name), _target))).as_posix()
        #     template = self._env.get_template(t_path)
        #     json_out.append(template.render(Input=self._template_output))

        # return json_out

    def get_target_name(self):
        return self._targets

    def _database_filter(self, database : str):
        database_string = ""
        if database == "~/database":
            self._database = os.path.join(Transfiguration._TEMPLATE_PATH, "database")

    def _traverse_recursive(self, key: str, config: any):
        # Handle dictionaries
        if isinstance(config, dict):
            return {k: self._traverse_recursive(k, v) for k, v in config.items()}
        # Handle lists
        if isinstance(config, list):
            return [self._traverse_recursive(key, i) for i in config]
        # Handle strings
        if isinstance(config, str):
            try:
                tree = ast.parse(config, mode='eval')

                tree = ast.fix_missing_locations(self.expression_handler.visit(tree))

                transformed_code = ast.unparse(tree).strip()

                return eval(transformed_code)

            except NameError:
                self._global_dict[key] = config
                return config

            except SyntaxError:
                self._global_dict[key] = config
                return config
