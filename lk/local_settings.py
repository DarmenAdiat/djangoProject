# import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'django-insecure-g$t)_&o=q#0^)bd@e7pwx(j6&$%0$6-ug&p6_8oqno_8ctr3)5'

DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
    '192.168.0.151',
    '192.168.101.2',
    '192.168.101.10',
    '79.143.20.160',
    'localhost',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# smtp
EMAIL_USE_TLS = True
# EMAIL_HOST = 'smtp.gmail.com'
# EMAIL_HOST_USER = 'isker.web@gmail.com'
# EMAIL_HOST_PASSWORD = 'Rfhbvjdf94'
EMAIL_HOST = 'mailer.isker.kz'
EMAIL_HOST_USER = 'erp@isker.kz'
EMAIL_HOST_PASSWORD = 'Sk272BV4'
EMAIL_PORT = 587