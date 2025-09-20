import logging


class LoggerFactory:
    @staticmethod
    def create_logger(obj):
        name = type(obj).__name__
        return LoggerFactory.create_static_class_logger(name)

    @staticmethod
    def create_static_class_logger(class_name: str):
        logger = logging.getLogger(class_name)
        logger.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        return logger
