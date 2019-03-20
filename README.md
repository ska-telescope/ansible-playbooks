# AnsiblePlaybook
This playbook allows to create a minimum but complete TANGO-controls develoment environemnt.

Steps to make it work with RSA KEY:
1. Edit the file "hosts" with the address(es) to want to manage (if not localhost).
2. Add the ssh key to the managed hosts (if not localhost). 
3. Install ansible:
``` 
    apt-add-repository --yes --update ppa:ansible/ansible && apt-get install ansible
```
4. Lunch ansible:
``` 
    ansible-playbook -i hosts deploy_tangoenv.yml 
```
or with password: 
```
    ansible-playbook -i hosts deploy_tangoenv.yml --extra-vars "ansible_become_pass=*password*"
```

To work with pytango, activate the virtualenv:
``` 
    source /venv/bin/activate
```

The following variables can be set:
```
    build_tango: default('yes')
    install_mysql: default('yes')
    start_mysql_server: default ('yes')
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

## Structure of the Playbook
There are 6 roles within this playbook
* mysqlserver: install the mysql server service
* tango: install the TANGO-controls framework (if the mysql service is available it creates also the database)
* pytango: install the pytango project (with virtual env and pipenv)
* ide: install pycharm and vscode
* ska-docker: install the ska-docker project locally
* update_hosts: update the file /etc/hosts

TESTED OS (using a box requires at least 4GB RAM):
* ubuntu:18.04
* ubuntu:16.04
* debian:stretch-slim
