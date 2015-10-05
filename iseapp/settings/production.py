from .base import *
import os

DEBUG = True
#SESSION_COOKIE_AGE=1000

TEMPLATE_DEBUG = True

#ALLOWED_HOSTS = []
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'iseapp_produccion',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}



THIRD_PARTY_APPS = (
 #   'mockups',
)
INSTALLED_APPS = INSTALLED_APPS + THIRD_PARTY_APPS

MEDIA_ROOT = BASE_DIR.child('media')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
STATIC_ROOT = '/'#os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
#AUTH_PROFILE_MODULE = 'apps.autorizaciones.perfil'
MEDIA_URL = 'http://127.0.0.1:8000/media/'
