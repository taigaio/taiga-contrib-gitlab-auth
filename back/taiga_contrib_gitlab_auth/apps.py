# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos Ventures SL

from django.apps import AppConfig


class TaigaContribGitlabAuthAppConfig(AppConfig):
    name = "taiga_contrib_gitlab_auth"
    verbose_name = "Taiga contrib gitlab auth App Config"

    def ready(self):
        from taiga.auth.services import register_auth_plugin
        from . import services
        register_auth_plugin("gitlab", services.gitlab_login_func)

