# -*- encoding:utf-8 -*-

from fabric.api import run, sudo 

def connect():
  run("uname -a")

def remote_run():
  run("whoami")
  run("date > remote_run.log")

def remote_sudo():
  sudo("whoami")
  sudo("yum -y install httpd")
  sudo("whoami > remote_sudo_root.log")

def remote_sudo_other_user():
  sudo("whoami > remote_sudo_vagrant.log", user='vagrant')

