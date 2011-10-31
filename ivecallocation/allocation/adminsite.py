from django.contrib.admin import AdminSite
from django.contrib.admin.forms import AdminAuthenticationForm
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy, ugettext as _
from django.conf import settings
from django.contrib.auth import authenticate, login
from django import http
from django.utils.webhelpers import url
from django.contrib.auth import REDIRECT_FIELD_NAME

from allocation.models import Application

ERROR_MESSAGE = ugettext_lazy("Please enter a correct username and password. Note that both fields are case-sensitive.")

class IvecAdminSite(AdminSite):
    
    @never_cache
    def login2(self, request, extra_context=None):
        """
        Displays the login form for the given HttpRequest.
        """
        from django.contrib.auth.views import login
        context = {
            'title': _('Log in'),
            'root_path': self.root_path,
            'app_path': request.get_full_path(),
            REDIRECT_FIELD_NAME: request.get_full_path(),
        }
        context.update(extra_context or {})
        defaults = {
            'extra_context': context,
            'current_app': self.name,
            'authentication_form': self.login_form or AdminAuthenticationForm,
            'template_name': self.login_template or 'admin/login.html',
        }
        return self.login(request, **defaults)
    
    @never_cache
    def login(self, request, **kwargs):
        # """
        # Displays the login form for the given HttpRequest.
        # """
        from django.contrib.auth.models import User, Group

        response = super(IvecAdminSite, self).login(request)
        
        if request.user and request.user.is_active and request.user.is_staff:
            # if applications are open we redirect to application page
            # otherwise main admin site
            if settings.APPLICATIONS_OPEN:
                unprivileged = Group.objects.get(name='unprivileged')

                # is user in group 'unprivileged'?
                if unprivileged in user.groups.all():
                    # yes. Does this user have an application form
                    try:
                        users_app_count = Application.objects.filter(created_by=user).count()
                        if users_app_count:
                            # goto changelist
                            return http.HttpResponseRedirect(url("/admin/allocation/application/"))
                        else:
                            # go to add application form
                            return http.HttpResponseRedirect(url("/admin/allocation/application/add/"))
                    except Application.DoesNotExist:
                        return http.HttpResponseRedirect(url("/admin/allocation/application/add/"))
                else:
                    # standard login location
                    return http.HttpResponseRedirect(request.get_full_path())
            else:
                return http.HttpResponseRedirect(request.get_full_path())
        else:
            return response
                                

##
## Our Site instance
##
site = IvecAdminSite()
