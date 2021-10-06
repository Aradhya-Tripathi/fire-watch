from core.settings import conf
from core.errorfactory import LogsNotEnabled
import logging


def get_logger(filename: str, level: int, formatter: str = None) -> logging.getLogger:
    """Get pre configured logger object with the configurations
       set above.

    Args:
        filename (str): `Log File`
        level (int): `Severity level`
        formatter (str): `Log formatted`

    Returns:
        Log: Logger object
    """
    if conf["logs"]:
        logger = logging.getLogger(__name__)
        logger.setLevel(level=level)
        file_handler = logging.FileHandler(filename, mode="a")
        if formatter:
            file_handler.setFormatter(logging.Formatter(formatter))
        logger.addHandler(file_handler)
        return logger
    raise LogsNotEnabled
