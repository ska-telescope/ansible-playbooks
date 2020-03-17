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

# TODO howto pass internalURL
auth = v3.Password(auth_url=os.environ["auth_url"],
				   username=os.environ["username"],
				   password=os.environ["password"],
				   project_name=os.environ["project_name"],
				   user_domain_id='default',
				   project_domain_name='default')

sess = session.Session(auth=auth, verify=False)

novac = novaclient.client.Client(2, session=sess)

heatc = heatclient.client.Client(1, session=sess)

stack_list = list()
for stack in heatc.stacks.list():
	stack_list.append(stack)

def valid_ip_address(ip_address):
	try:
	    socket.inet_aton(ip_address)

	    return True

	except socket.error:
	    return False

def process_yaml_file(template_content, return_content):
	# heat file content
	heat_content = yaml.load(template_content)

	# get stack name
	heat_stack_name = heat_content['heat_stack_name']
	del heat_content['heat_stack_name']

	if return_content == 'stack_name':
		return heat_stack_name

	# yaml keys
	main_key = 'resources'
	content_key = 'content'
	software_content = {}
	nova_resources = []

	# instance specs
	specs = heat_content.get(main_key)

	# instance keys
	inst_keys = specs.keys()

	for key in inst_keys:
		# get instance name
		inst_specs = specs.get(key)

		# get only Nova resources
		if specs[key]['type'] == 'OS::Nova::Server':
			nova_resources.append(key)

		if content_key in inst_specs:
			# append software content
			software_content.update({key : inst_specs.get(content_key)})

			# remove software from the heat content
			del heat_content[main_key][key][content_key]

	if return_content == 'resources':
		return nova_resources

	elif return_content == 'heat':
		return heat_content

	elif return_content == 'content':
		return software_content

	else:
		return


def instance_hostname_by_stack_and_resource(stack_name,resource_name):

	resource_info = heatc.resources.get(stack_name,resource_name).to_dict()

	return resource_info['attributes']['name']


def stack_status(stack_name):

	output = heatc.stacks.get(stack_name).to_dict()['stack_status']

	return output


def create_stack(stack_name, stack_template):

	output = heatc.stacks.create(stack_name=stack_name, template=stack_template)

	return output


def delete_stack(stack_name):
	output = heatc.stacks.delete(stack_name)

	return output


def resources_by_stack(stack_name):
	resources = []

	for value in heatc.resources.list(stack_name):
		if value.to_dict()['resource_type'] == 'OS::Nova::Server':
			resources.append(value.to_dict()['resource_name'])

	return resources


def list_stacks():
	return heatc.stacks.list()


def stack_exists(stack_name):
	global stack_list

	for x in range(0,len(stack_list)):
		if stack_name == stack_list[x].to_dict()['stack_name']:
			return True

	return False


def instance_ip_by_hostname(hostname):
	for server in novac.servers.list():
		if server.to_dict()['name'] == hostname:
			addresses = server.to_dict()['addresses']

			for key in addresses:
				for entry in addresses[key]:
					if "192.168.93" in entry["addr"]:
						return entry["addr"]


