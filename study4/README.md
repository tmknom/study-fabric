# 複数サーバへの実行に挑戦する！ 

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
$ fab install:jq -u ec2-user -i ~/.ssh/playground-development.pem -H xx.xx.xx.xx,yy.yy.yy.yy
```

すると、順番にjqコマンドがインストールされることが確認できるはずだ。


## 並列実行

次に二台のサーバに対して、並列にパッケージをインストールしてみよう。

fabコマンド実行時に -P オプションをつけるだけで並列実行になる。

ここでは、試しにgitをインストールしてみよう。

```bash
$ fab install:git -u ec2-user -i ~/.ssh/playground-development.pem -P -H xx.xx.xx.xx,yy.yy.yy.yy
```

二台のサーバに同時並行で、gitのインストールが確認できればOKだ！


## 免許皆伝

ここまで到達したキミは、Star Warsでいえばマスターヨーダだ。

チームの伝道師として、ぜひFabricを役立ててほしい。

きっとチームの武器になるはずだ！

オツカレサマでした！

