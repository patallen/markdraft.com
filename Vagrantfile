# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/vivid64"

  config.vm.network "private_network", ip: "10.10.10.9"
  config.vm.host_name = "api.markdraft.dev"
  config.vm.synced_folder "./repo", "/var/api", id: "vagrant-root",
    :owner => "vagrant",
    :group => "vagrant",
    :mount_options => ["dmode=775","fmode=774"]
  # config.ssh.private_key_path = "~/.ssh/id_rsa"
  config.ssh.forward_agent = true

  config.vm.provider "virtualbox" do |vb|
    vb.memory = "1024"
  end

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  config.vm.provision "shell", inline: <<-SHELL
    sudo apt-get update
    sudo apt-get install nginx -y
    sudo apt-get install gcc libncurses5-dev libffi-dev build-essential -y
    sudo apt-get install python python-dev -y
  SHELL
end