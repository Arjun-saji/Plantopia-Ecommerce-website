"""
Django settings for ecomproject project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from django.utils.translation import gettext_lazy as _
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-1(s0^&b^4i_8sruvb7j(z5^s4g8c#p_bx+$n-8vmmmlvyxkcj*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

LANGUAGES = [
    ('en', _('English')),
    ('ml', _('Malayalam')),
    ('ta', _('Tamil')),
]




LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'ecomapp', 'locale'),
)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ecomapp'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ecomproject.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'ecomapp.context_processors.cart_items',
                'ecomapp.context_processors.cart_length',
                'ecomapp.context_processors.wishlist_length',
                
                
                
            ],
        },
    },
]

WSGI_APPLICATION = 'ecomproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases
import dj_database_url

# DATABASES = {
#     #'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
#     'default': dj_database_url.config(default=os.getenv('DATABASE_URL')),
# }
# #
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('postgresql://plantopia_user:sjJYVsEynerKkqjCE9XvQDarHtO3kEic@dpg-cu0fpg5ds78s73dd75og-a/plantopia'),
        conn_max_age=600,
        ssl_require=True  # Use this only if your database requires SSL
    )
}



# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
# STATICFILES_DIRS=[os.path.join(BASE_DIR,'static')]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
STATIC_ROOT = os.path.join(BASE_DIR, 'static')


STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



RAZORPAY_KEY_ID = 'rzp_test_km4ndhiThtzd8t'
RAZORPAY_KEY_SECRET = '5yF9RX5QnYEUOD0SXQ7MsSKv'


LOGIN_URL = '/login/'


USE_I18N = True
USE_L10N = True
USE_TZ = True

