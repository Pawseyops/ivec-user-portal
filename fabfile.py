from fabric.api import env
from ccgplatform.fabric.commands import *

env.ccg.servers = {
    'default': {
	    'region': 'localhost',
	    'box_url': 'http://faramir.localdomain/boxes/centos62_64.box',
	    'image_id': 'centos62_fusion',
	    'instance_type': 'vmwarefusion',
	    'puppet_manifest': 'ivecallocation-local-dev.pp',
	    'ssh_user': 'ccg-user',
    },
}

