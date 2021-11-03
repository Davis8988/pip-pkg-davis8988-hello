# This module configures the root logger for logging
import logging
import inspect

# Returns the root logger
def getRootLogger(**kwargs):
    root_logger = logging.getLogger() if not logging.getLogger().hasHandlers() else logging.getLogger()
    if not root_logger.hasHandlers():
        summary_dict = _add_console_logging_handler()

    return root_logger


def _add_console_logging_handler(**kwargs):
    summary_dict = {"status" : True, "info" : '', 'logger': None}
    logger = kwargs.get("logger", None)
    if logger is None:
        func_name = inspect.stack[0][3]
        summary_dict['status'] = False
        summary_dict['info'] = f"Missing key 'logger' for module.func: {__name__ }.{func_name}()"
        return summary_dict
    summary_dict['logger'] = logger
    return summary_dict
