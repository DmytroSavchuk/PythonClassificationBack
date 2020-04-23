import logging
import sys


class ConsoleLogger:
    def __init__(self):
        logging.basicConfig(stream=sys.stderr, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logging.getLogger().setLevel(logging.INFO)

    def error(self, message, error):
        logging.error(message + f'. {str(error)}')

    def info(self, message):
        logging.info(message)


console_logger = ConsoleLogger()
