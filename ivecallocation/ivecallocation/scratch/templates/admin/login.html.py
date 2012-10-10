# -*- encoding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1349852317.280674
_enable_loop = True
_template_filename = u'/usr/local/src/ivecallocation/ivecallocation/allocation/templates/mako/admin/login.html'
_template_uri = 'admin/login.html'
_source_encoding = 'ascii'
_exports = ['block_content', 'title']


# SOURCE LINE 2
from ccg.utils.webhelpers import url 

# SOURCE LINE 3
from django.core.urlresolvers import reverse 

def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    pass
def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'registration/base.html', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n')
        # SOURCE LINE 3
        __M_writer(u'\n\n\n\n')
        # SOURCE LINE 13
        __M_writer(u'\n\n')
        # SOURCE LINE 15
        __M_writer(unicode(self.block_content()))
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_content(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        csrf_token = context.get('csrf_token', UNDEFINED)
        trans = context.get('trans', UNDEFINED)
        form = context.get('form', UNDEFINED)
        csrf_tag = context.get('csrf_tag', UNDEFINED)
        usertype = context.get('usertype', UNDEFINED)
        allocation_rounds = context.get('allocation_rounds', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 15
        __M_writer(u"\n\n<h3>Allocation Rounds</h3>\n<p>\nYou can register at any time. Once registered, applications are only available during\nopen allocation rounds. Open and recently closed rounds are listed below.\n</p>\n<p><font color=red>Applications are only accepted between the opening and closing dates below. Allocations are for the entire 2012 calendar year.</font></p>\n\n<table id='rounds' width=100%>\n<tr><th>Resource</th><th>Round Name</th><th>Opens</th><th>Closes</th><th>Status</th></tr>\n")
        # SOURCE LINE 26
        for round in allocation_rounds:
            # SOURCE LINE 27
            __M_writer(u'    ')
            closed = 'class="closed"' if round.status=='closed' else ''
            
            __M_writer(u'\n    <tr ')
            # SOURCE LINE 28
            __M_writer(unicode(closed))
            __M_writer(u'>\n        <td>')
            # SOURCE LINE 29
            __M_writer(unicode(round.system))
            __M_writer(u'</td>\n        <td>')
            # SOURCE LINE 30
            __M_writer(unicode(round.name))
            __M_writer(u'</td>\n        <td>')
            # SOURCE LINE 31
            __M_writer(unicode(round.start_date.strftime('%d %b %Y')))
            __M_writer(u'</td>\n        <td>')
            # SOURCE LINE 32
            __M_writer(unicode(round.end_date.strftime('%d %b %Y')))
            __M_writer(u'</td>\n        <td>')
            # SOURCE LINE 33
            __M_writer(unicode(round.status))
            __M_writer(u'</td>\n    </tr>\n')
        # SOURCE LINE 36
        __M_writer(u'</table>\n<br>\n\n\n\n<form action="')
        # SOURCE LINE 41
        __M_writer(unicode( reverse('admin:index') ))
        __M_writer(u'" method="post" class="login" id="login-form">')
        __M_writer(unicode( csrf_tag(csrf_token) ))
        __M_writer(u'\n\n')
        # SOURCE LINE 43
        if form.errors and '__all__' in form.errors:
            # SOURCE LINE 44
            for error in form.errors['__all__']:
                # SOURCE LINE 45
                __M_writer(u'\n<p class="errornote">\n    ')
                # SOURCE LINE 47
                __M_writer(unicode(error))
                __M_writer(u'\n</p>\n')
        # SOURCE LINE 51
        __M_writer(u'\nLog into iVEC Allocations here:\n<p><font color=red>This is not your iVEC login. It is your login for the allocations system only.</font></p>\n\n  <div class="form-row">\n    <label for="id_username">')
        # SOURCE LINE 56
        __M_writer(unicode(trans('Email:')))
        __M_writer(u'</label> <input type="text" name="username" id="id_username" />\n  </div>\n  <div class="form-row">\n    <label for="id_password">')
        # SOURCE LINE 59
        __M_writer(unicode(trans('Password:')))
        __M_writer(u'</label> <input type="password" name="password" id="id_password" />\n    <input type="hidden" name="this_is_the_login_form" value="1" />\n  </div>\n  <div class="submit-row">\n    <label>&nbsp;</label><input type="submit" value="')
        # SOURCE LINE 63
        __M_writer(unicode(trans('Log in')))
        __M_writer(u'" />\n  </div>\n  \n  No login?\n  <a href="')
        # SOURCE LINE 67
        __M_writer(unicode( reverse('registration.views.register') ))
        __M_writer(unicode(usertype))
        __M_writer(u'">Click here to register.</a><BR>\n  <a href="')
        # SOURCE LINE 68
        __M_writer(unicode( reverse('ivecallocation.allocation.views.password_reset') ))
        __M_writer(u'">Forgot password?</a>\n  \n</form>\n\n<script type="text/javascript">\ndocument.getElementById(\'id_username\').focus()\n</script>\n\n\n<p>\n')
        # SOURCE LINE 78
        if usertype=='director':
            # SOURCE LINE 79
            __M_writer(u'    Applicants are invited to access Directors\' Share of Pawsey-funded iVEC      \n    infrastructure. Contained within this web site is the process for\n    application. If you require any assistance completing this application,\n    please contact <a href="mailto:help@ivec.org">help@ivec.org</a>.\n')
            # SOURCE LINE 83
        else:
            # SOURCE LINE 84
            __M_writer(u'    Applicants are invited to access Pawsey-funded iVEC infrastructure.\n    Contained within this web site is the process for application. If you\n    require any assistance completing this application, please contact\n    <a href="mailto:help@ivec.org">help@ivec.org</a>.\n')
        # SOURCE LINE 89
        __M_writer(u'</p>\n\n<h3>Background</h3>\n\n\n<p>\n    The Pawsey project is an $80 million Commonwealth Super Science funded\n    infrastructure project to put a petascale supercomputing system in Perth\n    that will be managed by iVEC, and operated through funds from the Western\n    Australian State Government and the iVEC Partners. The allocation of time\n    on this Pawsey-funded infrastructure is determined through mechanisms\n    agreed by iVEC and the Commonwealth.\n</p>\n\n<p>\n    The agreed allocations are:\n\n    <ul>\n        <li>25% Radio Astronomy</li>\n        <li>25% Geosciences</li>\n        <li>30% iVEC Partners</li>\n        <li>15% National Merit Allocation Scheme</li>\n        <li>5% Director\'s Discretionary Allocation</li>\n    </ul> \n</p>\n\n<p>\n    These allocations may change in future years. Half of the machine has been\n    initially allocated to radio astronomy and the geosciences, both of which\n    are priority areas for the State and Commonwealth governments. The radio\n    astronomy share is predominantly for the operational requirements of\n    facilities like ASKAP, MWA, and DIRP. The Partner share is available only\n    to researchers from any of the iVEC Partners (i.e. CSIRO and the four WA\n    public universities), whereas the National Merit Allocation Scheme will be\n    available to researchers Australia-wide. Finally, the Director\'s share is\n    to support pilot or startup projects, code scaling work, urgent computing\n    requirements and large-scale data intensive visualisation.\n</p>\n\n<p>\nThis form is to be used to apply for time in 2012 for the Radio Astronomy, Geosciences and iVEC Partner share. Please note that time is awarded to projects, which may have many users.\n</p>\n\n<h3>Infrastructure</h3>\n\n<p>\nCompute resources in this second round of time allocation are available on epic.ivec.org, a 85 TF system comprised of 9,600 cores with 500 terabytes of high-performance storage housed at iVEC@Murdoch. The GPU based fornax.ivec.org will not be in production mode until the second quarter of 2012 and will be the subject of a separate allocation round.\n</p>\n\n<h3>Who should complete this application?</h3>\n\n<p>\n    Note that time is allocated to projects - these can have many team members.\n    Thus, applications are submitted by Project Leaders on behalf of the\n    project team. Members of a project team are not require to complete an \n    application, however they must still agree to the iVEC conditions of\n    use at <a href="http://www.ivec.org/services/apply-account/condition-use">http://www.ivec.org/services/apply-account/condition-use</a>. Typically\n    Project Leaders will be research leaders within a scientific research\n    group, laboratory, or community.\n</p>\n\n<p>\n    The Project Leader is responsible for\n    <ul>\n        <li>Completing the application contained within this web site</li>\n        <li>Being the primary point of contact between the project team members and iVEC</li>\n        <li>Completing the project reports within 30 days at the end of the granting period</li>\n        <li>Submitting requests to add/remove users to existing projects</li>\n        <li>Management of data storage and sharing during and after the project</li>\n    </ul>\n</p>\n\n<p>\nThe applications will be evaluated by a mixture of science and supercomputing experts, so please target your application to an audience with a generic scientific background. Do not assume they have deep knowledge of your application area. Please don\'t hesitate to contact help@ivec.org if you have any questions regarding this form.\n</p>\n\n<p>\n    Please note that iVEC will manage the allocation on a best effort basis but\n    cannot guarantee that approved projects will receive their full allocations\n    and that unused allocations will not roll over to the next allocation\n    period.\n</p>\n\n\n<br/>\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_title(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        usertype = context.get('usertype', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 7
        __M_writer(u'\n')
        # SOURCE LINE 8
        if usertype=='director':
            # SOURCE LINE 9
            __M_writer(u"Application for Directors' Share Resources on Pawsey-Funded iVEC Infrastructure\n")
            # SOURCE LINE 10
        else:
            # SOURCE LINE 11
            __M_writer(u'Application for Resources on Pawsey-Funded iVEC Infrastructure\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


