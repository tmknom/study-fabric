from fabric.api import local, run, env, put, get, cd, lcd

env.hosts = ['192.168.103.10']
env.user = 'vagrant'
env.password = 'vagrant'


def execute():
  run("uname -a")


def upload():
  local("date > local.txt")
  put("local.txt", "~/")


def download():
  run("date > ~/remote.txt")
  get("~/remote.txt", ".")


def with_local():
  local("pwd")
  with lcd('../'):
    local("pwd")


def with_remote():
  run("pwd")
  with cd('/vagrant'):
    run("pwd")

