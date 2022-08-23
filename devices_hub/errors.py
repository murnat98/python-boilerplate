from devices_hub.logger import get_logger


class LoggerError(Exception):
    """
    Base exception class for automatic logging
    """

    logger = ''

    def __init__(self, msg: str):
        super().__init__(msg)
        self.msg = msg
        logger = get_logger(self.logger)
        logger.error(self.msg)
