from typing import Optional, Dict
import logging


import requests

from . import __base__, __api__, __host__, LOGGER, setup_logging
from .rate_limit import RateLimit


class TwitterClient:
    f"""
    A Python Twitter/X API client for {__api__}

    Attributes:
        api_key (str): The API key for the API.
        timeout (int): The timeout for the requests. Default is 20.
        verbose (bool): Whether to enable verbose logging. Default is False.
        rate_limit (RateLimit): The rate limit object updated after each request.

    Methods:
        search(query, section="top", limit=20, cursor=None): Search for tweets.
        tweet_details(tweet_id, cursor=None): Get details of a tweet.
        tweet_retweeters(tweet_id, limit=20, cursor=None): Get users who retweeted a tweet.
        tweet_favoriters(tweet_id, limit=20, cursor=None): Get users who favorited a tweet.
        user_details(username=None, user_id=None): Get details of a user.
        user_tweets(username=None, user_id=None, limit=20, cursor=None): Get tweets of a user.
        user_tweets_and_replies(username=None, user_id=None, limit=20, cursor=None): Get tweets and replies of a user.
        user_followers(username=None, user_id=None, limit=20, cursor=None): Get followers of a user.
        user_following(username=None, user_id=None, limit=20, cursor=None): Get users followed by a user.
        user_likes(username=None, user_id=None, limit=20, cursor=None): Get tweets liked by a user.
        user_media(username=None, user_id=None, limit=20, cursor=None): Get media of a user.
        list_details(list_id): Get details of a list.
        list_tweets(list_id, limit=20, cursor=None): Get tweets of a list.
        trends_locations(): Get locations for trends.
        trends(woeid): Get trends for a location.
        community_details(community_id): Get details of a community.
        community_tweets(community_id, limit=20, cursor=None): Get tweets of a community.
        community_members(community_id, limit=20, cursor=None): Get members of a community.
    """

    def __init__(self, api_key: str, timeout: int = 20, verbose: bool = False):
        self.api_key: str = api_key
        self.rate_limit: Optional[RateLimit] = RateLimit(0, 0, 0)
        self.verbose: bool = verbose
        self.timeout: int = timeout
        self.__base_url: str = __base__
        self.__headers: Dict = self.__get_headers()
        self.__session: Optional[requests.Session] = requests.Session()
        if self.verbose:
            LOGGER = setup_logging(logging.DEBUG)
        else:
            LOGGER = setup_logging(logging.INFO)

    def __get_headers(self):
        return {
            "x-rapidapi-key": f"{self.api_key}",
            "x-rapidapi-host": __host__,
            "Content-Type": __host__,
        }

    def __enter__(self):
        self.__session = requests.Session()
        self.__session.headers.update(self.__headers)
        return self

    def __exit__(self, exc_type, exc, tb):
        self.__session.close()

    def search(self, query, section="top", limit=20, cursor=None) -> requests.Response:
        """
        Search for tweets using the Twitter/X API.

        Args:
            query (str): The query to search for.
            section (str): The section to search in. Possible values are "top", "latest", "people", "photos", "videos". Default is "top".
            limit (int): The limit of tweets to return. Default is 20.
            cursor (str): The cursor for pagination. Default is None.

        Returns:
            requests.Response: The response from the API.
        """
        url = f"{self.__base_url}search/"
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
        with self.__session.get(
            url, params=params, headers=self.__headers, timeout=self.timeout
        ) as response:
            if response.status_code == 200:
                self.rate_limit = RateLimit.from_headers(response.headers)
            LOGGER.debug(
                f"[Search] Response: {response.status_code}, elapsed time: {response.elapsed.total_seconds()}",
                extra={"limit": self.rate_limit.remaining},
            )
            return response

    def tweet_details(self, tweet_id: str, cursor=None) -> requests.Response:
        """
        Get details of a tweet using the Twitter/X API.

        Args:
            tweet_id (str): The ID of the tweet.
            cursor (str): The cursor for pagination. Default is None.

        Returns:
            requests.Response: The response from the API.
        """

        url = f"{self.__base_url}tweet/"
        params = {
            "tweet_id": tweet_id,
        }
        if cursor:
            params["cursor"] = cursor
        LOGGER.info(
            f"[Tweet Details] Tweet ID: {tweet_id}",
            extra={"limit": self.rate_limit.remaining},
        )
        with self.__session.get(
            url, params=params, headers=self.__headers, timeout=self.timeout
        ) as response:
            if response.status_code == 200:
                self.rate_limit = RateLimit.from_headers(response.headers)
            LOGGER.debug(
                f"[Tweet Details] Response: {response.status_code}, elapsed time: {response.elapsed.total_seconds()}",
                extra={"limit": self.rate_limit.remaining},
            )
            return response

    def tweet_retweeters(
        self, tweet_id: str, limit=20, cursor=None
    ) -> requests.Response:
        """
        Get users who retweeted a tweet using the Twitter/X API.

        Args:
            tweet_id (str): The ID of the tweet.
            limit (int): The limit of users to return. Default is 20.
            cursor (str): The cursor for pagination. Default is None.

        Returns:
            requests.Response: The response from the API.
        """

        url = f"{self.__base_url}tweet/retweeters/"
        params = {
            "tweet_id": tweet_id,
            "limit": limit,
        }
        if cursor:
            params["cursor"] = cursor
        LOGGER.info(
            f"[Tweet Retweeters] Tweet ID: {tweet_id} - Limit: {limit}",
            extra={"limit": self.rate_limit.remaining},
        )
        with self.__session.get(
            url, params=params, headers=self.__headers, timeout=self.timeout
        ) as response:
            if response.status_code == 200:
                self.rate_limit = RateLimit.from_headers(response.headers)
            LOGGER.debug(
                f"[Tweet Retweeters] Response: {response.status_code}, elapsed time: {response.elapsed.total_seconds()}",
                extra={"limit": self.rate_limit.remaining},
            )
            return response

    def tweet_favoriters(
        self, tweet_id: str, limit=20, cursor=None
    ) -> requests.Response:
        """
        Get users who favorited a tweet using the Twitter/X API.

        Args:
            tweet_id (str): The ID of the tweet.
            limit (int): The limit of users to return. Default is 20.
            cursor (str): The cursor for pagination. Default is None.

        Returns:
            requests.Response: The response from the API.
        """
        url = f"{self.__base_url}tweet/favoriters/"
        params = {
            "tweet_id": tweet_id,
            "limit": limit,
        }
        if cursor:
            params["cursor"] = cursor
        LOGGER.info(
            f"[Favoriters] Tweet ID: {tweet_id} - Limit: {limit}",
            extra={"limit": self.rate_limit.remaining},
        )
        with self.__session.get(
            url, params=params, headers=self.__headers, timeout=self.timeout
        ) as response:
            if response.status_code == 200:
                self.rate_limit = RateLimit.from_headers(response.headers)
            LOGGER.debug(
                f"[Favoriters] Response: {response.status_code}, elapsed time: {response.elapsed.total_seconds()}",
                extra={"limit": self.rate_limit.remaining},
            )
            return response

    def user_details(
        self, username: Optional[str] = None, user_id: Optional[str] = None
    ) -> requests.Response:
        """
        Get details of a user using the Twitter/X API.

        Args:
            username (str): The username of the user. Default is None.
            user_id (str): The ID of the user. Default is None.

        Returns:
            requests.Response: The response from the API.
        """
        if not username and not user_id:
            raise ValueError("Either username or user_id must be provided.")
        url = f"{self.__base_url}user/details"
        params = {}
        if username:
            params["username"] = username
            LOGGER.info(
                f"[User Details] Username: {username}",
                extra={"limit": self.rate_limit.remaining},
            )
        if user_id:
            params["user_id"] = user_id
            LOGGER.info(
                f"[User Details] User ID: {user_id}",
                extra={"limit": self.rate_limit.remaining},
            )
        with self.__session.get(
            url, params=params, headers=self.__headers, timeout=self.timeout
        ) as response:
            if response.status_code == 200:
                self.rate_limit = RateLimit.from_headers(response.headers)
            LOGGER.debug(
                f"[User Details] Response: {response.status_code}, elapsed time: {response.elapsed.total_seconds()}",
                extra={"limit": self.rate_limit.remaining},
            )
            return response

    def user_tweets(
        self,
        username: Optional[str] = None,
        user_id: Optional[str] = None,
        limit=20,
        cursor=None,
    ) -> requests.Response:
        """
        Get tweets of a user using the Twitter/X API.

        Args:
            username (str): The username of the user. Default is None.
            user_id (str): The ID of the user. Default is None.
            limit (int): The limit of tweets to return. Default is 20.
            cursor (str): The cursor for pagination. Default is None.

        Returns:
            requests.Response: The response from the API.
        """

        if not username and not user_id:
            raise ValueError("Either username or user_id must be provided.")
        url = f"{self.__base_url}user/tweets"
        params = {
            "limit": limit,
        }
        if username:
            params["username"] = username
            LOGGER.info(
                f"[User Tweets] Username: {username} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
        if user_id:
            params["user_id"] = user_id
            LOGGER.info(
                f"[User Tweets] User ID: {user_id} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
        if cursor:
            params["cursor"] = cursor
        with self.__session.get(
            url, params=params, headers=self.__headers, timeout=self.timeout
        ) as response:
            if response.status_code == 200:
                self.rate_limit = RateLimit.from_headers(response.headers)
            LOGGER.debug(
                f"[User Tweets] Response: {response.status_code}, elapsed time: {response.elapsed.total_seconds()}",
                extra={"limit": self.rate_limit.remaining},
            )
            return response

    def user_tweets_and_replies(
        self,
        username: Optional[str] = None,
        user_id: Optional[str] = None,
        limit=20,
        cursor=None,
    ) -> requests.Response:
        """
        Get tweets and replies of a user using the Twitter/X API.

        Args:
            username (str): The username of the user. Default is None.
            user_id (str): The ID of the user. Default is None.
            limit (int): The limit of tweets to return. Default is 20.
            cursor (str): The cursor for pagination. Default is None.

        Returns:
            requests.Response: The response from the API.
        """
        if not username and not user_id:
            raise ValueError("Either username or user_id must be provided.")
        url = f"{self.__base_url}user/tweetsandreplies"
        params = {
            "limit": limit,
        }
        if username:
            params["username"] = username
            LOGGER.info(
                f"[User Tweets and Replies] Username: {username} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
        if user_id:
            params["user_id"] = user_id
            LOGGER.info(
                f"[User Tweets and Replies] User ID: {user_id} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
        if cursor:
            params["cursor"] = cursor
        with self.__session.get(
            url, params=params, headers=self.__headers, timeout=self.timeout
        ) as response:
            if response.status_code == 200:
                self.rate_limit = RateLimit.from_headers(response.headers)
            LOGGER.debug(
                f"[User Tweets and Replies] Response: {response.status_code}, elapsed time: {response.elapsed.total_seconds()}",
                extra={"limit": self.rate_limit.remaining},
            )
            return response

    def user_followers(
        self,
        username: Optional[str] = None,
        user_id: Optional[str] = None,
        limit=20,
        cursor=None,
    ) -> requests.Response:
        """
        Get followers of a user using the Twitter/X API.

        Args:
            username (str): The username of the user. Default is None.
            user_id (str): The ID of the user. Default is None.
            limit (int): The limit of followers to return. Default is 20.
            cursor (str): The cursor for pagination. Default is None.

        Returns:
            requests.Response: The response from the API.
        """
        if not username and not user_id:
            raise ValueError("Either username or user_id must be provided.")
        url = f"{self.__base_url}user/followers"
        params = {
            "limit": limit,
        }
        if username:
            params["username"] = username
            LOGGER.info(
                f"[User Followers] Username: {username} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
        if user_id:
            params["user_id"] = user_id
            LOGGER.info(
                f"[User Followers] User ID: {user_id} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
        if cursor:
            params["cursor"] = cursor
        with self.__session.get(
            url, params=params, headers=self.__headers, timeout=self.timeout
        ) as response:
            if response.status_code == 200:
                self.rate_limit = RateLimit.from_headers(response.headers)
            LOGGER.debug(
                f"[User Followers] Response: {response.status_code}, elapsed time: {response.elapsed.total_seconds()}",
                extra={"limit": self.rate_limit.remaining},
            )
            return response

    def user_following(
        self,
        username: Optional[str] = None,
        user_id: Optional[str] = None,
        limit=20,
        cursor=None,
    ) -> requests.Response:
        """
        Get users followed by a user using the Twitter/X API.

        Args:
            username (str): The username of the user. Default is None.
            user_id (str): The ID of the user. Default is None.
            limit (int): The limit of users to return. Default is 20.
            cursor (str): The cursor for pagination. Default is None.

        Returns:
            requests.Response: The response from the API.
        """

        if not username and not user_id:
            raise ValueError("Either username or user_id must be provided.")

        url = f"{self.__base_url}user/following"
        params = {
            "limit": limit,
        }
        if username:
            params["username"] = username
            LOGGER.info(
                f"[User Following] Username: {username} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
        if user_id:
            params["user_id"] = user_id
            LOGGER.info(
                f"[User Following] User ID: {user_id} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
        if cursor:
            params["cursor"] = cursor
        with self.__session.get(
            url, params=params, headers=self.__headers, timeout=self.timeout
        ) as response:
            if response.status_code == 200:
                self.rate_limit = RateLimit.from_headers(response.headers)
            LOGGER.debug(
                f"[User Following] Response: {response.status_code}, elapsed time: {response.elapsed.total_seconds()}",
                extra={"limit": self.rate_limit.remaining},
            )
            return response

    def user_likes(
        self,
        username: Optional[str] = None,
        user_id: Optional[str] = None,
        limit=20,
        cursor=None,
    ) -> requests.Response:
        """
        Get tweets liked by a user using the Twitter/X API.

        Args:
            username (str): The username of the user. Default is None.
            user_id (str): The ID of the user. Default is None.
            limit (int): The limit of tweets to return. Default is 20.
            cursor (str): The cursor for pagination. Default is None.

        Returns:
            requests.Response: The response from the API.
        """

        if not username and not user_id:
            raise ValueError("Either username or user_id must be provided.")

        url = f"{self.__base_url}user/likes"
        params = {
            "limit": limit,
        }
        if username:
            params["username"] = username
            LOGGER.info(
                f"[User Likes] Username: {username} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
        if user_id:
            params["user_id"] = user_id
            LOGGER.info(
                f"[User Likes] User ID: {user_id} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
        if cursor:
            params["cursor"] = cursor
        with self.__session.get(
            url, params=params, headers=self.__headers, timeout=self.timeout
        ) as response:
            if response.status_code == 200:
                self.rate_limit = RateLimit.from_headers(response.headers)
            LOGGER.debug(
                f"[User Likes] Response: {response.status_code}, elapsed time: {response.elapsed.total_seconds()}",
                extra={"limit": self.rate_limit.remaining},
            )
            return response

    def user_media(
        self,
        username: Optional[str] = None,
        user_id: Optional[str] = None,
        limit=20,
        cursor=None,
    ) -> requests.Response:
        """
        Get media of a user using the Twitter/X API.

        Args:
            username (str): The username of the user. Default is None.
            user_id (str): The ID of the user. Default is None.
            limit (int): The limit of media to return. Default is 20.
            cursor (str): The cursor for pagination. Default is None.

        Returns:
            requests.Response: The response from the API.
        """
        if not username and not user_id:
            raise ValueError("Either username or user_id must be provided.")
        url = f"{self.__base_url}user/media"
        params = {
            "limit": limit,
        }
        if username:
            params["username"] = username
            LOGGER.info(
                f"[User Media] Username: {username} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
        if user_id:
            params["user_id"] = user_id
            LOGGER.info(
                f"[User Media] User ID: {user_id} - Limit: {limit}",
                extra={"limit": self.rate_limit.remaining},
            )
        if cursor:
            params["cursor"] = cursor
        with self.__session.get(
            url, params=params, headers=self.__headers, timeout=self.timeout
        ) as response:
            if response.status_code == 200:
                self.rate_limit = RateLimit.from_headers(response.headers)
            LOGGER.debug(
                f"[User Media] Response: {response.status_code}, elapsed time: {response.elapsed.total_seconds()}",
                extra={"limit": self.rate_limit.remaining},
            )
            return response

    def list_details(self, list_id: str) -> requests.Response:
        """
        Get details of a list using the Twitter/X API.

        Args:
            list_id (str): The ID of the list.

        Returns:
            requests.Response: The response from the API.
        """
        url = f"{self.__base_url}lists/details"
        params = {
            "list_id": list_id,
        }
        LOGGER.info(
            f"[List Details] List ID: {list_id}",
            extra={"limit": self.rate_limit.remaining},
        )
        with self.__session.get(
            url, params=params, headers=self.__headers, timeout=self.timeout
        ) as response:
            if response.status_code == 200:
                self.rate_limit = RateLimit.from_headers(response.headers)
            LOGGER.debug(
                f"[List Details] Response: {response.status_code}, elapsed time: {response.elapsed.total_seconds()}",
                extra={"limit": self.rate_limit.remaining},
            )
            return response

    def list_tweets(self, list_id: str, limit=20, cursor=None) -> requests.Response:
        """
        Get tweets of a list using the Twitter/X API.

        Args:
            list_id (str): The ID of the list.
            limit (int): The limit of tweets to return. Default is 20.
            cursor (str): The cursor for pagination. Default is None.

        Returns:
            requests.Response: The response from the API.
        """

        url = f"{self.__base_url}lists/tweets"
        params = {
            "list_id": list_id,
            "limit": limit,
        }
        if cursor:
            params["cursor"] = cursor
        LOGGER.info(
            f"[List Tweets] List ID: {list_id} - Limit: {limit}",
            extra={"limit": self.rate_limit.remaining},
        )
        with self.__session.get(
            url, params=params, headers=self.__headers, timeout=self.timeout
        ) as response:
            if response.status_code == 200:
                self.rate_limit = RateLimit.from_headers(response.headers)
            LOGGER.debug(
                f"[List Tweets] Response: {response.status_code}, elapsed time: {response.elapsed.total_seconds()}",
                extra={"limit": self.rate_limit.remaining},
            )
            return response

    def trends_locations(self) -> requests.Response:
        """
        Get locations for trends using the Twitter/X API.

        Returns:
            requests.Response: The response from the API.
        """
        url = f"{self.__base_url}trends/available"
        LOGGER.info("[Trends Location]", extra={"limit": self.rate_limit.remaining})
        with self.__session.get(url, timeout=self.timeout) as response:
            if response.status_code == 200:
                self.rate_limit = RateLimit.from_headers(response.headers)
            LOGGER.debug(
                f"[Trends Location] Response: {response.status_code}, elapsed time: {response.elapsed.total_seconds()}",
                extra={"limit": self.rate_limit.remaining},
            )
            return response

    def trends(self, woeid: str) -> requests.Response:
        """
        Get trends for a location using the Twitter/X API.

        Args:
            woeid (str): The WOEID of the location, which can be obtained from trends_locations().

        Returns:
            requests.Response: The response from the API.
        """
        url = f"{self.__base_url}trends/"
        params = {
            "woeid": woeid,
        }
        LOGGER.info(
            f"[Trends] WOEID: {woeid}", extra={"limit": self.rate_limit.remaining}
        )
        with self.__session.get(
            url, params=params, headers=self.__headers, timeout=self.timeout
        ) as response:
            if response.status_code == 200:
                self.rate_limit = RateLimit.from_headers(response.headers)
            LOGGER.debug(
                f"[Trends] Response: {response.status_code}, elapsed time: {response.elapsed.total_seconds()}",
                extra={"limit": self.rate_limit.remaining},
            )
            return response

    def community_details(self, community_id: str) -> requests.Response:
        """
        Get details of a community using the Twitter/X API.

        Args:
            community_id (str): The ID of the community.

        Returns:
            requests.Response: The response from the API.
        """
        url = f"{self.__base_url}community/details"
        params = {
            "community_id": community_id,
        }
        LOGGER.info(
            f"[Community Details] Community ID: {community_id}",
            extra={"limit": self.rate_limit.remaining},
        )
        with self.__session.get(
            url, params=params, headers=self.__headers, timeout=self.timeout
        ) as response:
            if response.status_code == 200:
                self.rate_limit = RateLimit.from_headers(response.headers)
            LOGGER.debug(
                f"[Community Details] Response: {response.status_code}, elapsed time: {response.elapsed.total_seconds()}",
                extra={"limit": self.rate_limit.remaining},
            )
            return response

    def community_tweets(
        self, community_id: str, limit=20, cursor=None
    ) -> requests.Response:
        """
        Get tweets of a community using the Twitter/X API.

        Args:
            community_id (str): The ID of the community.
            limit (int): The limit of tweets to return. Default is 20.
            cursor (str): The cursor for pagination. Default is None.

        Returns:
            requests.Response: The response from the API.
        """
        url = f"{self.__base_url}community/tweets"
        params = {
            "community_id": community_id,
            "limit": limit,
        }
        if cursor:
            params["cursor"] = cursor
        LOGGER.info(
            f"[Community Tweets] Community ID: {community_id} - Limit: {limit}",
            extra={"limit": self.rate_limit.remaining},
        )
        with self.__session.get(
            url, params=params, headers=self.__headers, timeout=self.timeout
        ) as response:
            if response.status_code == 200:
                self.rate_limit = RateLimit.from_headers(response.headers)
            LOGGER.debug(
                f"[Community Tweets] Response: {response.status_code}, elapsed time: {response.elapsed.total_seconds()}",
                extra={"limit": self.rate_limit.remaining},
            )
            return response

    def community_members(
        self, community_id: str, limit=20, cursor=None
    ) -> requests.Response:
        """
        Get members of a community using the Twitter/X API.

        Args:
            community_id (str): The ID of the community.
            limit (int): The limit of members to return. Default is 20.
            cursor (str): The cursor for pagination. Default is None.

        Returns:
            requests.Response: The response from the API.
        """

        url = f"{self.__base_url}community/members"
        params = {
            "community_id": community_id,
            "limit": limit,
        }
        if cursor:
            params["cursor"] = cursor
        LOGGER.info(
            f"[Community Members] Community ID: {community_id} - Limit: {limit}",
            extra={"limit": self.rate_limit.remaining},
        )
        with self.__session.get(
            url, params=params, headers=self.__headers, timeout=self.timeout
        ) as response:
            if response.status_code == 200:
                self.rate_limit = RateLimit.from_headers(response.headers)
            LOGGER.debug(
                f"[Community Members] Response: {response.status_code}, elapsed time: {response.elapsed.total_seconds()}",
                extra={"limit": self.rate_limit.remaining},
            )
            return response
