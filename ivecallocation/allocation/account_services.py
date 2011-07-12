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
from django.utils import simplejson


# TODO use Django's loader
TEMPLATE_LOOKUP = mako.lookup.TemplateLookup(directories=settings.TEMPLATE_DIRS)

def send_account_creation_mail(participant, request):
    subject = "Successful application for Pawsey funded iVEC infrastructure"
    message_template = TEMPLATE_LOOKUP.get_template('allocation/account_request_email.txt')
    email_hash = str(uuid.uuid4())
    link = "%s%s/%s" % (siteurl(request), 'account-request', email_hash)

    message = message_template.render(participant=participant, link=link)
    send_mail(subject, message, participant.email)

    participant.account_email_hash = email_hash
    participant.status_id = Participant.STATUS['EMAIL_SENT']
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
            try:
                participant_account = participant.participantaccount
            except ParticipantAccount.DoesNotExist:
                participant_account = ParticipantAccount(participant=participant)
            participant_account.old_ldap_details = simplejson.dumps(details)
            participant_account.first_name = details.get('givenName', [''])[0]
            participant_account.last_name = details.get('sn', [''])[0]
            participant_account.phone = details.get('telephoneNumber', [''])[0]
            participant_account.uid = details.get('uid', [''])[0]
            participant_account.uid_number = details.get('uidNumber', [''])[0]
            participant_account.gid_number = details.get('gidNumber', [''])[0]
            participant_account.password_hash = details.get('userPassword', [''])[0]
            participant_account.data_fetched_on = datetime.datetime.now() 
            participant_account.save()
            retval = True
        except Exception, e:
            logger.error("Could not parse returned ldap details, could not create participant account: %s" % (e));
            
    return retval

def send_mail(subject, message, to):
    assert 'ccg.murdoch.edu.au' in to, "Can send email just to a ccg.murdoch.edu.au address"    
    django_mail.send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to])

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

    usermatch = ld.ldap_query(base=settings.IVEC_LDAP_USERBASE, filter='(mail=%s)' % (emailaddress) )
    ld.close()
    if len(usermatch) == 0:
        return None
    else:
        return dict(usermatch[0].get_attributes())

def get_application_area(participant):
    app = participant.application
    areanum = str(app.id)
    if app.priority_area_radio_astronomy:
        area = 'Astronomy'
    elif app.priority_area_geosciences:
        area = 'Geosciences'
    elif app.priority_area_directors:
        area = 'Geosciences'
    elif app.priority_area_partner:
        area = 'Partners'
    elif app.priority_area_national:
        area = 'National'
    else:
        area = 'Other'  # should not happen
    print "participant %s area: %s areanum: %s" % (participant.email, area, areanum)
    return (area, areanum)

