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
import urllib.request


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
        title = driver.title[:-8]
    except:
        print("Timeout - start download anyway.")

    print(f'淘豆网: 《{title}》')
    time.sleep(5)

    while True:
        try:
            driver.execute_script("window.scrollBy(0,10000)")
            time.sleep(1)
            # 展开全部
            elem_cont_button = driver.find_element_by_class_name(
                "banner-more-btn")
            elem_cont_button = elem_cont_button.find_element_by_tag_name(
                'span')
            driver.execute_script(
                "arguments[0].scrollIntoView(true);", elem_cont_button)
            actions = ActionChains(driver)
            actions.move_to_element(elem_cont_button).perform()
            time.sleep(0.5)
            driver.execute_script("arguments[0].click();", elem_cont_button)
        except NoSuchElementException:
            break
        except JavascriptException:
            continue
    # 获取页数
    num_of_pages = driver.find_element_by_id(
        'docPage').get_attribute('innerHTML')
    num_of_pages = int(num_of_pages)

    if not os.path.exists(f'./temp/{title}'):
        os.mkdir(f'./temp/{title}')
    else:
        ls = os.listdir(f'./temp/{title}')
        for f in ls:
            os.remove(f'./temp/{title}/' + f)

    for pages in trange(num_of_pages):
        time.sleep(0.5)
        element = driver.find_element_by_id(f"page{pages + 1}")
        driver.execute_script("arguments[0].scrollIntoView(true);", element)
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
        time.sleep(0.5)
        imgElement = element.find_element_by_tag_name('img')
        imgUrl = imgElement.get_attribute('src')
        response = urllib.request.urlopen(imgUrl)
        html = response.read()
        with open(f'./temp/{title}/{pages}.jpg', 'wb') as f:
            f.write(html)

    driver.quit()
    print('下载完毕，正在转码')
    conpdf(f'{title}.pdf', f'temp/{title}', '.jpg')


if __name__ == "__main__":
    download('https://www.taodocs.com/p-292564682.html')
