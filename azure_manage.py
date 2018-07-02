""" start & stop virtual machine azure
    by nicogis
"""

import sys
import traceback
import json
import getopt
import logging
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.compute import ComputeManagementClient

# set here your proxy
PROXIES = {}
# for example
# PROXIES = {'http': 'http://myproxy:8080', 'https': 'https://myproxy:8080'}

def get_credentials(name_subscription):
    """ get credential """
    try:
        with open('config.json', encoding='utf-8') as file_json:
            data = json.load(file_json)

        subscription = None
        for item in data['subscriptions']:
            if item['name'] == name_subscription:
                subscription = item['subscription']
                break

        if subscription is None:
            raise Exception('{} not found in config.json'.format(name_subscription))

        subscription_id = subscription['subscription_id']
        credentials = ServicePrincipalCredentials(client_id=subscription['client_id'], secret=subscription['secret'], tenant=subscription['tenant'])

        if PROXIES:
            credentials.proxies = PROXIES

        return credentials, subscription_id
    except json.decoder.JSONDecodeError:
        raise Exception('Decoding config.json has failed')
    except:
        raise

def main(argv):
    """ main method """
    logging.basicConfig(level=logging.ERROR)

    try:
        opts, args = getopt.getopt(argv, 'ho:n:v:g:', ['operation=', 'alias_name_subscription=', 'vm_name=', 'group_name='])
    except getopt.GetoptError:
        print('azure_manage.py -o (deallocate|start|restart|stop) -n name_subscription -v name_vm -g name_group')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('azure_manage.py -o (deallocate|start|restart|stop) -n name_subscription -v name_vm -g name_group')
            sys.exit(0)
        elif opt in ('-n', '--alias_name_subscription'):
            alias_name_subscription = arg
        elif opt in ('-o', '--operation'):
            operation = arg
        elif opt in ('-v', '--vm_name'):
            vm_name = arg
        elif opt in ('-g', '--group_name'):
            group_name = arg
    try:

        credentials, subscription_id = get_credentials(alias_name_subscription)
        compute_client = ComputeManagementClient(credentials, subscription_id)
        if PROXIES:
            compute_client.config.proxies.use_env_settings = False
            compute_client.config.proxies.proxies = PROXIES

        async_vm = None
        if operation == 'deallocate':
            print('\nDeallocate virtual machine {}'.format(vm_name))
            async_vm = compute_client.virtual_machines.deallocate(group_name, vm_name)
        elif operation == 'start':
            print('\nStart virtual machine {}'.format(vm_name))
            async_vm = compute_client.virtual_machines.start(group_name, vm_name)
        elif operation == 'restart':
            print('\nRestart virtual machine {}'.format(vm_name))
            async_vm = compute_client.virtual_machines.restart(group_name, vm_name)
        elif operation == 'stop':
            print('\nStop virtual machine {}'.format(vm_name))
            async_vm = compute_client.virtual_machines.power_off(group_name, vm_name)
        else:
            print('Operation not supported {}'.format(operation))

        if not async_vm is None:
            async_vm.wait()

    except:
        print('A VM operation failed:', traceback.format_exc(), sep='\n')

if __name__ == '__main__':
    main(sys.argv[1:])
