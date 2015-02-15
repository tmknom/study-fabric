# -*- encoding:utf-8 -*-

from fabric.api import local

def run():
  pwd()
  hostname()

def pwd():
  local("pwd")

def hostname():
  local("hostname")

