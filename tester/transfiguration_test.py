from Transpell.transfiguration import Transfiguration
import json


if __name__ == "__main__":
    with open("../Template/VenusA/Cmu/configure.json", "r", encoding="utf-8") as f:
        json_data = json.load

        trs = Transfiguration(json_data)
