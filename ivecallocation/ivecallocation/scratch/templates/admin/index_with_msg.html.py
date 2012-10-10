# -*- encoding:ascii -*-
from mako import runtime, filters, cache
UNDEFINED = runtime.UNDEFINED
__M_dict_builtin = dict
__M_locals_builtin = locals
_magic_number = 8
_modified_time = 1349852754.986464
_enable_loop = True
_template_filename = u'/usr/local/src/ivecallocation/ivecallocation/allocation/templates/mako/admin/index_with_msg.html'
_template_uri = 'admin/index_with_msg.html'
_source_encoding = 'ascii'
_exports = ['block_content', 'block_title']


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
    return runtime._inherit_from(context, u'admin/index.html', _template_uri)
def render_body(context,**pageargs):
    __M_caller = context.caller_stack._push_frame()
    try:
        __M_locals = __M_dict_builtin(pageargs=pageargs)
        self = context.get('self', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 1
        __M_writer(u'\n\n')
        # SOURCE LINE 3
        __M_writer(unicode(self.block_title()))
        __M_writer(u'\n\n')
        # SOURCE LINE 5
        __M_writer(unicode(self.block_content()))
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_content(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        parent = context.get('parent', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 5
        __M_writer(u'\n\n<p>\nTo lodge an application, click the <b>Add</b> button to the right of <b>Applications</b>\n</p>\n\n')
        # SOURCE LINE 11
        __M_writer(unicode(parent.block_content()))
        __M_writer(u'\n\n')
        return ''
    finally:
        context.caller_stack._pop_frame()


def render_block_title(context):
    __M_caller = context.caller_stack._push_frame()
    try:
        trans = context.get('trans', UNDEFINED)
        __M_writer = context.writer()
        # SOURCE LINE 3
        __M_writer(unicode(trans('iVEC Allocations')))
        return ''
    finally:
        context.caller_stack._pop_frame()


