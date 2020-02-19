## List of playbooks

This is just a short list of all the currently available playbooks. Not all of them are "production ready" yet so are to be used with caution, and are not well-documented.

### Tango Development Environment
* `deploy_tangoenv.yml`

### Minikube
* `deploy_minikube.yml`
* `reset_k8s.yml`
* `deploy_skampi.yml` - currently deploys skampi on a Minikube system only.

### Runners
* `deploy_runners.yaml`
* `deploy_openstack_runner.yaml`

TODO: above two playbooks need to be merged.

* `clean_runners.yaml`

### Kubernetes clusters
* `setup_cluster.yml` - create a cluster as specified in the `hosts` file
* `join_cluster.yaml` - adding a node to the cluster

### Helm Linting
* `helm-linting.yml`

### Openstack provisioners
* `openstack.yml`
