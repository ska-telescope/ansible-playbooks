# Upgrade Helm 2 to Helm 3  
In order to upgrade your existing cluster to use Helm 3, you will need to uninstall Helm 2 and remove Tiller. This playbook removes Tiller, removes Helm 2 and installs Helm 3. The exact version is set in the ``group_vars/all.yml`` file.

There is a possibility that you may still need to delete PersistentVolumes and PersistentVolumeClaims, depending on your local setup, if they are not deployed correctly after the upgrade.

## Usage
Call the `upgrade_helm.yml` playbook on your Minikube cluster: 

```
    ansible-playbook upgrade_helm.yml -i hosts'
```

Change directory to the `skampi` repository, redeploy the full MVP, and check if all your pods are running

```
    make redeploy
    make smoketest    
```

You can also investigate if the deployment worked, using kubectl:

```
    kubectl get all -A
```

It may happen that some of your `pv`/`pvc` deployments do not run properly - you can delete them using `kubectl` and redeploy with `make redeploy` as above or `make deploy HELM_CHART=chart-name` if you prefer.