def port_is_open(ip,port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((ip, int(port)))
		s.shutdown(2)
		return True
	except:
		return False


def ssh_user_by_image(hostname):
	server = novac.servers.find(name=hostname)
	image_id = novac.servers.get(server).to_dict()['image']['id']
	image_name = novac.images.find(id=image_id).to_dict()['name']

	if "Ubuntu" in image_name:
		return 'ubuntu'
	elif "Centos" in image_name:
		return 'centos'
	else:
		return False

def ssh_instance_access(host,user):
	command_output = os.popen("ssh -o PreferredAuthentications=publickey -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no "+user+"@"+host+" \"echo 'AccessGranted'\"").read()

	if 'AccessGranted' in command_output:
		return True
	else:
		return False


def ssh_remote_bash_run(host,user,command,option=""):
	os.system("ssh -o PreferredAuthentications=publickey -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no " + option + " " + user + "@" + host + " " + command)


def ansible_playbook_install(hostname,host,playbook,extravars=""):
	os.system("ansible-playbook -u "+hostname+" -i "+host+", "+playbook+" --ssh-common-args='-o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no' --extra-vars '"+extravars+"'")


def stack_software_install(stack_name, resource, software_content, init_template, template_path):

	instance_hostname = instance_hostname_by_stack_and_resource(stack_name, resource)
	instance_ip = instance_ip_by_hostname(instance_hostname)

	# wait for SSH to be available
	while not port_is_open(instance_ip,'22'):
		time.sleep(1)
		print('SSH NOT YET AVAILABLE')

	# give time for HEAT to add SSH key to the instance		
	while not ssh_instance_access(instance_ip, ssh_user_by_image(instance_hostname)):
		time.sleep(1)
		print('SSH KEY NOT YET INJECTED')

	# install init content
	extravars = "hostname="+instance_hostname.lower()
	
	ansible_playbook_install(ssh_user_by_image(instance_hostname), instance_ip, init_template, extravars)

	# install software content
	if 'bash' in software_content[resource]:
		print('NOT-IMPLEMENTED-YET')

	elif 'ansible' in software_content[resource]:
		ansible_playbook_install(ssh_user_by_image(instance_hostname), instance_ip, template_path + '/' + software_content[resource]['ansible']['file'], software_content[resource]['ansible']['extra-vars'])

	else:
		print('NOTHING-TO-INSTALL')


def threads_start_and_wait(threads):
	# Start all threads
	for x in threads:
		x.start()

	# Wait for all of them to finish
	for x in threads:
		x.join()

	return []


def run_stack(yaml_file, action, nodes_count, compt_stack_name=None):
	script_path = os.getcwd()
	template_path = script_path + '/' +os.path.dirname(yaml_file)
	init_template = script_path + "/../init_openstack.yml"

	if action == 'remove':
		stages = {
			'template_analysis': True,
			'stack_delete': True,
			'stack_create': False,
			'software_content': False,
			'print_details': False
		}
	elif action == 'deploy':
		stages = {
			'template_analysis': True,
			'stack_delete': False,
			'stack_create': True,
			'software_content': True,
			'print_details': True
		}
	#lots of useful stuff can be added here
	elif action == 'dry-run':
		print("Node count: {count}".format(count=nodes_count))
		exit(0)
	else:
		print("the options are 'dry-run', remove' or 'deploy'")
		exit(0)

	if stages['template_analysis']:

		# original template
		heat_template = open(yaml_file, "r")

		# only heat content
		stack_template = process_yaml_file(open(yaml_file,"r"), 'heat')

		# only software content
		software_content = process_yaml_file(open(yaml_file,"r"), 'content')

		# get stack name
		stack_name = process_yaml_file(open(yaml_file,"r"), 'stack_name')

		# get stack resources
		stack_resources = process_yaml_file(open(yaml_file,"r"), 'resources')

	if stages['stack_delete']:

		# delete stack before creating
		if stack_exists(stack_name):
			# delete stack
			try:
				delete_stack(stack_name)
			except Exception as e:
				print(e)

			# print stack status
			print(stack_status(stack_name))

		# wait while stack is being deleted
		try:
			while stack_exists(stack_name):
				var_stack_status= stack_status(stack_name)
				print(var_stack_status)

				# force stack delete if failed during removal
				if var_stack_status == "DELETE_FAILED":
					try:
						delete_stack(stack_name)
					except Exception as e:
						print(e)

				time.sleep(1)
		except Exception as e:
			print('DELETE_COMPLETE')

	if stages['stack_create']:

		# deploy stack
		if not stack_exists(stack_name):
			create_stack(stack_name, yaml.dump(stack_template))
		else:
			print('Stack already exists')
			exit()

		# wait for stack completion
		while stack_status(stack_name) != 'CREATE_COMPLETE':
			time.sleep(10)
			print(stack_status(stack_name))

	if stages['software_content']:

		threads = []

		# for each instance
		for resource in stack_resources:

			t = Thread(target=stack_software_install, args=(stack_name, resource, software_content, init_template, template_path))
			threads.append(t)

		threads = threads_start_and_wait(threads)

	if stages['print_details']:

		for resource in stack_resources:

			instance_hostname = instance_hostname_by_stack_and_resource(stack_name, resource)
			instance_ip = instance_ip_by_hostname(instance_hostname)

			print(resource + ": " + instance_ip)


if __name__ == "__main__":
	file = sys.argv[1]
	action = sys.argv[2]
	nodes = 1
	if len(sys.argv)>3:
		nodes = sys.argv[3]

	run_stack(file, action, nodes)

	print(datetime.datetime.now() - start_time)

