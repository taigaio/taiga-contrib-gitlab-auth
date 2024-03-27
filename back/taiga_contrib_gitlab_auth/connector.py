# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos INC

import requests
import json

from collections import namedtuple
from urllib.parse import urljoin

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from taiga.base.connectors.exceptions import ConnectorBaseException


class GitLabApiError(ConnectorBaseException):
    pass


######################################################
## Data
######################################################

CLIENT_ID = getattr(settings, "GITLAB_API_CLIENT_ID", None)
CLIENT_SECRET = getattr(settings, "GITLAB_API_CLIENT_SECRET", None)

URL = getattr(settings, "GITLAB_URL", None)

API_RESOURCES_URLS = {
    "login": {
        "authorize": "oauth/authorize",
        "access-token": "oauth/token"
    },
    "user": {
        "profile": "api/v4/user",
    }
}


HEADERS = {"Accept": "application/json",}

AuthInfo = namedtuple("AuthInfo", ["access_token"])
User = namedtuple("User", ["id", "username", "full_name", "bio", "email"])


######################################################
## utils
######################################################

def _build_url(*args, **kwargs) -> str:
    """
    Return a valid url.
    """
    resource_url = API_RESOURCES_URLS
    for key in args:
        resource_url = resource_url[key]

    if kwargs:
        resource_url = resource_url.format(**kwargs)

    return urljoin(URL, resource_url)


def _get(url:str, headers:dict) -> dict:
    """
    Make a GET call.
    """
    response = requests.get(url, headers=headers)

    data = response.json()
    if response.status_code != 200:
        raise GitLabApiError({"status_code": response.status_code,
                                  "error": data.get("error", "")})
    return data


def _post(url:str, params:dict, headers:dict) -> dict:
    """
    Make a POST call.
    """
    response = requests.post(url, params=params, headers=headers)

    data = response.json()
    if response.status_code != 200 or "error" in data:
        raise GitLabApiError({"status_code": response.status_code,
                                  "error": data.get("error", "")})
    return data


######################################################
## Simple calls
######################################################

def login(access_code:str, redirect_uri:str, client_id:str=CLIENT_ID, client_secret:str=CLIENT_SECRET,
          headers:dict=HEADERS):
    """
    Get access_token from an user authorized code, the client id and the client secret key.
    (See https://docs.gitlab.com/ce/api/oauth2.html).
    """
    if not CLIENT_ID or not CLIENT_SECRET:
        raise GitLabApiError({"error_message": _("Login with gitlab account is disabled. Contact "
                                                     "with the sysadmins. Maybe they're snoozing in a "
                                                     "secret hideout of the data center.")})

    url = _build_url("login", "access-token")
    params={"client_id": client_id,
            "client_secret": client_secret,
            "code": access_code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri}
    data = _post(url, params=params, headers=headers)
    return AuthInfo(access_token=data.get("access_token", None))


def get_user_profile(headers:dict=HEADERS):
    """
    Get authenticated user info.
    (See https://docs.gitlab.com/ce/api/users.html#user).
    """
    url = _build_url("user", "profile")
    data = _get(url, headers=headers)
    return User(id=data.get("id", None),
                username=data.get("username", None),
                full_name=(data.get("name", None) or ""),
                email=(data.get("email", None) or ""),
                bio=(data.get("bio", None) or ""))


######################################################
## Convined calls
######################################################

def me(access_code:str, redirectUri:str) -> tuple:
    """
    Connect to a gitlab account and get all personal info (profile and the primary email).
    """
    auth_info = login(access_code, redirectUri)

    headers = HEADERS.copy()
    headers["Authorization"] = "Bearer {}".format(auth_info.access_token)

    user = get_user_profile(headers=headers)
    return user.email, user

