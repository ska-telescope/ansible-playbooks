# setup defaults
vname = ENV['V_NAME'] || "tango-dev"
vbox = ENV['V_BOX'] || "ubuntu/bionic64"
vsize = ENV['V_DISK_SIZE'] || "42GB"
vmem = (ENV['V_MEMORY'] || 8192).to_i
vcpus = (ENV['V_CPUS'] || 4).to_i
# Random IP in private address space
vip = ENV['V_IP'] || "172.16.0.92"
# if not explicitly stated or set to 'true' then enable the gui
vgui = (if !ENV.key?('V_GUI') || ENV['V_GUI'] == 'true' then true else false end)
vcalico = (if !ENV.key?('USE_CALICO') || ENV['USE_CALICO'] == 'true' then true else false end)
vnginx = (if !ENV.key?('USE_NGINX') || ENV['USE_NGINX'] == 'true' then true else false end)
vplaybook  = ENV['V_PLAYBOOK'] || "deploy_tangoenv.yml"

Vagrant.configure("2") do |config|
  config.vm.box = vbox
  config.disksize.size = vsize
  config.vm.synced_folder ".", "/vagrant"
  config.vm.network "private_network", ip: vip
  config.vm.boot_timeout = 300
  config.vm.provider "virtualbox" do |v|
    v.gui = vgui
    v.name = vname
    # 1GB RAM fails PyTango compiling
    v.memory = vmem
    v.cpus = vcpus
  end

  # Run ansible from within the Vagrant VM
  config.vm.provision "ansible_local" do |ansible|
    ansible.verbose = "vvv"
    ansible.inventory_path = "hosts"
    ansible.config_file = "ansible-local.cfg"
    ansible.limit = "development"
    ansible.playbook = vplaybook
    # only pass default vars to deploy_minikube
    ansible.extra_vars = ( if vplaybook == "deploy_minikube.yml" then { use_driver: false, use_calico: vcalico, use_nginx: vnginx } else {} end)
  end
end
