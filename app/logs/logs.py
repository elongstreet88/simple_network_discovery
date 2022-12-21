import logging
from logging.config import dictConfig
from typing import Any
from pydantic import BaseModel
import logging.config

"""
Default logging configuration.
Hooks into uvicorn and handles formatting
"""
LOGGING_CONFIG = { 
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s | %(filename)s | %(asctime)s | %(message)s", # Example: [INFO:     | app.py | 2022-06-03 20:59:59 | Dummy Info]
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    'handlers': {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    },
    'loggers': {
        "api": {
            "handlers": ["default"], 
            "level": logging.getLogger("uvicorn.access").level
        },
        '': {  # root logger
            "handlers": ["default"], 
            "level": logging.getLogger("uvicorn.access").level,
            'propagate': False
        },
        '__main__': {  # if __name__ == '__main__'
            "handlers": ["default"], 
            "level": logging.getLogger("uvicorn.access").level,
            'propagate': False
        },
    }
}

# Health endpoint filter
class HealthEndpointFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        return record.args and len(record.args) >= 3 and record.args[2] != "/health"

def get_logger(name:str) -> logging.Logger:
    """Sets up logger using default Simple API configurations

    Args:
        name (str): Name of logger, typically __name__

    Returns:
        logging.Logger: Returns a ready to use logger
    """

    # Load logging config
    logging.config.dictConfig(LOGGING_CONFIG)

    # Add health endpoint filter
    logging.getLogger("uvicorn.access").addFilter(HealthEndpointFilter())

    # Get logger
    logger = logging.getLogger(name)

    # Return logger
    return logger