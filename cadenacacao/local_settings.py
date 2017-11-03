import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'unag',
#     }
# }

#send mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'ermurillo22@gmail.com'
# EMAIL_HOST_PASSWORD = 'Erivmumo22.'
# EMAIL_PORT = 587

EMAIL_USE_TLS = True
EMAIL_HOST = 'box1400.bluehost.com'                                                                  
EMAIL_HOST_USER = 'noreply@unag-datos.org'                              
EMAIL_HOST_PASSWORD = 'N0r3ply123.'
EMAIL_PORT = 465 

