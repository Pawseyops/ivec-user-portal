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
    uid = participant.participantaccount.uid
    account_details = get_user_account_details(uid)
    project = participant.application.ldap_project_name 
    hours_allocated = participant.application.hours_allocated
    assert project is not None and len(project)>0, "Project could not be retrieved at time of 'account created' email for user %s" % (uid) 
    assert (hours_allocated is not None) and (hours_allocated > 0), "Invalid hours allocated (%s) at time of 'account created' email" % (str(hours_allocated) )
    message = message_template.render(participant=participant, project=project, uid=uid)
    send_mail(subject, message, participant.email)

    participant.status_id = Participant.STATUS['ACCOUNT_CREATED_EMAIL_SENT']
    participant.account_created_email_on = datetime.datetime.now()
    participant.save()

def fetch_old_ldap_details(participant):
    retval = False
    details = None
    try:
        details = get_ivec_ldap_details(participant.email)
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
    #assert 'ccg.murdoch.edu.au' in to, "Can send email just to a ccg.murdoch.edu.au address"    
    django_mail.send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to])

def get_ivec_ldap_details(emailaddress):
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

#TODO: remove when create_user_accounts calls create_application_group
def get_application_area(application):
    areanum = str(application.id)
    parentarea = application.priority_area
    childarea = application.posix_area
    return (parentarea, childarea, areanum)

def create_application_group(ldaphandler, application):
    '''
    Create the group in LDAP for the application. Create the parent area if needed
    return the project name if successful else None
    '''
    groupname = '%s%s' % (application.posix_area, str(application.id))
    gidnumber = str(30010 + application.id)     # TODO: CAUTION: the offset is hard coded here
    description = str(application.project_title)

    groupdone = create_group(ldaphandler = ldaphandler, parentou = application.priority_area, groupname = groupname, description = description, gidnumber = gidnumber)
    if groupdone:
        res = groupname
    else:
        res = None
    return res

def create_applications_groups(applicationidlist):
    '''
    Create the goups in LDAP for the application ids passed in
    returns a dict with the count created and errors.
    '''

    result = {'created': 0, 'errors': 0}
    
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

    for id in applicationidlist:
        app = Application.objects.get(id=id)
        logger.debug("Application: %s" % (app.project_title,) )

        groupname = create_application_group(ldaph, app) # returns groupname or None
        if groupname:
            # save the groupname like 'Astronomy23' in the application
            logger.debug("Application: %s ldap group created: %s" % (app.project_title, groupname) )
            app.ldap_project_name = groupname
            app.save()
            result['created'] += 1
        else: result['errors'] += 1

    ldaph.close()
    return result    

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
            logger.debug("\nParticipant: %s" % (participant.email,) )

            if participant.status_id != Participant.STATUS['DETAILS_FILLED']:   # account not ready yet
                result['errors'] += 1
                continue # next participant

            try:
                participant_account = participant.participantaccount
                email = participant.email

                if participant_account:
                    logger.debug("participant: %s %s email:%s" % (participant_account.first_name, participant_account.last_name, email) )
                    # get the user entry in the new ldap repo if it exists

                    #userdetails = ldaph.get_user_details_from_attribute(attribute = 'mail', value = email)
                    userdetails = ldaph.get_user_details_from_attribute(attribute = 'uid', value = participant_account.uid)
                    logger.debug("user uid: %s details: %s" % (participant_account.uid, userdetails) )
                    done = False

                    if not userdetails:
                        # user entry does not exist in the new ldap, create it
                        #print "creating user in LDAP"
                        userdone = create_user_account(ldaph, participant, usercontainer, userdn, basedn)
                        if userdone:
                            result['created'] += 1
                    else:
                        #print "updating user in LDAP"
                        userdone = update_user_account(ldaph, participant)
                        if userdone:
                            result['updated'] += 1

                    if userdone:
                        # user added or updated to the ldap directory, add the user to the group, create the group if it doesn't exist
                        (parentarea, childarea, areanum) = get_application_area(participant.application)

                        groupname = '%s%s' % (childarea, areanum)
                        gidnumber = str(30010 + participant.application.id)
                        description = str(participant.application.project_title)
                        groupdone = create_group(ldaphandler = ldaph, parentou = parentarea, groupname = groupname, description = description, gidnumber = gidnumber)
                        
                        uid = participant_account.uid
                        #print "Adding user uid: %s to group: %s" % (uid, groupname)
                        # ldap_add_user_to_group(username, groupname, objectclass='groupofuniquenames', membershipattr="uniqueMember"):
                        usergroupdone = ldaph.ldap_add_user_to_group(uid, groupname, objectclass='posixgroup', membershipattr='memberUid')
                        #print "Adding user uid: %s to group: %s RESULT: %s" % (uid, groupname, usergroupdone)

                        # create a posixGroup with cn=uid
                        posixgroupname = participant_account.uid
                        gidnumber = str(participant_account.gid_number)
                        parentou = settings.EPIC_LDAP_POSIXGROUPBASE # 'ou=POSIX,ou=Groups,dc=ivec,dc=org'
                        
                        
                        posixdone = ldaph.ldap_add_group_with_parent(groupname = posixgroupname, parentdn = parentou, objectClasses = ['top','posixGroup'], attributes = [('gidNumber',gidnumber)])

                        # update the user status only if all the steps went through
                        logger.debug( "groupdone %s usergroupdone %s posixdone %s" % (groupdone, usergroupdone, posixdone) )
                        if groupdone and usergroupdone and posixdone:
                            participant.status_id = Participant.STATUS['ACCOUNT_CREATED']
                            participant.account_created_on = datetime.datetime.now()
                            participant.save()

                        # save the groupname like 'Astronomy23' in the application
                        application = participant.application
                        application.ldap_project_name = groupname
                        application.save()

            except ParticipantAccount.DoesNotExist, e:
                logger.debug("ParticipantAccount.DoesNotExist %s error: %s" % (participant_account.uid, e) )
                result['errors'] += 1
        ldaph.close()
    return result

