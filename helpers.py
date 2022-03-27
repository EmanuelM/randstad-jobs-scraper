from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime
import json

def scrapSingleJobPage(url):
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(url)
    header = driver.find_element(By.XPATH, '//div[@class="header__content header__content--full-width content-block"]')

    title = header.find_element(By.XPATH, './/h1[@class="content-block__title"]').text
    publishedAt = header.find_elements(By.XPATH, './/li[@class="contact-details__link"]')[1].text
    finishAt = header.find_element(By.XPATH, './/li[@class="contact-details__link text--alternative"]').text
    description = driver.find_element(By.XPATH, '//div[@class="body-copy hidden--from-l"]').find_element(By.XPATH, './/div[@class="content"]').get_attribute('innerHTML')

    driver.quit()

    return {
        "title": title,
        "publishedAt": publishedAt,
        "finishAt": finishAt,
        "description": description,
    }

def exportJobsToJson(data):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    fileName = 'exports/' + timestamp + '_jobs.json'
    
    with open(fileName, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)