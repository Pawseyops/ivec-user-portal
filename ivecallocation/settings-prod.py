# -*- coding: utf-8 -*-
# Django settings for project.
import os
from django.utils.webhelpers import url

from appsettings.default_prod import *
from appsettings.ivecallocation.prod import *

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
LOGGING_LEVEL = logging.CRITICAL
LOGGING_FORMATTER = logging.Formatter('[%(name)s:%(levelname)s:%(filename)s:%(lineno)s:%(funcName)s] %(message)s')
LOGS = ['ivecallocation', 'mango_ldap']

# registration app settings
ACCOUNT_ACTIVATION_DAYS = 14

# this does not have an effect presently
#LOGIN_REDIRECT_URL = url('/admin/allocation/application/add/')

# used to get ccg domain name when live
SITE_ID = 2

# cookies expiration. Longer timeout requested, set to 8hrs now
SESSION_COOKIE_AGE = 8*60*60

# applications open, controls whether the login redirects to the Application Change Page or the main Admin site
APPLICATIONS_OPEN = False
