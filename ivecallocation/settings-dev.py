# -*- coding: utf-8 -*-
# Django settings for project.
import os
from django.utils.webhelpers import url

from appsettings.default_dev import *
from appsettings.ivecallocation.dev import *

ROOT_URLCONF = 'ivecallocation.urls'

INSTALLED_APPS.extend( [
    'ivecallocation.allocation',
    'ivecallocation.registration',
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
LOGS = ['ivecallocation', 'mango-ldap']
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

# this does not have an effect presently
#LOGIN_REDIRECT_URL = url('/admin/allocation/application/add/')

# cookies expiration. Longer timeout requested, set to 8hrs now
SESSION_COOKIE_AGE = 8*60*60

# applications open, controls whether the login redirects to the Application Change Page or the main Admin site
APPLICATIONS_OPEN = False

# needed by ldap_helper
AUTH_LDAP_ADMIN_BASE = ''

#FJ TODO REMOVE I am not sure why the settings in CCGAPPS don't work in my local dev environment
EPIC_LDAP_DOMAIN    = 'dc=org'
EPIC_LDAP_COMPANY   = 'dc=ivec'
EPIC_LDAP_BASE      = '%s,%s' % (EPIC_LDAP_COMPANY, EPIC_LDAP_DOMAIN)
EPIC_LDAP_USER_OU   = 'ou=People'
EPIC_LDAP_USERBASE  = '%s,%s' % (EPIC_LDAP_USER_OU, EPIC_LDAP_BASE)
EPIC_LDAP_GROUPBASE = 'ou=Projects,ou=Groups,%s' % (EPIC_LDAP_BASE)
EPIC_LDAP_SERVER    = 'ldaps://fdsdev.localdomain'  # 'ldap://..' if not authenticated, otherwise 'ldaps://...'
EPIC_LDAP_ADMINBASE = EPIC_LDAP_BASE
EPIC_LDAP_USERDN    = 'uid=portalapp,ou=System,ou=People' # 'uid=portalapp,ou=System,ou=People,dc=ivec,dc=org'
EPIC_LDAP_PASSWORD  = 'te3rueto'
