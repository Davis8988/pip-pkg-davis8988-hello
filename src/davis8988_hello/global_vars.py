# This module contains variables that should be used globally between modules

import logging
from os import environ as env_vars_dict

# Logging
_logging_format_date = '%H:%M:%S'
_logging_console_level = env_vars_dict.get('LOGLEVEL', 'DEBUG').upper()
spaces_count = len(_logging_console_level)
_logging_console_format = f'[%(levelname)-{spaces_count}s] %(asctime)s : %(message)s'
_logging_console_date_format = _logging_format_date
