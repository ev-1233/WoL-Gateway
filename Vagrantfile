# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Use Ubuntu 24.04 LTS
  config.vm.box = "bento/ubuntu-24.04"
  
  # Provider configuration for libvirt
  config.vm.provider :libvirt do |libvirt|
    libvirt.memory = 2048
    libvirt.cpus = 2
  end

  # Network configuration - forward Flask port
  config.vm.network "forwarded_port", guest: 5000, host: 5000, host_ip: "127.0.0.1"
  
  # Sync the current folder to /vagrant in the VM
  config.vm.synced_folder ".", "/vagrant", type: "rsync"
  
  # Provisioning script
  config.vm.provision "shell", inline: <<-SHELL
    echo "==> Updating system..."
    apt-get update
    
    echo "==> Installing Python 3 and pip..."
    apt-get install -y python3 python3-pip python3-venv git
    
    echo "==> VM provisioned successfully!"
    echo "==> To test the admin panel:"
    echo "    1. vagrant ssh"
    echo "    2. cd /vagrant"
    echo "    3. python3 setup_wol.py  # Choose option 2 for web admin"
    echo "    4. sudo python3 wol_gatway.py"
    echo "==> Then access http://localhost:5000/admin from your host browser"
  SHELL
end
