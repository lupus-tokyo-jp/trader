# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|

  config.vm.define "trade" do |trade|
    trade.vm.box = "trade.box"

    trade.vm.hostname = "trade.local"
    trade.vm.network "private_network", ip: "192.168.35.10"
    trade.vm.network "forwarded_port", auto_correct: true, id: "http", guest: 80, host: 8080
    trade.vm.network "forwarded_port", auto_correct: true, id:  "ssh", guest: 22, host: 2222

    trade.vm.synced_folder "data", "/srv/trade", create: true, owner: "vagrant", group: "vagrant", :mount_options => ['dmode=777', 'fmode=777']

    trade.vm.provider "virtualbox" do |vb_n|
      vb_n.gui = false
      vb_n.cpus = 2
      vb_n.memory = 40961
    end

  end
