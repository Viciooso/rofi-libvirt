#!/usr/bin/env python

import libvirt
import subprocess

# Connect to the local hypervisor
conn = libvirt.open()

# Get a list of all active and inactive domains
domains = conn.listAllDomains()
if len(domains) == 0:
    print('No domains.')
    exit()

# Build a dictionary of domain names and statuses
domain_info = {}
for domain in domains:
    domain_name = domain.name()
    domain_status = domain.state()[0]
    domain_info[domain_name] = domain_status

# Prompt the user to select a domain using rofi
domain_name = subprocess.check_output('echo -e "{}" | rofi -dmenu -p "Select a domain"'.format('\n'.join(domain_info.keys())), shell=True)
if not domain_name:
    exit()

# Get the selected domain object
domain = conn.lookupByName(domain_name.decode().strip())
if not domain:
    print('Invalid domain selected.')
    exit()

# Prompt the user to select an action to perform on the domain
actions = ['start', 'shutdown', 'reboot']
action = subprocess.check_output('echo -e "{}" | rofi -dmenu -p "Select an action"'.format('\n'.join(actions)), shell=True)
if not action:
    exit()

# Perform the selected action on the domain
if action == b'start\n':
    if domain.isActive():
        print('Domain is already active.')
    else:
        domain.create()
        print('Domain started.')
elif action == b'shutdown\n':
    if not domain.isActive():
        print('Domain is already inactive.')
    else:
        domain.shutdown()
        print('Domain shutdown initiated.')
elif action == b'reboot\n':
    if not domain.isActive():
        print('Domain is not active.')
    else:
        domain.reboot()
        print('Domain reboot initiated.')
else:
    print('Invalid action selected.')

# Close the connection to the hypervisor
conn.close()

