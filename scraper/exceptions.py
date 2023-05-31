from logger import logger


class MethodNotImplemented(Exception):
    """
    Raised when used method is not implemented in current class
    """
    pass


class InvalidItem(Exception):
    """
    Raised when item data is either invalid or incomplete
    """
    def __init__(self, msg):
        self.msg = msg

        logger.warning(msg)


class ScrapUnsuccessful(Exception):
    """
    Raised when error occurred during scrapping
    """
    def __init__(self, msg, log_to_console=True):
        self.msg = msg

        logger.warning(msg) if log_to_console else logger.trace(msg)
