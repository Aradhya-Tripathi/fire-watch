from fire_watch.settings import conf
from fire_watch.errorfactory import LogsNotEnabled
import logging

FMT = "%(asctime)s:%(name)s:%(message)s"


def get_logger(logger_name: str, filename: str, level: int = 10) -> logging.getLogger:
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
    logger = logging.getLogger(logger_name)
    if conf["logs"]:
        logger.setLevel(level=level)
        file_handler = logging.FileHandler(filename, mode="a")
        file_handler.setFormatter(logging.Formatter(FMT))

        logger.addHandler(file_handler)
        return logger
    raise LogsNotEnabled
