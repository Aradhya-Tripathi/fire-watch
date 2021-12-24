import json
import os
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Optional

import pymongo
from keydb import KeyDB
from rich.console import Console

import fire_watch

from .errorfactory import ConfigFileNotFound


class Flags(SimpleNamespace):
    """Class for application wide flags prints,
    to `stderr` in case of attribute error.
    """

    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError:
            fire_watch.print(f"[blod red]{name} flag does not exist")
            return


class Conf(dict):
    """dict like class allows accessing attributes"""

    def __getattr__(self, __name):
        return self.get(__name)


def get_config(base_path):
    """
    Search for config file in `fire_watch.config` name space
    if found return unsanitized config file as a dictionary.
    else raise `ConfigFileNotFound` error.
    """
    path = os.path.join(base_path, "config/config.json")
    if not os.path.exists(path):
        raise ConfigFileNotFound(path=path)

    with open(path) as f:
        return Conf(json.loads(f.read()))


def sanitized_configs(base_path: Path):
    """Sanitize config file if found by `get_config`"""
    conf = get_config(base_path)
    # TODO: sanitize config file
    return conf


def init_cache():
    """Connect to redis server with the configurations
    present in `fire_watch.conf`.
    """
    fire_watch.cache = KeyDB(
        host=fire_watch.conf.cache_conf["host"],
        port=fire_watch.conf.cache_conf["port"],
    )


def init_flags():
    fire_watch.flags = Flags()
    fire_watch.flags.use_secret = False if os.getenv("CI") else True


def set_debug_flags():
    fire_watch.flags.send_email = False
    fire_watch.flags.in_debug = True


def connect_db(conf: Conf):
    fire_watch.flags.db_name = (
        os.getenv("TESTDB") if conf.developer or os.getenv("CI") else os.getenv("DB")
    )
    client = pymongo.MongoClient(os.getenv("MONGO_URI"))
    fire_watch.print("[cyan green]Establishing Connection! :rocket:")
    fire_watch.db = client[fire_watch.flags.db_name]


def init_print_utils(
    file: Optional[str] = None,
):
    console = Console(file=file)
    fire_watch.print = console.print
    fire_watch.print_json = console.print_json
    fire_watch.print_exception = console.print_exception
