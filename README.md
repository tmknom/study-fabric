# Fabric超入門

Fabric初心者向けに解説するよ！

## 事前準備

### Fabricのインストール

Fabricは事前にインストールしておいてほしい。

Macの場合はこんな感じでいけるぞ。

```bash
$ brew install fabric
$ fab -V
Fabric 1.10.1
```

2015年3月現在、Fabricに対応しているPythonのバージョンは2.5-2.7なので、3系の人は注意しよう。


### git clone＆Vagrantのボックスのダウンロード

vagrant上のCentOSに対し、色々とFabric経由で操作を行うので、事前にvagrant upしてボックスをダウンロードしておこう。

ボックスは「chef/centos-6.5」を使うので、使ったことがある人はvagrant up不要だ。

```bash
$ git clone git@github.com:tmknom/study-fabric.git
$ cd study-fabric
$ vagrant up
$ vagrant destroy -f
```





