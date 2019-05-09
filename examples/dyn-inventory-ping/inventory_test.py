#!/usr/bin/env python3
#
import json
import argparse

# create dict object for inventory
# child groups
inventory = {}
inventory['csr'] = {'hosts': ['p1.pk.lab', 'pe2.pk.lab', 'pe3.pk.lab', 'bras1.pk.lab'], 'vars': {'ansible_network_os': 'ios'}}
inventory['xr'] = {'hosts': ['pe1.pk.lab'], 'vars': {'ansible_network_os': 'iosxr'}}
inventory['catalyst'] = {'hosts': ['sw1.pk.lab'], 'vars': {'ansible_network_os': 'ios'}}

# parent groups
inventory['mpls'] = {'children': ['ios', 'xr']}
inventory['ios'] = {'children': ['csr']}

# all groups vars
allgroupvars = {'ansible_user': 'pk', 'ansible_ssh_pass': 'pk'}

# host specific vars
hostvars = {}
hostvars['p1.pk.lab'] = {'ansible_host': '10.0.0.50'}
hostvars['pe1.pk.lab'] = {'ansible_host': '10.0.0.51'}
hostvars['pe2.pk.lab'] = {'ansible_host': '10.0.0.52'}
hostvars['pe3.pk.lab'] = {'ansible_host': '10.0.0.53'}
hostvars['bras1.pk.lab'] = {'ansible_host': '10.0.0.54'}
hostvars['sw1.pk.lab'] = {'ansible_host': '10.0.0.252'}

parser = argparse.ArgumentParser(description='Simple Inventory')
parser.add_argument('--list', action='store_true', help='List all hosts')
parser.add_argument('--host', help='List details of a host')
args = parser.parse_args()

if args.list:
    for group in inventory:
        # loop through each group, create a copy of the allgroupvars data, update that data with any data that may
        # already exist in the group, then replace the group's variable data with the newly updated copy.
        ag = allgroupvars.copy()
        ag.update(inventory[group].get('vars', {}))
        inventory[group]['vars'] = ag
    print(json.dumps(inventory))
elif args.host:
    print(json.dumps(hostvars.get(args.host, {})))
