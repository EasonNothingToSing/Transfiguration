import os
import sys
import logging

__all__ = ['global_var_init', 'global_set_var', 'global_get_var']
__global_var = {}

__TRANSFIGURATION_RUN_PATH__ = os.path.dirname(os.path.abspath(__file__))
__TRANSFIGURATION_TRANSPELL_MODULE_PATH__ = os.path.join(__TRANSFIGURATION_RUN_PATH__, "Transpell")

os.chdir(__TRANSFIGURATION_RUN_PATH__)

sys.path.append(__TRANSFIGURATION_TRANSPELL_MODULE_PATH__)


def global_var_init():
    global __global_var
    __global_var = {}


def global_set_var(key, value):
    global __global_var
    __global_var[key] = value


def global_get_var(key):
    global __global_var
    try:
        return __global_var[key]
    except KeyError as error:
        logging.error("Global '%s' value not exist, <error: '%s'> " % (key, error))
