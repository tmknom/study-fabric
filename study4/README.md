# 複数サーバへの実行に挑戦する！ 

## リモート環境の構築

これまでと異なり、二台のサーバを立ち上げるVagrantfileを用意しよう。

```ruby
$ vi Vagrantfile

VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "chef/centos-6.5"

  config.vm.define "web_server" do |web|
    web.vm.network :private_network, ip: "192.168.104.10"
    web.vm.hostname = "web-server"
  end

  config.vm.define "db_server" do |db|
    db.vm.network :private_network, ip: "192.168.104.11"
    db.vm.hostname = "db-server"
  end

end
```

では起動しよう。

```bash
$ vagrant up
```

## 実行するfabfile.pyの作成

ここでは、任意のパッケージをインストールするfabfile.pyを作成してみよう。

```python
$ vi fabfile.py

from fabric.api import sudo

def install(package_name):
  sudo("yum -y install %s" % (package_name))
```


## 直列実行

最初に二台のサーバに対して、直列にパッケージをインストールしてみよう。

ポイントは、カンマ区切りで２つのIPアドレスを指定する部分だ。

ここでは、試しにhttpdをインストールしてみる。

```bash
$ fab install:httpd -H 192.168.104.10,192.168.104.11 -u vagrant -p vagrant
```

すると、順番にhttpdがインストールされることが確認できるはずだ。


## 並列実行

次に二台のサーバに対して、並列にパッケージをインストールしてみよう。

fabコマンド実行時に -P オプションをつけるだけで並列実行になる。

ここでは、試しにmysql-serverをインストールしてみよう。

```bash
$ fab install:mysql-server -P -H 192.168.104.10,192.168.104.11 -u vagrant -p vagrant
```

二台のサーバに同時並行で、mysql-serverのインストールが確認できればOKだ！


## 免許皆伝

ここまで到達したキミは、Star Warsでいえばマスターヨーダだ。

チームの伝道師として、ぜひFabricを役立ててほしい。

きっとチームの武器になるはずだ！


## 後始末

では、最後に後始末して終了としよう。

```bash
$ vagrant destroy -f
```

オツカレサマでした！

