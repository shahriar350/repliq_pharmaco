import os
from datetime import timedelta
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# The root of the git repo - Could be ~/project or ~/repo
# REPO_DIR = os.path.realpath(os.path.join(BASE_DIR, ".."))
# The directory of the current user ie /home/django a.k.a. ~
# HOME_DIR = os.path.realpath(os.path.join(REPO_DIR, ".."))
# The directory where collectstatic command copies/symlinks the files to
# This can/should be located at ~/staticfiles, preferrably outside the git repo
# STATIC_DIR = os.path.realpath(os.path.join(REPO_DIR, "staticfiles"))
# The directory where different applications uploads media files to
# This can/should be located at ~/media, preferrably outside the git repo
# MEDIA_DIR = os.path.realpath(os.path.join(REPO_DIR, "media"))
MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = 'media/'
STATICFILES_DIRS = (BASE_DIR / 'static',)
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = "static/"

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)
INTERNAL_IPS = [
    "127.0.0.1",
]

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1(k)dd710l%!w&r=1@5kl%c_1r97bun#*mcnk-y2l^%s%!gh+4'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    'drf_spectacular',
    "django_filters",
    "versatileimagefield",
    "debug_toolbar",
    'django_cleanup.apps.CleanupConfig',
]
if DEBUG:
    THIRD_PARTY_APPS = [
                           "corsheaders",
                       ] + THIRD_PARTY_APPS
PROJECT_APPS = [
    'mediaroomio.apps.MediaroomioConfig',
    "core.apps.CoreConfig",
    "catalogio.apps.CatalogioConfig",
    'otpio.apps.OtpioConfig',
    'accountio.apps.AccountioConfig',
    'orderio.apps.OrderioConfig',
    'weio.apps.WeioConfig',
    'addressio.apps.AddressioConfig',
    'publicio.apps.PublicioConfig',
    'meio.apps.MeioConfig',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + PROJECT_APPS

# set base auth user model
AUTH_USER_MODEL = "core.User"

# middlewares
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    "whitenoise.middleware.WhiteNoiseMiddleware",
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    "debug_toolbar.middleware.DebugToolbarMiddleware",

]

ROOT_URLCONF = 'projectile.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'projectile.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dhaka'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {"anon": "30/minute", "user": "120/minute"},
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000", 'http://localhost:4000', "http://127.0.0.1:5173"
]

CSRF_TRUSTED_ORIGINS = ['http://localhost:3000', 'http://localhost:4000', "http://127.0.0.1:5173"]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=10),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}
SPECTACULAR_SETTINGS = {
    'SCHEMA_PATH_PREFIX': r'/api/v[0-9]',
}
