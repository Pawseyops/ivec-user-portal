from django.contrib.admin import AdminSite
from django.contrib.admin.forms import AdminAuthenticationForm
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy, ugettext as _
from django.conf import settings
from django.contrib.auth import authenticate, login
from django import http
from django.utils.webhelpers import url
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.decorators.csrf import csrf_protect
from django.utils.functional import update_wrapper

from allocation.models import Application

ERROR_MESSAGE = ugettext_lazy("Please enter a correct username and password. Note that both fields are case-sensitive.")

class IvecAdminSite(AdminSite):
    
    def index(self, request, **kwargs):
        res = super(IvecAdminSite, self).index(request)
        return res
    
    def admin_view(self, view, cacheable=False):
        """
        Override to pass kwargs to self.login so we can pass in URL variables
        """
        def inner(request, *args, **kwargs):
            if not self.has_permission(request):
                return self.login(request, *args, **kwargs)
            return view(request, *args, **kwargs)
        if not cacheable:
            inner = never_cache(inner)
        # We add csrf_protect here so this function can be used as a utility
        # function for any view, without having to repeat 'csrf_protect'.
        if not getattr(view, 'csrf_exempt', False):
            inner = csrf_protect(inner)
        return update_wrapper(inner, view)
    
    @never_cache
    def login(self, request, usertype=None, **kwargs):
        # """
        # Displays the login form for the given HttpRequest.
        # """
        from django.contrib.auth.models import User, Group

        # Provide some extra variables for the admin login template
        # Show a list of all the open and recently closed allocation rounds
        from datetime import datetime, timedelta
        from ivecallocation.allocation.models import AllocationRound
        from django.db.models import Q
        from operator import attrgetter
        today = datetime.today()
        delta = timedelta(182)
        allocation_rounds = AllocationRound.objects.filter(
            Q(start_date__lte=today,end_date__gte=today) | Q(end_date__gte=(today - delta)))
        allocation_rounds = sorted(allocation_rounds, key=attrgetter('end_date'), reverse=True)

        extra_context = {'allocation_rounds': allocation_rounds,
                         'usertype': usertype or ''}

        response = super(IvecAdminSite, self).login(request, extra_context)
        
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
