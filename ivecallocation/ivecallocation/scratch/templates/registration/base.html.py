# -*- encoding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1349852317.2948611
_enable_loop = True
_template_filename = u'/usr/local/src/ivecallocation/ivecallocation/allocation/templates/mako/registration/base.html'
_template_uri = u'registration/base.html'
_source_encoding = 'ascii'
_exports = ['head']


def _mako_get_namespace(context, name):
    try:
        return context.namespaces[(__name__, name)]
    except KeyError:
        _mako_generate_namespaces(context)
        return context.namespaces[(__name__, name)]
def _mako_generate_namespaces(context):
    # SOURCE LINE 2
    ns = runtime.ModuleNamespace(u'admin', context._clean_inheritance_tokens(), callables=None, calling_uri=_template_uri, module=u'django.contrib.admin.templatetags.adminmedia')
    context.namespaces[(__name__, u'admin')] = ns

def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        admin_media_prefix = context.get('admin_media_prefix', UNDEFINED)
        next = context.get('next', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        from ccg.utils.webhelpers import url 
        
        __M_locals_builtin_stored = __M_locals_builtin()
        __M_locals.update(__M_dict_builtin([(__M_key, __M_locals_builtin_stored[__M_key]) for __M_key in ['url'] if __M_key in __M_locals_builtin_stored]))
        __M_writer(u'\n')
        # SOURCE LINE 2
        __M_writer(u'\n<!DOCTYPE HTML>\n<html lang="en-AU">\n    <head>\n        <meta charset="UTF-8">\n        <title>')
        # SOURCE LINE 7
        __M_writer(unicode(self.title()))
        __M_writer(u'</title>\n\n        <link type="text/css" rel="stylesheet" media="all" href="')
        # SOURCE LINE 9
        __M_writer(unicode(url('/static/css/html5reset-1.6.1.css')))
        __M_writer(u'">\n        <link type="text/css" rel="stylesheet" media="all" href="')
        # SOURCE LINE 10
        __M_writer(unicode(url('/static/css/ivec.css')))
        __M_writer(u'">\n        <link type="text/css" rel="stylesheet" media="all" href="')
        # SOURCE LINE 11
        __M_writer(unicode(admin_media_prefix()))
        __M_writer(u'css/login.css">\n\n        <!--[if lt IE 9]>\n        <script type="text/javascript" src="')
        # SOURCE LINE 14
        __M_writer(unicode(url('/static/js/html5.js')))
        __M_writer(u'"></script>\n        <![endif]-->\n\n        ')
        # SOURCE LINE 17
        __M_writer(unicode(self.head()))
        __M_writer(u'\n    </head>\n    <body>\n        <header>\n            <h1>')
        # SOURCE LINE 21
        __M_writer(unicode(self.title()))
        __M_writer(u'</h1>\n        </header>\n\n        <section id="content">\n            ')
        # SOURCE LINE 25
        __M_writer(unicode(next.body()))
        __M_writer(u'\n        <div id=footer>\n        <p>\n        Developed for iVEC by the Centre for Comparative Genomics, Murdoch University.\n        </p>\n        </div>\n        </section>\n\n    </body>\n</html>\n\n')
        # SOURCE LINE 37
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_head(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


