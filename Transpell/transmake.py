from .transfiguration import Transfiguration
import glob


class Transmake:
    def __init__(self, path: str):
        self._path = path

    def scan_dir(self):
        dir = glob.glob(self._path + "/**/*.json", recursive=True)

        return dir
    
    def tmake(self, dir):
        for file in dir:
            with open(file, "r", encoding="utf-8") as f:
                json_data = f.read()
                trs = Transfiguration(json_data, "a")
                output = trs.get_result()
                print(output)

