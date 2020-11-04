# DEPRECATION NOTICE
This repository is no longer supported. The Ansible roles generated in this repository have been moved to single-purpose repositories on the SKA Gitlab repository.

## Common roles for Docker, Kubernetes and OpenStack Heat Clusters
Common Ansible roles that are frequently used are hosted in the [Systems Common Roles](https://gitlab.com/ska-telescope/sdi/systems-common-roles) repository.

## Prometheus & Grafana deployment
Deployment of Prometheus is now done using the dedicated [Prometheus Deployment](https://gitlab.com/ska-telescope/sdi/deploy-prometheus) project. Users **must** consult the README and check all the `make` variables before deployment of a Prometheus server for personal use.

## SKAMPI & Minikube
Deploying minikube is best done using the dedicated [Minikube Deployment](https://gitlab.com/ska-telescope/sdi/deploy-minikube) project. Installation of [SKAMPI](https://gitlab.com/ska-telescope/skampi) should be done as per the documentation.

## Other roles
The Systems Team is maintaining dedicated repositories for Gitlab runners, Rook-ceph integration, Elasticstack and other infrastructure under the [Software Defined Infrastructure](https://gitlab.com/ska-telescope/sdi) Gitlab group.

## Ansible installation note
The PPA does not exist for Ubuntu 20.04 at the time of writing. Consult the [Ansible documentation](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html#installing-ansible-with-pip) for installation steps using pip.
