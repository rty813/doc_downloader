import doc88
import fire
import pymysql

conn = None


def insertDB(url):
    cursor = conn.cursor()
    sql = f"INSERT INTO history(url) VALUES ('{url}');"
    cursor.execute(sql)
    conn.commit()
    cursor.close()


def main(debuggable=False, filename=None):
    global conn
    conn = pymysql.connect("orca-tech.cn", "root", "orcatech", "doc_download")

    while True:
        url = input("请输入网址（输入exit退出）：")
        if 'doc88' in url:
            import doc88
            doc88.download(url, filename, debuggable)
        elif 'exit' in url:
            conn.close()
            break
        else:
            print('暂不支持')
        insertDB(url)


if __name__ == "__main__":
    fire.Fire(main)
    # "https://www.doc88.com/p-6099938057537.html"
