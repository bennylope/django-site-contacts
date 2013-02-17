import django

if django.VERSION[:2] >= (1, 3):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:',
        }
    }
else:
    DATABASE_ENGINE = 'sqlite3'


INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'contact',
]

SITE_MANAGERS = (('Donkey Kong', 'donkey@kong.io'),)

EMAIL_BACKEND='django.core.mail.backends.console.EmailBackend'

SECRET_KEY = "BusTransportingCarnivalCruisePassengersCrashesIntoSewageTreatmentPlant"
