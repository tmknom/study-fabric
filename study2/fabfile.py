from fabric.api import run, sudo 

def connect():
  run("uname -a")

def remote_run():
  run("whoami")
  run("date > /tmp/remote_run.log")

def remote_sudo():
  sudo("whoami")
  sudo("yum -y install httpd")
  sudo("whoami > /tmp/remote_sudo_root.log")

def remote_sudo_other_user():
  sudo("whoami > /tmp/remote_sudo_apache.log", user='apache')

