Vagrant::Config.run do |config|
  config.vm.box = "centos56"
  config.vm.forward_port "django", 8000, 8000
  config.vm.provision :shell, :inline => "createdb -Upostgres ivecallocation || (echo 'Postgres is probably not up yet, trying again in 10 seconds...'; sleep 10; createdb -Upostgres ivecallocation)"
  config.vm.provision :shell, :inline => "cd /vagrant/ivecallocation; sh bootstrap.sh -p python26"
  config.vm.provision :shell, :inline => "cd /vagrant/ivecallocation; virt_ivecallocation/bin/python manage.py syncdb --noinput; virt_ivecallocation/bin/python manage.py migrate"
end
