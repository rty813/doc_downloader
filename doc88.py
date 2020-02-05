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

    print(f'道客巴巴: 《{title}》')
    time.sleep(5)

    try:
        # 展开全部
        elem_cont_button = driver.find_element_by_id("continueButton")
        driver.execute_script(
            "arguments[0].scrollIntoView(true);", elem_cont_button)
        actions = ActionChains(driver)
        actions.move_to_element(elem_cont_button).perform()
        time.sleep(0.5)
        elem_cont_button.click()
    except NoSuchElementException:
        pass

    # 获取页数
    num_of_pages = driver.find_element_by_id('readshop').find_element_by_class_name(
        'mainpart').find_element_by_class_name('shop3').find_element_by_class_name('text').get_attribute('innerHTML')
    num_of_pages = int(num_of_pages.split(' ')[-1])

    for i in range(5):
        # 缩放
        driver.find_element_by_id('zoomInButton').click()
        time.sleep(0.5)

    if os.path.exists(f'./temp/{title}'):
        shutil.rmtree(f'./temp/{title}')
    os.makedirs(f'./temp/{title}')

    for pages in trange(num_of_pages):
        time.sleep(0.5)

        canvas_id = "page_" + str(pages + 1)
        pagepb_id = "pagepb_" + str(pages + 1)

        element = driver.find_element_by_id(canvas_id)
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        time.sleep(0.5)

        # Check loading status
        while(len(driver.find_element_by_id(pagepb_id).get_attribute('innerHTML')) != 0):
            time.sleep(1)
            # print(driver.find_element_by_id(
            #     pagepb_id).get_attribute('innerHTML'))

        js_cmd = "var canvas = document.getElementById('{}');".format(canvas_id) + \
            "return canvas.toDataURL();"
        img_data = driver.execute_script(js_cmd)

        img_data = (img_data[22:]).encode()

        with open(f"./temp/{title}/{pages}.png", "wb") as fh:
            fh.write(base64.decodebytes(img_data))
    driver.quit()
    print('下载完毕，正在转码')
    conpdf(f'output/{title}.pdf', f'temp/{title}', '.png')
