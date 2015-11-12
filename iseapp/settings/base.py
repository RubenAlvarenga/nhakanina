#import os
#BASE_DIR = os.path.dirname(os.path.dirname(__file__))

from unipath import Path
BASE_DIR=Path(__file__).ancestor(3)

SECRET_KEY = 'f*e+*z@m(1)uy!u*=jwu(bqnu^lvoey18rfc2^f&b0kyxk)#l6'

DJANGO_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
)
LOCAL_APPS = (
    'apps.aranceles',
    'apps.entidades',
    'apps.catedras',
    'apps.finanzas',
    'apps.autorizaciones',
    'apps.rendiciones',
    'apps.descuentos'
)
THIRD_PARTY_APPS = (
    'wkhtmltopdf',
    'django_tables2',
    #'debug_toolbar.apps.DebugToolbarConfig',
)
INSTALLED_APPS = DJANGO_APPS + LOCAL_APPS + THIRD_PARTY_APPS


# from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS as TCP
# TEMPLATE_CONTEXT_PROCESSORS = TCP + (
#     'django.core.context_processors.request',
#     # 'apps.context_processors.menu',
#     'django.contrib.messages.context_processors.messages',
# )


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [  BASE_DIR.child('templates'), ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',
                'apps.context_processors.menu',
            ],
        },
    },
]

WSGI_APPLICATION = 'iseapp.wsgi.application'



from django.core.urlresolvers import reverse_lazy
LOGIN_URL = reverse_lazy('logout')
LOGIN_REDIRECT_URL = reverse_lazy('login')
LOGOUT_URL = reverse_lazy('logout')

MIDDLEWARE_CLASSES = (
    'apps.middlewares.RequestAddSessionVars',
    'apps.middlewares.RequestTimeLoggingMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    #'breadcrumbs.middleware.BreadcrumbsMiddleware',
    #'webstack_django_sorting.middleware.SortingMiddleware',
)

ROOT_URLCONF = 'iseapp.urls'

WSGI_APPLICATION = 'iseapp.wsgi.application'

LANGUAGE_CODE = 'es-py'

TIME_ZONE = 'America/Asuncion'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Deprecated Django 1.8
# TEMPLATE_DIRS = (
#     BASE_DIR.child('templates'),
# )


