from .base import *
DEBUG = True

ALLOWED_HOSTS = ['django-ecomerce-a.herokuapp.com']


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'dd7o7jlfs6t54q',
        'USER': 'ivhfdufcpcshou',
        'PASSWORD': '7e6444ba6f230d1a887f6d81dddc8cfd772dafc2c79ecf323575aa8769ea297b',
        'HOST': 'ec2-54-80-122-11.compute-1.amazonaws.com',
        'PORT': '5432',
    }
}

STATICFILES_DIRS = (BASE_DIR,'static')