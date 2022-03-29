"""This creates a singleton object of our application for Logging."""
import logging
import os
import datetime
from django.conf import settings

class Logger:
    """
    This creates a logger instance of rentezzy application.
    It is used for demonstrating singleton implementation.
    """
    _logger = None

    def __init__(self):
        if not self._logger:
            print("Logging Initialized...")
            self._logger = logging.getLogger("crumbs")
            self._logger.setLevel(logging.DEBUG)
            formatter = logging.Formatter(
                '%(asctime)s \t [%(levelname)s | %(filename)s:%(lineno)s] > %(message)s'
            )
            now = datetime.datetime.now()
            dir_name = settings.LOG_LOCATION

            if not os.path.isdir(dir_name):
                os.mkdir(dir_name)

            file_handler = logging.FileHandler(
                str(dir_name) + "/log_" + now.strftime("%Y-%m-%d") + ".log"
            )
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)

    def get_logger(self):
        """
        Getter for returning the singleton object.
        """
        return self._logger
