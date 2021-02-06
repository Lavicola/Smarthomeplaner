"""
Django settings for Smarthomeplaner project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from django.utils.translation import gettext_lazy as _
import os




# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Add these new lines




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'fmc8=)wj_(r%&7y1)o5unr!8mbv%xx=en)5mb+7b@2l4507j+)'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []
AUTH_USER_MODEL = 'users.CustomUser'


# Application definition

INSTALLED_APPS = [
    # The following apps are required:


    ###
    'django.contrib.sites',
    'rest_framework',
    'django_filters',
    'modeltranslation',
    'django_countries',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    ### 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ####self start
    'users',
    'api.apps.APIConfig',
    'smarthome.apps.SmarthomeConfig',
    'configurator.apps.ConfiguratorConfig'
    ###self end



]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Smarthomeplaner.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

LOCALE_PATHS = ( os.path.join(BASE_DIR, 'locale'), )


AUTHENTICATION_BACKENDS = [
    
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
]

EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'


ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
LOGIN_REDIRECT_URL = "/configurator"
ACCOUNT_LOGOUT_REDIRECT_URL ="/userauth/accounts/login"


ACCOUNT_FORMS = {
'signup': 'userauth.forms.RegisterUser',
}
ACCOUNT_ADAPTER = 'userauth.adapter.CustomAccountAdapter'



SITE_ID = 1


WSGI_APPLICATION = 'Smarthomeplaner.wsgi.application'


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}



# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'django_database',
#        'USER': 'root',
#        'PASSWORD': '',
#        'HOST': 'localhost',
#        'PORT': '3306',
#    }
#}


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Provide a lists of languages which your site supports.
LANGUAGES = (
    ('en', _('English')),
    ('de', _('German'))
)
MODELTRANSLATION_LANGUAGES = ('en', 'de')



# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.cobvgxm/en/3.1/howto/static-files/
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),)
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')



MEDIA_ROOT  = os.path.join(BASE_DIR, 'Media')
MEDIA_URL = "/media/"

