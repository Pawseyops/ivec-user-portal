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

def send_account_created_notification_mail(participant, request):
    subject = "Account created for Pawsey funded iVEC infrastructure"
    message_template = TEMPLATE_LOOKUP.get_template('allocation/account_created_email.txt')

    message = message_template.render(participant=participant)
    send_mail(subject, message, participant.email)

    participant.status_id = Participant.STATUS['ACCOUNT_CREATED_EMAIL_SENT']
    participant.account_created_email_on = datetime.datetime.now()
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
    #print "participant %s area: %s areanum: %s" % (participant.email, area, areanum)
    return (area, areanum)

def create_user_accounts(participant_id_list):
    '''
    Create the account in LDAP and add it to the group
    if the user account doesn't exist, create it else update it.
    Update means update the attributes already in the LDAP entry
    and add the ones from the old LDAP entry that are not the in the new LDAP
    '''
    created_count = 0
    error_count = 0
    result = {'created':0, 'errors':0, 'updated':0, 'msg': ''}
    
    #connect to the 'new' ldap repo, where we create all the accounts
    logger.debug("ldap bind with: server: %s userdn: %s" % (settings.EPIC_LDAP_SERVER, settings.EPIC_LDAP_USERDN) )
    ldaph = ldap_helper.LDAPHandler(userdn     = settings.EPIC_LDAP_USERDN, 
                                 password   = settings.EPIC_LDAP_PASSWORD, 
                                 server     = settings.EPIC_LDAP_SERVER, 
                                 user_base  = settings.EPIC_LDAP_USERBASE, 
                                 group      = None, 
                                 group_base = settings.EPIC_LDAP_GROUPBASE, 
                                 admin_base = settings.EPIC_LDAP_ADMINBASE,
                                 dont_require_cert=True, debug=True)

    # needed for ldap_helper.ldap_add_user: dn = 'uid=%s,%s,%s,%s' % (username, usercontainer, userdn, basedn)
    usercontainer = settings.EPIC_LDAP_USER_OU
    userdn = settings.EPIC_LDAP_COMPANY
    basedn = settings.EPIC_LDAP_DOMAIN

    if ldaph:
        for id in participant_id_list:
            participant = Participant.objects.get(id=id)
            institution = participant.participantaccount.institution.ldap_ou_name
            logger.debug("\nParticipant: %s institution: %s" % (participant.email, institution) )

            if participant.status_id != Participant.STATUS['DETAILS_FILLED']:   # account not ready yet
                result['errors'] += 1
                continue # next participant

            try:
                participant_account = participant.participantaccount
                email = participant.email

                if participant_account:
                    logger.debug("participant: %s %s email:%s" % (participant_account.first_name, participant_account.last_name, email) )
                    # get the user entry in the new ldap repo if it exists

                    userdetails = ldaph.get_user_details_from_attribute(attribute = 'mail', value = email)
                    logger.debug("user email: %s details: %s" % (email, userdetails) )
                    done = False

                    if not userdetails:
                        # user entry does not exist in the new ldap, create it
                        done = create_user_account(ldaph, participant, usercontainer, userdn, basedn)
                        if done:
                            result['created'] += 1
                    else:
                        done = update_user_account(ldaph, participant)
                        if done:
                            result['updated'] += 1

                    done = True # force the addition to the group even if there is an error
                    if done:
                        # user added or updated to the ldap directory, add the user to the group, create the group if it doesn't exist
                        (area, areanum) = get_application_area(participant)

                        groupname = '%s-%s' % (area, areanum)
                        create_group(ldaphandler = ldaph, parentou = area, groupname = groupname, description = str(participant.application.project_title))
                        uid = participant_account.uid
                        done = ldaph.ldap_add_user_to_group(uid, groupname)

                        participant.status_id = Participant.STATUS['ACCOUNT_CREATED']
                        participant.save()

            except ParticipantAccount.DoesNotExist, e:
                logger.debug("ParticipantAccount.DoesNotExist %s error: %s" % (participant.email, e) )
                result['errors'] += 1
        ldaph.close()
    return result

def create_group(ldaphandler, parentou, groupname, description):
    # create the OU for this group like 'Astronomy'
    ldaphandler.create_ou(name = parentou, parentdn = settings.EPIC_LDAP_GROUPBASE) # 'ou=Projects,ou=Groups,%s' % (EPIC_LDAP_BASE)

    # can't create the group if the parent doesn't exist
    # the group name would be like 'Astronomy-01'
    groupparent = 'ou=%s,%s' % (parentou, settings.EPIC_LDAP_GROUPBASE)
    ldaphandler.ldap_add_group_with_parent(groupname = groupname, parentdn = groupparent, description = description)
    return

def add_user_to_group(ldaphandler, uid, groupname):
    done = False
    done = ldaph.ldap_add_user_to_group(uid, groupname)
    return done

