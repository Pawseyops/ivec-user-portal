Vagrant::Config.run do |config|
  config.vm.box = "centos56"
  config.vm.forward_port "django", 8000, 8000
  config.vm.provision :shell, :inline => "sudo easy_install-2.6 /vagrant/ivecallocation/eggs/*.*"
  config.vm.provision :shell, :inline => "createdb -Upostgres ivecallocation || (echo 'Postgres is probably not up yet, trying again in 10 seconds...'; sleep 10; createdb -Upostgres ivecallocation)"
  config.vm.provision :shell, :inline => "cd /vagrant/ivecallocation; python26 manage.py syncdb --noinput; python26 manage.py migrate"
end