def create_group(ldaphandler, parentou, groupname, description, gidnumber):
    '''
    description, gidnumber must be string (not a unicode string)
    '''
    # create the OU for this group like 'Astronomy'
    oudescription = None
    parentdn = settings.EPIC_LDAP_GROUPBASE
    #print "create_group create_ou: parentou: %s parentdn: %s" % (parentou, parentdn)
    res = ldaphandler.create_ou(name = parentou, parentdn = parentdn) # 'ou=Projects,ou=Groups,%s' % (EPIC_LDAP_BASE)
    # ignore the result, the OU can exist already
    #print "create_group: create_ou res: %s" % res

    # can't create the group if the parent doesn't exist
    # the group name would be like 'Astronomy18' where 18 is the application number
    groupparent = 'ou=%s,%s' % (parentou, settings.EPIC_LDAP_GROUPBASE)
    #print "create_group ldap_add_group_with_parent: groupname: %s parentou: %s, gidnumber: %s" % (groupname, groupparent, gidnumber)
    res = ldaphandler.ldap_add_group_with_parent(groupname = groupname, parentdn = groupparent, description = description,  objectClasses = ['top','posixGroup'], attributes = [('gidNumber',gidnumber)])
    return res

def add_user_to_group(ldaphandler, uid, groupname):
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
    #only want non blank telephone nums
    if participantaccount.phone is not None and len(participantaccount.phone) > 0: 
        detailsdict['telephoneNumber'] = [participantaccount.phone]
    detailsdict['userPassword'] = [participantaccount.password_hash]
    detailsdict['mail'] = [participant.email]

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
    participant_account.constrain_uidgid()
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

    #print "update_user_account %s uid: %s" % (participant.email, uid)

    res = ldaph.ldap_update_user(username = uid,
                             newusername = uid,
                             newpassword = participant_account.password_hash,
                             detailsDict = detailsdict,
                             pwencoding = None)

    # ldap_update_user does not return anything, assume success
    # TODO: change ldap_update_user to return a real result code
    res = True
    return res

def get_user_accounts_CSV(participant_id_list):
    returnlist = []
    #so the format we will do is:
    #username, emailaddress, homedir, shell, uidnum, gidnum, institution, groups (space separated)
    returnlist.append("#UID, EMAIL, HOMEDIR, SHELL, UIDNUM, GIDNUM, INSTITUTION, GROUPS")
    for id in participant_id_list:
        p = Participant.objects.get(id=id)
        pa = p.participantaccount
        try:
            detailsdict = get_user_account_details(pa.uid)
            ldap_details = detailsdict['details']
            groups = detailsdict['groups'] 
            institution = pa.institution.ldap_ou_name
            groupsstr = " ".join(groups)
            summarystr = "%s,%s,%s,%s,%s,%s,%s,%s" % (pa.uid,p.email,ldap_details['homeDirectory'][0], ldap_details['loginShell'][0], ldap_details['uidNumber'][0], ldap_details['gidNumber'][0], institution, groupsstr)
        except Exception, e:
            summarystr = "Error occurred getting ldap details for uid %s:%s" % (pa.uid, e)
        
        returnlist.append(summarystr)
    
    return returnlist

def get_user_account_details(uid):
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

    #try a bunch of stuff to capture all their group info
    ldaph.GROUP_BASE = settings.EPIC_LDAP_GROUPBASE
    ldaph.GROUPOC = 'posixgroup'
    ldap_details = ldaph.ldap_get_user_details(uid)
    groups = ldaph.ldap_get_user_groups(uid, use_udn=False)
    ldaph.MEMBERATTR = 'memberUid'
    groups += ldaph.ldap_get_user_groups(uid, use_udn=False)
    #ldaph.GROUPOC = 'posixgroup'
    ldaph.GROUP_BASE = settings.EPIC_LDAP_POSIXGROUPBASE
    groups += ldaph.ldap_get_user_groups(uid, use_udn=False)


    ldaph.close()
    return {'details': ldap_details, 'groups': groups}

def hash_password(newpassword, pwencoding='md5'):
    return ldap_helper.createpassword(newpassword, pwencoding=pwencoding)

def get_applications_CSV(id_list):
    returnlist = []

    # first line with column names
    returnlist.append("PROJECTNAME,HOURSALLOCATED,PROJECTTITLE")

    for id in id_list:
        app = Application.objects.get(id=id)
        if app.ldap_project_name:
            if not app.hours_allocated:
                app.hours_allocated = 0
            summarystr = '%s,%s,"%s"' % (app.ldap_project_name, app.hours_allocated, app.project_title)
            returnlist.append(summarystr)
    
    return returnlist

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

