import logging

import fire_watch
from fire_watch.errorfactory import LogsNotEnabled

FMT = "%(asctime)s:%(name)s:%(message)s"


def get_logger(
    logger_name: str,
    filename: str,
    level: int = 10,
) -> logging.getLogger:
    """Simple logger configuration implemented to support
       safe logging.

    Args:
        logger_name (str): name given to current logger.
        level (int): severity level.
        filename (str): file to throw all logs to.

    Raises:
        LogsNotEnabled: Raised if logging is tried with out enabling logger in configurations

    Returns:
        logging.getLogger: logger object
    """
    if fire_watch.conf["logs"]:
        logger = logging.getLogger(logger_name)

        file_handler = logging.FileHandler(filename, mode="a")
        file_handler.setFormatter(logging.Formatter(FMT))
        file_handler.setLevel(level=level)

        logger.addHandler(file_handler)
        return logger
    raise LogsNotEnabled
