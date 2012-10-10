# -*- encoding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1349852755.0201681
_enable_loop = True
_template_filename = u'/usr/local/src/ivecallocation/ivecallocation/allocation/templates/mako/admin/base_site.html'
_template_uri = u'admin/base_site.html'
_source_encoding = 'ascii'
_exports = ['block_nav_global', 'block_branding', 'block_title']


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
    return runtime._inherit_from(context, u'admin/base.html', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n\n')
        # SOURCE LINE 4
        __M_writer(unicode(self.block_title()))
        __M_writer(u'\n\n')
        # SOURCE LINE 6
        __M_writer(unicode(self.block_branding()))
        # SOURCE LINE 8
        __M_writer(u'\n\n')
        # SOURCE LINE 10
        __M_writer(unicode(self.block_nav_global()))
        __M_writer(u'\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_nav_global(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_writer = context.writer()
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_branding(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        trans = context.get('trans', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 6
        __M_writer(u'\n<h1 id="site-name">')
        # SOURCE LINE 7
        __M_writer(unicode(trans('iVEC Allocations')))
        __M_writer(u'</h1>\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_title(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        trans = context.get('trans', UNDEFINED)
        title = context.get('title', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 4
        __M_writer(unicode(title))
        __M_writer(u' | ')
        __M_writer(unicode(trans('iVEC Allocations')))
        return ''
    finally:
        context.caller_stack._pop_frame()


