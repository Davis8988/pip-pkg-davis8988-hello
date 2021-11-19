# This module configures the root logger for logging
import logging
import davis8988_hello.global_vars as global_vars
import inspect
from sys import stdout  # Only need to log to console


# Returns the root logger or raises an exception
def get_root_logger_or_fail(**kwargs):
    get_root_logger_result_dict = get_root_logger() 
    if not get_root_logger_result_dict['result']:
        print(get_root_logger_result_dict['info']) 
        raise Exception(get_root_logger_result_dict['info']) 
    return get_root_logger_result_dict['root_logger']  # No need to check if this is not None since: get_root_logger_result_dict['result'] == True


# Returns a result dict with the root logger under 'logger' key
def get_root_logger(**kwargs):
    result_dict = {"result" : True, "info" : '', 'root_logger': None}
    root_logger = logging.getLogger()
    if not root_logger.hasHandlers():
        add_console_logging_handler_result_dict = _add_console_logging_handler(logger=root_logger)  # Add console logging to 'root_logger' obj
        if not add_console_logging_handler_result_dict['result']:
            prev_err_msg = add_console_logging_handler_result_dict['info']
            err_msg = f"Error: {prev_err_msg} \nFailed adding console logging handler to root logger"
            # print(err_msg)
            result_dict['info'] = err_msg
            result_dict['result'] = False
            return result_dict
    log_level = global_vars._logging_console_level
    root_logger.setLevel(log_level)
    result_dict['root_logger'] = root_logger
    return result_dict


# Adds a console logging handler
def _add_console_logging_handler(**kwargs):
    result_dict = {"result" : True, "info" : '', 'logger': None}
    logger = kwargs.get("logger", None)
    try:
        if logger is None:
            func_name = inspect.stack[0][3]
            raise TypeError(f"Missing key 'logger' for module.func: {__name__ }.{func_name}()")
        console_handler = logging.StreamHandler(stdout)
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter(fmt=global_vars._logging_console_format, datefmt=global_vars._logging_console_date_format)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        result_dict['logger'] = logger  # Success case
    except Exception as err_msg:
        result_dict['result'] = False
        result_dict['info'] = err_msg
        result_dict['logger'] = None
    return result_dict
