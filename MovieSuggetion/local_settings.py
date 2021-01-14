import os

SECRET_KEY = 'sg4&vtj7avt#1ss^$3nd9pohb4di#v2f4$lt@gf2xh+5-72rkj'

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

DEBUG = True