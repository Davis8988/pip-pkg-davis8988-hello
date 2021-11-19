# This module contains variables that should be used globally between modules

import logging
import os.environ

# Logging
_logging_format_date = '%H:%M:%S'
_logging_console_format = '[%(levelname)-5s] %(asctime)s : %(message)s'
_logging_console_date_format = _logging_format_date
_logging_console_level = os.environ.get('LOGLEVEL', 'DEBUG').upper()
