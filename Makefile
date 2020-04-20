# Set dir of Makefile to a variable to use later
MAKEPATH := $(abspath $(lastword $(MAKEFILE_LIST)))
BASEDIR := $(notdir $(patsubst %/,%,$(dir $(MAKEPATH))))

# find IP addresses of this machine, setting THIS_HOST to the first address found
THIS_HOST := $(shell (ip a 2> /dev/null || ifconfig) | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\2/p' | head -n1)
DISPLAY := $(THIS_HOST):0
XAUTHORITYx ?= ${XAUTHORITY}
INGRESS_HOST ?= integration.engageska-portugal.pt ## Ingress HTTP hostname

# Vagrant
VAGRANT_VERSION = 2.2.5
V_NAME ?= tango-dev  ## Virtualbox instance name
V_PLAYBOOK ?= deploy_tangoenv.yml  ## Ansible playbook run in Vagrant
V_BOX ?= ubuntu/bionic64  ## Vagrant Box
V_GUI ?= false  ## Vagrant enable GUI
V_DISK_SIZE ?=  32GB  ## Vagrant/Minikube disk size allocaiton in GB
V_MEMORY ?=  4096  ## Vagrant/Minikube memory allocation in MB
V_CPUS ?=  2  ## Vagrant/Minikube no. CPU allocation
# V_IP ?= 172.200.0.25
V_IP ?= 172.16.0.92  ## Vagrant private network IP

# Minikube
DRIVER ?= true  ## Run Minikube via 'kvm2' driver (true) or 'none' (false)
USE_CALICO ?= true  ## Use Calico for Pod Networking
USE_NGINX ?= false  ## Use NGINX as the Ingress Controller

# Format the disk size for minikube - 999g
FORMATTED_DISK_SIZE = $(shell echo $(V_DISK_SIZE) | sed 's/[^0-9]*//g')g


.PHONY: vars k8s minikube localip vagrantip vagrant_install vagrant_up vagrant_down help inventory kubespray cluster components reset skampi
.DEFAULT_GOAL := help

# define targets for creating a k8s cluster
-include k8s_cluster.mk
-include PrivateRules.mak

vars: ## Vagrant and DISPLAY variables
	@echo "V_BOX: $(V_BOX)"
	@echo "V_PLAYBOOK: $(V_PLAYBOOK)"
	@echo "V_GUI: $(V_GUI)"
	@echo "V_DISK_SIZE: $(V_DISK_SIZE)"
	@echo "V_MEMORY: $(V_MEMORY)"
	@echo "V_CPUS: $(V_CPUS)"
	@echo "DRIVER: $(DRIVER)"
	@echo "USE_CALICO: $(USE_CALICO)"
	@echo "USE_NGINX: $(USE_NGINX)"
	@echo "V_IP: $(V_IP)"
	@echo "INGRESS_HOST: $(INGRESS_HOST)"
	@echo "DISPLAY: $(DISPLAY)"
	@echo "XAUTHORITY: $(XAUTHORITYx)"

k8s: ## Which kubernetes are we connected to
	@echo "Kubernetes cluster-info:"
	@kubectl cluster-info
	@echo ""
	@echo "kubectl version:"
	@kubectl version
	@echo ""
	@echo "Helm version:"
	@helm version --client

localip:  ## set local Minikube IP in /etc/hosts file for Ingress $(INGRESS_HOST)
	@new_ip=`minikube ip` && \
	existing_ip=`grep $(INGRESS_HOST) /etc/hosts || true` && \
	echo "New IP is: $${new_ip}" && \
	echo "Existing IP: $${existing_ip}" && \
	if [ -z "$${existing_ip}" ]; then echo "$${new_ip} $(INGRESS_HOST)" | sudo tee -a /etc/hosts; \
	else sudo perl -i -ne "s/\d+\.\d+.\d+\.\d+/$${new_ip}/ if /$(INGRESS_HOST)/; print" /etc/hosts; fi && \
	echo "/etc/hosts is now: " `grep $(INGRESS_HOST) /etc/hosts`

vagrantip:  ## set Vagrant Minikube IP in /etc/hosts file for Ingress $(INGRESS_HOST)
	@existing_ip=`grep $(INGRESS_HOST) /etc/hosts || true` && \
	echo "New IP is: $(V_IP)" && \
	echo "Existing IP: $${existing_ip}" && \
	if [ -z "$${existing_ip}" ]; then echo "$(V_IP) $(INGRESS_HOST)" | sudo tee -a /etc/hosts; \
	else sudo perl -i -ne "s/\d+\.\d+.\d+\.\d+/$(V_IP)/ if /$(INGRESS_HOST)/; print" /etc/hosts; fi && \
	echo "/etc/hosts is now: " `grep $(INGRESS_HOST) /etc/hosts`

vagrant_install:  ## install vagrant and vagrant-disksize on Ubuntu
	@VER=`vagrant version 2>/dev/null | grep Installed | awk '{print $$3}' | sed 's/\./ /g'` && \
	echo "VER: $${VER}" && \
	MAJ=`echo $${VER} | awk '{print $$1}'` && \
	echo "MAJOR: $${MAJ}" && \
	MIN=`echo $${VER} | awk '{print $$2}'` && \
	echo "MINOR: $${MIN}" && \
	if [ "0$${MAJ}" -ge "2" ] || [ "0$${MIN}" -ge "1" ]; then \
	  echo "Vagrant is OK - "`vagrant version`; \
	else \
	  cd /tmp/ && wget https://nexus.engageska-portugal.pt/repository/raw/vagrant/vagrant_$(VAGRANT_VERSION)_x86_64.deb && \
	   sudo dpkg -i /tmp/vagrant_$(VAGRANT_VERSION)_x86_64.deb && \
	  rm -f /tmp/vagrant_$(VAGRANT_VERSION)_x86_64.deb; \
	fi

vagrant_up: vars  ## startup minikube in vagrant
	V_NAME=$(V_NAME) \
	V_PLAYBOOK=$(V_PLAYBOOK) \
	V_BOX=$(V_BOX) \
	V_DISK_SIZE=$(V_DISK_SIZE) \
	V_MEMORY=$(V_MEMORY) \
	V_CPUS=$(V_CPUS) \
	V_IP=$(V_IP) \
	V_GUI=$(V_GUI) \
	USE_CALICO=$(USE_CALICO) \
	USE_NGINX=$(USE_NGINX) \
		vagrant up

vagrant_down: vars  ## destroy vagrant instance
	V_NAME=$(V_NAME) \
	V_PLAYBOOK=$(V_PLAYBOOK) \
	V_BOX=$(V_BOX) \
	V_DISK_SIZE=$(V_DISK_SIZE) \
	V_MEMORY=$(V_MEMORY) \
	V_CPUS=$(V_CPUS) \
	V_IP=$(V_IP) \
	V_GUI=$(V_GUI) \
	USE_CALICO=$(USE_CALICO) \
	USE_NGINX=$(USE_NGINX) \
		vagrant destroy -f

minikube:  ## Ansible playbook for installing k8s and launching Minikube
	PYTHONUNBUFFERED=1 ANSIBLE_FORCE_COLOR=true ANSIBLE_CONFIG='ansible-local.cfg' \
	ansible-playbook --inventory=hosts \
	 -vvvv \
   --limit=development \
	 --extra-vars='{"use_driver": $(DRIVER), "use_calico": $(USE_CALICO), "use_nginx": $(USE_NGINX), "minikube_disk_size": $(FORMATTED_DISK_SIZE), "minikube_memory": $(V_MEMORY), "minikube_cpus": $(V_CPUS)}' \
	 deploy_minikube.yml

skampi:  ## Ansible playbook for installing k8s and launching skampi on a Minikube cluster
	PYTHONUNBUFFERED=1 ANSIBLE_FORCE_COLOR=true ANSIBLE_CONFIG='ansible-local.cfg' \
	ansible-playbook --inventory=hosts \
	 -vvv \
	 --extra-vars='{"use_driver": false, "use_calico": $(USE_CALICO), "use_nginx": $(USE_NGINX), "minikube_disk_size": $(FORMATTED_DISK_SIZE), "minikube_memory": $(V_MEMORY), "minikube_cpus": $(V_CPUS)}' \
	 deploy_skampi.yml

ansible_install: ## Add the repository and install in the current system python
	sudo apt-add-repository --yes --update ppa:ansible/ansible && sudo apt-get install ansible -y

help:  ## show this help.
	@echo "make targets:"
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ": .*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ""; echo "make vars (+defaults):"
	@grep -E '^[0-9a-zA-Z_-]+ \?=.*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = " \\?\\= "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
