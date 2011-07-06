import mako 
from django.core import mail as django_mail
from ivecallocation import settings
from django.utils.webhelpers import siteurl
import uuid
import datetime

# TODO
FROM_EMAIL = 'us@ccg.murdoch.edu.au'
# TODO use Django's loader
TEMPLATE_LOOKUP = mako.lookup.TemplateLookup(directories=settings.TEMPLATE_DIRS)

def send_account_creation_mail(participant, request):
    subject = "Account creation at iVEC"
    message_template = TEMPLATE_LOOKUP.get_template('allocation/account_creation_email.txt')
    email_hash = str(uuid.uuid4())
    link = siteurl(request) + 'account/create/' + email_hash

    message = message_template.render(participant=participant, link=link)
    send_mail(subject, message, participant.email)

    participant.account_email_hash = email_hash
    participant.status_id = 2
    participant.account_email_on = datetime.datetime.now()
    participant.save()

def send_mail(subject, message, to):
    assert 'ccg.murdoch.edu.au' in to, "Can send email just to a ccg.murdoch.edu.au address"    
    django_mail.send_mail(subject, message, FROM_EMAIL, [to])