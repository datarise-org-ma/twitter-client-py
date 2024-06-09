# Unofficial Twitter Python Client for [Twitter/X Rapid API](https://rapidapi.com/datarise-datarise-default/api/twitter-x)

<!-- Add badges for CI/CD, Code Coverage, PyPI, etc. -->
[![PyPI](https://img.shields.io/pypi/v/twitter-client-py)](https://pypi.org/project/twitter-client-py/)
![Build Status](https://github.com/datarise-org-ma/twitter-client-py/actions/workflows/ci.yaml/badge.svg)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/twitter-client-py)](https://pypi.org/project/twitter-client-py/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/twitter-client-py)](https://pypi.org/project/twitter-client-py/)


## Overview

This is a Python client for interacting with the Twitter V2 API via the [RapidAPI platform](https://rapidapi.com/datarise-datarise-default/api/twitter-x). The library provides synchronous, asynchronous, and multi-threaded capabilities for retrieving Twitter user details and tweets.


## Installation

```bash
pip install -U twitter-client-py
```

## Usage

### Simple Example

The following example demonstrates how to use the library to get user details and tweets.

```python
from os import getenv
import json

from twitter_client_py import TwitterClient

api_key = getenv('API_KEY')

client = TwitterClient(api_key=api_key, timeout=20, verbose=True)

# Get user details by username
user_details  = client.user_details(username='elonmusk')
if user_details.status_code == 200:
    print(json.dumps(user_details.json(), indent=4))

# Get user details by id
user_details  = client.user_details(user_id='44196397')
if user_details.status_code == 200:
    print(json.dumps(user_details.json(), indent=4))

# Get user tweets by username
user_tweets = client.user_tweets(username='elonmusk')
if user_tweets.status_code == 200:
    print(json.dumps(user_tweets.json(), indent=4))
    
# Get user tweets by id
user_tweets = client.user_tweets(user_id='44196397')
if user_tweets.status_code == 200:
    print(json.dumps(user_tweets.json(), indent=4))
```

### Advanced Example

*TwitterClient* class is thread-safe, so you can use it in a multi-threaded environment.

```python
from os import getenv
import json
from concurrent.futures import ThreadPoolExecutor

from twitter_client_py import TwitterClient

api_key = getenv('API_KEY')

client = TwitterClient(api_key=api_key, timeout=20, verbose=True)

users = ['elonmusk', 'BillGates', 'JeffBezos', 'tim_cook', 'satyanadella']

def get_user_details(username):
    user_details  = client.user_details(username=username)
    if user_details.status_code == 200:
        return user_details.json()

with ThreadPoolExecutor(max_workers=5) as executor:
    results = executor.map(get_user_details, users)

for result in results:
    print(json.dumps(result, indent=4))
```

### Asynchronous Example

The library also supports asynchronous requests using `aiohttp` with `asyncio`

```python
from os import getenv
import asyncio
import json

from twitter_client_py import AsyncTwitterClient

api_key = getenv('API_KEY') # X-RapidAPI-Key

client = AsyncTwitterClient(api_key=api_key, timeout=20, verbose=True)

users = ['elonmusk', 'BillGates', 'JeffBezos', 'tim_cook', 'satyanadella']

async def get_user_details(username):
    user_details  = await client.user_details(username=username)
    if user_details.status == 200:
        return user_details.json()

async def main():
    tasks = [get_user_details(username) for username in users]
    results = await asyncio.gather(*tasks)
    for result in results:
        print(json.dumps(await result, indent=4))

await main()
```

### Check Rate Limit

You can check the rate limit of the API using the `rate_limit` method. TwitterClient and AsyncTwitterClient have a `rate_limit` attribute that returns the rate limit details. It's updated after each request.

```python
rate_limit = client.rate_limit
print(f"Limit: {rate_limit.limit}")
print(f"Remaining requests: {rate_limit.remaining}")
print(f"Reset time: {rate_limit.reset}")
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or feedback, feel free to reach out to us at contact [at] datarise [dot] ma.
