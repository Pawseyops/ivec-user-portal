from fabric.api import env
from ccgfab.base import *

env.app_root = '/usr/local/python/ccgapps/'
env.app_name = 'ivecallocation'
env.app_install_names = ['ivecallocation'] # use app_name or list of names for each install
env.vc = 'mercurial'
env.repo_path = '' # empty for mercurial

env.writeable_dirs.extend(["scratch"]) # add directories you wish to have created and made writeable
env.content_excludes.extend([]) # add quoted patterns here for extra rsync excludes
env.content_includes.extend([]) # add quoted patterns here for extra rsync includes

def deploy():
    """
    Make a user deployment
    """
    _ccg_deploy_user()

def snapshot():
    """
    Make a snapshot deployment
    """
    _ccg_deploy_snapshot()

def release():
    """
    Make a release deployment
    """
    env.ccg_virtualenv = "/usr/local/python/cleanpython/bin/python virt_ivecallocation/bin/virtualenv"
    _ccg_deploy_release()

def testrelease():
    """
    Make a release deployment using the dev settings file
    """
    _ccg_deploy_release(devrelease=True)

def purge():
    """
    Remove the user deployment
    """
    _ccg_purge_user()

def purge_snapshot():
    """
    Remove the snapshot deployment
    """
    _ccg_purge_snapshot()
