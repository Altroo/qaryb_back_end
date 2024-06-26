import os
from datetime import timedelta
from decouple import config

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Basic config
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)
ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    config('API_IP'),
    config('API_DOMAIN'),
]

# SSL secure proxy config
SECURE_PROXY_SSL_HEADER = (config('SECURE_PROXY_SSL_HEADER_1'),
                           config('SECURE_PROXY_SSL_HEADER_2'))

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'daphne',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.postgres',
    # 'drf_yasg',
    'corsheaders',
    'channels',
    'chat.apps.ChatConfig',
    'rest_framework',
    'colorfield',
    'rest_framework_simplejwt',
    # 'rest_framework_simplejwt.token_blacklist',
    # 'rest_framework.authtoken',
    'django_filters',
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'dj_rest_auth.registration',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'ckeditor',
    'ckeditor_uploader',
    'account.apps.AccountConfig',
    'shop.apps.ShopConfig',
    'offers.apps.OffersConfig',
    'cart.apps.CartConfig',
    'order.apps.OrderConfig',
    'ratings.apps.RatingsConfig',
    'places.apps.PlacesConfig',
    'subscription.apps.SubscriptionConfig',
    'notifications.apps.NotificationsConfig',
    'seo_pages.apps.SeoPagesConfig',
    'blog.apps.BlogConfig',
    'version.apps.VersionConfig'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'allauth.account.middleware.AccountMiddleware'
]

# CORS_ALLOW_ALL_ORIGINS = True
# CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
    'https://qaryb.com',
    'https://www.qaryb.com',
    'https://dev.qaryb.com',
)

# Root url, asgi & wsgi config
ROOT_URLCONF = config('ROOT_URLCONF')
ASGI_APPLICATION = config('ASGI_APPLICATION')
WSGI_APPLICATION = config('WSGI_APPLICATION')

# Templates config
TEMPLATES = [
    {
        'BACKEND': config('TEMPLATES_BACKEND'),
        # 'DIRS': [(os.path.join(BASE_DIR, config('SWAGGER_ADMIN_LINK_PATH')))],
        'DIRS': [(os.path.join(BASE_DIR, 'templates'))],
        'APP_DIRS': config('TEMPLATES_APP_DIRS', cast=bool),
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

# Database
DATABASES = {
    'default': {
        'ENGINE': config('QARYB_DB_BACKEND'),
        'NAME': config('QARYB_DB_NAME'),
        'USER': config('QARYB_DB_USER'),
        'PASSWORD': config('QARYB_DB_PASSWORD'),
        'HOST': config('QARYB_DB_HOST'),
        'PORT': '',
    },
}

# Default password validators config
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': config('AUTH_PASSWORD_VALIDATORS'),
    },
]

# Internationalization config
LANGUAGE_CODE = config('LANGUAGE_CODE')
TIME_ZONE = config('TIME_ZONE')
USE_I18N = config('USE_I18N', cast=bool)
USE_L10N = config('USE_L10N', cast=bool)
USE_TZ = config('USE_TZ', cast=bool)

# Default user model config
AUTH_USER_MODEL = config('AUTH_USER_MODEL')
DEFAULT_AUTO_FIELD = config('DEFAULT_AUTO_FIELD')

# Static & media files config
STATIC_URL = config('STATIC_URL')
# STATIC_ROOT = "static"
STATIC_PATH = os.path.join(BASE_DIR, config('STATIC_PATH'))
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, config('STATIC_PATH')),
)
MEDIA_ROOT = os.path.join(BASE_DIR, config('MEDIA_PATH'))
MEDIA_URL = '/media/'

# allauth config
AUTHENTICATION_BACKENDS = [
    config('AUTHENTICATION_BACKENDS_1'),
    config('AUTHENTICATION_BACKENDS_2'),
]
SITE_ID = config('SITE_ID', cast=int)

# Rest framework config
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        config('REST_FRAMEWORK_DEFAULT_AUTHENTICATION_CLASSES_1'),
        config('REST_FRAMEWORK_DEFAULT_AUTHENTICATION_CLASSES_2'),
    ),
    'DEFAULT_PERMISSION_CLASSES': (config('REST_FRAMEWORK_DEFAULT_PERMISSION_CLASSES'),),
    'DEFAULT_VERSIONING_CLASS': config('REST_FRAMEWORK_DEFAULT_VERSIONING_CLASS'),
    'ALLOWED_VERSIONS': ('1.0.0',),
    'DEFAULT_VERSION': config('REST_FRAMEWORK_DEFAULT_VERSION'),
    'DEFAULT_PAGINATION_CLASS': config('REST_FRAMEWORK_DEFAULT_PAGINATION_CLASS'),
    'PAGE_SIZE': config('REST_FRAMEWORK_PAGE_SIZE', cast=int),
    'DEFAULT_RENDERER_CLASSES': (config('REST_FRAMEWORK_DEFAULT_RENDERER_CLASSES'),),
    'DEFAULT_SCHEMA_CLASS': config('REST_FRAMEWORK_DEFAULT_SCHEMA_CLASS'),
    'DEFAULT_FILTER_BACKENDS': (config('REST_FRAMEWORK_DEFAULT_FILTER_BACKENDS'),),
    'EXCEPTION_HANDLER': 'shop.base.utils.api_exception_handler',
    'NON_FIELD_ERRORS_KEY': 'error',
    'TOKEN_MODEL': None,
}

