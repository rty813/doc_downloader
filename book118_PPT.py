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
    time.sleep(5)

    if os.path.exists(f'./temp/{title}'):
        shutil.rmtree(f'./temp/{title}')
    os.makedirs(f'./temp/{title}')

    pageCount = int(driver.find_element_by_id(
        'PageCount').get_attribute('innerHTML'))
    for i in trange(pageCount):
        driver.save_screenshot(f'temp/{title}/capture.png')
        page = driver.find_element_by_id('ppt')

        left = page.location['x']
        top = page.location['y']
        right = left + page.size['width']
        bottom = top + page.size['height'] - 35

        im = Image.open(f'temp/{title}/capture.png')
        im = im.crop((left, top, right, bottom))  # 元素裁剪
        im.save(f'temp/{title}/{i}.png')  # 元素截图
        driver.find_element_by_id('pageNext').click()
        time.sleep(1)  # 防止还没加载出来
    os.remove(f'./temp/{title}/capture.png')
    driver.quit()
    print('下载完毕，正在转码')
    conpdf(f'output/{title}.pdf', f'temp/{title}', '.png')


if __name__ == '__main__':
    download("https://max.book118.com/html/2019/1002/8052020057002053.shtm")