def set_user_ldap_dict(participant):
    '''set the user attributes from the old dictionary and add/'override the attributes we really need'''
    
    detailsdict = {}
    participantaccount = participant.participantaccount

    # uncomment these lines if adding the old LDAP details is necessary
    '''
    if participantaccount and participantaccount.old_ldap_details:
        detailsdict = simplejson.loads(participantaccount.old_ldap_details)
    '''

    #print "set_user_ldap_dict type: %s detailsdict BEFORE: %s" % (type(detailsdict), detailsdict)

    detailsdict["givenName"] = [participantaccount.first_name]
    detailsdict["sn"] = [participantaccount.last_name]
    detailsdict["cn"] = [participantaccount.first_name + ' ' + participantaccount.last_name] # required attribute
    detailsdict['telephoneNumber'] = [participantaccount.phone]
    detailsdict['userPassword'] = [participantaccount.password_hash]

    uid =  str(participantaccount.uid)
    detailsdict['uid'] = [uid]
    
    #POSIX STUFF
    detailsdict['uidNumber'] = [participantaccount.uid_number]
    detailsdict['gidNumber'] = [participantaccount.gid_number]
    detailsdict['homeDirectory'] = ['/home/%s' % (uid)]
    #pull out the previous login shell.
    loginshell = '/bin/bash'
    if participantaccount.old_ldap_details is not None:
        try:
            prev_details = simplejson.loads(participantaccount.old_ldap_details)
            loginshell = str(prev_details['loginShell'][0])
        except:
            pass
    detailsdict['loginShell'] = [loginshell]


    # convert the unicode strings in strings for ldap, will be done in ldap_handler in the future
    for attr in detailsdict:
        valuelist = detailsdict[attr] # list of attributes in unicode strings
        #print 'valuelist: %s' % valuelist
        strlist = [str(value) for value in valuelist]
        detailsdict[attr] = strlist

    #print "set_user_ldap_dict type: %s detailsdict AFTER:  %s" % (type(detailsdict), detailsdict)

    return detailsdict

def create_user_account(ldaph, participant, usercontainer, userdn, basedn):
    res = False
    participant_account = participant.participantaccount
    uid = participant_account.uid
    unique_uid = participant_account.get_unique_uid()
    if uid != unique_uid:
        logger.debug("Unwilling to submit non-unique uid (%s) for LDAP account creation - suggest %s" % (uid, unique_uid) )
    else: 
        institution = participant_account.institution.ldap_ou_name
        usercontainer = 'ou=%s,%s' % (institution,usercontainer)
        olddict = {}
       
        detailsdict = set_user_ldap_dict(participant)

        logger.debug( "create_user_account %s uid: %s userdn: %s basedn: %s" % (participant.email, uid, userdn, basedn) )
        # ldap_handler.add_user build the user dn like this:
        # dn = 'uid=%s,%s,%s,%s' % (username, usercontainer, userdn, basedn)
        # real example from ldap browser: uid=hum092,ou=CSIRO,ou=People,dc=ivec,dc=org
        res = ldaph.ldap_add_user(username = uid,
                      detailsDict = detailsdict,
                      pwencoding = None,
                      #objectclasses = ['top', 'inetOrgPerson', 'organizationalPerson', 'person', 'posixAccount'],
                      objectclasses = ['top', 'inetOrgPerson', 'organizationalPerson', 'person', 'posixAccount'],
                      usercontainer = usercontainer,
                      userdn = userdn,
                      basedn = basedn)

    # ldap_add_user returns false if the user was not added
    logger.debug("create_user_account result: %s" % (res,) )
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

def get_user_accounts_details(participant_id_list):
    returnlist = []
    ldaph = ldap_helper.LDAPHandler(userdn     = settings.EPIC_LDAP_USERDN, 
                                 password   = settings.EPIC_LDAP_PASSWORD, 
                                 server     = settings.EPIC_LDAP_SERVER, 
                                 user_base  = settings.EPIC_LDAP_USERBASE, 
                                 group      = None, 
                                 group_base = settings.EPIC_LDAP_GROUPBASE, 
                                 admin_base = settings.EPIC_LDAP_ADMINBASE,
                                 dont_require_cert=True, debug=True)

    usercontainer = settings.EPIC_LDAP_USER_OU
    userdn = settings.EPIC_LDAP_COMPANY
    basedn = settings.EPIC_LDAP_DOMAIN
   
    #so the format we will do is:
    #username, emailaddress, homedir, shell, uidnum, gidnum, institution, groups (space separated)
    returnlist.append("#UID, EMAIL, HOMEDIR, SHELL, UIDNUM, GIDNUM, INSTITUTION, GROUPS")
    for id in participant_id_list:
        p = Participant.objects.get(id=id)
        pa = p.participantaccount
        try:
            ldap_details = ldaph.ldap_get_user_details(pa.uid)
            institution = pa.institution.ldap_ou_name
            groups = ldaph.ldap_get_user_groups(pa.uid)
            groupsstr = " ".join(groups)
            summarystr = "%s,%s,%s,%s,%s,%s,%s,%s" % (pa.uid,p.email,ldap_details['homeDirectory'][0], ldap_details['loginShell'][0], ldap_details['uidNumber'][0], ldap_details['gidNumber'][0], institution, groupsstr)
        except Exception, e:
            summarystr = "Error occurred getting ldap details for uid %s:%s" % (pa.uid, e)
        
        returnlist.append(summarystr)
    

    ldaph.close()
    return returnlist

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
    participant_account.constrain_uidgid() #'fixes' the uidnumber/gidnumber and saves
     
    participant.save()

