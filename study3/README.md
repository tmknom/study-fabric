# ファイルの送受信と実行ディレクトリの指定

## 接続先ホストの設定

study2では接続先情報をコマンドの引数で渡していたけど、fabfile.pyに事前に書いておくこともできる。

```python
$ vi fabfile.py

from fabric.api import local, run, env, put, get, cd, lcd

env.hosts = ['xx.xx.xx.xx']
env.user = 'ec2-user'
env.key_filename = ['~/.ssh/playground-development.pem']

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
2016年 8月 4日 木曜日 11時09分22秒 JST

[remote ~]$ cat ~/local.txt
2016年 8月 4日 木曜日 11時09分22秒 JST
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
[remote ~]$ cat ~/remote.txt
Thu Aug  4 02:11:06 UTC 2016

$ cat remote.txt
Thu Aug  4 02:11:06 UTC 2016
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
[xx.xx.xx.xx] Executing task 'with_local'
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
  with cd('../'):
    run("pwd")
```

実行してみよう。

```bash
$  fab with_remote
[xx.xx.xx.xx] Executing task 'with_remote'
[xx.xx.xx.xx] run: pwd
[xx.xx.xx.xx] out: /home/ec2-user
[xx.xx.xx.xx] out:

[xx.xx.xx.xx] run: pwd
[xx.xx.xx.xx] out: /home
[xx.xx.xx.xx] out:


Done.
Disconnecting from xx.xx.xx.xx... done.
```

ローカルの時と同様、cdされて実行されていることが確認できた！


## 達人クラス

もうこの時点でキミはFabricの達人と言えるレベルに到達したぞ！

Fabric単体でできることは、この時点でほぼできるようになっているはずだ。

もちろん、Fabricには他にも色々機能があって、もっと複雑なこともできるけど、まずはシンプルに使い始めよう！

ここから先は[Fabricのドキュメント](http://fabric-ja.readthedocs.org/ja/latest/)を必要に応じて参照するぐらいで十分だ。

