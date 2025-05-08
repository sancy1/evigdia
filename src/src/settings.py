
from pathlib import Path
from decouple import config
from datetime import timedelta
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
from django.core.exceptions import ImproperlyConfigured

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'django-insecure-wvjpxae+v+=9w9feh)^rzuy(aiwf4g4-=0a3naz6*!us7ltq+#'
# DEBUG = True
# ALLOWED_HOSTS = []

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS').split(',')

PRICE_API_KEY = config('PRICE_API_KEY')
APP_MANAGEMENT_API_KEY = config('APP_MANAGEMENT_API_KEY')
EVIGDIA_WEBSITE_URL = config('EVIGDIA_WEBSITE_URL')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'axes',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'drf_yasg',
    'drf_spectacular',
    
    # Third-party apps
    'rest_framework_simplejwt',
    'rest_framework',
    'rest_framework.authtoken',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.microsoft',
    'dj_rest_auth',
    'dj_rest_auth.registration',

    # Custom apps
    'user_account',
    'desktop-apis.price_api',
    'desktop-apis.app_management',
    'web_apis.blog',
    'web_apis.contact',
    'web_apis.evigdia_services',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'axes.middleware.AxesMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    'allauth.account.middleware.AccountMiddleware',
    
    # 'desktop-apis.price_api.middleware.NeonKeepAliveMiddleware',
    # 'desktop-apis.user_account.middleware.ping_render.RenderKeepAlive',

]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'src.wsgi.application'



# SQLite Database ------------------------------------------------------------------
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# POSTGRESQL DATABASE ------------------------------------------------------------------

# DATABASE_URL = os.getenv('DATABASE_URL')  # From .env
# parsed = urlparse(DATABASE_URL)

# if DATABASE_URL:
#     parsed = urlparse(DATABASE_URL)
#     #print(f"Parsed URL: {parsed}") #for debugging
#     DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql',
#             'NAME': parsed.path.lstrip('/'),  # Remove the leading slash
#             'USER': parsed.username,
#             'PASSWORD': parsed.password,
#             'HOST': parsed.hostname,
#             'PORT': parsed.port or 5432,  # Use 5432 as default if port is None
#             'OPTIONS': {
#                 'sslmode': 'require',  # Ensure SSL is required
#             }
#         }
#     }
# else:
#     # Handle the case where DATABASE_URL is not set.  This is crucial!
#     # DATABASES = {
#     #     'default': {
#     #         'ENGINE': 'django.db.backends.sqlite3',
#     #         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     #     }
#     # }
#     print("DATABASE_URL is not set. Using SQLite instead.")
    
    

# --------------------------------------------------------------------------------


# DATABASES = {
#     'default': {
#         'ENGINE': config('ENGINE'),
#         'NAME': config('PGDATABASE'),
#         'USER': config('PGUSER'),
#         'PASSWORD': config('PGPASSWORD'),
#         'HOST': config('PGHOST'),
#         'PORT': config('PGPORT', cast=int, default=5432),
#         'OPTIONS': {
#             'sslmode': config('OPTIONS_SSLMODE', default='require'),
#         },
#     }
# }



# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_simplejwt.authentication.JWTAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#     ),
# }


# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
#     'ROTATE_REFRESH_TOKENS': True,
#     'BLACKLIST_AFTER_ROTATION': True,
# }





# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


STATIC_URL = 'static/'

# Media files (uploads)
MEDIA_URL = '/media/'  # URL for media files (uploads, images, etc.)

# Directory for media files (uploads)
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Directory for uploaded media files

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'user_account.CustomUser'

# Social account settings
SOCIALACCOUNT_STORE_TOKENS = True
SOCIALACCOUNT_EMAIL_AUTHENTICATION = True
SOCIALACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'  # Change if needed
SOCIALACCOUNT_AUTO_SIGNUP = True

