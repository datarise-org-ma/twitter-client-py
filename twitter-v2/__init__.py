import logging

__host__ = ""
__base__ = f"https://{__host__}/"
__api__ = ""
__version__ = "0.1.0"
__author__ = "Datarise"
__name__ = "twitter-client-py"


def setup_logging(level: int = logging.INFO):
    l = logging.getLogger(__name__)
    if l.hasHandlers():
        l.handlers.clear()
    handler = logging.StreamHandler()
    handler.formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)6s - %(limit)s - %(message)s"
    )
    handler.formatter.datefmt = "%Y-%m-%d %H:%M:%S"
    logging.getLogger(__name__).addHandler(handler)
    logging.getLogger(__name__).setLevel(level)
    logging.getLogger(__name__).propagate = False


LOGGER = logging.getLogger(__name__)

from .async_twitter_client import AsyncTwitterClient
from .twitter_client import TwitterClient

__all__ = [
    "__base__",
    "__version__",
    "__author__",
    "__name__",
    "AsyncTwitterClient",
    "TwitterClient",
]
