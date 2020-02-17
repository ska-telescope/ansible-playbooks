# SKA Ansible Playbooks
This repository consists of a Makefile and a set of playbooks that allow a developer to easily prepare working environments, be it bare metail or virtual machines, for

* working on TANGO-controls;
* deploying, testing and running the SKA MVP Integration project (SKA MPI)
* setting up Gitlab Runners
* creating and deploying Kubernetes clusters on Openstack
* Deploying a Prometheus service for monitoring resources
* Helm linting

... and more. Please visit our [Documentation](https://developer.skatelescope.org/projects/ansible-playbooks/en/latest/) for details on all the playbooks.

# Quick Start

* Clone the repo:
```
git clone https://gitlab.com/ska-telescope/ansible-playbooks.git && cd ansible-playbooks
```

For working with Ansible, you need to install it and set up a connection (ssh if it's not localhost) to the machine(s) where the playbooks will run. Most of the `make` targets merely call one or more Ansible playbooks, so you need to install Ansible to use it too.

* Install Ansible:
``` 
    apt-add-repository --yes --update ppa:ansible/ansible && apt-get install ansible -y
```
or with sudo:
```    
    sudo apt-add-repository --yes --update ppa:ansible/ansible && sudo apt-get install ansible -y

```

* Edit the file "hosts" with the address(es) to want to manage (if not localhost).

* Add the ssh key to the managed hosts (if not localhost). 

## Make

If you run `make help` you will get an output of all the currently available targets, and variables that you can set, with their defaults. Examples:

### Deploy the SKA MVP Prototype Integration (Skampi) on Minikube

In order to install and run Minikube, as well as deploy the **SKA MPI** project on it, simply run
```
make skampi
```
The above `make` target installs Docker, Minikube, kubectl, Helm, Tiller and starts up the Kubernetes cluster (Minikube). It clones the `skampi` repository into `/usr/src/skampi`. See example below for setting up a development environment.

## Playbooks
There are also a few playbooks in this repository that are not wrapped in a `make` target. You can run the playbooks as well, for instance for deploying a local Tango Controls development environment:

### Deploy Tango Environment

To deploy a Tango development environment, you simply now need to launch the ansible-playbook `deploy_tangoenv.yml`:
``` 
    ansible-playbook -i hosts deploy_tangoenv.yml 
```
or with a password (replace `$PASSWORD` with an actual password): 
```
    export PASSWORD=my-sudo-user-password
    ansible-playbook -i hosts deploy_tangoenv.yml --extra-vars "ansible_become_pass=$PASSWORD"
```

To work with pytango, activate the virtualenv:
``` 
    source /venv/bin/activate
```

The following variables can be set:
```
    build_tango: default('yes')
    install_pytango: default('yes')
    install_ide: default('yes')
    install_ska_docker: default('yes')
    start_tango: default('yes')
    update_hosts: default('yes')
```

For example:
```
    ansible-playbook -i hosts deploy_tangoenv.yml --extra-vars "build_tango='no' install_mysql='no' install_ide='no'"
```

For all the other playbooks, visit the [Documentation](https://developer.skatelescope.org/projects/ansible-playbooks/en/latest/).

## Development Environment TESTED OS (using a box requires at least 4GB RAM):
* ubuntu:18.04
* ubuntu:16.04
* debian:stretch-slim
