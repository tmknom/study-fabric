# -*- encoding:utf-8 -*-

from fabric.api import local

def failure():
  local("ls")
  local("ls ../")
  local("ls invalid_dir")
  local("ls /")

