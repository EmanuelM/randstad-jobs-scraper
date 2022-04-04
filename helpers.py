import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

def scrap_job_page_by_url(url):
    chromedriver = os.getenv('SELENIUM_DRIVER_PATH')
    driver = webdriver.Chrome(chromedriver)
    driver.get(url)

    header = driver.find_element(By.XPATH, '//div[@class="header__content header__content--full-width content-block"]')
    title = header.find_element(By.XPATH, './/h1[@class="content-block__title"]').text
    published_at = header.find_elements(By.XPATH, './/li[@class="contact-details__link"]')[1].text
    finish_at = header.find_element(By.XPATH, './/li[@class="contact-details__link text--alternative"]').text
    description = driver.find_element(By.XPATH, '//div[@class="body-copy hidden--from-l"]').find_element(By.XPATH, './/div[@class="content"]').get_attribute('innerHTML')

    driver.quit()

    return {
        "url": url,
        "title": title,
        "published_at": published_at,
        "finish_at": finish_at,
        "description": description,
    }

def export_to_json(data):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    fileName = 'exports/' + timestamp + '_jobs.json'
    
    with open(fileName, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)