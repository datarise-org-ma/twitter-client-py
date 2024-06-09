import logging

__host__ = "twitter-x.p.rapidapi.com"
__base__ = f"https://{__host__}/"
__api__ = "https://rapidapi.com/datarise-datarise-default/api/twitter-x"
__version__ = "0.3.0"
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
from .rate_limit import RateLimit

__all__ = [
    "__base__",
    "__version__",
    "__author__",
    "__name__",
    "AsyncTwitterClient",
    "TwitterClient",
    "RateLimit",
]
