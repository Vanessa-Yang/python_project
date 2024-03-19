import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scratch(url):
    # 设置浏览器驱动路径
    driver_path = "/path/to/chromedriver"  # 替换为你的驱动路径

    # 创建Chrome浏览器实例
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service)

    # 打开网页
    driver.get(url)

    # 等待页面加载完成（使用显式等待）
    wait = WebDriverWait(driver, 10)
    title_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'h1.ItemHeader--mainTitle--3CIjqW5')))
    ul_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.PicGallery--thumbnails--1cEhJzK')))

    # 获取标题内容并打印
    title = title_element.text.strip()
    print("Title:", title)

    # 获取图片链接并打印
    li_elements = ul_element.find_elements(By.TAG_NAME, 'li')
    for li_element in li_elements:
        img_element = li_element.find_element(By.TAG_NAME, 'img')
        img_src = img_element.get_attribute('src')
        print("Image URL:", img_src)

    # 关闭浏览器
    driver.quit()

def scratchFromUrl(url):
    # 发送GET请求获取页面内容
    response = requests.get(url)
    html_content = response.text

    # 使用Beautiful Soup解析HTML内容
    soup = BeautifulSoup(html_content, 'html.parser')

    # 获取<h1 class="ItemHeader--mainTitle--3CIjqW5">标签中的内容并打印
    title_tag = soup.find('h1', class_='ItemHeader--mainTitle--3CIjqW5')
    title = title_tag.text.strip()
    print("Title:", title)

    # 获取<ul class="PicGallery--thumbnails--1cEhJzK">标签下所有<li>标签下的所有<img> 标签中的src属性并打印
    ul_tag = soup.find('ul', class_='PicGallery--thumbnails--1cEhJzK')
    li_tags = ul_tag.find_all('li')
    for li_tag in li_tags:
        img_tag = li_tag.find('img')
        img_src = img_tag['src']
        print("Image URL:", img_src)


if __name__ == '__main__':
    detail_url = 'https://item.taobao.com/item.htm?id=13848551459&pvid=b1bb724a-24e9-4940-b8cd-c05aaa8e1fb9&scm=1007.40986.275655.0&spm=a21bo.jianhua.201876.1.319b11d92RAaSN'
    scratchFromUrl(detail_url)