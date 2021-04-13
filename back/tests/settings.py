from settings.testing import *

SKIP_SOUTH_TESTS = True
SOUTH_TESTS_MIGRATE = False
CELERY_ALWAYS_EAGER = True
CELERY_ENABLED = False

MEDIA_ROOT = "/tmp"

EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"
INSTALLED_APPS = INSTALLED_APPS + [
    "taiga_contrib_gitlab_auth",
]
INSTALLED_APPS = list(set(INSTALLED_APPS) - set(["taiga.hooks.github", "taiga.hooks.gitlab", "taiga.hooks.bitbucket"]))
