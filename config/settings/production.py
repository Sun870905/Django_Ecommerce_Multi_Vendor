import os

import dj_database_url
import dotenv

from .base import BASE_DIR

env = BASE_DIR / '.env'

dotenv.read_dotenv(env)

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

ALLOWED_HOSTS = ["multiple-vendor-e-commerce.herokuapp.com"]

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

db_from_env = dj_database_url.config()
DATABASES['default'].update(db_from_env)

# Stripe

STRIPE_PUBLIC_KEY = os.environ['STRIPE_PUBLIC_KEY']

STRIPE_SECRET_KEY = os.environ['STRIPE_SECRET_KEY']

# Handling Emails

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_USER = 'mugdhaarunimahmed2017@gmail.com'

EMAIL_HOST_PASSWORD = os.environ['EMAIL_HOST_PASSWORD']

EMAIL_PORT = 587

EMAIL_USE_LTS = True

DEFAULT_EMAIL_FROM = 'E-commerce <noreply@maxelitecoding.com>'

CONTACT_EMAIL = 'mugdhaarunimahmed2017@gmail.com'
