# Twitter Python Client for [Twitter/X Rapid API](https://rapidapi.com/datarise-datarise-default/api/twitter-x)


## Installation

```bash
pip install twitter-client-py
```

## Usage

```python
from os import getenv

from twitter_client_py import TwitterClient

api_key = getenv('API_KEY')

client = TwitterClient(api_key)

# Get user by username
user = client.get_user_by_username('elonmusk')
print(user)

# Get user by id
user = client.get_user_by_id('44196397')
print(user)
```
