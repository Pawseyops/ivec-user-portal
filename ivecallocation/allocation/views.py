import operator
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from django.core import urlresolvers
from django.utils.webhelpers import siteurl
from models import *
from forms import *
from ivecallocation.allocation.utils import get_querylist
from django.db.models import Q
from ivecallocation.allocation import models
from ivecallocation.allocation import account_services

PROCESSED_PARTICIPANT_SESSION_KEY = 'PROCESSED_PARTICIPANT'

@staff_member_required
def summary(request):

    query_list = get_querylist(request=request)
    if query_list:
        apps = Application.objects.filter(reduce(operator.or_,query_list)).filter(complete=True)
    else:
        apps = []

    # Build a dictionary full of application objects keyed on priority_area name
    all_apps = {}
    for a in apps:
        if a.priority_area.name not in all_apps.keys():
            all_apps[a.priority_area.name] = []
        all_apps[a.priority_area.name].append(a)


    # Flag to show/hide the review column based on user permissions
    show_review = False
    reviewer_permissions = ['allocation.add_reviewerscore', 'allocation.add_reviewercomment']
    if all(permission in request.user.get_all_permissions() for permission in reviewer_permissions):
        show_review = True

    return render_to_response('allocation/summary.html', {
#        'tool': tool,
        'user':request.user,
        'title': 'Resource Application Summary',
        'root_path':urlresolvers.reverse('admin:index'),
        'all_apps':all_apps,
        'edit_url': urlresolvers.reverse('admin:allocation_application_change', args=(1,)),
        'urlresolvers':urlresolvers,
        'show_review':show_review,
#        'edit_url': urlresolvers.reverse('admin:yabi_tool_change', args=(tool.id,)),
#        'json_url': webhelpers.url('/ws/tool/' + quote(tool.name)),
#        'tool_params': format_params(tool.toolparameter_set.order_by('id')),
        })

def account_request(request, email_hash):
    try:
        participant = Participant.objects.get(account_email_hash=email_hash)
    except Participant.DoesNotExist:
        return render_to_response('allocation/invalid_hash.html', {})

    had_ldap_details = False
    try:
        participant_account = participant.participantaccount
        had_ldap_details = True
    except ParticipantAccount.DoesNotExist:
        participant_account = ParticipantAccount(participant=participant) 
 
    if request.method == 'POST':
        if had_ldap_details:
            form = ParticipantAccountForm(request.POST)
        else:
            form = ParticipantAccountWithPasswordForm(request.POST)

        if form.is_valid():
            participant_account.first_name = form.cleaned_data.get('first_name')
            participant_account.last_name = form.cleaned_data.get('last_name')
            participant_account.institution_id = form.cleaned_data.get('institution').id
            participant_account.phone = form.cleaned_data.get('phone')
            if not had_ldap_details:
                participant_account.password_hash = account_services.hash_password(form.cleaned_data.get('password1'))
            account_services.save_account_details(participant_account)
            request.session[PROCESSED_PARTICIPANT_SESSION_KEY] = email_hash
            return HttpResponseRedirect(siteurl(request) + 'account-details/thanks')
    else:
  
        if had_ldap_details:
            data_dict = {}
            data_dict['first_name'] = participant_account.first_name
            data_dict['last_name'] = participant_account.last_name
            data_dict['phone'] = participant_account.phone
            #data_dict['institution'] = participant_account.institution.id
            
            form = ParticipantAccountForm(data=data_dict)
        else:
            form = ParticipantAccountWithPasswordForm()

    return render_to_response('allocation/account_request.html', {
        'form': form, 'participant_email': participant.email
    })


def account_details_thanks(request):
    participant_email_hash = None
    try:
        participant_email_hash = request.session.get(PROCESSED_PARTICIPANT_SESSION_KEY,None)
    except:
        pass
    
    #now remove the session key if it existed
    if participant_email_hash is not None:
        del request.session[PROCESSED_PARTICIPANT_SESSION_KEY]
    
    participantdetails = None
    error = None
    if participant_email_hash is None:
        error = "Unable to retrieve participant by hash: no hash provided."
    else:
        try:
            participant = Participant.objects.get(account_email_hash = participant_email_hash)
            #erase the email hash - we don't need it anymore
            participant.account_email_hash = None
            participant.save()
            
            ppt_account = participant.participantaccount
            participantdetails = []
            participantdetails.append( ("First Name", ppt_account.first_name) )
            participantdetails.append( ("Last Name", ppt_account.last_name) )
            participantdetails.append( ("Email", participant.email) )
            participantdetails.append( ("Phone Number", ppt_account.phone) )
            participantdetails.append( ("Username (pending)", ppt_account.uid) )
            participantdetails.append( ("Institution", ppt_account.institution.display_name) )

        except Participant.DoesNotExist:
            error = "Unable to retrieve participant by hash: %s" % (str(participant_email_hash))
    return render_to_response('allocation/account_details_thanks.html', {"participantdetails": participantdetails, "error":error})

