Role Name
=========

Install and run Elasticsearch as Docker container.

Requirements
------------

Need to set `vm.max_map_count=262144` via sysctl and open up `memlock` and `nofile` limits.

Role Variables
--------------

```
elasticsearch_args: []
elasticsearch_cluster_name: "elasticsearch"
elasticsearch_config:
  discovery.zen.minimum_master_nodes: 1
  action.auto_create_index: false
  indices.cache.cleanup_interval: "1m"
  network.host: "0.0.0.0"
  transport.host: "0.0.0.0"
  bootstrap.memory_lock: true
  node.master: true
  node.data: true
  node.ingest: true
elasticsearch_enabled: true
elasticsearch_image: docker.elastic.co/elasticsearch/elasticsearch-oss:6.1.2
elasticsearch_jvm_heapsize: "256M"
elasticsearch_node_name: "{{ inventory_hostname }}"
elasticsearch_path: "/opt/elasticsearch"
elasticsearch_service: "elasticsearch"
```

Dependencies
------------

lmickh.docker

Example Playbook
----------------

    - name: servers
      roles:
        - {{ lmickh.elasticsearch }}

License
-------

MIT
