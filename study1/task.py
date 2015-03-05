from fabric.decorators import task

@task
def deploy():
  task_one()
  task_two()

def task_one():
  print("one!")

def task_two():
  print("two!!")

