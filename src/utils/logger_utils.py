import logging

class Logger:
    _instance = None

    def __new__(cls, log_level=logging.INFO):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize(log_level)
        return cls._instance

    def _initialize(self, log_level):
        # Create a custom logger
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(log_level)

        # Create a console handler
        c_handler = logging.StreamHandler()

        # Create a formatter and set it for the handler
        c_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        c_handler.setFormatter(c_format)

        # Add the console handler to the logger
        self.logger.addHandler(c_handler)

    def get_logger(self):
        return self.logger
