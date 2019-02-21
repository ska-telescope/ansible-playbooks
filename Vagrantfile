Vagrant.configure("2") do |config|
    config.vm.box = "ubuntu/bionic64"
    config.vm.synced_folder ".", "/vagrant"
    config.ssh.username = "vagrant"
    config.ssh.password = "vagrant"
    config.vm.provider "virtualbox" do |v|
       v.gui = true
       v.name = "TANGO-dev"
       # 1GB RAM fails PyTango compiling
       v.memory = 4096
       v.cpus = 2
    end
    # Run ansible from within the Vagrant VM
    config.vm.provision "ansible_local" do |ansible|
       ansible.verbose = "vvv"
       ansible.inventory_path = "hosts"
       ansible.config_file = "ansible-local.cfg"
       ansible.limit = "development"
       ansible.playbook = "deploy_tangoenv.yml"
       ansible.become = true
     end
 end
 
