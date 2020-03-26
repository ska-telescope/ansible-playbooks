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

print("Username: " + os.environ["username"] + " & Password: " + os.environ["password"] + " & Project name: " + os.environ["project_name"] + " & OpenStack Endpoint: " + os.environ["auth_url"])

start_time = datetime.datetime.now()

logging.basicConfig(level=logging.INFO)

LOG = logging.getLogger(__name__)

if os.environ.get('http_proxy') or os.environ.get('https_proxy'):
	LOG.WARN("Proxy env vars set")

proj_list = os.environ["project_name"].split(';')

runners = []
nodes = []

for proj_name in proj_list:
    auth = v3.Password(auth_url=os.environ["auth_url"],
                    username=os.environ["username"],
                    password=os.environ["password"],
                    project_name=proj_name,
                    user_domain_id='default',
                    project_domain_name='default')

    sess = session.Session(auth=auth, verify=False)

    novac = novaclient.client.Client(2, session=sess)

    for server in novac.servers.list():
        server_name = str(server.to_dict()['name']).lower()
        address = "-"
        addresses = server.to_dict()['addresses']
        for key in addresses:
            for entry in addresses[key]:
                if "192.168.93" in entry["addr"]:
                    address = entry["addr"]
        
        if address == "-":
            continue

        if "runner" in server_name:
            runners.append(address)
        else:
            nodes.append(address)
                        

print(runners)

print(nodes)