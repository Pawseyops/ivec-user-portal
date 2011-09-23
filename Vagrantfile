Vagrant::Config.run do |config|
  config.vm.box = "centos56_django13"
  config.vm.forward_port "django", 8000, 8000
  config.vm.provision :shell, :inline => "sleep 30; createdb -Upostgres ivecallocation"
  config.vm.provision :shell, :inline => "psql -Upostgres ivecallocation < /vagrant/ivecallocation/sql/*.sql"
end
