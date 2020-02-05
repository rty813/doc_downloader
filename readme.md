# 多种文档下载器
本工具适用于下载豆丁、道客巴巴、淘豆网、原创力、新浪爱问、金锄头网站的可以预览的文档。只要可以预览，就可以下载。下载下来是图片格式，然后会通过reportlab库，将图片转换成PDF。

其中，由于新浪爱问网站用的都是svg格式的文件，将其转换成图片需要调用svg2png库。因此，需要先安装nodejs，再利用npm安装svg2png，然后才能正常使用。

## 使用方法
```
1. 安装nodejs
2. 命令提示符内输入：npm install -g svg2png
3. 命令提示符内输入：Set-ExecutionPolicy -ExecutionPolicy RemoteSigned
4. 命令提示符内输入：python docDownloader.py
```