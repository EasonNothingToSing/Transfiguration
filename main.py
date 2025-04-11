from Transpell import *
from global_env import *


if __name__ == "__main__":
    global_var_init()
    tmake = Transmake("./Template/VenusA/Bsp")
    tmake.tmake()
