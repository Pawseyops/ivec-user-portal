from django.contrib.admin.sites import AdminSite, LOGIN_FORM_KEY
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy, ugettext as _
from django.conf import settings
from django.contrib.auth import authenticate, login
from django import http
from django.utils.webhelpers import url

from allocation.models import Application

ERROR_MESSAGE = ugettext_lazy("Please enter a correct username and password. Note that both fields are case-sensitive.")

class IvecAdminSite(AdminSite):
    def login(self, request):
        """
        Displays the login form for the given HttpRequest.
        """
        from django.contrib.auth.models import User, Group

        # If this isn't already the login page, display it.
        if not request.POST.has_key(LOGIN_FORM_KEY):
            if request.POST:
                message = _("Please log in again, because your session has expired.")
            else:
                message = ""
            return self.display_login_form(request, message)

        # Check that the user accepts cookies.
        if not request.session.test_cookie_worked():
            message = _("Looks like your browser isn't configured to accept cookies. Please enable cookies, reload this page, and try again.")
            return self.display_login_form(request, message)
        else:
            request.session.delete_test_cookie()

        # Check the password.
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        user = authenticate(username=username, password=password)
        if user is None:
            return self.display_login_form(request, ERROR_MESSAGE)

        # The user data is correct; log in the user in and continue.
        else:
            if user.is_active and user.is_staff:
                login(request, user)

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
                return self.display_login_form(request, ERROR_MESSAGE)
    login = never_cache(login)

##
## Our Site instance
##
site = IvecAdminSite()
