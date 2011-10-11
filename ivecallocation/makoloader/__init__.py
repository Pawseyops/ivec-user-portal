import os, re, posixpath
from mako.template import Template as makoTemplate
from mako.lookup import TemplateLookup as makoTemplateLookup
from mako import exceptions
from django.template import defaultfilters
from django.template.base import TemplateDoesNotExist

class TemplateLookup(makoTemplateLookup):
    def get_template(self, uri, debug = False):
        # this is a HACK to get mako to also look back a directory if the template is not found
        
        uri_search_parts = uri.split(os.sep)
                
        for i in range(len(uri_search_parts)):
            uri = os.path.join(*uri_search_parts[i:])
            try:
                if self.filesystem_checks:
                    return self._check(uri, self._collection[uri])
                else:
                    return self._collection[uri]
            except KeyError:
                u = re.sub(r'^\/+', '', uri)
                #print "dirs",self.directories
                for dir in self.directories:
                    srcfile = posixpath.normpath(posixpath.join(dir, u))
                    if os.path.exists(srcfile):
                        return self._load(srcfile, uri)
        
        # raise django.template.base.TemplateDoesNotExist instead of Mako's exception
        # type to cause the next Loader in TEMPLATE_LOADERS to be tried
        raise TemplateDoesNotExist("Cant locate template for uri '%s'" % uri)
        
    def _load(self, filename, uri):
        self._mutex.acquire()
        try:
            try:
                # try returning from collection one 
                # more time in case concurrent thread already loaded
                return self._collection[uri]
            except KeyError:
                pass
            try:
                if self.modulename_callable is not None:
                    module_filename = self.modulename_callable(filename, uri)
                else:
                    module_filename = None
                self._collection[uri] = template = Template(
                                        uri=uri,
                                        filename=posixpath.normpath(filename),
                                        lookup=self, 
                                        module_filename=module_filename,
                                        **self.template_args)
                return template
            except:
                # if compilation fails etc, ensure 
                # template is removed from collection,
                # re-raise
                self._collection.pop(uri, None)
                raise
        finally:
            self._mutex.release()

def trans(inp):
    return inp

def url(var):
    return var
    
from django.contrib.admin.templatetags.adminmedia import admin_media_prefix
from django.contrib.admin.templatetags.log import AdminLogNode
from django.template.base import compile_string

def get_admin_log(limit, varname, user=None):
    return AdminLogNode(limit=limit, varname=varname, user=user)

class Template(makoTemplate):
    
    default_list = ['capfirst', 'center', 'csrf_tag', 'cut', 'date', 'default', 'default_if_none', 'dictsort',
                    'dictsortreversed', 'divisibleby', 'escape', 'escapejs', 'filesizeformat', 'first', 'fix_ampersands',
                    'floatformat', 'force_escape', 'get_digit', 'iriencode', 'join', 'last', 'length', 'length_is',
                    'linebreaks', 'linebreaksbr', 'linenumbers', 'ljust', 'lower', 'make_list', 'phone2numeric',
                    'pluralize', 'pprint', 'removetags', 'random', 'rjust', 'safe', 'safeseq', 'slugify', 'stringformat',
                    'striptags', 'time', 'timesince', 'timeuntil', 'title', 'truncatewords', 'truncatewords_html',
                    'unordered_list', 'upper', 'urlencode', 'urlize', 'urlizetrunc', 'wordcount', 'wordwrap', 'yesno']
    
    standard_tags = {}
    for name in default_list:
        standard_tags[name] = getattr(defaultfilters,name)
    
    def __init__(self, **kwargs):
        super(Template, self).__init__(**kwargs)
        self.nodelist = compile_string(self.source, kwargs['uri'])
   
    def _render(self, context):
        return self.render(context)
    
    def render(self, context):
        context_dict = {}
        for d in context.dicts:
            context_dict.update(d)
        context_dict['csrf_tag'] = defaultfilters.csrf_tag
        context_dict['trans'] = trans
        context_dict['url'] = url
        context_dict['admin_media_prefix'] = admin_media_prefix
        context_dict['LANGUAGE_CODE'] = 'en'
        context_dict['slice'] = defaultfilters.slice_  
        context_dict['get_admin_log'] = get_admin_log
        context_dict.update(self.standard_tags)
        return super(Template, self).render(**context_dict)

