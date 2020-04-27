import os
import logging
from keystoneauth1.identity import v3
from keystoneauth1 import session
import novaclient.client
import heatclient.client
import yaml
import time
import socket
import datetime
import sys
from threading import Thread
import socket
import json, argparse
import re

NAMESPACE_PREFIX = 'prom:'
EXPORTERS = {'gitlab_exporter': {'name': 'runner', 'port': 9252},
             'node_exporter': {'name': 'node', 'port': 9100},
             'elasticsearch_exporter': {'name': 'elasticsearch', 'port': 9114},
             'ceph-mgr': {'name': 'ceph_cluster', 'port': 9283},
             'docker_exporter': {'name': 'docker', 'port': 9323},
             'kubernetes_exporter': {'name': 'k8smetrics', 'port': 32080},
             'kubernetes_telemetry': {'name': 'k8stelemetry', 'port': 32081}
             }
RELABEL_KEY = 'prometheus_node_metric_relabel_configs'

def check_port(address, port):
    location = (address, port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return sock.connect_ex(location)

def get_novac(proj_name):
    auth = v3.Password(auth_url=os.environ["auth_url"],
                        username=os.environ["username"],
                        password=os.environ["password"],
                        project_name=proj_name,
                        user_domain_id='default',
                        project_domain_name='default')

    sess = session.Session(auth=auth, verify=False)

    return novaclient.client.Client(2, session=sess)

def get_address(server):
    address = "-"
    addresses = server.to_dict()['addresses']
    for key in addresses:
        for entry in addresses[key]:
            if "192.168.93" in entry["addr"]:
                address = entry["addr"]
                break
            address = entry["addr"]
        if address != "-":
            break
    return address

def update_openstack_metadata():
    proj_list = os.environ["project_name"].split(';')

    runners = []
    nodes = []

    runners2ansible = []
    nodes2ansible = []

    for proj_name in proj_list:
        novac = get_novac(proj_name)
        for server in novac.servers.list():
            server_name = str(server.to_dict()['name']).lower()
            address = get_address(server)
            print("Server " + server_name + " address " + str(address))
            if address == "-":
                continue

            updated_metadata = False
            for exporter_name, details in EXPORTERS.items():
                result_of_check = check_port(address, details['port'])
                if result_of_check == 0:
                    try:
                        novac.servers.set_meta_item(server.id, NAMESPACE_PREFIX + exporter_name, address+":"+str(details['port']))
                        if exporter_name == 'gitlab_exporter':
                            runners.append(address)
                        elif exporter_name == 'node_exporter':
                            nodes.append(address)
                        updated_metadata = True
                    except:
                        print("Problem with server " + server.id)
                        print (server)

            if(updated_metadata):
                continue

            str_append = address + " ## " + server_name
            if "runner" in server_name:
                runners2ansible.append(str_append)
            else:
                nodes2ansible.append(str_append)

    print("Generating ansible hosts file")
    with open("hosts", "w") as outfile:
        outfile.write("[nodexporter]\n")
        for runner in runners2ansible:
            outfile.write(runner + "\n")
        for node in nodes2ansible:
            outfile.write(node + "\n")
        outfile.write("\n[runners]\n")
        for runner in runners2ansible:
            outfile.write(runner + "\n")

    print("*** Metadata added to the following runners ***")
    print(runners)

    print("*** Metadata added to the following nodes ***")
    print(nodes)

def generate_targets_from_metadata():
    proj_list = os.environ["project_name"].split(';')

    targets = {}
    hostrelabelling = {RELABEL_KEY: []}

    for proj_name in proj_list:
        novac = get_novac(proj_name)
        for server in novac.servers.list():
            server_name = str(server.to_dict()['name']).lower()
            address = get_address(server)
            if address == "-":
                continue

            hostrelabelling[RELABEL_KEY].append(
                                   {'source_labels': ["instance"],
                                    'regex': re.escape(address)+':(\d+)',
                                    'action': "replace",
                                    'target_label': "instance",
                                    'replacement': server_name+':9100'})

            for exporter_name, details in EXPORTERS.items():
                if not exporter_name in targets:
                    targets[exporter_name] = []
                try:
                    targets[exporter_name].append(server.to_dict()['metadata'][NAMESPACE_PREFIX + exporter_name])
                except KeyError:
                    pass

    for exporter_name, export_targets in targets.items():
        json_job = [{
            "labels": {
                "job": EXPORTERS[exporter_name]['name']
                },
                "targets": export_targets
        }]

        json_file = exporter_name + ".json"
        print("Generating %s" % json_file)
        with open(json_file, "w") as outfile:
            json.dump(json_job, outfile, indent=2)

    yaml_file = "%s.yaml" % RELABEL_KEY
    print("Generating %s" % yaml_file)
    with open(yaml_file, "w") as outfile:
        yaml.dump(hostrelabelling, outfile, indent=2)

start_time = datetime.datetime.now()

logging.basicConfig(level=logging.INFO)

LOG = logging.getLogger(__name__)

if os.environ.get('http_proxy') or os.environ.get('https_proxy'):
	LOG.WARN("Proxy env vars set")

if (os.environ.get('auth_url') is None) or (os.environ.get('username') is None) or (os.environ.get('password') is None) or (os.environ.get('project_name') is None):
    print("Please provide the following environment variables: auth_url, username, password, project_name(comma separated values)")
    sys.exit(1)

parser = argparse.ArgumentParser()
parser.add_argument('-u', '--update_metadata', help='update metadata on openstack and generate ansible hosts inventory file',action='store_true')
parser.add_argument('-g', '--generate_targets', help='generate targets file',action='store_true')

args = parser.parse_args()

if len(sys.argv)==1:
    parser.print_help(sys.stderr)
    sys.exit(1)

if(args.update_metadata):
    update_openstack_metadata()
if(args.generate_targets):
    generate_targets_from_metadata()
