import os
from makoloader import Template, TemplateLookup
from django.conf import settings
from django.template.loaders import filesystem
from django.template.base import TemplateDoesNotExist
from mako import exceptions
from django.template.loaders import app_directories

class Loader(filesystem.Loader):
    is_usable = True
    
    app_template_dirs = []
    for dir in app_directories.app_template_dirs:
        app_template_dirs.append(os.path.join(dir, 'mako'))
    template_dirs = settings.TEMPLATE_DIRS + app_template_dirs
    
    mako_lookup = TemplateLookup(directories=template_dirs, module_directory='/tmp/mako_modules')

    def load_template(self, template_name, template_dirs=None):
        try:
            template = self.mako_lookup.get_template(template_name)
        except (exceptions.TopLevelLookupException, exceptions.TemplateLookupException), e:
            raise TemplateDoesNotExist(str(e))
        return template, template_name