from fabric.api import sudo

def install(package_name):
  sudo("yum -y install %s" % (package_name))

