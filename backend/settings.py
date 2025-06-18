from pathlib import Path
import os
from datetime import timedelta


BASE_DIR = Path(__file__).resolve().parent.parent

from dotenv import load_dotenv
from pathlib import Path

dotenv_path = Path(os.getcwd() + '/config.env')
load_dotenv(dotenv_path=dotenv_path)

DEBUG= os.environ.get('DEBUG')

SECRET_KEY = os.environ.get('SECRET_KEY')
FIREBASE_KEY=os.environ.get('FIREBASE_KEY')
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')

# DEFAULT_HOST = os.environ.get('DEFAULT_HOST', 'http://127.0.0.1:8000')
DEFAULT_HOST = 'https://kienos-backend-4w2a.onrender.com'
# NODEJS_HOST = os.environ.get('NODEJS_HOST', 'http://127.0.0.1:8888')
NODEJS_HOST = 'https://kienos-nodejs-j3x1.onrender.com'
FE_HOST = os.environ.get('FE_HOST', 'http://localhost:3000')

CORS_ALLOW_CREDENTIALS = bool(os.environ.get('CORS_ALLOW_CREDENTIALS'))

# CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS').split(',')

CORS_ALLOW_ALL_ORIGINS = bool(os.environ.get('CORS_ALLOW_ALL_ORIGINS'))
CORS_ALLOWED_ORIGINS = [
    "http://192.168.110.40:3000",
    "http://localhost:3000",
    "http://192.168.204.181:3000",
    "http://192.168.1.6:3000"
    "http://192.168.1.6:3000",
    "https://kienos-frontend-z1ie.onrender.com",
    "kienos-backend-4w2a.onrender.com"
]

CLOUD_SECRET=os.environ.get('CLOUD_SECRET')
CLOUD_API=os.environ.get('CLOUD_API')
# CLOUDINARY_URL=f'cloudinary://{CLOUD_API}:{CLOUD_SECRET}@dzcvenbcx'
CLOUDINARY_URL=os.environ.get('CLOUDINARY_URL')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'channels',
    'storages',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'message',
    'service',
    'user',
    'user_profile',
    'workout',
    'notification',
    'device_token'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'base.middleware.BaseMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

]

ROOT_URLCONF = 'backend.urls'



WSGI_APPLICATION = 'backend.wsgi.application'
ASGI_APPLICATION = 'backend.asgi.application'


DATABASES = {
	'default': {
		'ENGINE': os.environ.get('DB_ENGINE'),
		'NAME': os.environ.get('DB_NAME'),
		'USER': os.environ.get('DB_USER'),
		'PASSWORD': os.environ.get('DB_PASSWORD'),
		'HOST':os.environ.get('DB_HOST'),
		'PORT':os.environ.get('DB_PORT'),
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

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=int(os.environ.get('ACCESS_TOKEN_LIFETIME', 30))),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=int(os.environ.get('REFRESH_TOKEN_LIFETIME', 2))),
    'ROTATE_REFRESH_TOKENS': os.environ.get('ROTATE_REFRESH_TOKENS'),
    'BLACKLIST_AFTER_ROTATION': os.environ.get('BLACKLIST_AFTER_ROTATION'),
    'ALGORITHM': os.environ.get('ALGORITHM', 'HS256'),
    'SIGNING_KEY': os.environ.get('SECRET_KEY'),
    # 'AUTH_HEADER_TYPES': (os.environ.get('AUTH_HEADER_TYPES', 'Bearer'),),
}

AUTH_USER_MODEL = 'user.User'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Ho_Chi_Minh'

USE_I18N = True

USE_TZ = True

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# EMAIL
EMAIL_BACKEND = os.environ.get('EMAIL_BACKEND')
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = os.environ.get('EMAIL_PORT')
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')

# SMS
TWILIO_ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.environ.get('TWILIO_PHONE_NUMBER')


SINCH_KEY_ID = os.environ.get('SINCH_KEY_ID')
SINCH_KEY_SECRET = os.environ.get('SINCH_KEY_SECRET')
SINCH_PHONE_NUMBER = os.environ.get('SINCH_PHONE_NUMBER')
SINCH_SMS_URL = os.environ.get('SINCH_SMS_URL')


# AWS Bucket settings
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME')
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL = None
AWS_S3_VERIFY = True

AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.{AWS_S3_REGION_NAME}.amazonaws.com'

# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
MEDIA_URL = f'https://res.cloudinary.com/'
STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
TEMPLATES_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/templates/'


# STORAGES = {
#     "default": {
#         "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",
#         "OPTIONS": {
#             "bucket_name": AWS_STORAGE_BUCKET_NAME,
#             "access_key": AWS_ACCESS_KEY_ID,
#             "secret_key": AWS_SECRET_ACCESS_KEY,
#             "region_name": AWS_S3_REGION_NAME,
#             "file_overwrite": AWS_S3_FILE_OVERWRITE,
#             "default_acl": AWS_DEFAULT_ACL,
#             "verify": AWS_S3_VERIFY,
#         },
#     },
#     "staticfiles": {
#         "BACKEND": "storages.backends.s3boto3.S3StaticStorage",
#         "OPTIONS": {
#             "bucket_name": AWS_STORAGE_BUCKET_NAME,
#             "access_key": AWS_ACCESS_KEY_ID,
#             "secret_key": AWS_SECRET_ACCESS_KEY,
#             "region_name": AWS_S3_REGION_NAME,
#             "file_overwrite": AWS_S3_FILE_OVERWRITE,
#             "default_acl": AWS_DEFAULT_ACL,
#             "verify": AWS_S3_VERIFY,
#         },
#     },
# }

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# # Additional S3 settings
# AWS_S3_OBJECT_PARAMETERS = {
#     'CacheControl': 'max-age=86400',
# }
# AWS_QUERYSTRING_AUTH = False

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'), 
        ],
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
