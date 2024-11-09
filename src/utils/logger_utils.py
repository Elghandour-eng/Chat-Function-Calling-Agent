import logging
from logging.handlers import RotatingFileHandler

class Logger:
    _instance = None

    def __new__(cls, log_file='app.log', log_level=logging.INFO):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize(log_file, log_level)
        return cls._instance

    def _initialize(self, log_file, log_level):
        # Create a custom logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        # Create handlers
        c_handler = logging.StreamHandler()
        f_handler = RotatingFileHandler(log_file, maxBytes=2000, backupCount=5)

        # Create formatters and add them to handlers
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to the logger
        self.logger.addHandler(c_handler)
        self.logger.addHandler(f_handler)

    def get_logger(self):
        return self.logger