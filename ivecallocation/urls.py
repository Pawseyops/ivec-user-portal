import os

from django.conf.urls.defaults import *
from django.contrib import admin

from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
admin.autodiscover()

from django.utils.webhelpers import url

urlpatterns = patterns('',
    # Example:
    # (r'^{{ project_name }}/', include('{{ project_name }}.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
        
    # Uncomment this line to enable the mango status system
    #(r'^project_status', status_view),
    
    # registration
    (r'^accounts/', include('registration.backends.ivec.urls')),
    
    (r'^$', redirect_to, {'url': url('/accounts/register/')}),
    (r'^login[/]$', redirect_to, {'url': url('/admin/')}),
    
)



urlpatterns += patterns('',
        (r'^static/(?P<path>.*)$',
        'django.views.static.serve',
        {'document_root': os.path.join(os.path.dirname(__file__),"static"), 'show_indexes': True}),
)

