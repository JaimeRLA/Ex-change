# config/settings.py
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

# 🔴 Añade esta línea para leer ~/Ex-change/erasmus/.env
load_dotenv(BASE_DIR / ".env")

SECRET_KEY = os.getenv("SECRET_KEY", "dev-key")

# Lee DEBUG/ALLOWED_HOSTS del .env (opcional pero recomendable)
DEBUG = os.getenv("DEBUG", "true").lower() == "true"
ALLOWED_HOSTS = (
    ["*"] if DEBUG else [h for h in os.getenv("ALLOWED_HOSTS", "").split(",") if h]
)

# === APPS ===
INSTALLED_APPS = [
    # Django core + admin
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Terceros
    "rest_framework",
    "django_filters",

    # Tu app
    "communities",
]

# === MIDDLEWARE (orden importa) ===
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",    # requerido por admin
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware", # requerido por admin
    "django.contrib.messages.middleware.MessageMiddleware",    # requerido por admin
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# === TEMPLATES (para admin y DRF browsable API) ===
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],  # <— añade esto
        "APP_DIRS": True,
        "OPTIONS": { "context_processors": [
            "django.template.context_processors.debug",
            "django.template.context_processors.request",
            "django.contrib.auth.context_processors.auth",
            "django.contrib.messages.context_processors.messages",
        ]},
    },
]


# === URL/WSGI ===
ROOT_URLCONF = "config.urls"                 # si tu paquete NO es 'config', cámbialo
WSGI_APPLICATION = "config.wsgi.application" # idem

# === Base de datos (dev) ===
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

LANGUAGE_CODE = "es"
TIME_ZONE = "Europe/Madrid"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Opcional: DRF
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}
