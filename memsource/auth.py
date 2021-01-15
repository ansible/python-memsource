#!/usr/bin/env python

"""."""

import json
import requests

from memsource.constants import MEMSOURCE_ENDPOINT_V1_URL


def get_token(username, password):
    """Gets a 24 hour access token from Memsource"""

    url = "%s/auth/login" % MEMSOURCE_ENDPOINT_V1_URL

    data = {"userName": username, "password": password}

    headers = {"Content-type": "application/json"}

    response = requests.post(url, json=data, headers=headers)

    try:
        token = json.loads(response.content)["token"]
    except Exception as exc:
        raise exc

    return token


class Auth(object):
    """Auth related class for Memsource interaction"""

    def __init__(self, username, password):
        self.token = get_token(username, password)
