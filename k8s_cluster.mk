V_CLUSTERNAME ?= mycluster## Name of the cluster to be created
V_IPs ?= "192.168.100.45 192.168.100.15" ## All internal IPs of the cluster
V_MASTER_IP ?= "192.168.93.19" ## Master node floating ip

V_REMOTE_USER ?= ubuntu## remote username to access the machines nodes of k8s
V_PRIVATE_SSH_KEY ?= ~/cloud.key## ssh private key to access the machines nodes of k8s

V_KUBESPRAY_DIR ?= /usr/src/kubespray## temporary directory for cloning and configuring kubespray

V_dex_issuer ?= "http://192.168.93.19:32000"
V_dex_redirectURI ?= "http://192.168.93.19:32000/callback"
V_gitlab_client_id ?= "417ea12283741e0d74b22778d2dd3f5d0dcee78828c6e9a8fd5e8589025b8d2f"
V_gitlab_client_secret ?= "27a5830ca37bd1956b2a38d747a04ae9414f9f411af300493600acc7ebe6107f"
V_dex_k8s_authenticator_redirectURI ?= "http://192.168.93.19:31000/callback/mycluster"

V_k8s_master_uri ?= "https://192.168.93.19:6443"
V_master_cert ?= "XXXXX"

inventory: ## create the inventory files input for kubespray
	ansible-playbook -b --extra-vars='{"cluster_name": $(V_CLUSTERNAME), "ips": $(V_IPs), "master_floating_ip": $(V_MASTER_IP)}' k8s_create_inventory.yml

kubespray: ## create a k8s cluster using an existing inventory
	ansible-playbook --flush-cache -u $(V_REMOTE_USER) -b -i $(V_KUBESPRAY_DIR)/inventory/$(V_CLUSTERNAME)/hosts.yaml $(V_KUBESPRAY_DIR)/cluster.yml --private-key=$(V_PRIVATE_SSH_KEY) && \
	cp -rf $(V_KUBESPRAY_DIR)/inventory/$(V_CLUSTERNAME) ./inventory/$(V_CLUSTERNAME)

cluster: inventory ## create a k8s cluster with ansible with IPs
	ansible-playbook --flush-cache -u $(V_REMOTE_USER) -b -i $(V_KUBESPRAY_DIR)/inventory/$(V_CLUSTERNAME)/hosts.yaml $(V_KUBESPRAY_DIR)/cluster.yml --private-key=$(V_PRIVATE_SSH_KEY) && \
		cp -rf $(V_KUBESPRAY_DIR)/inventory/$(V_CLUSTERNAME) ./inventory/$(V_CLUSTERNAME) 

components: ## install dex and traefik into the cluster specified in the kubeconfig
	ansible-playbook --flush-cache -u $(V_REMOTE_USER) -b k8s_deploy_components.yml --private-key=$(V_PRIVATE_SSH_KEY) \
		--extra-vars='{"dex_issuer": $(V_dex_issuer), "dex_redirectURI": $(V_dex_redirectURI), "gitlab_client_id": $(V_gitlab_client_id), "gitlab_client_secret": $(V_gitlab_client_secret),  "dex_k8s_authenticator_redirectURI": $(V_dex_k8s_authenticator_redirectURI), "k8s_master_uri": $(V_k8s_master_uri), "master_cert": $(V_master_cert)}'

reset: inventory ## reset the k8s cluster with ansible with IPs
	ansible-playbook --flush-cache -u $(V_REMOTE_USER) -b -i $(V_KUBESPRAY_DIR)/inventory/$(V_CLUSTERNAME)/hosts.yaml $(V_KUBESPRAY_DIR)/reset.yml --private-key=$(V_PRIVATE_SSH_KEY)

