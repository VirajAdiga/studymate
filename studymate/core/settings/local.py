"""The project settings for local development."""

from .base import *


ALLOWED_HOSTS += ["127.0.0.1", "localhost"]

INSTALLED_APPS += ["debug_toolbar"]

MIDDLEWARE.append("debug_toolbar.middleware.DebugToolbarMiddleware")


SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
