"""
Django settings for codo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '==4iht@8*v@x=z1@ge$z-5fdgu=1t$nwvjo5j&@#qq4i+*30%k'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'formtools',
    'campaigns',
    'payments',
    'bootstrap3',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'widget_tweaks',
    'django_countries',
    'embed_video',
    'datetimewidget',
    'debug_toolbar',
    'django_wysiwyg',
    'tinymce',
    
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
)

ROOT_URLCONF = 'config.urls'

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

if 'RDS_DB_NAME' in os.environ:
    DATABASES = {
        'default':{
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.environ['RDS_DB_NAME'],
            'USER': os.environ['RDS_USERNAME'],
            'PASSWORD': os.environ['RDS_PASSWORD'],
            'HOST':os.environ['RDS_HOSTNAME'],
            'PORT':os.environ['RDS_PORT'],
        }
    }
else:
    DATABASES = {
        'default': {
            
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'codo',
            'USER': 'joe',
            'PASSWORD': '12345',
            'HOST':'',
            'PORT':'5432',

        }
    }
# Cache

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Dubai'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)

STATIC_ROOT = os.path.join(BASE_DIR, "..", "www", "static")
STATIC_URL = '/static/'


# Templates 

TEMPLATE_DEBUG = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                # `allauth` needs this from django
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.request',

            ],
        },
    },
]


#########################
# OAUTH with allauth    #
########################

#this is for dev only
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend' 
ACCOUNT_SIGNUP_FORM_CLASS = 'campaigns.forms.SignupForm'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_LOGOUT_ON_GET = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
SITE_ID = 1
SOCIALACCOUNT_QUERY_EMAIL = True
LOGIN_REDIRECT_URL = "/"
AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)


SOCIALACCOUNT_PROVIDERS = \
    {'facebook':
       {'METHOD': 'oauth2',
        'SCOPE': ['email'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time'],
        'LOCALE_FUNC': lambda request: 'en_US',
        'EXCHANGE_TOKEN': True,
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.4'}}




# Django-crispy-forms Settings
CRISPY_TEMPLATE_PACK = 'bootstrap3'

# Uploaded Files (Media)
MEDIA_ROOT = os.path.join(BASE_DIR, "..", "media/")
MEDIA_URL = "/media/"

# For django-phonenumber
PHONENUMBER_DB_FORMAT = 'E164'

# Django-date-time widget
USE_L10N = True
USE_TZ = True 
USE_I18N = True

# Payment Settings (with wepay)
WEPAY_REDIRECT_URI = 'http://localhost:8000/wepay'
WEPAY_PRODUCTION = False
if 'WEPAY_CLIENT_SECRET' in os.environ: 
    WEPAY_CLIENT_SECRET = os.environ['WEPAY_CLIENT_SECRET']
else:
    WEPAY_CLIENT_SECRET = "d08080ea95"

if 'WEPAY_CLIENT_ID' in os.environ: 
    WEPAY_CLIENT_ID = os.environ['WEPAY_CLIENT_ID']
else:
    WEPAY_CLIENT_ID = "196430"

#This is the list of countries currently supported by Stripe
AUTHORIZED_ORGANIZER_COUNTRIES = ['AU','CA','DK','FI','IE', 'NO', 'US', 'GB','SE']

#Django WYSIWYG
DJANGO_WYSIWYG_FLAVOR = "tinymce"






