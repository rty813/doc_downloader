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
import requests
from tqdm import trange
from img2pdf import conpdf


def download(url):
    option = webdriver.ChromeOptions()
    option.add_argument('--headless')
    option.add_argument('log-level=3')
    driver = webdriver.Chrome(options=option)

    title = "output"
    try:
        # driver.implicitly_wait(15)
        driver.set_page_load_timeout(15)
        driver.get(url)
        title = driver.title
    except Exception as e:
        print("Timeout - start download anyway.")

    print(title)
    time.sleep(5)

    while True:
        try:
            # 展开全部
            elem_cont_button = driver.find_element_by_class_name(
                "banner-download")
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", elem_cont_button)
            actions = ActionChains(driver)
            actions.move_to_element(elem_cont_button).perform()
            time.sleep(0.5)
            driver.find_element_by_class_name("down-arrow").click()
        except Exception:
            break

    # 获取页数
    num_of_pages = driver.find_element_by_id('readshop').find_element_by_class_name(
        'mainpart').find_element_by_class_name('shop3').find_elements_by_class_name('text')[-1].get_attribute('innerHTML')
    num_of_pages = int(num_of_pages.split(';')[-1])

    if os.path.exists(f'./temp/{title}'):
        shutil.rmtree(f'./temp/{title}')
    os.makedirs(f'./temp/{title}')

    for pages in trange(num_of_pages):
        try:
            time.sleep(0.5)
            elem = driver.find_element_by_id(f'outer_page_{pages+1}')
            actions = ActionChains(driver)
            actions.move_to_element(elem).perform()
            img = elem.find_element_by_tag_name('img')
            img_url = img.get_attribute('src')
            res = requests.get(img_url)

            with open(f"./temp/{title}/{pages}.gif", "wb") as fh:
                fh.write(res.content)
        except Exception as e:
            print("下载失败，可能由于文档为收费预览文档。错误信息：\n%r" % e)
            break
    driver.quit()
    print('下载完毕，正在转码')
    conpdf(f'output/{title}.pdf', f'temp/{title}', '.gif')


if __name__ == '__main__':
    download("https://www.jinchutou.com/p-120187856.html")
