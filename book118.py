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
    # option.add_argument('headless')
    option.add_argument('log-level=3')
    driver = webdriver.Chrome(
        executable_path='.//chromedriver', options=option)

    title = "output"
    try:
        # driver.implicitly_wait(15)
        driver.set_page_load_timeout(15)
        driver.get(url)
        title = driver.title
    except:
        print("Timeout - start download anyway.")

    print(title)
    if 'ppt' in title:
        import book118_PPT
        driver.quit()
        book118_PPT.download(url)
        return
    time.sleep(2)

    driver.find_element_by_id("agree_full").click()
    time.sleep(1)

    driver.get(driver.find_element_by_id(
        "layer_new_view_iframe").get_attribute("src"))
    time.sleep(3)

    while True:
        try:
            # 展开全部
            elem_cont_button = driver.find_element_by_id("btn_read")
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", elem_cont_button)
            actions = ActionChains(driver)
            actions.move_to_element(elem_cont_button).perform()
            time.sleep(2)
            elem_cont_button.click()
        except NoSuchElementException:
            break
        except Exception:
            continue

    # 获取页数
    num_of_pages = driver.find_element_by_class_name(
        'page-counts').get_attribute('innerHTML')
    num_of_pages = int(num_of_pages.split(' ')[-1])

    if os.path.exists(f'./temp/{title}'):
        shutil.rmtree(f'./temp/{title}')
    os.makedirs(f'./temp/{title}')

    elems = driver.find_elements_by_class_name("webpreview-item")
    for pages in trange(num_of_pages):
        try:
            elem = elems[pages]
            time.sleep(0.5)
            actions = ActionChains(driver)
            actions.move_to_element(elem).perform()
            img = elem.find_element_by_tag_name('img')
            img_url = img.get_attribute('src')
            if img_url is None or not 'http' in img_url:
                img_url = "http:" + img.get_attribute('data-src')
            res = requests.get(img_url)

            with open(f"./temp/{title}/{pages}.png", "wb") as fh:
                fh.write(res.content)
        except Exception as e:
            print("下载失败！\n%r" % e)
            driver.quit()
            return
    driver.quit()
    print('下载完毕，正在转码')
    conpdf(f'output/{title}.pdf', f'temp/{title}', '.png')


if __name__ == '__main__':
    download("https://max.book118.com/html/2020/0203/5123223334002220.shtm")
