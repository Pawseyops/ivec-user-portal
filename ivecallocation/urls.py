import os

from django.conf.urls.defaults import *

from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin

import admin

from django.utils.webhelpers import url as wh_url
from django.contrib.auth.forms import PasswordResetForm

urlpatterns = patterns('',
    # Example:
    # (r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^', include(admin.site.urls)),
    url(r'^(?P<usertype>director)/', include(admin.site.urls), name='directors'),
    
        
    # Uncomment this line to enable the mango status system
    #(r'^project_status', status_view),
    
    # registration
    (r'^accounts/login', redirect_to, {'url': wh_url('/')}),
    (r'^accounts/', include('registration.backends.ivec.urls')),
    
    #(r'^$', redirect_to, {'url': wh_url('/accounts/register/')}),
    (r'^login[/]$', redirect_to, {'url': wh_url('/')}),
    (r'^admin[/]$', redirect_to, {'url': wh_url('/')}),

    (r'^reset-password[/]$', 'django.contrib.auth.views.password_reset', {'password_reset_form': PasswordResetForm}),
)

urlpatterns += patterns('ivecallocation.allocation.views',
    url(r'^priority_areas/(?P<allocationround_id>\d+)/$', 'priority_areas', name='priority-areas'),
    url(r'^summary/$', 'summary', name='summary'),
    url(r'^account-request/(?P<email_hash>[\w\d\-]+)[/]$', 'account_request', name='account-request'),
    url(r'^account-details/thanks[/]$', 'account_details_thanks', name='account-details-thanks'),
)

urlpatterns += patterns('',
    (r'^static/(?P<path>.*)$',
    'django.views.static.serve',
    {'document_root': os.path.join(os.path.dirname(__file__),"static"), 'show_indexes': True}),
)

