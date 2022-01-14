# Application definition
import os

from settings.settings_base import BASE_DIR

INSTALLED_APPS = [
    'admin_interface',
    'colorfield',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'dynamic_rest',
    'corsheaders',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.apple',
    'rest_auth',
    'rest_auth.registration',
    'amazons3_module',
    'models',
    'analytics_module',
    'rest_auth_module',
]

# https://docs.djangodjango_settingscom/ko/1.11/ref/contrib/sites/
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': (os.path.join(BASE_DIR, 'email_module/templates'), os.path.join(BASE_DIR, 'pdf_module/templates')),
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

WSGI_APPLICATION = 'settings.wsgi.application'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ajpk8r4#)f7^y%p!)ik4^q#ghu633=u(ivb_f#+fbofopi+p(j'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '18.194.48.246', '3.121.251.31', 'api.beatpulse.app',
                 'test-api.beatpulse.app']

# csrf setup
CSRF_COOKIE_NAME = "csrftoken"
