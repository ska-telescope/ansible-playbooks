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

## Playbooks
This repository contains a large number of ansible-playbooks that can assist a developer with installing and configuring software and infrastructure on local, virtual or cloud based machines.

The `deploy_tangoenv.yml` playbook can be used for deploying a local Tango Controls development environment, as described on the [SKA Developer Portal](https://developer.skatelescope.org/en/latest/tools/tango-devenv-setup.html#creating-a-development-environment):

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
To finish the installation, reboot the system:
```
    sudo reboot
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

For more information on the other playbooks available in this repo, visit the [Documentation](https://developer.skatelescope.org/projects/ansible-playbooks/en/latest/).

## Development Environment TESTED OS (using a box requires at least 4GB RAM):
* ubuntu:18.04
* ubuntu:16.04
* debian:stretch-slim
