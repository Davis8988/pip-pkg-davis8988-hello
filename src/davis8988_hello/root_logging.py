# This module configures the root logger for logging
import logging

# Returns the root logger
def getRootLogger(**kwargs):
    root_logger = logging.getLogger() if not logging.getLogger().hasHandlers() else logging.getLogger()
    return root_logger

