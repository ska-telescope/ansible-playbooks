V_CLUSTERNAME ?= mycluster## Name of the cluster to be created
V_IPs ?= "192.168.100.25 192.168.100.26" ## Master node first, worker node after

V_REMOTE_USER ?= ubuntu## remote username to access the machines nodes of k8s
V_PRIVATE_SSH_KEY ?= ~/cloud.key## ssh private key to access the machines nodes of k8s

V_KUBESPRAY_DIR ?= /usr/src/kubespray## temporary directory for cloning and configuring kubespray

inventory: ## create the inventory files input for kubespray
	ansible-playbook -b --extra-vars='{"cluster_name": $(V_CLUSTERNAME), "ips": $(V_IPs)}' k8s_create_inventory.yml

kubespray: ## create a k8s cluster using an existing inventory
	ansible-playbook --flush-cache -u $(V_REMOTE_USER) -b -i $(V_KUBESPRAY_DIR)/inventory/$(V_CLUSTERNAME)/hosts.yaml $(V_KUBESPRAY_DIR)/cluster.yml --private-key=$(V_PRIVATE_SSH_KEY) && \
	cp -rf $(V_KUBESPRAY_DIR)/inventory/$(V_CLUSTERNAME) ./inventory/$(V_CLUSTERNAME)

cluster: inventory ## create a k8s cluster with ansible with IPs
	ansible-playbook --flush-cache -u $(V_REMOTE_USER) -b -i $(V_KUBESPRAY_DIR)/inventory/$(V_CLUSTERNAME)/hosts.yaml $(V_KUBESPRAY_DIR)/cluster.yml --private-key=$(V_PRIVATE_SSH_KEY) && \
		cp -rf $(V_KUBESPRAY_DIR)/inventory/$(V_CLUSTERNAME) ./inventory/$(V_CLUSTERNAME) 

components: ## install dex and traefik into the cluster specified in the kubeconfig
	ansible-playbook --flush-cache -u $(V_REMOTE_USER) -b k8s_deploy_components.yml --private-key=$(V_PRIVATE_SSH_KEY)

reset: inventory ## reset the k8s cluster with ansible with IPs
	ansible-playbook --flush-cache -u $(V_REMOTE_USER) -b -i $(V_KUBESPRAY_DIR)/inventory/$(V_CLUSTERNAME)/hosts.yaml $(V_KUBESPRAY_DIR)/reset.yml --private-key=$(V_PRIVATE_SSH_KEY)

