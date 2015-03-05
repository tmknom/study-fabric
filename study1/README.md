# Fabric事始め

## Hello, World!

まずはお決まりのアレをやっとこう。

```python
$ vi fabfile.py

def hello():
  print("Hello world!")
```

確認してみよう。

```bash
$ fab hello
Hello world!

Done.
```

最初の一歩はOKだ！

## 実行ファイルを指定

fabコマンドはデフォルトでfabfile.pyの内容を実行する。

しかし、もちろん任意のファイルを実行することもできるぞ。

```python
$ vi message.py

def bye():
  print("Good bye!")
```

実行ファイルを指定してみよう。

```bash
$ fab bye -f message.py
Good bye!

Done.
```

ちゃんと表示されたね！


## 複数タスク実行

複数のタスクも同時に実行できる。

```bash
$ fab one two -f multitask.py
one!
two!!

Done.
```

これを駆使すれば、必要なタスクだけ実行することができるぞ！

## 実行できるタスクの確認


実行可能なタスクは--listオプションを使うと見れる。

```bash
$ fab -f multitask.py --list
Available commands:

    one
    two
```

message.pyでは二つのメソッドを定義していて、それがきちんと表示されたね！


## カラー出力

fabricでは簡単にカラー出力もできる。

```python
$ vi color.py

from fabric.colors import green, red

def success():
  print(green("build success!"))

def failure():
  print(red("build failure!!"))
```

それぞれ実行してみよう。

```bash
$ fab success -f color.py
$ fab failure -f color.py
```

最初は緑、次は赤で表示されれば成功だ！


## タスク定義

fabricでは、タスクを明示的に指定できる。メソッド名の上に"@task"とつけるだけでいい。

```python
$ vi task.py

from fabric.decorators import task

@task
def deploy():
  task_one()
  task_two()

def task_one():
  print("one!")

def task_two():
  print("two!!")
```

確認してみよう。

```bash
$ fab -f task.py --list
Available commands:

    deploy
```

タスク一覧に@taskがついてるメソッドだけ表示されたね。

では、実行してみよう。

```bash
$ fab deploy -f task.py
one!
two!!

Done.
```

なお、タスク定義してない場合はエラーで落ちるぞ。

```bash
$ fab task_one -f task.py
Warning: Command(s) not found:
    task_one

Available commands:

    deploy
```


## タスク引数

タスクには実行時に引数を渡すこともできる。

```python
$ vi switch.py

def env(environment = "development"):
  print(environment)
```

確認してみよう。まずは、引数なしの場合。

```bash
$ fab env -f switch.py
development

Done.
```

メソッドのデフォルト引数の「development」が表示されたね！

次に引数を渡してみよう。"タスク名:引数の値"で渡せる。

```bash
$ fab env:production -f switch.py
production

Done.
```


## ローカルでコマンド実行

いよいよローカルでのコマンド実行を試してみるぞ。localメソッドを使うだけで実現できる。

```python
$ vi local.py

from fabric.api import local

def pwd():
  local("pwd")
```

では確認してみよう。

```bash
$ fab pwd -f local.py
[localhost] local: pwd
/path/to/study-fabric/study1

Done.
```

無事、ローカルでコマンド実行できた！


## 途中で失敗した場合

Fabricは途中でエラーが有った場合、自動でストップする。

```python
$ vi failure.py

from fabric.api import local

def failure():
  local("ls")
  local("ls ../")
  local("ls invalid_dir")
  local("ls /")
```

確認してみよう。

```bash
$ fab failure -f failure.py
・・・
[localhost] local: ls invalid_dir
ls: invalid_dir: No such file or directory

Fatal error: local() encountered an error (return code 1) while executing 'ls invalid_dir'

Aborting.
local() encountered an error (return code 1) while executing 'ls invalid_dir'
```

3つめのlsコマンドでエラーが出て、止まったことが確認できた！


