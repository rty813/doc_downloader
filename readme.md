# 多种文档下载器
本工具适用于下载豆丁、道客巴巴、淘豆网、原创力、新浪爱问、金锄头网站的可以预览的文档。只要可以预览，就可以下载。下载下来是图片格式，然后会通过reportlab库，将图片转换成PDF。

其中，由于新浪爱问网站用的都是svg格式的文件，将其转换成图片格式需要调用第三方库。Windows下可用svg2png库，Linux下可使用rsvg库。当然，在windows上面也可以安装rsvg库，需要下载CRAN，利用CRAN安装rsvg，实现svg的转换。

### 本项目还提供了一个简易的在线下载网页，[点击进入](http://129.211.158.185/)

## rsvg库安装方法
Binary packages for __OS-X__ or __Windows__ can be installed directly from CRAN:

```r
install.packages("rsvg")
```

Installation from source on Linux or OSX requires [`librsvg2`](https://developer.gnome.org/rsvg/). On __Debian__ or __Ubuntu__ install [librsvg2-dev](https://packages.debian.org/testing/librsvg2-dev):

```
sudo apt-get install -y librsvg2-dev
```

On __Fedora__, __CentOS or RHEL__ we need [librsvg2-devel](https://apps.fedoraproject.org/packages/librsvg2-devel):

```
sudo yum install librsvg2-devel
````

On __OS-X__ use [rsvg](https://github.com/Homebrew/homebrew-core/blob/master/Formula/librsvg.rb) from Homebrew:

```
brew install librsvg
```
## svg2png安装方法（仅限Windows操作系统）
```
1. 安装nodejs
2. 命令提示符内输入：npm install -g svg2png
3. 命令提示符内输入：Set-ExecutionPolicy -ExecutionPolicy 
```

## 本项目使用方法
终端内输入：
```
python docDownloader.py
```
