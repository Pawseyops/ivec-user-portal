# -*- coding: utf-8 -*-
# Django settings for project.
# These are the baked-in defaults
# Edit here or override under appsettings.ivecallocation

import os
from django.utils.webhelpers import url

# SCRIPT_NAME isnt set when not under wsgi
if not os.environ.has_key('SCRIPT_NAME'):
    os.environ['SCRIPT_NAME']=''

SCRIPT_NAME =   os.environ['SCRIPT_NAME']
PROJECT_DIRECTORY = os.environ['PROJECT_DIRECTORY']

DEBUG = True
DEV_SERVER = True
SITE_ID = 1

# https
if SCRIPT_NAME:
    SSL_ENABLED = True
else:
    SSL_ENABLED = False

# Locale
TIME_ZONE = 'Australia/Perth'
LANGUAGE_CODE = 'en-us'
USE_I18N = True

LOG_DIRECTORY = os.path.join(PROJECT_DIRECTORY, 'logs')
TEMPLATE_DEBUG = DEBUG

LOGIN_URL = url('/accounts/login/')
LOGOUT_URL = url('/accounts/logout/')

##
## Django Core stuff
##
TEMPLATE_LOADERS = [
    'django.template.loaders.makoloader.filesystem.Loader',
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.email.EmailExceptionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.middleware.ssl.SSLRedirect'
]
TEMPLATE_DIRS = [
    os.path.join(PROJECT_DIRECTORY,"templates"),
]
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'south',
]

# for local development, this is set to the static serving directory. For deployment use Apache Alias
STATIC_SERVER_PATH = os.path.join(PROJECT_DIRECTORY,"static")

# a directory that will be writable by the webserver, for storing various files...
WRITABLE_DIRECTORY = os.path.join(PROJECT_DIRECTORY,"scratch")

##
## Mako settings stuff
##

# mako compiled templates directory
MAKO_MODULE_DIR = os.path.join(WRITABLE_DIRECTORY, "templates")

# mako module name
MAKO_MODULENAME_CALLABLE = ''

# cookies
SESSION_COOKIE_AGE = 60*60

#STATIC_ROOT = os.path.join(PROJECT_DIRECTORY,"static")
MEDIA_ROOT = os.path.join(PROJECT_DIRECTORY,"static","media")
MEDIA_URL = '/static/media/'
ADMIN_MEDIA_PREFIX = url('/static/admin-media/')

# there is no default setup here as one of these configs should be made 'default' by the settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ivecallocation',                      # Or path to database file if using sqlite3.
        'USER': 'postgres',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# LDAP settings for accessing the read only ivec LDAP details
IVEC_LDAP_BASE      = 'dc=ivec,dc=org'
IVEC_LDAP_USERBASE  = 'cn=users,dc=ldap,%s' % (IVEC_LDAP_BASE)
IVEC_LDAP_GROUPBASE = 'cn=groups,dc=ldap,%s' % (IVEC_LDAP_BASE)
IVEC_LDAP_SERVER    = 'ldap://absinthe.ivec.org'
IVEC_LDAP_ADMINBASE = IVEC_LDAP_BASE
IVEC_LDAP_USERDN    = 'uid=allocationapp,ou=Special Users,dc=informatics'
IVEC_LDAP_PASSWORD  = 'default'

#LDAP settings for the directory of users for EPIC
EPIC_LDAP_DOMAIN    = 'dc=org'
EPIC_LDAP_COMPANY   = 'dc=ivec'
EPIC_LDAP_BASE      = '%s,%s' % (EPIC_LDAP_COMPANY, EPIC_LDAP_DOMAIN)
EPIC_LDAP_USER_OU   = 'ou=People'
EPIC_LDAP_USERBASE  = '%s,%s' % (EPIC_LDAP_USER_OU, EPIC_LDAP_BASE)
EPIC_LDAP_GROUPBASE = 'ou=Projects,ou=Groups,%s' % (EPIC_LDAP_BASE)
EPIC_LDAP_SERVER    = 'ldaps://fdsdev.localdomain'
EPIC_LDAP_ADMINBASE = EPIC_LDAP_BASE
EPIC_LDAP_POSIXGROUPBASE = 'ou=POSIX,ou=Groups,%s' % (EPIC_LDAP_BASE)
EPIC_LDAP_USERDN    = 'uid=portalapp,ou=System,ou=People' # 'uid=portalapp,ou=System,ou=People,dc=ivec,dc=org'
EPIC_LDAP_PASSWORD  = 'default'

#These need to be defined for the ldap module to work, and can be overridden later.
AUTH_LDAP_SERVER = None
AUTH_LDAP_GROUP =  None
AUTH_LDAP_GROUP_BASE = None
AUTH_LDAP_ADMIN_BASE = None
AUTH_LDAP_USER_BASE = None

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'default'

# memcache server list
MEMCACHE_SERVERS = ['localhost:11211']
MEMCACHE_KEYSPACE = "ivecallocation"

# email server
DEFAULT_FROM_EMAIL = 'noreply@yourdomain.com'
EMAIL_HOST = 'localhost'
EMAIL_APP_NAME = "iVEC Allocation "
SERVER_EMAIL = "apache@yourdomain.com"                      # from address
EMAIL_SUBJECT_PREFIX = ""

# default emails
ADMINS = [
    ( 'alert', 'alerts@yourdomain.com' )
]
MANAGERS = ADMINS

##
## CAPTCHA settings
##

# Captcha image directory
CAPTCHA_IMAGES = os.path.join(WRITABLE_DIRECTORY, "captcha")

# the filesystem space to write the captchas into
CAPTCHA_ROOT = os.path.join(MEDIA_ROOT, 'captchas')

# the URL base that points to that directory served out
CAPTCHA_URL = os.path.join(MEDIA_URL, 'captchas')

# these default recaptcha keys will only work on 127.0.0.1/localhost
RECAPTCHA_PUBLIC_KEY = "6LdDRcgSAAAAAF8vUvW4eC-B3t_J3V5hK-SEIl1V"
RECAPTCHA_PRIVATE_KEY = "6LdDRcgSAAAAAOY7q8rX8rPRbCKNRY6-cxm2WL4q"



###############################################
ROOT_URLCONF = 'ivecallocation.urls'

INSTALLED_APPS.extend( [
    'allocation',
    'registration',
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
LOGS = ['ivecallocation', 'mango_ldap']
# registration app settings
ACCOUNT_ACTIVATION_DAYS = 14

# this does not have an effect presently
#LOGIN_REDIRECT_URL = url('/admin/allocation/application/add/')

# cookies expiration. Longer timeout requested, set to 8hrs now
SESSION_COOKIE_AGE = 8*60*60

# applications open, controls whether the login redirects to the Application Change Page or the main Admin site
APPLICATIONS_OPEN = False

#TODO: add this to ccg-apps-settings
# ou=POSIX,ou=Groups,dc=ivec,dc=org
# needs objectClass = 'top' and 'posixGroup'
EPIC_LDAP_POSIXGROUPBASE = 'ou=POSIX,ou=Groups,%s' % (EPIC_LDAP_BASE)

# Override defaults with your local instance settings.
# They will be loaded from appsettings.ivecallocation, which can exist anywhere
# in the instance's pythonpath. This is a CCG convention designed to support
# global shared settings among multiple Django projects.
try:
    from appsettings.ivecallocation import *
except ImportError, e:
    pass
