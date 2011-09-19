# -*- coding: utf-8 -*-
# Django settings for project.

# Load default settings.
# These are part of the project manifest.
from settingsdefault import *

# Load instance settings.
# These are installed locally to this project instance.
# They will be loaded from appsettings.ivecallocation, which can exist anywhere
# in the instance's pythonpath. This is a CCG convention designed to support
# global shared settings among multiple Django projects.
try:
    from appsettings.ivecallocation import *
except ImportError, e:
    pass