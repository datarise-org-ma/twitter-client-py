from typing import Optional, Dict
import asyncio
import logging
import time

import aiohttp

from . import __base__, __host__, LOGGER, setup_logging
from .rate_limit import RateLimit

sem = asyncio.Semaphore(100)


class AsyncTwitterClient:
    def __init__(
        self, api_key: str, timeout: int = 20, verbose: bool = False, loop=None
    ):
        self.base_url: str = __base__
        self.api_key: str = api_key
        self.loop = loop if loop is not None else asyncio.get_event_loop()
        self.headers: Dict = self.__headers()
        self.session: Optional[aiohttp.ClientSession] = aiohttp.ClientSession(
            loop=self.loop
        )
        self.rate_limit: Optional[RateLimit] = RateLimit(0, 0, 0)
        self.verbose: bool = verbose
        self.timeout: int = timeout
        if self.verbose:
            LOGGER = setup_logging(logging.DEBUG)
        else:
            LOGGER = setup_logging(logging.INFO)

    def __headers(self):
        return {
            "x-rapidapi-key": f"{self.api_key}",
            "x-rapidapi-host": __host__,
            "Content-Type": __host__,
        }

    async def __aenter__(self):
        self.session = aiohttp.ClientSession(loop=self.loop)
        self.session.headers.update(self.headers)
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()

    async def search(
        self, query, section="top", limit=20, cursor=None
    ) -> aiohttp.ClientResponse:
        url = f"{self.base_url}search/"
        LOGGER.info(
            f"[Search] Query: {query} - Section: {section} - Limit: {limit}",
            extra={"limit": self.rate_limit.remaining},
        )
        params = {
            "query": query,
            "section": section,
            "limit": limit,
        }
        if cursor:
            params["cursor"] = cursor
        start = time.perf_counter()
        response = await self.session.get(url, params=params, timeout=self.timeout)
        if response.status == 200:
            self.rate_limit = RateLimit.from_headers(response.headers)
        LOGGER.debug(
            f"[Search] Response: {response.status}, elapsed time: {time.perf_counter() - start:.2f}s",
            extra={"limit": self.rate_limit.remaining},
        )
        return response

    async def tweet_details(self, tweet_id: str, cursor=None) -> aiohttp.ClientResponse:
        url = f"{self.base_url}tweet/"
        LOGGER.info(
            f"[Tweet Details] Tweet ID: {tweet_id}",
            extra={"limit": self.rate_limit.remaining},
        )
        params = {"tweet_id": tweet_id}
        if cursor:
            params["cursor"] = cursor
        start = time.perf_counter()
        response = await self.session.get(url, params=params, timeout=self.timeout)
        if response.status == 200:
            self.rate_limit = RateLimit.from_headers(response.headers)
        LOGGER.debug(
            f"[Tweet Details] Response: {response.status}, elapsed time: {time.perf_counter() - start:.2f}s",
            extra={"limit": self.rate_limit.remaining},
        )
        return response

    async def tweet_retweeters(
        self, tweet_id: str, limit=20, cursor=None
    ) -> aiohttp.ClientResponse:
        url = f"{self.base_url}tweet/retweeters/"
        LOGGER.info(
            f"[Tweet Retweeters] Tweet ID: {tweet_id} - Limit: {limit}",
            extra={"limit": self.rate_limit.remaining},
        )
        params = {"tweet_id": tweet_id, "limit": limit}
        if cursor:
            params["cursor"] = cursor
        start = time.perf_counter()
        response = await self.session.get(url, params=params, timeout=self.timeout)
        if response.status == 200:
            self.rate_limit = RateLimit.from_headers(response.headers)
        LOGGER.debug(
            f"[Tweet Retweeters] Response: {response.status}, elapsed time: {time.perf_counter() - start:.2f}s",
            extra={"limit": self.rate_limit.remaining},
        )
        return response

    async def tweet_favoriters(
        self, tweet_id: str, limit=20, cursor=None
    ) -> aiohttp.ClientResponse:
        url = f"{self.base_url}tweet/favoriters/"
        LOGGER.info(
            f"[Tweet Favoriters] Tweet ID: {tweet_id} - Limit: {limit}",
            extra={"limit": self.rate_limit.remaining},
        )
        params = {"tweet_id": tweet_id, "limit": limit}
        if cursor:
            params["cursor"] = cursor
        start = time.perf_counter()
        response = await self.session.get(url, params=params, timeout=self.timeout)
        if response.status == 200:
            self.rate_limit = RateLimit.from_headers(response.headers)
        LOGGER.debug(
            f"[Tweet Favoriters] Response: {response.status}, elapsed time: {time.perf_counter() - start:.2f}s",
            extra={"limit": self.rate_limit.remaining},
        )
        return response

    async def user_details(
        self, username: Optional[str] = None, user_id: Optional[str] = None
    ) -> aiohttp.ClientResponse:
        url = f"{self.base_url}user/details"
        if username:
            LOGGER.info(
                f"[User Details] Username: {username}",
                extra={"limit": self.rate_limit.remaining},
            )
            params = {"username": username}
        elif user_id:
            LOGGER.info(
                f"[User Details] User ID: {user_id}",
                extra={"limit": self.rate_limit.remaining},
            )
            params = {"user_id": user_id}
        start = time.perf_counter()
        response = await self.session.get(url, params=params, timeout=self.timeout)
        if response.status == 200:
            self.rate_limit = RateLimit.from_headers(response.headers)
        LOGGER.debug(
            f"[User Details] Response: {response.status}, elapsed time: {time.perf_counter() - start:.2f}s",
            extra={"limit": self.rate_limit.remaining},
        )
        return response

    async def user_tweets(
        self,
        username: Optional[str] = None,
        user_id: Optional[str] = None,
        limit=20,
        cursor=None,
    ) -> aiohttp.ClientResponse:
        url = f"{self.base_url}user/tweets"
        if username:
            LOGGER.info(
                f"[User Tweets] Username: {username} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
            params = {"username": username, "limit": limit}
        elif user_id:
            LOGGER.info(
                f"[User Tweets] User ID: {user_id} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
            params = {"user_id": user_id, "limit": limit}
        if cursor:
            params["cursor"] = cursor
        start = time.perf_counter()
        response = await self.session.get(url, params=params, timeout=self.timeout)
        if response.status == 200:
            self.rate_limit = RateLimit.from_headers(response.headers)
        LOGGER.debug(
            f"[User Tweets] Response: {response.status}, elapsed time: {time.perf_counter() - start:.2f}s",
            extra={"limit": self.rate_limit.remaining},
        )
        return response

    async def user_tweets_and_replies(
        self,
        username: Optional[str] = None,
        user_id: Optional[str] = None,
        limit=20,
        cursor=None,
    ) -> aiohttp.ClientResponse:
        url = f"{self.base_url}user/tweetsandreplies"
        if username:
            LOGGER.info(
                f"[User Tweets and Replies] Username: {username} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
            params = {"username": username, "limit": limit}
        elif user_id:
            LOGGER.info(
                f"[User Tweets and Replies] User ID: {user_id} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
            params = {"user_id": user_id, "limit": limit}
        if cursor:
            params["cursor"] = cursor
        start = time.perf_counter()
        response = await self.session.get(url, params=params, timeout=self.timeout)
        if response.status == 200:
            self.rate_limit = RateLimit.from_headers(response.headers)
        LOGGER.debug(
            f"[User Tweets and Replies] Response: {response.status}, elapsed time: {time.perf_counter() - start:.2f}s",
            extra={"limit": self.rate_limit.remaining},
        )
        return response

    async def user_followers(
        self,
        username: Optional[str] = None,
        user_id: Optional[str] = None,
        limit=20,
        cursor=None,
    ) -> aiohttp.ClientResponse:
        url = f"{self.base_url}user/followers"
        if username:
            LOGGER.info(
                f"[User Followers] Username: {username} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
            params = {"username": username, "limit": limit}
        elif user_id:
            LOGGER.info(
                f"[User Followers] User ID: {user_id} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
            params = {"user_id": user_id, "limit": limit}
        if cursor:
            params["cursor"] = cursor
        start = time.perf_counter()
        response = await self.session.get(url, params=params, timeout=self.timeout)
        if response.status == 200:
            self.rate_limit = RateLimit.from_headers(response.headers)
        LOGGER.debug(
            f"[User Followers] Response: {response.status}, elapsed time: {time.perf_counter() - start:.2f}s",
            extra={"limit": self.rate_limit.remaining},
        )
        return response

    async def user_following(
        self,
        username: Optional[str] = None,
        user_id: Optional[str] = None,
        limit=20,
        cursor=None,
    ) -> aiohttp.ClientResponse:
        url = f"{self.base_url}user/following"
        if username:
            LOGGER.info(
                f"[User Following] Username: {username} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
            params = {"username": username, "limit": limit}
        elif user_id:
            LOGGER.info(
                f"[User Following] User ID: {user_id} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
            params = {"user_id": user_id, "limit": limit}
        if cursor:
            params["cursor"] = cursor
        start = time.perf_counter()
        response = await self.session.get(url, params=params, timeout=self.timeout)
        if response.status == 200:
            self.rate_limit = RateLimit.from_headers(response.headers)
        LOGGER.debug(
            f"[User Following] Response: {response.status}, elapsed time: {time.perf_counter() - start:.2f}s",
            extra={"limit": self.rate_limit.remaining},
        )
        return response

    async def user_likes(
        self,
        username: Optional[str] = None,
        user_id: Optional[str] = None,
        limit=20,
        cursor=None,
    ) -> aiohttp.ClientResponse:
        url = f"{self.base_url}user/likes"
        if username:
            LOGGER.info(
                f"[User Likes] Username: {username} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
            params = {"username": username, "limit": limit}
        elif user_id:
            LOGGER.info(
                f"[User Likes] User ID: {user_id} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
            params = {"user_id": user_id, "limit": limit}
        if cursor:
            params["cursor"] = cursor
        start = time.perf_counter()
        response = await self.session.get(url, params=params, timeout=self.timeout)
        if response.status == 200:
            self.rate_limit = RateLimit.from_headers(response.headers)
        LOGGER.debug(
            f"[User Likes] Response: {response.status}, elapsed time: {time.perf_counter() - start:.2f}s",
            extra={"limit": self.rate_limit.remaining},
        )
        return response

    async def user_media(
        self,
        username: Optional[str] = None,
        user_id: Optional[str] = None,
        limit=20,
        cursor=None,
    ) -> aiohttp.ClientResponse:
        url = f"{self.base_url}user/media"
        if username:
            LOGGER.info(
                f"[User Media] Username: {username} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
            params = {"username": username, "limit": limit}
        elif user_id:
            LOGGER.info(
                f"[User Media] User ID: {user_id} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
            params = {"user_id": user_id, "limit": limit}
        if cursor:
            params["cursor"] = cursor
        start = time.perf_counter()
        response = await self.session.get(url, params=params, timeout=self.timeout)
        if response.status == 200:
            self.rate_limit = RateLimit.from_headers(response.headers)
        LOGGER.debug(
            f"[User Media] Response: {response.status}, elapsed time: {time.perf_counter() - start:.2f}s",
            extra={"limit": self.rate_limit.remaining},
        )
        return response

    async def list_details(self, list_id: str) -> aiohttp.ClientResponse:
        url = f"{self.base_url}lists/details"
        LOGGER.info(
            f"[List Details] List ID: {list_id}",
            extra={"limit": self.rate_limit.remaining},
        )
        params = {"list_id": list_id}
        start = time.perf_counter()
        response = await self.session.get(url, params=params, timeout=self.timeout)
        if response.status == 200:
            self.rate_limit = RateLimit.from_headers(response.headers)
        LOGGER.debug(
            f"[List Details] Response: {response.status}, elapsed time: {time.perf_counter() - start:.2f}s",
            extra={"limit": self.rate_limit.remaining},
        )
        return response

    async def list_tweets(
        self, list_id: str, limit=20, cursor=None
    ) -> aiohttp.ClientResponse:
        url = f"{self.base_url}lists/tweets"
        LOGGER.info(
            f"[List Tweets] List ID: {list_id} - Limit: {limit}",
            extra={"limit": self.rate_limit.remaining},
        )
        params = {"list_id": list_id, "limit": limit}
        if cursor:
            params["cursor"] = cursor
        start = time.perf_counter()
        response = await self.session.get(url, params=params, timeout=self.timeout)
        if response.status == 200:
            self.rate_limit = RateLimit.from_headers(response.headers)
        LOGGER.debug(
            f"[List Tweets] Response: {response.status}, elapsed time: {time.perf_counter() - start:.2f}s",
            extra={"limit": self.rate_limit.remaining},
        )
        return response

    async def trends_locations(self) -> aiohttp.ClientResponse:
        url = f"{self.base_url}trends/available"
        LOGGER.info("[Trends Locations]", extra={"limit": self.rate_limit.remaining})
        start = time.perf_counter()
        response = await self.session.get(url, timeout=self.timeout)
        if response.status == 200:
            self.rate_limit = RateLimit.from_headers(response.headers)
        LOGGER.debug(
            f"[Trends Locations] Response: {response.status}, elapsed time: {time.perf_counter() - start:.2f}s",
            extra={"limit": self.rate_limit.remaining},
        )
        return response

    async def trends(self, woeid: str) -> aiohttp.ClientResponse:
        url = f"{self.base_url}trends/"
        LOGGER.info(
            f"[Trends] WOEID: {woeid}", extra={"limit": self.rate_limit.remaining}
        )
        params = {"woeid": woeid}
        start = time.perf_counter()
        response = await self.session.get(url, params=params, timeout=self.timeout)
        if response.status == 200:
            self.rate_limit = RateLimit.from_headers(response.headers)
        LOGGER.debug(
            f"[Trends] Response: {response.status}, elapsed time: {time.perf_counter() - start:.2f}s",
            extra={"limit": self.rate_limit.remaining},
        )
        return response
