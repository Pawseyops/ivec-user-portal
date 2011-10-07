import os, re, posixpath
from django.conf import settings
from mako.template import Template as makoTemplate
from mako.lookup import TemplateLookup as makoTemplateLookup

from django.template.defaultfilters import *

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
         
        raise exceptions.TopLevelLookupException("Cant locate template for uri '%s'" % uri)

class Template(makoTemplate):
     def render(self, context):
         context_dict = {}
         for d in context.dicts:
             context_dict.update(d)
         context_dict['csrf_tag'] = csrf_tag
         return super(Template, self).render(**context_dict)

from django.template.loaders import filesystem
class Loader(filesystem.Loader):
    is_usable = True
    mako_lookup = TemplateLookup(directories=settings.TEMPLATE_DIRS, module_directory='/tmp/mako_modules')

    def load_template(self, template_name, template_dirs=None):  
        filename = self.mako_lookup.get_template(template_name).filename
        template = Template(filename=filename, lookup=self.mako_lookup)
        #assert(False)
        return template, template_name
        
