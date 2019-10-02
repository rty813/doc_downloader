import fire
import pymysql
import os

conn = None


def insertDB(url):
    cursor = conn.cursor()
    sql = f"INSERT INTO history(url) VALUES ('{url}');"
    cursor.execute(sql)
    conn.commit()
    cursor.close()


def main():
    global conn
    conn = pymysql.connect("orca-tech.cn", "root", "orcatech", "doc_download")
    if not os.path.exists('./temp'):
        os.mkdir('./temp')
    if not os.path.exists('./output'):
        os.mkdir('./output')

    while True:
        url = input("请输入网址（输入exit退出）：")
        if 'doc88' in url:
            # 道客巴巴
            import doc88
            doc88.download(url)
        elif 'book118' in url:
            # 原创力
            from book118 import Book118
            from bs4 import BeautifulSoup
            import urllib
            html = BeautifulSoup(urllib.request.urlopen(
                url).read(), features='lxml')
            title = html.title.string[:-4]
            Book118(url.split('/')[-1].split('.')[0], title).getPDF()
        elif 'taodocs' in url:
            # 淘豆网
            import taodocs
            taodocs.download(url)
        elif 'docin' in url:
            # 豆丁
            # http://211.147.220.164/index.jsp?file=96519470&width=800&pageno=1
            import douding
            douding.download(url)
        # elif 'jinchutou' in url:
        #     # 金锄头
        #     import jinchutou
        #     jinchutou.download(url)
        elif 'ishare' in url:
            import ishare
            ishare.download(url)
        elif 'exit' in url:
            conn.close()
            break
        else:
            print('暂不支持')

        try:
            insertDB(url)
        except Exception:
            pass


if __name__ == "__main__":
    fire.Fire(main)
    # "https://www.doc88.com/p-6099938057537.html"
