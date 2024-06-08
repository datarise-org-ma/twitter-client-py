from dataclasses import dataclass

from . import LOGGER


@dataclass
class RateLimit:
    """
    Rate limit dataclass to store rate limit information.

    Attributes:
        limit: int - The limit of requests that can be made.
        remaining: int - The remaining requests that can be made.
        reset: int - The time in seconds until the rate limit resets.
    """

    limit: int
    remaining: int
    reset: int

    @classmethod
    def from_headers(cls, headers):
        c = cls(
            limit=int(headers.get("x-ratelimit-rapid-free-plans-hard-limit-limit")),
            remaining=int(
                headers.get("x-ratelimit-rapid-free-plans-hard-limit-remaining")
            ),
            reset=int(headers.get("x-ratelimit-rapid-free-plans-hard-limit-reset")),
        )
        LOGGER.debug(f"Rate limit: {c}", extra={"limit": c.remaining})
        return c
