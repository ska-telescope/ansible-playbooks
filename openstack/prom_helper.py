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
            if address == "-":
                continue

            updated_metadata = False
            # it is a runner if 9252 is open
            result_of_check = check_port(address, 9252)
            if result_of_check == 0:
                try: 
                    novac.servers.set_meta_item(server.id, "prom_gitlab_exporter", address+":9252")
                    runners.append(address)
                    updated_metadata = True
                except:
                    print("Problem with server " + server.id)
                    print (server)

            # it is a node-exporter if 9100 is open
            result_of_check = check_port(address, 9100)
            if result_of_check == 0:
                try: 
                    novac.servers.set_meta_item(server.id, "prom_node_exporter", address+":9100")
                    nodes.append(address)
                    updated_metadata = True
                except:
                    print("Problem with server " + server.id)
                    print (server)

            if(updated_metadata):
                continue

            if "runner" in server_name:
                runners2ansible.append(address)
            else:
                nodes2ansible.append(address)

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

    runners_targets = []
    nodes_targets = []

    for proj_name in proj_list:
        novac = get_novac(proj_name)
        for server in novac.servers.list():
            server_name = str(server.to_dict()['name']).lower()
            address = get_address(server)
            if address == "-":
                continue

            try:
                runners_targets.append(server.to_dict()['metadata']['prom_gitlab_exporter'])
            except KeyError:
                pass

            try:
                nodes_targets.append(server.to_dict()['metadata']['prom_node_exporter'])
            except KeyError:
                pass

    json_nodes = [{
        "labels": {
            "job": "node"
            },
            "targets": nodes_targets
    }]

    print("Generating node_targets.json")
    with open("node_targets.json", "w") as outfile:
        json.dump(json_nodes, outfile, indent=2)

    json_runners = [{
        "labels": {
            "job": "gitlab-runner"
            },
            "targets": runners_targets
    }]

    print("Generating gitlab.json")
    with open("gitlab.json", "w") as outfile:
        json.dump(json_runners, outfile, indent=2)


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
