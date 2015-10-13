#!/usr/bin/env python

# This script creates a dynamic inventory appropriate for installing MaaS on
# a RHEL OSP cluster.
import os
import sys
import json
from novaclient import client

nova = client.Client('2', os.getenv('OS_USERNAME'), os.getenv('OS_PASSWORD'),
                     os.getenv('OS_TENANT_NAME'), os.getenv('OS_AUTH_URL'),
                     cacert=os.getenv('OS_CACERT'))
inventory = {'all': [],
             'infra_all': [],
             'compute_all': []}
for server in nova.servers.list():
    name = server.name
    ip = server.networks['ctlplane'][0]
    inventory['all'].append(ip)
    if 'compute' in name:
        inventory['compute_all'].append(ip)
    if 'controller' in name:
        inventory['infra_all'].append(ip)
    inventory[name] = {'hosts': [ip], 'vars': {'ansible_ssh_user': 'heat-admin',
                                               'ansible_become': True}}
inventory['hosts'] = inventory['all']

if sys.argv[1] == '--list':
    print(json.dumps(inventory))
else:
    print '{}'
