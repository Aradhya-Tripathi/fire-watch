import logging
from core.settings import conf
from core.errorfactory import LogsNotEnabled


class Log:
    def __new__(cls, *args, **kwargs):
        if conf["logs"]:
            return super().__new__(cls, *args, **kwargs)
        raise LogsNotEnabled

    def __init__(self, *args, **kwargs):
        self._is_enabled = True
