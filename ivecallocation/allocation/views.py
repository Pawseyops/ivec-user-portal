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
    apps = Application.objects.filter(reduce(operator.or_,query_list)).filter(complete=True)

    all_apps = {
        'radio astronomy':[],
        'geosciences':[],
        'directors':[],
        'partner':[],
        'national':[],
        'other':[]        
        }


    for a in apps:

        has_priority = False
        if a.priority_area_radio_astronomy:
            all_apps['radio astronomy'].append(a)
            has_priority = True
        if a.priority_area_geosciences:
            all_apps['geosciences'].append(a)
            has_priority = True            
        if a.priority_area_directors:
            all_apps['directors'].append(a)
            has_priority = True            
        if a.priority_area_partner:
            all_apps['partner'].append(a)
            has_priority = True            
        if a.priority_area_national:
            all_apps['national'].append(a)
            has_priority = True            
        if not has_priority:
            all_apps['other'].append(a)


    return render_to_response('allocation/summary.html', {
#        'tool': tool,
        'user':request.user,
        'title': 'Resource Application Summary',
        'root_path':urlresolvers.reverse('admin:index'),
        'all_apps':all_apps,
        'display_order':['radio astronomy', 'geosciences', 'directors', 'partner', 'national', 'other'],
        'edit_url': urlresolvers.reverse('admin:allocation_application_change', args=(1,)),
        'urlresolvers':urlresolvers,
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
            request.session[PROCESSED_PARTICIPANT_SESSION_KEY] = participant.email
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
    p_email = request.session(PROCESSED_PARTICIPANT_SESSION_KEY,None)
    
    return render_to_response('allocation/account_details_thanks.html', {})

