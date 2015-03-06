# ファイルの送受信と実行ディレクトリの指定

## リモート環境の構築

改めてVagrantfileを用意する。

study2と違うのはIPアドレスだけなので、study2のモノをそのまま流用してもらってもいいぞ！

```ruby
$ vi Vagrantfile

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "chef/centos-6.5"
  config.vm.network :private_network, ip: "192.168.103.10"
end
```

では起動しよう。

```bash
$ vagrant up
```

## 接続先ホストの設定

study2では接続先情報をコマンドの引数で渡していたけど、fabfile.pyに事前に書いておくこともできる。

```python
$ vi fabfile.py

from fabric.api import local, run, env, put, get, cd, lcd

env.hosts = ['192.168.103.10']
env.user = 'vagrant'
env.password = 'vagrant'

def execute():
  run("uname -a")
```

ユースケースに応じてぜひ使い分けてほしい。

メンドウなので、ここでは、fabfile.pyに接続先情報を書いてある前提でコマンドを実行していくぞ。

```bash
$ fab execute
```


## SFTPでファイルアップロード

デプロイスクリプトとしてFabricを活用する場合、ファイルアップロードをしたくなるケースも多い。

そんな時は、putメソッドを使おう！

```python
$ vi fabfile.py

def upload():
  local("date > local.txt")
  put("local.txt", "~/")
```

では、実行してみよう。

```bash
$ fab upload
```

確認してみよう。

```bash
$ cat local.txt
2015年 2月16日 月曜日 01時41分31秒 JST

$ vagrant ssh

[vagrant ~]$ cat ~/local.txt
2015年 2月16日 月曜日 01時41分31秒 JST
```

確かに、ローカルに作成されたファイルが、サーバへもアップロードされているね！



## SFTPでファイルダウンロード

アップロードではなく、ダウンロードを行いたい場合もある。

そんな時は、getメソッドを使おう！

```python
$ vi fabfile.py

def download():
  run("date > ~/remote.txt")
  get("~/remote.txt", ".")
```

実行してみる。

```bash
$ fab download 
```

では、確認だ。

```bash
$ vagrant ssh

[vagrant ~]$ cat ~/remote.txt
Sun Feb 15 16:42:53 UTC 2015

$ cat remote.txt
Sun Feb 15 16:42:53 UTC 2015
```

たしかに、リモートで作成されたファイルが、ダウンロードできているね！


## ローカルの指定のディレクトリで処理を実行

ローカルの指定のディレクトリで処理を実行したいってケース、たまによくあるよね！

そんな時は、with構文＋lcdメソッドを使おう。

```python
$ vi fabfile.py

def with_local():
  local("pwd")
  with lcd('../'):
    local("pwd")
```

実行してみよう。

```bash
$ fab with_local
[192.168.103.10] Executing task 'with_local'
[localhost] local: pwd
/path/to/study-fabric/study3
[localhost] local: pwd
/path/to/study-fabric/

Done.
```

２つ目のpwdコマンドが、キチンとcdされて実行されているね！


## リモートの指定のディレクトリで処理を実行

ローカルではなく、リモートでディレクトリを指定した場合ももちろんあると思う。

予想はつくと思うけど、with構文＋cdメソッドを使えばOKだ。

```python
$ vi fabfile.py

def with_remote():
  run("pwd")
  with cd('/vagrant'):
    run("pwd")
```

実行してみよう。

```bash
$  fab with_remote
[192.168.103.10] Executing task 'with_remote'
[192.168.103.10] run: pwd
[192.168.103.10] out: /home/vagrant
[192.168.103.10] out:

[192.168.103.10] run: pwd
[192.168.103.10] out: /vagrant
[192.168.103.10] out:


Done.
Disconnecting from 192.168.103.10... done.
```

ローカルの時と同様、cdされて実行されていることが確認できた！


## 達人クラス

もうこの時点でキミはFabricの達人と言えるレベルに到達したぞ！

Fabric単体でできることは、この時点でほぼできるようになっているはずだ。

もちろん、Fabricには他にも色々機能があって、もっと複雑なこともできるけど、まずはシンプルに使い始めよう！

ここから先は[Fabricのドキュメント](http://fabric-ja.readthedocs.org/ja/latest/)を必要に応じて参照するぐらいで十分だ。


## 後始末

では、忘れずに後始末しておく。

```bash
$ vagrant destroy -f
```

