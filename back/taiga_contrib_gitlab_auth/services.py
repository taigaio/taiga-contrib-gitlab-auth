# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos INC

from django.db import transaction as tx
from django.db import IntegrityError
from django.conf import settings
from django.utils.translation import gettext as _

from django.apps import apps

from taiga.base.utils.slug import slugify_uniquely
from taiga.base import exceptions as exc
from taiga.auth.exceptions import AuthenticationFailed
from taiga.auth.services import send_register_email
from taiga.auth.services import make_auth_response_data, get_membership_by_token
from taiga.auth.signals import user_registered as user_registered_signal

from . import connector


GITLAB_SAAS_URL = "https://gitlab.com"


def _normalize_gitlab_url(url: str) -> str:
    return (url or "").rstrip("/")


def is_gitlab_instance_allowed(url: str = None) -> bool:
    """Return whether the configured GitLab instance may use this plugin."""
    configured_url = _normalize_gitlab_url(url if url is not None else connector.URL)
    if configured_url == GITLAB_SAAS_URL:
        return True

    allowed_instances = getattr(settings, "GITLAB_ALLOWED_SELF_MANAGED_INSTANCES", [])
    return configured_url in {
        _normalize_gitlab_url(instance) for instance in allowed_instances
    }


@tx.atomic
def gitlab_register(username:str, email:str, full_name:str, gitlab_id:int, bio:str,
                    confirmed_at, token:str=None):
    """
    Register a new user from gitlab.

    This can raise `exc.IntegrityError` exceptions in
    case of conflics found.

    :returns: User
    """
    if not is_gitlab_instance_allowed():
        raise AuthenticationFailed(
            _("Unable to authenticate with GitLab."),
            code="sso_authentication_failed",
        )

    auth_data_model = apps.get_model("users", "AuthData")
    user_model = apps.get_model("users", "User")

    try:
        # Gitlab user association exist?
        auth_data = auth_data_model.objects.get(key="gitlab", value=gitlab_id)
        user = auth_data.user
    except auth_data_model.DoesNotExist:
        if not email or not confirmed_at:
            raise AuthenticationFailed(
                _("Unable to authenticate with GitLab."),
                code="sso_authentication_failed",
            )

        try:
            # Is a user with the same email as the gitlab user?
            user = user_model.objects.get(email=email)

            auth_data_model.objects.create(user=user, key="gitlab", value=gitlab_id, extra={})
        except user_model.DoesNotExist:
            # Create a new user
            username_unique = slugify_uniquely(username, user_model, slugfield="username")
            user = user_model.objects.create(email=email,
                                             username=username_unique,
                                             full_name=full_name,
                                             bio=bio)
            auth_data_model.objects.create(user=user, key="gitlab", value=gitlab_id, extra={})

            send_register_email(user)
            user_registered_signal.send(sender=user.__class__, user=user)

    if token:
        membership = get_membership_by_token(token)

        try:
            membership.user = user
            membership.save(update_fields=["user"])
        except IntegrityError:
            raise exc.IntegrityError(_("This user is already a member of the project."))

    return user


def gitlab_login_func(request):
    if not is_gitlab_instance_allowed():
        raise AuthenticationFailed(
            _("Unable to authenticate with GitLab."),
            code="sso_authentication_failed",
        )

    code = request.DATA.get('code', None)
    token = request.DATA.get('token', None)
    redirectUri = request.DATA.get('redirectUri', None)

    email, user_info = connector.me(code, redirectUri)

    user = gitlab_register(username=user_info.username,
                           email=email,
                           full_name=user_info.full_name,
                           gitlab_id=user_info.id,
                           bio=user_info.bio,
                           confirmed_at=user_info.confirmed_at,
                           token=token)
    data = make_auth_response_data(user)
    return data
