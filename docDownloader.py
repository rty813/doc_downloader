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

    while True:
        url = input("请输入网址（输入exit退出）：")
        if 'doc88' in url:
            import doc88
            doc88.download(url)
        elif 'book118' in url:
            from book118 import Book118
            from bs4 import BeautifulSoup
            import urllib
            html = BeautifulSoup(urllib.request.urlopen(
                url).read(), features='lxml')
            title = html.title.string[:-4]
            Book118(url.split('/')[-1].split('.')[0], title).getPDF()
        elif 'taodocs' in url:
            import taodocs
            taodocs.download(url)
        elif 'exit' in url:
            conn.close()
            break
        else:
            print('暂不支持')
        insertDB(url)


if __name__ == "__main__":
    fire.Fire(main)
    # "https://www.doc88.com/p-6099938057537.html"
