from .base import *


DEBUG = False

ALLOWED_HOSTS = [
    env.str("IP"),
]

CSRF_TRUSTED_ORIGINS = [

]

# SECURE_SSL_REDIRECT = True

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"


SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"
