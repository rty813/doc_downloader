from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException

import base64
import time
import sys
import os
import shutil
from tqdm import trange
from img2pdf import conpdf
from PIL import Image


def download(url):
    option = webdriver.ChromeOptions()
    # option.add_argument('headless')
    option.add_argument('log-level=3')
    driver = webdriver.Chrome(
        executable_path='.//chromedriver', chrome_options=option)

    title = "output"
    try:
        driver.set_page_load_timeout(15)
        driver.get(url)
        title = driver.title
    except:
        print("Timeout - start download anyway.")

    print(f'原创力: 《{title}》')
    time.sleep(5)

    driver.find_element_by_id('btn_preview_remain').click()

    time.sleep(2)
    frame = driver.find_elements_by_class_name('preview-iframe')[0]
    src = frame.get_attribute('src')
    print(src)

    driver.get(src)
    time.sleep(3)

    driver.maximize_window()  # 最大化当前页
    time.sleep(3)

    if not os.path.exists('./output'):
        os.mkdir('./output')

    if os.path.exists(f'./temp/{title}'):
        shutil.rmtree(f'./temp/{title}')
    os.makedirs(f'./temp/{title}')

    pageCount = int(driver.find_element_by_id('PageCount').get_attribute('innerHTML'))

    pageIndex = 0  # 当前页数
    imageIndex = 0  # 保存图片用的索引
    saveEveryAction = False  # TODO 是否需要保存每一个动画

    # 修改窗口为ptt比例，这样就不用截图后裁剪了
    window_size = driver.get_window_size()  # 浏览器窗口的大小
    html = driver.find_element_by_tag_name('html')  # PPT底部，到浏览器顶部的大小
    page = driver.find_element_by_id('ppt')  # PPT显示部分的大小

    diff_height = window_size['height'] - html.size['height'] * 2 + page.size['height']  # 浏览器高度上，额外的部分（标签栏）
    driver.set_window_size(page.size['width'], page.size['height'] + diff_height)

    # 如何处理动画：使用“下一个动画”按钮，点击一次，就截图。然后根据 不同图片索引 保存文件

    while pageIndex < pageCount:
        pageIndex = int(driver.find_element_by_id('PageIndex').get_attribute('innerHTML'))
        print(f'循环，当前页：{pageIndex}，当前图片索引：{imageIndex}')

        # 不同的保存策略
        if saveEveryAction:
            imageIndex = pageIndex  # 每页只保留一页-->同一页，使用相同名称保存，文件会覆盖，则最后保留的就只有一页
        else:
            imageIndex += 1  # 每一个动画都保存一页

        driver.save_screenshot(f'temp/{title}/{imageIndex}.png')
        driver.find_element_by_class_name('btmRight').click()  # 点击“下一个动画”按钮
        time.sleep(2)  # 用于加载。TODO 如果截图时，动画没有完成，则放宽此时间

    driver.quit()
    print('下载完毕，正在转码')
    conpdf(f'output/{title}.pdf', f'temp/{title}', '.png')


if __name__ == '__main__':
    download("https://max.book118.com/html/2021/1211/7136026114004063.shtm")
