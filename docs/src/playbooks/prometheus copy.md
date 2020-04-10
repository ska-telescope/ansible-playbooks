# Upgrade Helm 2 to Helm 3  
In order to upgrade your existing cluster to use Helm 3, you will need to uninstall Helm 2 and remove Tiller. This playbook attempts to do all of that in-place. 
There is a chance that you may still need to delete PersistentVolumes and PersistentVolumeClaims, depending on your local setup, but we have attempted to take care of a few scenarios.

# Usage
Call the `upgrade_helm.yml` playbook on your Minikube cluster: 

```
    ansible-playbook upgrade_helm.yml -i hosts -e 'ansible_python_interpreter=/usr/bin/python3'
```

Call the playbook with the following command to install the node-exporter: 

```
    ansible-playbook deploy_prometheus.yaml --extra-vars "mode='exporter'" -i hosts -e 'ansible_python_interpreter=/usr/bin/python3'
```

Call the playbook with the following command to install both server and exporter: 

```
    ansible-playbook deploy_prometheus.yaml --extra-vars -i hosts -e 'ansible_python_interpreter=/usr/bin/python3'
```

Remember to check the variable file available in roles/prometheus/vars before calling the playbook. 

