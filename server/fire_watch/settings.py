import os
from pathlib import Path

import fire_watch
from fire_watch.config_utils import set_debug_flags


_path = Path(__file__).resolve()

BASE_DIR = _path.parent.parent

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = fire_watch.conf.developer

if not DEBUG:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(dsn=os.getenv("SENTRY_DSN"), integrations=[DjangoIntegration()])
    fire_watch.print("[bold cyan blue]Sentry Enabled :rocket:")

if DEBUG:
    set_debug_flags()

ALLOWED_HOSTS = fire_watch.conf.allowed_hosts

import patches

INSTALLED_APPS = [
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "alerts",
    "apis",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "authentication.middleware.AuthMiddleWare",
]

AUTH_PASSWORD_VALIDATORS = [
    "django.contrib.auth.password_validation.MinimumLengthValidator",
    "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    "django.contrib.auth.password_validation.CommonPasswordValidator",
    "django.contrib.auth.password_validation.NumericPasswordValidator",
]


ROOT_URLCONF = "fire_watch.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

ASGI_APPLICATION = "fire_watch.asgi.application"
WSGI_APPLICATION = "fire_watch.wsgi.application"

throttle_rate = (
    fire_watch.conf.throttle_rate["debug"]
    if DEBUG or os.getenv("CI")
    else fire_watch.conf.throttle_rate["production"]
)
fire_watch.flags.throttle_rate = throttle_rate
REST_FRAMEWORK = {
    "DEFAULT_THROTTLE_RATES": {
        "basic_throttle": throttle_rate,
    },
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
    "DEFAULT_PARSER_CLASSES": (("rest_framework.parsers.JSONParser",)),
}


fire_watch.print("[bold green]Current server configurations")

fire_watch.print(f"[blue]DEBUG: {DEBUG} USING-DB: {fire_watch.flags.db_name}")
fire_watch.print(f"[blue]Current throttle setting {fire_watch.flags.throttle_rate}")

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                (
                    fire_watch.conf.cache_conf["host"],
                    fire_watch.conf.cache_conf["port"],
                )
            ],
        },
    },
}

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


STATIC_URL = "/static/"
APPEND_SLASH = False

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
