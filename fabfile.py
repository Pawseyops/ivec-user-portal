from fabric.api import env, task
from ccg.fabric.commands import *


env.ccg.servers = {
    'centos': {
	'region': 'localhost',
	'box_url': 'http://faramir.localdomain/boxes/centos62_64.box',
	'image_id': 'centos62_64',
	'instance_type': 'vagrant',
	'puppet_manifest': 'ivecallocation.pp',
    },
}

