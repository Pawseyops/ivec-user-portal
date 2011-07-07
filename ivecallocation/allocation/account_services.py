import mako 
from django.core import mail as django_mail
from django.core.urlresolvers import reverse
from ivecallocation import settings
from django.utils.webhelpers import siteurl
import uuid
import datetime
import ldap_helper
from django.utils import simplejson
from django.contrib import logging
logger = logging.getLogger('ivecallocation') 
from ivecallocation.allocation.models import *
from django.db import transaction

# TODO
FROM_EMAIL = 'us@ccg.murdoch.edu.au'
# TODO use Django's loader
TEMPLATE_LOOKUP = mako.lookup.TemplateLookup(directories=settings.TEMPLATE_DIRS)

def send_account_creation_mail(participant, request):
    subject = "Account creation at iVEC"
    message_template = TEMPLATE_LOOKUP.get_template('allocation/account_request_email.txt')
    email_hash = str(uuid.uuid4())
    site_url = siteurl(request)
    link = siteurl(request).rstrip('/') + reverse('account-request', args=[email_hash])

    message = message_template.render(participant=participant, link=link)
    send_mail(subject, message, participant.email)

    participant.account_email_hash = email_hash
    participant.status_id = 2
    participant.account_email_on = datetime.datetime.now()
    participant.save()

def fetch_old_ldap_details(participant):
    retval = False
    details = None
    try:
        details = get_ldap_details(participant.email)
    except Exception, e:
        logger.warning("Could not fetch ldap details for %s: %s" % (participant.email, e)); 
    #only create the participant account if we successfully 
    #pulled old ldap details.

    if details is not None:
        try:
            participant_account = ParticipantAccount()
            participant_account.participant = participant
            participant_account.old_ldap_details = simplejson.dumps(details)
            participant_account.first_name = details.get('givenName', [''])[0]
            participant_account.last_name = details.get('sn', [''])[0]
            participant_account.phone = details.get('telephoneNumber', [''])[0]
            participant_account.uid = details.get('uid', [''])[0]
            participant_account.uid_number = details.get('uidNumber', [''])[0]
            participant_account.gid_number = details.get('gidNumber', [''])[0]
            participant_account.password_hash = details.get('userPassword', [''])[0]
            participant_account.save()
            retval = True
        except Exception, e:
            logger.warning("Could not parse returned ldap details, could not create participant account: %s" % (e));
            
    return retval

def send_mail(subject, message, to):
    assert 'ccg.murdoch.edu.au' in to, "Can send email just to a ccg.murdoch.edu.au address"    
    django_mail.send_mail(subject, message, FROM_EMAIL, [to])

def get_ldap_details(emailaddress):
    ld = ldap_helper.LDAPHandler(userdn     = settings.IVEC_LDAP_USERDN, 
                                 password   = settings.IVEC_LDAP_PASSWORD, 
                                 server     = settings.IVEC_LDAP_SERVER, 
                                 user_base  = settings.IVEC_LDAP_USERBASE, 
                                 group      = None, 
                                 group_base = settings.IVEC_LDAP_GROUPBASE, 
                                 admin_base = settings.IVEC_LDAP_ADMINBASE,
                                 dont_require_cert=True, debug=True)
    usermatch = ld.ldap_query(base=settings.IVEC_LDAP_USERBASE, filter='(mail=%s)' % (emailaddress) )
    ld.close()
    if len(usermatch) == 0:
        return None
    else:
        return dict(usermatch[0].get_attributes())

def hash_password(newpassword, pwencoding='md5'):
    return ldap_helper.createpassword(newpassword, pwencoding=pwencoding)

@transaction.commit_on_success
def save_account_details(participant_account):
    participant = participant_account.participant
    participant.status_id = 3
    participant.account_email_hash = None
    participant.details_filled_on = datetime.datetime.now()
    participant_account.save()
    participant.save()

