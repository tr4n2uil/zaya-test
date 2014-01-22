from settings import *

DEBUG = False
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'backend',
        'USER': 'root',
        'PASSWORD': 'krishna',
        'HOST': '',
        'PORT': '',
    }
}

ROOTPATH = 'http://www.zaya-test.com'
SESSION_COOKIE_DOMAIN = 'zaya-test.com'

