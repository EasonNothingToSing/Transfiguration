import os.path

from .transfiguration import Transfiguration
import glob
import json


class Transmake:
    def __init__(self, path: str):
        self._path = path
        self._json_dir = None
        self._trans = Transfiguration()
        self.scan_dir()


    def scan_dir(self):
        self._json_dir = glob.glob(self._path + "/**/*.json", recursive=True)

        return dir
    
    def tmake(self):
        for file in self._json_dir:
            self._trans.process(file)

