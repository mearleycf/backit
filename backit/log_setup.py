from loguru import logger
import os
import sys

class LogConfig:
    def __init__(self, config):
        self.config = config
        self._configure_logger()

    def _configure_logger(self):
        logger.remove()