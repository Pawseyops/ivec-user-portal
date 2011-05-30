# -*- coding: utf-8 -*-
# Django settings for project.
import os
from django.utils.webhelpers import url

# PROJECT_DIRECTORY isnt set when not under wsgi
if not os.environ.has_key('PROJECT_DIRECTORY'):
    os.environ['PROJECT_DIRECTORY']=os.path.dirname(__file__).split("/appsettings/")[0]

from appsettings.default_dev import *
from appsettings.ivecallocation.dev import *

ROOT_URLCONF = 'ivecallocation.urls'

INSTALLED_APPS.extend( [
    'ivecallocation.allocation',
    'ivecallocation.registration'
] )

AUTHENTICATION_BACKENDS = [
 'django.contrib.auth.backends.ModelBackend',
]

SESSION_COOKIE_PATH = url('/')
SESSION_SAVE_EVERY_REQUEST = True
CSRF_COOKIE_NAME = "csrftoken_IVECALLOCATION"


APPEND_SLASH = True
SITE_NAME = 'ivecallocation'

# ssl for entire site
SSL_FORCE = True

##
## LOGGING
##
import logging
LOG_DIRECTORY = os.path.join(PROJECT_DIRECTORY,"logs")
LOGGING_LEVEL = logging.DEBUG
LOGGING_FORMATTER = logging.Formatter('[%(name)s:%(levelname)s:%(filename)s:%(lineno)s:%(funcName)s] %(message)s')
LOGS = ['ivecallocation']


# registration app settings
ACCOUNT_ACTIVATION_DAYS = 14


##
## CAPTCHA settings
##

# Captcha image directory
CAPTCHA_IMAGES = os.path.join(WRITABLE_DIRECTORY, "captcha")

# the filesystem space to write the captchas into
CAPTCHA_ROOT = os.path.join(MEDIA_ROOT, 'captchas')

# the URL base that points to that directory served out
CAPTCHA_URL = os.path.join(MEDIA_URL, 'captchas')


RECAPTCHA_PUBLIC_KEY = "6LcB0sQSAAAAAJv_KVDzDjRbAMpJfc9b2t6rlOdV"
RECAPTCHA_PRIVATE_KEY = "6LcB0sQSAAAAAPy2brzHv_A6i3Atft6rmrfC32-g"
