import mako 
from django.core import mail as django_mail
from django.core.urlresolvers import reverse
from ivecallocation import settings
from django.utils.webhelpers import siteurl
import uuid
import datetime
import ldap_helper
from django.utils import simplejson

logger = logging.getLogger('ivecallocation') 

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
            participant_account.old_ldap_details = simplejson.dumps(details))
            participant_account.first_name = details.get('givenname', [''])[0]
            participant_account.last_name = details.get('sn', [''])[0]
            participant_account.phone = details.get('telephonenumber', [''])[0]
        except Exception, e:
            logger.warning("Could not parse returned ldap details, could not create participant account: %s" % (e));
            
        participant_account.save()
        retval = True
    return retval

def send_mail(subject, message, to):
    assert 'ccg.murdoch.edu.au' in to, "Can send email just to a ccg.murdoch.edu.au address"    
    django_mail.send_mail(subject, message, FROM_EMAIL, [to])

def get_ldap_details(emailaddress):
    base = 'dc=ivec,dc=org'
    userbase = 'cn=users,dc=ldap,%s' % (base)
    groupbase = 'cn=groups,dc=ldap,%s' % (base)
    ld = ldap_helper.LDAPHandler(server='ldap://absinthe.ivec.org', user_base=userbase,
                                    group = None, group_base = groupbase, admin_base=None
    
    )
    usermatch = ld.ldap_query(base=userbase filter='(mail=%s)' % (emailaddress) )
    if len(usermatch) == 0:
        return None
    else:
        return usermatch[0].get_attributes()

