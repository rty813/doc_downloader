from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, JavascriptException

import base64
import time
import sys
import os
from tqdm import trange
from img2pdf import conpdf
import requests
import os
from PIL import Image
import shutil


def download(url):
    option = webdriver.ChromeOptions()
    option.add_argument('headless')
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

    print(f'新浪爱问: 《{title}》')
    time.sleep(5)

    lastPageNum = None
    while True:
        try:
            driver.execute_script("window.scrollBy(0,10000)")
            time.sleep(1)
            # 展开全部
            elem_cont_button = driver.find_element_by_class_name(
                "state-bottom")
            elem_cont_button = elem_cont_button.find_element_by_tag_name('a')
            text = elem_cont_button.find_element_by_tag_name(
                'p').get_attribute('innerHTML')
            if text == lastPageNum:
                print('收费文档！无法下载')
                driver.quit()
                return
            lastPageNum = text
            if '结束' in text or '>0</em>' in text:
                break
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", elem_cont_button)
            actions = ActionChains(driver)
            actions.move_to_element(elem_cont_button).perform()
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", elem_cont_button)
        except JavascriptException:
            continue
    # 获取页数
    num_of_pages = driver.find_element_by_class_name(
        'page-input-con').find_element_by_tag_name('span').get_attribute('innerHTML')
    num_of_pages = int(num_of_pages)
    driver.execute_script("window.scrollBy(0,10000)")

    if os.path.exists(f'./temp/{title}'):
        shutil.rmtree(f'./temp/{title}')
    os.makedirs(f'./temp/{title}')

    imgs = driver.find_elements_by_class_name('data-detail')
    for pages in trange(num_of_pages):
        try:
            # svg格式
            imgUrl = imgs[pages].find_element_by_tag_name(
                'embed').get_attribute('src')
            html = requests.get(imgUrl).content
            with open(f'./temp/{title}/{title}.svg', 'wb') as svgFile:
                svgFile.write(html)
                svgFile.flush()
                os.system(
                    f'svg2png "./temp/{title}/{title}.svg" -o "./temp/{title}/{title}.png" -w 1500')
                im = Image.open(f'./temp/{title}/{title}.png')
                bg = Image.new('RGB', im.size, (255, 255, 255))
                bg.paste(im, im)
                bg.save(f'./temp/{title}/{pages}.jpg')
                os.remove(f'./temp/{title}/{title}.png')
            os.remove(f'./temp/{title}/{title}.svg')
        except NoSuchElementException:
            # 图片格式
            while True:
                try:
                    imgUrl = imgs[pages].find_element_by_tag_name(
                        'img').get_attribute('src')
                    html = requests.get(imgUrl).content
                    with open(f'./temp/{title}/{pages}.jpg', 'wb') as f:
                        f.write(html)
                    break
                except Exception as e:
                    actions = ActionChains(driver)
                    actions.move_to_element(imgs[pages]).perform()
                    time.sleep(1)
                    driver.execute_script("window.scrollBy(0,10000)")

    driver.quit()
    print('下载完毕，正在转码')
    conpdf(f'output/{title}.pdf', f'temp/{title}', '.jpg', True)


if __name__ == "__main__":
    download("http://ishare.iask.sina.com.cn/f/CSBjG4CX6D.html")
