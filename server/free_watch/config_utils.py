import json
import os
from pathlib import Path
from types import SimpleNamespace

import free_watch

from .errorfactory import ConfigFileNotFound


def get_config(base_path):
    """
    Search for config file in `core.config` name space
    if found return unsanitized config file as a dictionary.
    else raise `ConfigFileNotFound` error.
    """
    path = os.path.join(base_path, "config/config.json")
    if not os.path.exists(path):
        raise ConfigFileNotFound(path=path)

    with open(path) as f:
        return json.loads(f.read())


def sanitized_configs(base_path: Path):
    """Sanitize config file if found by `get_config`"""
    conf = get_config(base_path)
    # TODO: sanitize config file
    return conf


def init_flags():
    free_watch.flags = SimpleNamespace()