# dj_rest_auth config
# USE_JWT = config('REST_USE_JWT', cast=bool)
# JWT_AUTH_RETURN_EXPIRATION = config('JWT_AUTH_RETURN_EXPIRATION', cast=bool)
# JWT_AUTH_COOKIE = config('JWT_AUTH_COOKIE')
# JWT_AUTH_REFRESH_COOKIE = config('JWT_AUTH_REFRESH_COOKIE')
# TOKEN_MODEL = None
# OLD_PASSWORD_FIELD_ENABLED = True

REST_AUTH = {
    'USE_JWT': config('REST_USE_JWT', cast=bool),
    'JWT_AUTH_RETURN_EXPIRATION': config('JWT_AUTH_RETURN_EXPIRATION', cast=bool),
    'JWT_AUTH_COOKIE': config('JWT_AUTH_COOKIE'),
    'JWT_AUTH_REFRESH_COOKIE': config('JWT_AUTH_REFRESH_COOKIE'),
    'TOKEN_MODEL': None,
    'OLD_PASSWORD_FIELD_ENABLED': True,
    'JWT_AUTH_HTTPONLY': False,
    # 'LOGIN_SERIALIZER': 'account.base.serializers.TokenObtainPairSerializer'
}

# Logging
LOGGING = {
    'version': config('LOGGING_VERSION', cast=int),
    'disable_existing_loggers': config('LOGGING_DISABLE_EXISTING_LOGGERS', cast=bool),
    'formatters': {
        'verbose': {
            'format': config('LOGGING_VERBOSE_FORMAT'),
            'style': config('LOGGING_VERBOSE_STYLE'),
        },
        'simple': {
            'format': config('LOGGING_SIMPLE_FORMAT'),
            'style': config('LOGGING_VERBOSE_STYLE'),
        },
    },
    'handlers': {
        'file': {
            'level': config('LOGGING_FILE_LEVEL'),
            'class': config('LOGGING_FILE_CLASS'),
            'filename': os.path.join(BASE_DIR, config('LOGGGING_PATH')),
        },
    },
    'loggers': {
        'django': {
            'handlers': [config('LOGGING_LOGGERS_HANDLERS')],
            'level': config('LOGGING_FILE_LEVEL'),
            'propagate': config('LOGGING_LOGGERS_PROPAGATE', cast=bool),
        },
    },
}

API_URL = config('API_URL')

# Nominatim settings
NOMINATIM_PROTOCOL = config('NOMINATIM_PROTOCOL')
MAP_DOMAIN = config('MAP_DOMAIN')

# SIMPLE_JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=config('ACCESS_TOKEN_LIFETIME', cast=int)),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=config('REFRESH_TOKEN_LIFETIME', cast=int)),
    'BLACKLIST_AFTER_ROTATION': config('BLACKLIST_AFTER_ROTATION', cast=bool),
    'ROTATE_REFRESH_TOKENS': config('ROTATE_REFRESH_TOKENS', cast=bool),
}

# Redis config
REDIS_HOST = config('REDIS_HOST')
REDIS_PORT = config('REDIS_PORT')

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': config('REDIS_BACKEND'),
        'CONFIG': {
            "hosts": [(REDIS_HOST, REDIS_PORT)],
        },
    },
}
# Celery
CELERY_BROKER_URL = config('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND')
# Celery localhost debug enabled :
# Doesn't call eta shift
# CELERY_TASK_ALWAYS_EAGER = True

