# リモートサーバを操作してみよう！

## SSHの確認

Fabricの前にSSHで接続できることを確認しておこう。

あとで、Fabricの実行結果を確認するのにログインするので、別ターミナルを立ち上げておくのがオススメだ。

```bash
$ ssh -l ec2-user -i ~/.ssh/playground-development.pem xx.xx.xx.xx
```


## リモート接続の確認

まずは、fabfile.pyを作成しよう。

今は詳細を無視して、とりあえず、このままコピペしてほしい。

```python
$ vi fabfile.py

from fabric.api import run, sudo

def connect():
  run("uname -a")
```

では、実行だ。

ここでのポイントは、接続先ホスト、ログインユーザ名、SSH鍵を指定しているところだ。

```bash
$ fab connect -u ec2-user -i ~/.ssh/playground-development.pem -H xx.xx.xx.xx
[xx.xx.xx.xx] Executing task 'connect'
[xx.xx.xx.xx] run: uname -a
[xx.xx.xx.xx] out: Linux ip-xx-xx-xx-xx 4.4.11-23.53.amzn1.x86_64 #1 SMP Wed Jun 1 22:22:50 UTC 2016 x86_64 x86_64 x86_64 GNU/Linux
[xx.xx.xx.xx] out:

Done.
Disconnecting from xx.xx.xx.xx... done.
```

こんな感じで表示されればOKだ！


## リモートでコマンド実行 

もう気付いてると思うけど、リモートでコマンドを実行するには、runメソッドを使うだけでOKだ！

先ほどのfabfile.pyにremote_runタスクを追記しよう。

```python
$ vi fabfile.py

def remote_run():
  run("whoami")
  run("date > /tmp/remote_run.log")
```

実行してみよう。


```bash
$ fab remote_run -u ec2-user -i ~/.ssh/playground-development.pem -H xx.xx.xx.xx
```

リモートサーバにログインして確認してみよう。

```bash
[remote ~]$ cat /tmp/remote_run.log
Thu Aug  4 02:01:00 UTC 2016
```

たしかに、時刻情報が書かれたファイルが作成できたね！


## リモートでsudo実行

リモートでsudoを実行したい場合、そのままズバリ、sudoメソッドを使えばOKだ！

fabfile.pyにremote_sudoタスクを追記してみよう。

```python
$ vi fabfile.py

def remote_sudo():
  sudo("whoami")
  sudo("yum -y install httpd")
  sudo("whoami > /tmp/remote_sudo_root.log")
```

では実行してみよう。


```bash
$ fab remote_sudo -u ec2-user -i ~/.ssh/playground-development.pem -H xx.xx.xx.xx
```

リモートサーバ側で確認してみよう。


```bash
[remote ~]$ which httpd
/usr/sbin/httpd
[remote ~]$ cat /tmp/remote_sudo_root.log
root
```

sudoでコマンド実行されたことが確認できたね！


## リモートでsudoを別ユーザで実行

単にsudoするだけではなく、別ユーザとして実行することもできる。

そのためには、sudoメソッドの第二引数にユーザ名を指定しよう。

では、fabfile.pyにremote_sudo_other_userタスクを追記しよう。

```python
$ vi fabfile.py

def remote_sudo_other_user():
  sudo("whoami > /tmp/remote_sudo_apache.log", user='apache')
```

実行してみる。

```bash
$ fab remote_sudo_other_user -u ec2-user -i ~/.ssh/playground-development.pem -H xx.xx.xx.xx
```

では、確認だ。


```bash
[remote ~]$ cat /tmp/remote_sudo_apache.log
apache
[remote ~]$ ls -l /tmp/*.log
-rw-rw-r-- 1 ec2-user ec2-user 29  8月  4 02:01 /tmp/remote_run.log
-rw-r--r-- 1 apache   apache    7  8月  4 02:03 /tmp/remote_sudo_apache.log
-rw-r--r-- 1 root     root      5  8月  4 02:02 /tmp/remote_sudo_root.log
```

確かに指定したユーザで実行されたことが確認できるね。


## 基本は以上

「えっ、こんだけ？」と思われるかもしれないが、これだけだ。

実行したいコマンドをrunかsudoで囲めば終了という、圧倒的な学習コストの低さがFabricの魅力なのだ！

こんなに簡単で便利なのに、使わない手はないよね！！

