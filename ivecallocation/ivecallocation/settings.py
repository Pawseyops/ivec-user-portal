# -*- coding: utf-8 -*-
# Django settings for project.
# These are the baked-in defaults
# Edit here or override under appsettings.ivecallocation

import os
import logging
from ccg.utils.webhelpers import url

# SCRIPT_NAME isnt set when not under wsgi
if not os.environ.has_key('SCRIPT_NAME'):
    os.environ['SCRIPT_NAME']=''

SCRIPT_NAME =   os.environ['SCRIPT_NAME']
PROJECT_DIRECTORY = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


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

TEMPLATE_DEBUG = DEBUG

LOGIN_URL = url('/accounts/login/')
LOGOUT_URL = url('/accounts/logout/')

##
## Django Core stuff
##
TEMPLATE_LOADERS = [
    'ccg.template.loaders.makoloader.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.common.CommonMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'ccg.middleware.ssl.SSLRedirect'
]

INSTALLED_APPS = [
    'django_extensions',
    'ivecallocation.allocation',
    'registration',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'south',
]

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


STATIC_ROOT = os.path.join(PROJECT_DIRECTORY,"static")
STATIC_URL = url('/static/')
MEDIA_ROOT = os.path.join(PROJECT_DIRECTORY,"static","media")
MEDIA_URL = url('/static/media/')
ADMIN_MEDIA_PREFIX = url('/static/admin/')

# there is no default setup here as one of these configs should be made 'default' by the settings
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'ivecallocation',                      # Or path to database file if using sqlite3.
        'USER': 'ivecallocation',                      # Not used with sqlite3.
        'PASSWORD': 'ivecallocation',                  # Not used with sqlite3.
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
EPIC_LDAP_DOMAIN    = 'dc=com'
EPIC_LDAP_COMPANY   = 'dc=my-domain'
EPIC_LDAP_BASE      = '%s,%s' % (EPIC_LDAP_COMPANY, EPIC_LDAP_DOMAIN)
EPIC_LDAP_USER_OU   = 'ou=People'
EPIC_LDAP_USERBASE  = '%s,%s' % (EPIC_LDAP_USER_OU, EPIC_LDAP_BASE)
EPIC_LDAP_GROUPBASE = 'ou=Projects,ou=Groups,%s' % (EPIC_LDAP_BASE)
EPIC_LDAP_SERVER    = 'ldap://localhost'
EPIC_LDAP_ADMINBASE = EPIC_LDAP_BASE
EPIC_LDAP_POSIXGROUPBASE = 'ou=POSIX,ou=Groups,%s' % (EPIC_LDAP_BASE)
EPIC_LDAP_USERDN    = 'cn=Manager' # 'uid=portalapp,ou=System,ou=People,dc=ivec,dc=org'
EPIC_LDAP_PASSWORD  = 'secret'

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
APPLICATION_NOTICES = ADMINS

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

#INSTALLED_APPS.extend( [
#    'django_extensions',
#    'ivecallocation.allocation',
#    'registration',
#] )

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
LOG_DIRECTORY = os.path.join(PROJECT_DIRECTORY, "logs")
#if not os.path.exists(LOG_DIRECTORY):
#    os.mkdir(LOG_DIRECTORY)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': 'IVECALLOCATION [%(name)s:' + 'ivecallocation' + ':%(levelname)s:%(asctime)s:%(filename)s:%(lineno)s:%(funcName)s] %(message)s'
        },
        'db': {
            'format': 'IVECALLOCATION [%(name)s:' + 'ivecallocation' + ':%(duration)s:%(sql)s:%(params)s] %(message)s'
        },
        'simple': {
            'format': 'IVECALLOCATION ' + 'ivecallocation' + ' %(levelname)s %(message)s'
        },
    },
    'filters': {
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class':'django.utils.log.NullHandler',
        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file':{
            'level':'DEBUG',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIRECTORY, 'ivecallocation.log'),
            'when':'midnight',
            'formatter': 'verbose'
        },
        'db_logfile':{
            'level':'DEBUG',
            'class':'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(LOG_DIRECTORY, 'ivecallocation_db.log'),
            'when':'midnight',
            'formatter': 'db'
        },
        'syslog':{
            'level':'DEBUG',
            'class':'logging.handlers.SysLogHandler',
            'address':'/dev/log',
            'facility':'local4',
            'formatter': 'verbose'
        },        
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'formatter':'verbose',
            'include_html':True
        }
    },
    'loggers': {
        'django': {
            'handlers':['null'],
            'propagate': True,
            'level':'DEBUG',
        },
        'django.request': {
            'handlers': ['file', 'syslog', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['db_logfile', 'mail_admins'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'mango_ldap': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

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

try:
    print
    print 'Attepting to import appsettings.ivecallocation if it exists ...',
    from appsettings.ivecallocation import *
    print 'OK'
except Exception, e:
    print 'Fail'
