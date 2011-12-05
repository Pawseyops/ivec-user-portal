import os

from django.conf.urls.defaults import *

from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin

import admin

from ccg.utils.webhelpers import url as wh_url
from allocation.admin_forms import RecaptchaPasswordResetForm

urlpatterns = patterns('',
    # Example:
    # (r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # accept 'director' url suffix at top level to guide director class
    # users to their own registration page
    url(r'^(?P<usertype>director)', admin.site.admin_view(admin.site.index)),

    # deprecated URLs
    (r'^login[/]$', redirect_to, {'url': wh_url('/')}),
    (r'^admin[/]$', redirect_to, {'url': wh_url('/')}),

    # Uncomment this line to enable the mango status system
    #(r'^project_status', status_view),
    
    # registration
    (r'^accounts/login', redirect_to, {'url': wh_url('/')}),
    (r'^accounts/', include('registration.backends.ivec.urls')),
    
    # forgot password link
    (r'^reset-password[/]$', 'ivecallocation.allocation.views.password_reset'),
)

urlpatterns += patterns('ivecallocation.allocation.views',
    url(r'^priority_areas/(?P<allocationround_id>\d+)/$', 'priority_areas', name='priority-areas'),
    url(r'^summary/$', 'summary', name='summary'),
    url(r'^account-request/(?P<email_hash>[\w\d\-]+)[/]$', 'account_request', name='account-request'),
    url(r'^account-details/thanks[/]$', 'account_details_thanks', name='account-details-thanks'),

)

# put admin at the end to consume everything that doesn't match
urlpatterns += patterns('',
    url(r'^', include(admin.site.urls)),
)