def create_user_accounts(participant_id_list):
    # #################################################
    '''
    Create the account in LDAP
    if the user account doesn't exist, create it
    else update it.
    Update means update the attributes already in the LDAP entry
    and add the ones from the old LDAP entry that are not the in the new LDAP
    '''
    created_count = 0
    error_count = 0
    result = {'created':0, 'errors':0, 'updated':0, 'msg': ''}
    
    #connect to the 'new' ldap repo, where we create all the accounts
    #print "ldap bind with: server: %s userdn: %s password: %s" % (settings.EPIC_LDAP_SERVER, settings.EPIC_LDAP_USERDN, settings.EPIC_LDAP_PASSWORD)
    ldaph = ldap_helper.LDAPHandler(userdn     = settings.EPIC_LDAP_USERDN, 
                                 password   = settings.EPIC_LDAP_PASSWORD, 
                                 server     = settings.EPIC_LDAP_SERVER, 
                                 user_base  = settings.EPIC_LDAP_USERBASE, 
                                 group      = None, 
                                 group_base = settings.EPIC_LDAP_GROUPBASE, 
                                 admin_base = settings.EPIC_LDAP_ADMINBASE,
                                 dont_require_cert=True, debug=True)

    '''
    # test code: it works
    create_group(ldaphandler = ldaph, parentou = 'Gastronomy', groupname='Gastronomy101')
    ldaph.ldap_add_user_to_group(username='Ratatouille', groupname = 'Gastronomy101')
    # the username (uid) must exists
    ldaph.ldap_add_user_to_group(username='ahunter', groupname = 'Gastronomy101')
    return result
    '''

    # needed for ldap_helper.ldap_add_user: dn = 'uid=%s,%s,%s,%s' % (username, usercontainer, userdn, basedn)
    usercontainer = settings.EPIC_LDAP_USER_OU
    userdn = settings.EPIC_LDAP_COMPANY
    basedn = settings.EPIC_LDAP_DOMAIN

    if ldaph:
        for id in participant_id_list:
            participant = Participant.objects.get(id=id)
            institution = participant.participantaccount.institution.ldap_ou_name
            #print "\nParticipant: %s institution: %s" % (participant.email, institution)

            #if participant.status != 3: # TODO: change this!
            #    continue # account not ready yet

            try:
                participant_account = participant.participantaccount
                email = participant.email

                if participant_account:
                    #print "participant: %s %s email:%s" % (participant_account.first_name, participant_account.last_name, email)
                    # get the user entry in the new ldap repo if it exists

                    userdetails = ldaph.get_user_details_from_attribute(attribute = 'mail', value = email)
                    #print "user email: %s details: %s" % (email, userdetails)
                    done = False

                    if not userdetails:
                        # user entry does not exist in the new ldap, create it
                        done = create_user_account(ldaph, participant, usercontainer, userdn, basedn)
                        if done:
                            #TODO: update the account status
                            # participant.status = 4 # what number should that be??
                            result['created'] += 1
                    else:
                        # user entry does not exist in the new ldap, create it
                        done = update_user_account(ldaph, participant)
                        if done:
                            #TODO: update the account status
                            # participant.status = 4
                            result['updated'] += 1

                    done = True
                    if done:
                        # user added or updated to the ldap directory, add the user to the group, create the group if it doesn't exist
                        (area, areanum) = get_application_area(participant)
                        # TODO: add description of the application to the group
                        groupname = '%s-%s' % (area, areanum)
                        create_group(ldaphandler = ldaph, parentou = area, groupname = groupname)
                        uid = participant_account.uid
                        #done = add_user_to_group(ldaphandler = ldaph, uid = uid, groupname = areanum)
                        done = ldaph.ldap_add_user_to_group(uid, groupname)
            except ParticipantAccount.DoesNotExist, e:
                #print "\nParticipantAccount.DoesNotExist %s error: %s" % (participant.email, e)
                result['errors'] += 1
        ldaph.close()
    return result

def create_group(ldaphandler, parentou, groupname):
    """
    # Group creation test: it works.
    area = 'Area'
    cn = 'Area51'
    parent = 'ou=%s,%s' % (area, settings.EPIC_LDAP_GROUPBASE)

    ou = 'Area'
    parentdn = settings.EPIC_LDAP_GROUPBASE
    ldaph.create_ou(name = ou, parentdn = parentdn)

    # can't create the group if the parent doesn't exist
    ldaph.ldap_add_group_with_parent(groupname = cn, parentdn = parent)
    #ldaph.ldap_add_group('cn=Area51,ou=Area')
    return result
    """

    # create the OU for this group like 'Astronomy'
    ldaphandler.create_ou(name = parentou, parentdn = settings.EPIC_LDAP_GROUPBASE) # 'ou=Projects,ou=Groups,%s' % (EPIC_LDAP_BASE)

    # can't create the group if the parent doesn't exist
    # the group name would be like 'Astronomy01'
    groupparent = 'ou=%s,%s' % (parentou, settings.EPIC_LDAP_GROUPBASE)
    ldaphandler.ldap_add_group_with_parent(groupname = groupname, parentdn = groupparent)
    return

def add_user_to_group(ldaphandler, uid, groupname):
    done = False
    # find or create the group, should be ou=Astronomy01,ou=Astronomy,ou=Projects,ou=Groups,dc=ivec,dc=org
    '''
    project_title = models.CharField(max_length=100, help_text=help_text_project_title)
    project_summary = models.CharField(max_length=1000, help_text=help_text_project_summary, null=True, blank=True)
    priority_area_radio_astronomy = models.BooleanField()
    priority_area_geosciences = models.BooleanField()
    priority_area_directors = models.BooleanField()
    priority_area_partner = models.BooleanField()
    priority_area_national = models.BooleanField()    
    '''
    done = ldaph.ldap_add_user_to_group(uid, groupname)
    return done

