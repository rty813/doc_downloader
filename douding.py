from bs4 import BeautifulSoup
import requests
from tqdm import trange
import urllib
import shutil
import os
from img2pdf import conpdf


def download(url):
    text = requests.get(url).text
    pos = text.index('allPage:')
    pages = int(text[pos + 8: pos + 12].split(',')[0])
    id = url.split('.')[-2].split('-')[-1]
    html = BeautifulSoup(text, features='lxml')
    title = html.title.string
    print(f'豆丁：《{title}》')

    if os.path.exists(f'./temp/{title}'):
        shutil.rmtree(f'./temp/{title}')
    os.makedirs(f'./temp/{title}')

    for i in trange(pages):
        url = f"http://211.147.220.164/index.jsp?file={id}&width=1600&pageno={i + 1}"
        response = urllib.request.urlopen(url)
        res = response.read()
        with open(f'./temp/{title}/{i+1}.jpg', 'wb') as f:
            f.write(res)
    print('下载完毕，正在转码')
    conpdf(f'output/{title}.pdf', f'./temp/{title}', '.jpg', True)


if __name__ == "__main__":
    download("https://www.docin.com/p-96519470.html")