# Django AllAuth settings
AUTHENTICATION_BACKENDS = [
    'axes.backends.AxesBackend',
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# Axes configuration
AXES = {
    # Basic Protection
    'FAILURE_LIMIT': config('AXES_FAILURE_LIMIT', default=10, cast=int),
    'COOLOFF_TIME': timedelta(hours=config('AXES_COOLOFF_TIME', default=1, cast=int)),
    # 'FAILURE_LIMIT': 10,  # Lock after 10 attempts
    # 'COOLOFF_TIME': timedelta(hours=1),  # Precise 1-hour lockout
    
    # API Response Handling
    'LOCKOUT_CALLABLE': 'src.utils.custom_lockout',
    'HTTP_RESPONSE_CODE': 403,
    
    # Behavior Tuning
    'RESET_ON_SUCCESS': True,
    'NEVER_LOCKOUT_GET': True,
    'LOCKOUT_PARAMETERS': ['ip_address', 'username'],  # Dual tracking
    
    # Security
    'AXES_HEADERS': ['User-Agent', 'X-Forwarded-For'],  # Enhanced fingerprinting
    'PROXY_COUNT': 1,  # If behind proxy
}

SITE_ID = 1

ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_UNIQUE_EMAIL = True

ACCOUNT_EMAIL_VERIFICATION = 'none'  # Change this to 'mandatory' if email verification is required
# SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_EMAIL_REQUIRED = False
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_QUERY_EMAIL = True

# Security headers and protections
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'same-origin'

# HTTPS Settings (auto-configure based on environment)
is_development = DEBUG or any(host in ['127.0.0.1', 'localhost'] for host in ALLOWED_HOSTS)

if not is_development:
    # Production security settings
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
else:
    # Development settings
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False
    SECURE_SSL_REDIRECT = False

# Redirect URL after successful social auth
API_BASE_URL = config('API_BASE_URL', default='evigdia.onrender.com')
LOGIN_REDIRECT_URL = config('LOGIN_REDIRECT_URL', default='/api/user/profile/')
LOGOUT_REDIRECT_URL = config('LOGOUT_REDIRECT_URL', default='/')

# Enhanced CORS settings
def validate_origin(url):
    parsed = urlparse(url)
    if not all([parsed.scheme, parsed.netloc]):
        raise ImproperlyConfigured(f"Invalid origin URL: {url}")
    return url

# Get and validate all origins
CORS_ALLOWED_ORIGINS = [
    validate_origin(API_BASE_URL),
    *[validate_origin(origin) for origin in config(
        'DEV_CORS_ORIGINS',
        default='http://localhost:3000,http://127.0.0.1:3000,http://localhost:8000',
        cast=lambda v: [s.strip() for s in v.split(',')]
    )]
]
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:3000",
#     "http://127.0.0.1:3000",
#     'http://127.0.0.1:8000',
#     'http://localhost:8000',
#     # Add your production domains here
# ]

# For development, you might want to allow all (remove in production)
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
    CORS_ALLOWED_ORIGINS = []  # Clear the specific origins in dev
else:
    CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOW_CREDENTIALS = True
CORS_EXPOSE_HEADERS = [
    'Content-Type', 
    'X-CSRFToken',
    'Authorization',
    'X-Requested-With',
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]


# Enhanced cookie settings
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG  # True in production
SESSION_COOKIE_SAMESITE = 'Lax'  # Strict if you don't need cross-site
SESSION_COOKIE_AGE = 86400  # 1 day in seconds
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS.copy()


# Change to these exact settings:
CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', cast=bool, default=not DEBUG)
CSRF_COOKIE_HTTPONLY = False  # Must be False for React
CSRF_COOKIE_SAMESITE = 'Lax'  # Allows OAuth redirects
CSRF_HEADER_NAME = 'X-CSRFToken'  # Standard React header
CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS.copy()
CSRF_FAILURE_VIEW = 'user_account.views.csrf_failure'  # Custom JSON response


# ======================== REST Framework Settings ========================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_SCHEMA_CLASS': ['drf_spectacular.openapi.AutoSchema',],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}


# Only enable browsable API in development
if DEBUG:{
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    # ...
}


# JWT settings
# ======================== JWT Settings ========================
SIMPLE_JWT = {
    # Token Lifetimes
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=config('JWT_ACCESS_TOKEN_LIFETIME_MINUTES', default=60, cast=int)),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=config('JWT_REFRESH_TOKEN_LIFETIME_DAYS', default=7, cast=int)),
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=config('JWT_SLIDING_TOKEN_LIFETIME_MINUTES', default=60, cast=int)),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=config('JWT_SLIDING_TOKEN_REFRESH_LIFETIME_DAYS', default=1, cast=int)),
    
    # Behavior Flags
    'ROTATE_REFRESH_TOKENS': config('JWT_ROTATE_REFRESH_TOKENS', default=True, cast=bool),
    'BLACKLIST_AFTER_ROTATION': config('JWT_BLACKLIST_AFTER_ROTATION', default=True, cast=bool),
    'UPDATE_LAST_LOGIN': config('JWT_UPDATE_LAST_LOGIN', default=True, cast=bool),
    
    # Algorithm and Signing
    'ALGORITHM': config('JWT_ALGORITHM', default='HS256'),
    'SIGNING_KEY': SECRET_KEY,  # From Django's default SECRET_KEY
    
    # These typically don't need env configuration
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    
    # Header configuration
    'AUTH_HEADER_TYPES': ('Bearer', 'JWT'),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    
    # Claims
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    'JTI_CLAIM': 'jti',
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
}