def set_user_ldap_dict(participant):
    '''set the user attributes from the old dictionary and add/'override the attributes we really need'''
    participantaccount = participant.participantaccount
    if participantaccount and participantaccount.old_ldap_details:
        detailsdict = simplejson.loads(participantaccount.old_ldap_details)
    else:
        detailsdict = {}

    # DEBUG TEST ONLY
    detailsdict = {}

    #print "set_user_ldap_dict type: %s detailsdict BEFORE: %s" % (type(detailsdict), detailsdict)

    detailsdict["givenName"] = [participantaccount.first_name]
    detailsdict["sn"] = [participantaccount.last_name]
    detailsdict["cn"] = [participantaccount.first_name + ',' + participantaccount.last_name] # required attribute
    detailsdict['telephoneNumber'] = [participantaccount.phone]
    detailsdict['userPassword'] = [participantaccount.password_hash]


    uid =  str(participantaccount.uid)
    detailsdict['uid'] = [uid]
    
    #POSIX STUFF
    detailsdict['uidNumber'] = [participantaccount.uid_number]
    detailsdict['gidNumber'] = [participantaccount.gid_number]
    detailsdict['homeDirectory'] = '/home/%s' % (uid)
    #pull out the previous login shell.
    loginshell = '/bin/bash'
    if participantaccount.old_ldap_details is not None:
        try:
            prev_details = simplejson.loads(participantaccount.old_ldap_details)
            loginshell = str(prev_details['loginShell'][0])
        except:
            pass
    detailsdict['loginShell'] = loginshell


    # convert the unicode strings in strings for ldap, will be done in ldap_handler in the future
    for attr in detailsdict:
        valuelist = detailsdict[attr] # list of attributes in unicode strings
        #print 'valuelist: %s' % valuelist
        strlist = [str(value) for value in valuelist]
        detailsdict[attr] = strlist

    #print "set_user_ldap_dict type: %s detailsdict AFTER:  %s" % (type(detailsdict), detailsdict)

    return detailsdict

def create_user_account(ldaph, participant, usercontainer, userdn, basedn):
    participant_account = participant.participantaccount
    uid = participant_account.uid
    institution = participant_account.institution.ldap_ou_name
    usercontainer = 'ou=%s,%s' % (institution,usercontainer)
    olddict = {}
   
    detailsdict = set_user_ldap_dict(participant)

    print "create_user_account %s uid: %s userdn: %s basedn: %s" % (participant.email, uid, userdn, basedn)
    res = False
    # ldap_handler.add_user build the user dn like this:
    # dn = 'uid=%s,%s,%s,%s' % (username, usercontainer, userdn, basedn)
    # real example from ldap browser: uid=hum092,ou=CSIRO,ou=People,dc=ivec,dc=org
    res = ldaph.ldap_add_user(username = uid,
                  detailsDict = detailsdict,
                  pwencoding = None,
                  #objectclasses = ['top', 'inetOrgPerson', 'organizationalPerson', 'person', 'posixAccount'],
                  objectclasses = ['top', 'inetOrgPerson', 'organizationalPerson', 'posixAccount', 'person'],
                  usercontainer = usercontainer,
                  userdn = userdn,
                  basedn = basedn)

    # ldap_add_user returns false if the user was not added
    print "create_user_account res: %s" % (res,)
    return res

def update_user_account(ldaph, participant):
    participant_account = participant.participantaccount
    uid = participant_account.uid

    detailsdict = set_user_ldap_dict(participant)

    print "update_user_account %s uid: %s" % (participant.email, uid)
    res = False
    res = ldaph.ldap_update_user(username = uid,
                             newusername = uid,
                             newpassword = participant_account.password_hash,
                             detailsDict = detailsdict,
                             pwencoding = None)

    # ldap_update_user does not return anything, assume success
    # TODO: change ldap_update_user to return a real result code
    res = True
    return res

def hash_password(newpassword, pwencoding='md5'):
    return ldap_helper.createpassword(newpassword, pwencoding=pwencoding)

@transaction.commit_on_success
def save_account_details(participant_account):
    participant = participant_account.participant
    participant.status_id = Participant.STATUS['DETAILS_FILLED']
    participant.details_filled_on = datetime.datetime.now()
    #make sure the uid is valid
    participant_account.uid = participant_account.get_unique_uid()
    participant_account.save()
    #set the gid and uid based on the part_accnt id.
    participant_account.uid_number = participant_account.id + 20050
    participant_account.gid_number = participant_account.id + 20050
    participant_account.save()
    participant.save()

