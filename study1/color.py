from fabric.colors import green, red

def success():
  print(green("build success!"))

def failure():
  print(red("build failure!!"))


