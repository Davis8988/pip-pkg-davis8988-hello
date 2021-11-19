# This module contains variables that should be used globally between modules

import logging
from os import environ as env_vars_dict

# Logging
_logging_format_date = '%H:%M:%S'
_logging_console_level = env_vars_dict.get('LOGLEVEL', 'DEBUG').upper()

_logging_console_format = '[{levelname:^5s}] {asctime} : {message}'
_logging_console_date_format = _logging_format_date