# SIMPLE_JWT = {
#     'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
#     'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
#     'ROTATE_REFRESH_TOKENS': True,
#     'BLACKLIST_AFTER_ROTATION': True,
#     'UPDATE_LAST_LOGIN': True,
#     'ALGORITHM': 'HS256',
#     'SIGNING_KEY': SECRET_KEY,
#     'VERIFYING_KEY': None,
#     'AUDIENCE': None,
#     'ISSUER': None,
#     'JWK_URL': None,
#     'LEEWAY': 0,
#     'AUTH_HEADER_TYPES': ('Bearer', 'JWT'),
#     'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
#     'USER_ID_FIELD': 'id',
#     'USER_ID_CLAIM': 'user_id',
#     'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
#     'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
#     'TOKEN_TYPE_CLAIM': 'token_type',
#     'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
#     'JTI_CLAIM': 'jti',
#     'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
#     'SLIDING_TOKEN_LIFETIME': timedelta(minutes=60),
#     'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
# }


REST_AUTH = {
    'USE_JWT': True,  # Enable JWT for dj-rest-auth
    'JWT_AUTH_COOKIE': 'jwt-auth',  # Optional: Use cookies for JWT
    'JWT_AUTH_REFRESH_COOKIE': 'jwt-refresh-auth',
}


# Social account providers
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': config('GOOGLE_CLIENT_ID'),
            'secret': config('GOOGLE_CLIENT_SECRET'),
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
            'https://www.googleapis.com/auth/userinfo.profile',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
            'prompt': 'select_account'
        }
    },
    'microsoft': {
        'APP': {
            'client_id': config('MICROSOFT_CLIENT_ID'),
            'secret': config('MICROSOFT_CLIENT_SECRET'),
            'key': ''
        },
        'SCOPE': [
            'openid',  # Add openid scope for authentication
            'profile',  # Include profile scope for basic user info
            'email',  # Include email scope to retrieve the user's email
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
            'prompt': 'select_account',
            'response_type': 'code'
        },
        'METHOD': 'oauth2',
        'VERIFIED_EMAIL': True,
        'EXCHANGE_TOKEN': True,
        'OAUTH_PKCE_ENABLED': True,
    }
    
}


SOCIALACCOUNT_ADAPTER = 'user_account.adapters.CustomSocialAccountAdapter'
ACCOUNT_ADAPTER = 'user_account.adapters.CustomAccountAdapter'

SOCIALACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGIN_ON_GET = True
ACCOUNT_LOGOUT_ON_GET = True 

# Add these settings
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'  # Change to 'https' in production
SOCIALACCOUNT_AUTO_SIGNUP = True



# DEBUGGING -------------------------------------------------------------------------
# ======================== Logging Configuration ========================
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'include_html': True,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file', 'mail_admins'],
            'level': 'INFO',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'apps': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'DEBUG' if DEBUG else 'INFO',
    },
}

