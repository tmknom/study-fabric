from fabric.api import local, run, env, put, get, cd, lcd

env.hosts = ['xx.xx.xx.xx']
env.user = 'ec2-user'
env.key_filename = ['~/.ssh/playground-development.pem']


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
  with cd('../'):
    run("pwd")

