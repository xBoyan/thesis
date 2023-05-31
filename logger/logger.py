import os
from loguru import logger

LOGS_PATH = "C:\\Users\\Adam\\thesis\\logs\\test.log"

os.remove(LOGS_PATH)
logger.add(LOGS_PATH, level="TRACE")


def log_output(func):
    def log_output_wrapper(*args, **kwargs):
        logger.debug(f"Calling {func.__qualname__}")
        result = func(*args, **kwargs)

        logger.debug(f"Returning from {func.__qualname__}: {result}")
        return result

    return log_output_wrapper


def log_input_and_output(func):
    def log_input_and_output_wrapper(*args, **kwargs):
        _args = f", args: {args}" if args else ""
        _kwargs = f", kwargs: {kwargs}" if kwargs else ""
        logger.debug(f"Calling {func.__name__}{_args}{_kwargs}")

        result = func(*args, **kwargs)

        logger.debug(f"Returning from {func.__name__}: {result}")
        return result

    return log_input_and_output_wrapper
