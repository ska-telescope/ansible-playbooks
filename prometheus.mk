prometheus-server:
	ansible-playbook deploy_prometheus.yml \
	        --extra-vars "mode='server' project_name='$(OS_PROJECT_NAME)' auth_url='$(OS_AUTH_URL)' username='$(OS_USERNAME)' password='$(OS_PASSWORD)'" \
		-i hosts \
		-e 'ansible_python_interpreter=/usr/bin/python3' \
		-e @/path/to/prometheus_node_metric_relabel_configs.yaml



prometheus-node-exporter:
	ansible-playbook deploy_prometheus.yml --extra-vars "mode='exporter'" \
		-i hosts \
		-e 'ansible_python_interpreter=/usr/bin/python3'

prometheus-all:
	ansible-playbook deploy_prometheus.yml -i hosts \
	        --extra-vars "project_name='$(OS_PROJECT_NAME)' auth_url='$(OS_AUTH_URL)' username='$(OS_USERNAME)' password='$(OS_PASSWORD)'" \
		-e 'ansible_python_interpreter=/usr/bin/python3' \
		-e @/path/to/prometheus_node_metric_relabel_configs.yaml
