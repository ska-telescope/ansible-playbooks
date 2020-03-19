# Prometheus playbook
The prometheus playbook is now composed by the following tasks:
* server.yml: configure (prometheus configuration+recording rules+alerting rules) and start the prometheus server as docker container
* alert_manager.yml: configure and start the alert manager as docker container
* node_exporter.yml: this was the only task that was present before and it has simplified with the installation of the debian package (no need to install the service the package installs it)
* blackbox_exporter.yml: pull and start the black box exporter
* main.yml: depending on the mode (server, executor and all) it includes the other tasks.

The variable file include an example configuration made for testing purpose which includes: 
* various scrape configs (a scrape config represent an endpoint which usually corresponding to a single process where prometheus collects information). Scrape configs are grouped by job, that is a collection of instances with the same purpose. 
* alert rules, recording rules and all the necessary information that goes into the prometheus server. 
