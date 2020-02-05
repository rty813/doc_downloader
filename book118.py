import re
import json
import os
import shutil
import ssl
import urllib.request
from tqdm import tqdm
from img2pdf import conpdf


def makeURL(host, args):
    url = host
    for key in args:
        url += key + '=' + args[key] + '&'
    url = url[0:-1]
    return url


def getHTML(url, byte=False):
    # print("getting " + url)
    response = urllib.request.urlopen(url)
    html = response.read()
    if not byte:
        html = html.decode('utf-8')
    return html


class Book118:
    def __init__(self, pid, title, url):
        ssl._create_default_https_context = ssl._create_unverified_context
        self.pid = str(pid)
        self.title = '原创力 ' + title.replace('-文档在线预览', '')
        self.url = url
        self.pdfInfo = {}
        self.domain = ''
        self.index = -1
        self.total = 0
        self.imgList = []

    def getPDF(self):
        try:
            print(self.title)
            # 获取需要的信息
            self.__getPdfInfo()
            #　获得所有图片的地址
            img = self.pdfInfo.get('Img')
            imgUrl = img if img != None else ""
            print('解析地址')
            while self.index != self.total:
                self.__getNextPage(
                    self.imgList[-1]
                    if len(self.imgList) != 0 else imgUrl)
            self.pbar.close()
            # 下载图片
            self.__getIMG()
            # 生成pdf
            print('下载完毕，正在转码')
            conpdf(f'output/{self.title}.pdf', f'temp/{self.title}/', '.jpg')
        except Exception:
            import book118_PPT
            book118_PPT.download(self.url)

    def __getPdfInfo(self):
        url = makeURL('https://max.book118.com/index.php?',
                      {
                          'g': 'Home',
                          'm': 'View',
                          'a': 'viewUrl',
                          'cid': str(self.pid),
                          'flag': '1'
                      })
        viewPage = getHTML(url)
        self.domain = re.findall(r'//(.*?)\..*', viewPage)[0]
        rawHTML = getHTML('https:' + viewPage)
        res = re.findall(
            r'<input type="hidden" id="(.*?)" value="(.*?)".*?/>', rawHTML)
        for lst in res:
            self.pdfInfo[lst[0]] = lst[1]
        for info in self.pdfInfo.items():
            print(info)

    def __getNextPage(self, imgUrl):
        url = makeURL('https://' + self.domain + '.book118.com/PW/GetPage/?', {
            'f': self.pdfInfo['Url'],
            'img': imgUrl,
            'isMobile': 'false',
            'isNet': 'True',
            'readLimit': self.pdfInfo['ReadLimit'],
            'furl': self.pdfInfo['Furl']
        })
        result = getHTML(url)
        res = json.loads(result)

        if self.total == 0:
            self.total = res['PageCount']
            self.pbar = tqdm(total=self.total)
            self.pbar.update(1)
        else:
            self.pbar.update(1)
        self.index = res['PageIndex']
        self.imgList.append(res['NextPage'])

        # print(self.index, '/', self.total, 'url finish', res['NextPage'])

        return res

    def __getIMG(self):
        print('下载图片')
        if os.path.exists(f'./temp/{self.title}'):
            shutil.rmtree(f'./temp/{self.title}')
        os.makedirs(f'./temp/{self.title}')
        with tqdm(total=len(self.imgList)) as pbar:
            for (idx, img) in enumerate(self.imgList):
                pbar.update(1)
                res = getHTML(
                    makeURL('http://' + self.domain + '.book118.com/img/?', {'img': img}), byte=True)
                with open(f'./temp/{self.title}/{idx+1}.jpg', 'wb') as f:
                    f.write(res)
