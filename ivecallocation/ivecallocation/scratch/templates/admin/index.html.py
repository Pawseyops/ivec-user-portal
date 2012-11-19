# -*- encoding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1349852755.0050721
_enable_loop = True
_template_filename = u'/usr/local/webapps/ivecallocation/virtualenv/lib/python2.6/site-packages/Mango_py-1.3.1_ccg1_3-py2.6.egg/django/contrib/admin/templates/mako/admin/index.html'
_template_uri = u'admin/index.html'
_source_encoding = 'ascii'
_exports = ['block_breadcrumbs', 'block_stylesheet', 'block_content', 'block_coltype', 'block_bodyclass', 'block_sidebar']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 4
    ns = runtime.ModuleNamespace(u'admin', context._clean_inheritance_tokens(), callables=None, calling_uri=_template_uri, module=u'django.contrib.admin.templatetags.adminmedia')
    context.namespaces[(__name__, u'admin')] = ns

def _mako_inherit(template, context):
    _mako_generate_namespaces(context)
    return runtime._inherit_from(context, u'admin/base_site.html', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n\n')
        # SOURCE LINE 4
        __M_writer(unicode(self.block_stylesheet()))
        __M_writer(u'\n\n')
        # SOURCE LINE 6
        __M_writer(unicode(self.block_coltype()))
        __M_writer(u'\n\n')
        # SOURCE LINE 8
        __M_writer(unicode(self.block_bodyclass()))
        __M_writer(u'\n\n')
        # SOURCE LINE 10
        __M_writer(unicode(self.block_breadcrumbs()))
        __M_writer(u'\n\n')
        # SOURCE LINE 12
        __M_writer(unicode(self.block_content()))
        # SOURCE LINE 45
        __M_writer(u'\n\n')
        # SOURCE LINE 47
        __M_writer(unicode(self.block_sidebar()))
        # SOURCE LINE 95
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_breadcrumbs(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_stylesheet(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        admin_media_prefix = context.get('admin_media_prefix', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 4
        __M_writer(unicode(admin_media_prefix()))
        __M_writer(u'css/dashboard.css')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_content(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        trans = context.get('trans', UNDEFINED)
        app_list = context.get('app_list', UNDEFINED)
        def blocktrans():
            __M_caller = context.caller_stack._push_frame()
            try:
                __M_writer = context.writer()
                # SOURCE LINE 18
                name = app['name'] 
                
                __M_writer(unicode(name))
                return ''
            finally:
                context.caller_stack._pop_frame()
        __M_writer = context.writer()
        # SOURCE LINE 12
        __M_writer(u'\n<div id="content-main">\n')
        # SOURCE LINE 14
        if app_list:
            # SOURCE LINE 15
            for app in app_list:
                # SOURCE LINE 16
                __M_writer(u'        <div class="module">\n        <table summary="')
                # SOURCE LINE 17
                __M_writer(unicode(blocktrans()))
                __M_writer(u'">\n        <caption><a href="')
                # SOURCE LINE 18
                __M_writer(unicode(app['app_url']))
                __M_writer(u'" class="section">')
                __M_writer(unicode(blocktrans()))
                __M_writer(u'</a></caption>\n')
                # SOURCE LINE 19
                for model in app['models']:
                    # SOURCE LINE 20
                    __M_writer(u'            <tr>\n')
                    # SOURCE LINE 21
                    if model['perms']['change']:
                        # SOURCE LINE 22
                        __M_writer(u'                <th scope="row"><a href="')
                        __M_writer(unicode(model['admin_url']))
                        __M_writer(u'">')
                        __M_writer(unicode(model['name']))
                        __M_writer(u'</a></th>\n')
                        # SOURCE LINE 23
                    else:
                        # SOURCE LINE 24
                        __M_writer(u'                <th scope="row">')
                        __M_writer(unicode(model['name']))
                        __M_writer(u'</th>\n')
                    # SOURCE LINE 26
                    if model['perms']['add']:
                        # SOURCE LINE 27
                        __M_writer(u'                <td><a href="')
                        __M_writer(unicode(model['admin_url']))
                        __M_writer(u'add/" class="addlink">')
                        __M_writer(unicode(trans('Add')))
                        __M_writer(u'</a></td>\n')
                        # SOURCE LINE 28
                    else:
                        # SOURCE LINE 29
                        __M_writer(u'                <td>&nbsp;</td>\n')
                    # SOURCE LINE 31
                    if model['perms']['change']:
                        # SOURCE LINE 32
                        __M_writer(u'                <td><a href="')
                        __M_writer(unicode(model['admin_url']))
                        __M_writer(u'" class="changelink">')
                        __M_writer(unicode(trans('Change')))
                        __M_writer(u'</a></td>\n')
                        # SOURCE LINE 33
                    else:
                        # SOURCE LINE 34
                        __M_writer(u'                <td>&nbsp;</td>\n')
                    # SOURCE LINE 36
                    __M_writer(u'            </tr>\n')
                # SOURCE LINE 38
                __M_writer(u'        </table>\n        </div>\n')
            # SOURCE LINE 41
        else:
            # SOURCE LINE 42
            __M_writer(u'    <p>')
            __M_writer(unicode(trans("You don't have permission to edit anything.")))
            __M_writer(u'</p>\n')
        # SOURCE LINE 44
        __M_writer(u'</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_coltype(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 6
        __M_writer(u'colMS')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_bodyclass(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        # SOURCE LINE 8
        __M_writer(u'dashboard')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_sidebar(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        admin_log = context.get('admin_log', UNDEFINED)
        capfirst = context.get('capfirst', UNDEFINED)
        user = context.get('user', UNDEFINED)
        get_admin_log = context.get('get_admin_log', UNDEFINED)
        escape = context.get('escape', UNDEFINED)
        trans = context.get('trans', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 47
        __M_writer(u'\n<div id="content-related">\n    <div class="module" id="recent-actions-module">\n        <h2>')
        # SOURCE LINE 50
        __M_writer(unicode(trans('Recent Actions')))
        __M_writer(u'</h2>\n        <h3>')
        # SOURCE LINE 51
        __M_writer(unicode(trans('My Actions')))
        __M_writer(u'</h3>\n            \n            ')
        # SOURCE LINE 53
        get_admin_log(10, 'admin_log', user) 
        
        __M_writer(u'\n            \n')
        # SOURCE LINE 55
        if not admin_log:
            # SOURCE LINE 56
            __M_writer(u'\n            <p>')
            # SOURCE LINE 57
            __M_writer(unicode(trans('None available')))
            __M_writer(u'</p>\n            \n')
            # SOURCE LINE 59
        else:
            # SOURCE LINE 60
            __M_writer(u'\n            <ul class="actionlist">\n            \n')
            # SOURCE LINE 63
            for entry in admin_log:
                # SOURCE LINE 64
                __M_writer(u'\n            <li class="\n')
                # SOURCE LINE 66
                if entry.is_addition():
                    # SOURCE LINE 67
                    __M_writer(u'addlink\n')
                # SOURCE LINE 69
                __M_writer(u'\n')
                # SOURCE LINE 70
                if entry.is_change():
                    # SOURCE LINE 71
                    __M_writer(u'changelink\n')
                # SOURCE LINE 73
                __M_writer(u'\n')
                # SOURCE LINE 74
                if entry.is_deletion():
                    # SOURCE LINE 75
                    __M_writer(u'deletelink\n')
                # SOURCE LINE 77
                __M_writer(u'">\n')
                # SOURCE LINE 78
                if not entry.is_deletion() and entry.content_type:
                    # SOURCE LINE 79
                    __M_writer(u'<a href="')
                    __M_writer(unicode(entry.get_admin_url()))
                    __M_writer(u'">\n')
                # SOURCE LINE 81
                __M_writer(escape(unicode(entry.object_repr)))
                __M_writer(u'\n')
                # SOURCE LINE 82
                if not entry.is_deletion() and entry.content_type:
                    # SOURCE LINE 83
                    __M_writer(u'</a>\n')
                # SOURCE LINE 85
                __M_writer(u'<br /><span class="mini quiet">')
                __M_writer(unicode(capfirst(trans(entry.content_type))))
                __M_writer(u'</span></li>\n            \n')
            # SOURCE LINE 88
            __M_writer(u'\n            </ul>\n            \n')
        # SOURCE LINE 92
        __M_writer(u'\n    </div>\n</div>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


