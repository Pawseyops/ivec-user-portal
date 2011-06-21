from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from django.core import urlresolvers
from models import *

@staff_member_required
def summary(request):


    apps = Application.objects.all()

    all_apps = {
        'radio astronomy':[],
        'geosciences':[],
        'directors':[],
        'partner':[],
        'national':[]
        }


    for a in apps:

        if a.priority_area_radio_astronomy:
            all_apps['radio astronomy'].append(a)
        if a.priority_area_geosciences:
            all_apps['geosciences'].append(a)
        if a.priority_area_directors:
            all_apps['directors'].append(a)
        if a.priority_area_partner:
            all_apps['partner'].append(a)
        if a.priority_area_national:
            all_apps['national'].append(a)



    return render_to_response('allocation/summary.html', {
#        'tool': tool,
        'user':request.user,
        'title': 'Resource Application Summary',
        'root_path':urlresolvers.reverse('admin:index'),
        'all_apps':all_apps,
        'edit_url': urlresolvers.reverse('admin:allocation_application_change', args=(1,)),
        'urlresolvers':urlresolvers,
#        'edit_url': urlresolvers.reverse('admin:yabi_tool_change', args=(tool.id,)),
#        'json_url': webhelpers.url('/ws/tool/' + quote(tool.name)),
#        'tool_params': format_params(tool.toolparameter_set.order_by('id')),
        })
