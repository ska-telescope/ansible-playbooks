# Kubernetes and the MVP

The simplest way of deploying the MVP is by running it on a Minikube system. Minikube is a single-node cluster provisioned with all the basics that give a developer the opportunity to try out kubernetes.

## Skampi

It is possible to install the integration environment locally with minikube (**CHANGE USER AND PASSWORD**), as well as deploy the SKA MPI project (the MVP), by running a playbook or calling `make skampi`.

The make target calls the playbook for setting up the skampi repository, with additional parameters already passed from the rules (or PrivateRules.mak, if you've set it up). 

```
ansible-playbook -i hosts deploy_skampi.yml
```

At the following link will be setup the webjive webapplication: http://integration.engageska-portugal.pt/testdb


## Ansible Playbook for local Kubernetes

The following are a set of instructions for deploying Kubernetes either directly locally or on a Vagrant VirtualBox.  It has been tested on minikube v1.1.1 with Kubernetes v1.14.3 on Ubuntu 18.04, using Vagrant 2.2.4.

### The Aim

The aim of these instructions, scripts, and playbook+roles is to provide a canned locally available Kubernetes development environment.  This environment will contain:

* Kubernetes at 1.14+ on Docker
* Tools: `kubectl` and `helm` configured with a local [Tiller-less Helm](https://rimusz.net/tillerless-helm)
* A running Ingress Controller
* [Network Policies](https://kubernetes.io/docs/concepts/services-networking/network-policies/) implemented with Calico as the Pod network
* This project mounted into the Guest OS at `/vagrant`


# Makefile

All actions are available as targets in the `Makefile` - type `make help` to get the list of available targets, and variables that can be supplied at the command line.  To make your own variables permanent, place them in a `PrivateRules.mak` file in the root of this project.

```
    $ make
    Makefile:help                  show this help.
    Makefile:k8s                   Which kubernetes are we connected to
    Makefile:localip               set local Minikube IP in /etc/hosts file for Ingress $(INGRESS_HOST)
    Makefile:minikube              Ansible playbook for install and launching Minikube
    Makefile:skampi                Ansible playbook for install and launching Minikube and the Skampi project
    Makefile:vagrant_down          destroy vagrant instance
    Makefile:vagrant_install       install vagrant and vagrant-disksize on Ubuntu
    Makefile:vagrantip             set Vagrant Minikube IP in /etc/hosts file for Ingress $(INGRESS_HOST)
    Makefile:vagrant_up            startup minikube in vagrant
    Makefile:vars                  Vagrant and DISPLAY variables

    make vars (+defaults):
    Makefile:DRIVER                true  ## Run Minikube via 'kvm2' driver (true) or 'none' (false)
    Makefile:INGRESS_HOST          integration.engageska-portugal.pt ## Ingress HTTP hostname
    Makefile:USE_NGINX             false  ## Use NGINX as the Ingress Controller
    Makefile:V_BOX                 ubuntu/bionic64  ## Vagrant Box
    Makefile:V_CPUS                 2  ## Vagrant/Minikube no. CPU allocation
    Makefile:V_DISK_SIZE            32GB  ## Vagrant/Minikube disk size allocaiton in GB
    Makefile:V_GUI                 false  ## Vagrant enable GUI
    Makefile:V_IP                  172.16.0.92  ## Vagrant private network IP
    Makefile:V_MEMORY               4096  ## Vagrant/Minikube memory allocation in MB
    Makefile:V_PLAYBOOK            deploy_tangoenv.yml  ## Ansible playbook run in Vagrant
    Makefile:XAUTHORITYx           ${XAUTHORITY}
```

## With Vagrant

Install Vagrant and VirtualBox - on Ubuntu 18.04+ use:
```
apt install virtualbox vagrant
```
and then:
```
make vagrant_install
```
This will ensure that Vagrant is at minimally working level, and that the Vagrant plugin `vagrant-disksize` is installed which is required for the guest base box disk resizing.

There are two tested options for Vagrant base boxes - `ubuntu/bionic64`, and `fedora/29-cloud-base`.  These can be supplied by var `V_BOX`.

Adjust the vcpus, memory, and initial disk size with: `V_CPUS`, `V_MEMORY`, and `V_DISK_SIZE` as above.

## Minikube with Vagrant

Once Vagrant and VirtualBox are installed, launching a guest OS and installing Minikube with Ansible is carried out with the following:
```
make vagrant_up
```

The default action is to run the `deploy_tangoenv.yml` playbook creating a virtual machine named `tango-dev`.  To create a vanilla Minikube+Vagrant system, add vars `V_NAME=minikube-vm V_PLAYBOOK=deploy_minikube.yml`.

Once successfully completed, inspect Minikube by ssh'ing onto the box with `vagrant ssh`, where all the usual `kubectl` capabilities are available:
```
kubectl get all --all-namespaces
```
The repository has been shared into the guest OS in `/vagrant` where the associated Helm Charts and `make` commands are available.

## Clean up

Clean up with:
```
$ make vagrant_down
```
## Reset Minikube cluster

Kubernetes environment can be reset using the following command:
``` 

ansible-playbook reset_k8s.yml
``` 

## Minikube Direct

Minikube on kvm2
----------------

Minikube can be installed onto your Debian or RedHat based machine within a kvm2 virtual machine instance with:
```
make minikube DRIVER=kvm2
```

## Clean up

Clean up with:
```
$ minikube delete
```

## Minikube direct install (for the brave)

Minikube can also be installed directly onto your Debian or RedHat based machine with:
```
make minikube DRIVER=none
```
***WARNING*** This will overwrite anything that you have locally installed for `docker`, `helm`, `kubectl`, and `minikube` which could be disastrous if you have an existing and customised configuration.



# Deploy Kubernetes Cluster

A fully-fledged Kubernetes cluster can be deployed using the following command, BUT make sure `hosts` file is modified according to your needs:

## Set up N-node cluster
After setting up the `hosts`, you can run the following playbook to provision the nodes. 

``` 
ansible-playbook -i hosts setup_cluster.yml
```

This playbook is intended for CentOS 7 operating system. If deployed within the EngageSKA cluster, please create all nodes with `int_net` network and add to each VM floating IP. After the instalation, remove floating IP's only from the worked nodes.

## Join nodes to Kubernetes Cluster

Kubernetes worker can be joined to the cluster using the following command, BUT make sure `hosts` file is modified according to your needs:

``` 
ansible-playbook -i hosts join_cluster.yml
```