# Email settings
EMAIL_BACKEND = config('EMAIL_BACKEND')
EMAIL_HOST = config('EMAIL_HOST')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', cast=bool)
EMAIL_PORT = config('EMAIL_PORT')
EMAIL_HOST_USER = config('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = config('DEFAULT_FROM_EMAIL')

# Chat settings
CONVERSATIONS_TO_LOAD = config('CONVERSATIONS_TO_LOAD', cast=int)
MESSAGES_TO_LOAD = config('MESSAGES_TO_LOAD', cast=int)

# SOCIALACCOUNT settings
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': config('FACEBOOK_METHOD'),
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': config('FACEBOOK_AUTH_TYPE')},
        'LOCALE_FUNC': lambda request: config('FACEBOOK_LOCALE_FUNC'),
        'INIT_PARAMS': {'cookie': config('FACEBOOK_COOKIE', cast=bool)},
        'FIELDS': [
            'id',
            'email',
            'first_name',
            'last_name',
            'middle_name',
            'name',
            'name_format',
            'picture',
            'short_name',
        ],
        'EXCHANGE_TOKEN': config('FACEBOOK_EXCHANGE_TOKEN', cast=bool),
        'VERIFIED_EMAIL': config('FACEBOOK_VERIFIED_EMAIL', cast=bool),
        'VERSION': config('FACEBOOK_VERSION'),
        'APP': {
            'client_id': config('FACEBOOK_CLIENT_ID'),
            'secret': config('FACEBOOK_SECRET')
        }
    },
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        # in order to receive a refresh token on first login and on reauthentication requests
        # (which is needed to refresh authentication tokens in the background,
        # without involving the user’s browser)
        'AUTH_PARAMS': {
            'access_type': config('GOOGLE_ACCESS_TYPE'),
        },
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID'),
            'secret': config('GOOGLE_SECRET'),
        },
    }
}
SOCIALACCOUNT_ADAPTER = config('SOCIALACCOUNT_ADAPTER')
SOCIALACCOUNT_STORE_TOKENS = config('SOCIALACCOUNT_STORE_TOKENS', cast=bool)
SOCIALACCOUNT_QUERY_EMAIL = config('SOCIALACCOUNT_QUERY_EMAIL', cast=bool)
SOCIALACCOUNT_EMAIL_VERIFICATION = config('SOCIALACCOUNT_EMAIL_VERIFICATION', cast=bool)
SOCIALACCOUNT_AUTO_SIGNUP = config('SOCIALACCOUNT_AUTO_SIGNUP', cast=bool)

# ACCOUNT settings (dj_rest_auth & allauth)
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = config('ACCOUNT_USERNAME_REQUIRED', cast=bool)
ACCOUNT_AUTHENTICATION_METHOD = config('ACCOUNT_AUTHENTICATION_METHOD')
ACCOUNT_EMAIL_REQUIRED = config('ACCOUNT_EMAIL_REQUIRED', cast=bool)
ACCOUNT_EMAIL_VERIFICATION = config('ACCOUNT_EMAIL_VERIFICATION')
ACCOUNT_MAX_EMAIL_ADDRESSES = config('ACCOUNT_MAX_EMAIL_ADDRESSES', cast=int)
ACCOUNT_DEFAULT_HTTP_PROTOCOL = config('ACCOUNT_DEFAULT_HTTP_PROTOCOL')

DATA_UPLOAD_MAX_MEMORY_SIZE = None

# ckeditor
CKEDITOR_BASEPATH = "/static/ckeditor/ckeditor/"
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_BROWSE_SHOW_DIRS = True
CKEDITOR_CONFIGS = {
    'blog_editor': {
        'skin': 'moono-dark',
        'defaultLanguage': 'en',
        'language': 'en',
        'toolbar': 'Custom',
        'toolbar_Custom': [
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', '-', 'RemoveFormat']},
            {'name': 'styles', 'items': ['Styles', 'Format', 'Font', 'FontSize']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Blockquote', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'links', 'items': ['Link', 'Unlink']},
            {'name': 'insert', 'items': ['Image', 'Smiley']},
        ],
        'width': '100%',
    },
}
CKEDITOR_IMAGE_BACKEND = 'ckeditor_uploader.backends.PillowBackend'
CKEDITOR_THUMBNAIL_SIZE = (75, 75)
CKEDITOR_FORCE_JPEG_COMPRESSION = True
CKEDITOR_ALLOW_NONIMAGE_FILES = False

GOOGLE_SPREADSHEET_ID = config('GOOGLE_SPREADSHEET_ID')

# SWAGGER_SETTINGS settings
# SWAGGER_SETTINGS = {
#     'SECURITY_DEFINITIONS': {
#         'basic': {
#             'type': config('SECURITY_DEFINITIONS_BASIC_TYPE')
#         },
#         'Bearer': {
#             'type': config('SECURITY_DEFINITIONS_BEARER_TYPE'),
#             'name': config('SECURITY_DEFINITIONS_BEARER_NAME'),
#             'in': config('SECURITY_DEFINITIONS_BEARER_IN')
#         }
#     },
#     'LOGIN_URL': config('SWAGGER_LOGIN_URL'),
#     'LOGOUT_URL': config('SWAGGER_LOGOUT_URL'),
# }
