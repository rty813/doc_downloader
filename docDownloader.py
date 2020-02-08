import fire
import os

def main():
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
            import book118
            book118.download(url)
        elif 'taodocs' in url:
            # 淘豆网
            import taodocs
            taodocs.download(url)
        elif 'docin' in url:
            # 豆丁
            import douding
            douding.download(url)
        elif 'jinchutou' in url:
            # 金锄头
            import jinchutou
            jinchutou.download(url)
        elif 'ishare' in url:
            import ishare
            ishare.download(url)
        elif 'exit' in url:
            break
        else:
            print('暂不支持')

if __name__ == "__main__":
    fire.Fire(main)
    # "https://www.doc88.com/p-6099938057537.html"
