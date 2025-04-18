import os.path
import global_env
from .transfiguration import Transfiguration
import glob
import json


class Transmake:
    def __init__(self, target_name, path: str):
        self._path = path
        self._target_name = target_name
        # Search for json files in the path
        self._json_dir = None
        self._trans = Transfiguration()
        self.scan_dir()

    def scan_dir(self):
        self._json_dir = glob.glob(self._path + "/**/*.json", recursive=True)
    
    def tmake(self):
        output_target = os.path.join(global_env.__TRANSFIGURATION_RUN_PATH__, "out", self._target_name)
        os.makedirs(output_target, exist_ok=True)
        for file in self._json_dir:
            # using Transfiguration to process the json file and render the template
            self._trans.process(file)
            # file_name = self._trans.get_target_name()
            # for o, n in zip(output, file_name):
            #     file_name = os.path.join(global_env.__TRANSFIGURATION_RUN_PATH__, "out", self._target_name, n)
            #     with open(file_name, 'w', encoding='utf-8') as f:
            #         f.write(o)
