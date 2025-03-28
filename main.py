from Transpell import *


if __name__ == "__main__":
    tmake = Transmake("./Template/VenusA/Bsp")
    tmake.tmake(tmake.scan_dir())