# Ensure logs directory exists
os.makedirs(BASE_DIR / 'logs', exist_ok=True)


# Ping Tp Wake Neo
# Neon Keep-Alive Settings
NEON_KEEPALIVE_ENABLED = True  # Set to False to disable
NEON_PING_INTERVAL = 200  # 4 minutes (less than Neon's 5-minute timeout)
# NEON_PING_INTERVAL = 10  # 10 seconds for testing


# ======================== Cache Configuration ========================
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake',
    }
}

# In production, switch to Redis if available
if not DEBUG and config('REDIS_URL', default=''):
    CACHES['default'] = {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': config('REDIS_URL'),
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'SOCKET_CONNECT_TIMEOUT': 5,
            'SOCKET_TIMEOUT': 5,
            'IGNORE_EXCEPTIONS': True,
        }
    }
    
    

# ======================== Sentry Configuration ========================
if not DEBUG and config('SENTRY_DSN', default=''):
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration

    sentry_sdk.init(
        dsn=config('SENTRY_DSN'),
        integrations=[DjangoIntegration()],
        traces_sample_rate=0.2,
        send_default_pii=True,
        environment=config('ENVIRONMENT', default='production'),
    )
    
    
# ======================== Brevo Email Configuration ========================
BREVO_API_KEY = config('BREVO_API_KEY')
EMAIL_SENDER_NAME = config('EMAIL_SENDER_NAME')
EMAIL_SENDER_EMAIL = config('EMAIL_SENDER_EMAIL')
FRONTEND_URL = config('FRONTEND_URL')

    
# ======================== Render Ping ========================
RENDER_HEALTHCHECK_URL = "https://evigdia.onrender.com/healthcheck"  # Your Render URL
RENDER_KEEPALIVE_ENABLED = True  # Optional disable flag


# ============================= SWAGGER DOCUMENTATION =============================

SPECTACULAR_SETTINGS = {
    'TITLE': 'Social DM API',
    'DESCRIPTION': 'API for FusionPex',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,

    # 👇 Swagger UI Settings (Add Bearer Token Input)
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,  # Saves token even after refresh
        'displayOperationId': True,
        'filter': True,
        'docExpansion': 'none',  # Collapses all docs by default
        'defaultModelsExpandDepth': -1,  # Hides schemas by default
        'operationsSorter': 'method',
        'tagsSorter': 'alpha',
        # 👇 This enables the "Authorize" button for Bearer Token
        'securityDefinitions': {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header',
                'description': 'Type in the **Value** field: `Bearer <your_token>`',
            }
        },
    },

    # 👇 Security Scheme (Required for OpenAPI 3.0)
    'COMPONENT_SECURITY_SCHEMES': {
        'Bearer': {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }
    },

    # 👇 Apply security globally (if all endpoints require auth)
    'SECURITY': [{'Bearer': []}],  # Optional: Remove if some endpoints are public

    # Rest of your settings...
    'SCHEMA_PATH_PREFIX': r'/api/',
    'SERVERS': [{'url': 'http://localhost:8000/', 'description': 'Dev Server'}],
}



# -------------------------------
# Warning Suppression Configuration
# -------------------------------

import warnings

# Suppress dj-rest-auth deprecation warnings
warnings.filterwarnings(
    'ignore',
    message="app_settings.USERNAME_REQUIRED is deprecated",
    category=UserWarning,
    module="dj_rest_auth.registration.serializers"
)

warnings.filterwarnings(
    'ignore',
    message="app_settings.EMAIL_REQUIRED is deprecated",
    category=UserWarning,
    module="dj_rest_auth.registration.serializers"
)

# Suppress django-allauth deprecation warnings
warnings.filterwarnings(
    'ignore',
    message="settings.ACCOUNT_AUTHENTICATION_METHOD is deprecated",
    category=UserWarning
)

warnings.filterwarnings(
    'ignore',
    message="settings.ACCOUNT_EMAIL_REQUIRED is deprecated",
    category=UserWarning
)

warnings.filterwarnings(
    'ignore',
    message="settings.ACCOUNT_USERNAME_REQUIRED is deprecated",
    category=UserWarning
)
