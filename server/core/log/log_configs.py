from core.settings import conf
from core.errorfactory import LogsNotEnabled
from importlib import import_module


class Log:
    # TODO: Find a better way to do this (if required)
    #! init class only if configurations allow it
    #! Ristrict all logging if logger is disabled
    def __new__(cls, *args, **kwargs):
        if conf["logs"]:
            return super().__new__(cls, *args, **kwargs)
        raise LogsNotEnabled

    def __init__(self, *args, **kwargs):
        self.logger = import_module("logging")
