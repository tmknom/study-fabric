# リモートサーバを操作してみよう！

## リモート環境の構築

擬似的にリモートサーバを作成するため、Vagrantfileを用意する。

```bash
$ vi Vagrantfile

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "chef/centos-6.5"
  config.vm.network :private_network, ip: "192.168.102.10"
end
```

では起動しよう。

```bash
$ vagrant up
```


## リモート接続の確認

まずは、fabfile.pyを作成しよう。

今は詳細を無視して、とりあえず、このままコピペしてほしい。

```bash
$ vi fabfile.py

from fabric.api import run, sudo

def connect():
  run("uname -a")
```

では、実行だ。

ここでのポイントは、接続先ホスト、ログインユーザ名、パスワードを指定しているところだ。

```bash
$ fab connect -H 192.168.102.10 -u vagrant -p vagrant
[192.168.102.10] Executing task 'connect'
[192.168.102.10] run: uname -a
[192.168.102.10] out: Linux localhost.localdomain 2.6.32-431.el6.x86_64 #1 SMP 
Fri Nov 22 03:15:09 UTC 2013 x86_64 x86_64 x86_64 GNU/Linux
[192.168.102.10] out:


Done.
Disconnecting from 192.168.102.10... done.
```

こんな感じで表示されればOKだ！


## リモートでコマンド実行 

もう気付いてると思うけど、リモートでコマンドを実行するには、runメソッドを使うだけでOKだ！

先ほどのfabfile.pyにremote_runタスクを追記しよう。

```bash
$ vi fabfile.py

def remote_run():
  run("whoami")
  run("date > remote_run.log")
```

実行してみよう。


```bash
$ fab remote_run -H 192.168.102.10 -u vagrant -p vagrant
```

リモートサーバにログインして確認してみよう。

```bash
$ vagrant ssh
[vagrant ~]$ cat remote_run.log
Sun Feb 15 15:41:12 UTC 2015
```

たしかに、時刻情報が書かれたファイルが作成できたね！


## リモートでsudo実行

リモートでsudoを実行したい場合、そのままズバリ、sudoメソッドを使えばOKだ！

fabfile.pyにremote_sudoタスクを追記してみよう。

```bash
$ vi fabfile.py

def remote_sudo():
  sudo("whoami")
  sudo("yum -y install httpd")
  sudo("whoami > remote_sudo_root.log")
```

では実行してみよう。


```bash
$ fab remote_sudo -H 192.168.102.10 -u vagrant -p vagrant
```

ログインして確認してみよう。


```bash
$ vagrant ssh
[vagrant ~]$ which httpd
/usr/sbin/httpd
[vagrant ~]$ cat remote_sudo_root.log
root
```

sudoでコマンド実行されたことが確認できたね！


## リモートでsudoを別ユーザで実行

単にsudoするだけではなく、別ユーザとして実行することもできる。

そのためには、sudoメソッドの第二引数にユーザ名を指定しよう。

では、fabfile.pyにremote_sudo_other_userタスクを追記しよう。

```bash
$ vi fabfile.py

def remote_sudo_other_user():
  sudo("whoami > remote_sudo_vagrant.log", user='vagrant')
```

実行してみる。

```bash
$ fab remote_sudo_other_user -H 192.168.102.10 -u vagrant -p vagrant
```

では、確認だ。


```bash
$ vagrant ssh

[vagrant ~]$ cat remote_sudo_vagrant.log
vagrant

[vagrant ~]$ ls -l
合計 12
-rw-rw-r--. 1 vagrant vagrant 29  2月 15 16:02 2015 remote_run.log
-rw-r--r--. 1 root    root     5  2月 15 16:13 2015 remote_sudo_root.log
-rw-rw-r--. 1 vagrant vagrant  8  2月 15 16:15 2015 remote_sudo_vagrant.log
```

確かに指定したユーザで実行されたことが確認できるね。


## 基本は以上

「えっ、こんだけ？」と思われるかもしれないが、これだけだ。

実行したいコマンドをrunかsudoで囲めば終了という、圧倒的な学習コストの低さがFabricの魅力なのだ！

では、最後に忘れずに後始末しておこう。

```bash
$ vagrant destroy -f
```

