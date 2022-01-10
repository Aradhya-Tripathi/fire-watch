import sys
from pathlib import Path

from dotenv import load_dotenv

import fire_watch

from .config_utils import (
    connect_db,
    init_cache,
    init_flags,
    init_print_utils,
    sanitized_configs,
)


def init():
    load_dotenv()
    _path = Path(__file__).resolve()
    # Initialize configuration
    fire_watch.conf = sanitized_configs(base_path=_path.parent)

    # Initialize application wide flags
    init_flags()

    # Initialize print utils
    init_print_utils(file=sys.stderr)

    # Connect to db
    connect_db(fire_watch.conf)
    init_cache()
