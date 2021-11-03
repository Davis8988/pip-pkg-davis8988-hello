# This module configures the root logger for logging
import logging
import inspect
from sys import stdout  # Only need to log to console


# Returns a summary dict with the root logger under 'logger' key
def get_root_logger(**kwargs):
    result_dict = {"status" : True, "info" : '', 'logger': None}
    root_logger = logging.getLogger() if not logging.getLogger().hasHandlers() else logging.getLogger()
    if not root_logger.hasHandlers():
        add_console_logging_handler_result_dict = _add_console_logging_handler(logger=root_logger)  # Add console logging to 'root_logger' obj
        if not add_console_logging_handler_result_dict['status']:
            prev_err_msg = add_console_logging_handler_result_dict['info']
            err_msg = f"Error: {prev_err_msg} \nFailed adding console logging handler to root logger"
            # print(err_msg)
            result_dict['info'] = err_msg
            result_dict['status'] = False
            return result_dict
    result_dict['logger'] = root_logger
    return result_dict


# Adds a console logging handler
def _add_console_logging_handler(**kwargs):
    result_dict = {"status" : True, "info" : '', 'logger': None}
    logger = kwargs.get("logger", None)
    try:
        if logger is None:
            func_name = inspect.stack[0][3]
            raise TypeError(f"Missing key 'logger' for module.func: {__name__ }.{func_name}()")
        logger.addHandler(logging.StreamHandler(stdout))
        result_dict['logger'] = logger  # Success case
    except Exception as err_msg:
        result_dict['status'] = False
        result_dict['info'] = err_msg
        result_dict['logger'] = None
    return result_dict
