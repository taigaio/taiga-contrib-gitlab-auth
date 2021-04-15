# -*- coding: utf-8 -*-
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#
# Copyright (c) 2021-present Kaleidos Ventures SL

import uuid
import threading

from django.conf import settings

import factory


class Factory(factory.DjangoModelFactory):
    class Meta:
        strategy = factory.CREATE_STRATEGY
        model = None
        abstract = True

    _SEQUENCE = 1
    _SEQUENCE_LOCK = threading.Lock()

    @classmethod
    def _setup_next_sequence(cls):
        with cls._SEQUENCE_LOCK:
            cls._SEQUENCE += 1
        return cls._SEQUENCE


class ProjectTemplateFactory(Factory):
    class Meta:
        strategy = factory.CREATE_STRATEGY
        model = "projects.ProjectTemplate"
        django_get_or_create = ("slug",)

    name = "Template name"
    slug = settings.DEFAULT_PROJECT_TEMPLATE
    description = factory.Sequence(lambda n: "Description {}".format(n))

    us_statuses = []
    points = []
    task_statuses = []
    issue_statuses = []
    epic_statuses = []
    issue_types = []
    priorities = []
    severities = []
    roles = []
    us_custom_attributes = []
    task_custom_attributes = []
    issue_custom_attributes = []
    epic_custom_attributes = []
    default_owner_role = "tester"


class ProjectFactory(Factory):
    class Meta:
        model = "projects.Project"
        strategy = factory.CREATE_STRATEGY

    name = factory.Sequence(lambda n: "Project {}".format(n))
    slug = factory.Sequence(lambda n: "project-{}-slug".format(n))
    description = "Project description"
    owner = factory.SubFactory("tests.factories.UserFactory")
    creation_template = factory.SubFactory("tests.factories.ProjectTemplateFactory")


class RoleFactory(Factory):
    class Meta:
        model = "users.Role"
        strategy = factory.CREATE_STRATEGY

    name = factory.Sequence(lambda n: "Role {}".format(n))
    slug = factory.Sequence(lambda n: "test-role-{}".format(n))
    project = factory.SubFactory("tests.factories.ProjectFactory")


class UserFactory(Factory):
    class Meta:
        model = "users.User"
        strategy = factory.CREATE_STRATEGY

    username = factory.Sequence(lambda n: "user{}".format(n))
    email = factory.LazyAttribute(lambda obj: '%s@email.com' % obj.username)
    password = factory.PostGeneration(lambda obj, *args, **kwargs: obj.set_password(obj.username))


class MembershipFactory(Factory):
    class Meta:
        model = "projects.Membership"
        strategy = factory.CREATE_STRATEGY

    token = factory.LazyAttribute(lambda obj: str(uuid.uuid1()))
    project = factory.SubFactory("tests.factories.ProjectFactory")
    role = factory.SubFactory("tests.factories.RoleFactory")
    user = factory.SubFactory("tests.factories.UserFactory")
