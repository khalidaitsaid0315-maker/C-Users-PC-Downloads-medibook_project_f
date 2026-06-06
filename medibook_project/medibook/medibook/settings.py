import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def env(name, default=None):
    return os.environ.get(name, default)


SECRET_KEY = env("SECRET_KEY", env("DJANGO_SECRET_KEY", "django-insecure-medibook-dev-key"))
DEBUG = env("DEBUG", "True").lower() == "true"
ALLOWED_HOSTS = [
    host.strip()
    for host in env("ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")
    if host.strip()
]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "accounts",
    "patients",
    "doctors",
    "appointments",
    "schedules",
    "dashboard",
    "ai_orientation",
    "notifications",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "medibook.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "medibook.wsgi.application"

DB_ENGINE = env("DB_ENGINE", "sqlite").lower()
if DB_ENGINE == "mysql":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.mysql",
            "NAME": env("DB_NAME", "medibook_db"),
            "USER": env("DB_USER", "root"),
            "PASSWORD": env("DB_PASSWORD", ""),
            "HOST": env("DB_HOST", "localhost"),
            "PORT": env("DB_PORT", "3306"),
        }
    }
elif DB_ENGINE == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DB_NAME", "medibook_db"),
            "USER": env("DB_USER", "postgres"),
            "PASSWORD": env("DB_PASSWORD", "postgres"),
            "HOST": env("DB_HOST", "db"),
            "PORT": env("DB_PORT", "5432"),
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "fr-fr"
TIME_ZONE = env("TIME_ZONE", "Africa/Casablanca")
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "home"
LOGOUT_REDIRECT_URL = "home"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ===== Security Settings for Production/Dockplay =====
SECURE_SSL_REDIRECT = env("SECURE_SSL_REDIRECT", "False").lower() == "true"
SESSION_COOKIE_SECURE = env("SESSION_COOKIE_SECURE", "False").lower() == "true"
CSRF_COOKIE_SECURE = env("CSRF_COOKIE_SECURE", "False").lower() == "true"
SECURE_BROWSER_XSS_FILTER = env("SECURE_BROWSER_XSS_FILTER", "True").lower() == "true"
SECURE_CONTENT_TYPE_NOSNIFF = env("SECURE_CONTENT_TYPE_NOSNIFF", "True").lower() == "true"
X_FRAME_OPTIONS = env("X_FRAME_OPTIONS", "DENY" if not DEBUG else "SAMEORIGIN")

# Trust proxy headers from Dockplay
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") if not DEBUG else None
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS", "").split(",") if env("CSRF_TRUSTED_ORIGINS", "") else []

if not DEBUG and env("SECURE_HSTS_SECONDS"):
    SECURE_HSTS_SECONDS = int(env("SECURE_HSTS_SECONDS", "0"))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = env("SECURE_HSTS_INCLUDE_SUBDOMAINS", "False").lower() == "true"
    SECURE_HSTS_PRELOAD = env("SECURE_HSTS_PRELOAD", "False").lower() == "true"

# Logging configuration
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
}
