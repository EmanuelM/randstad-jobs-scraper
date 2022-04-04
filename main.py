import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from helpers import scrap_job_page_by_url, export_to_json
from selenium.common.exceptions import NoSuchElementException   
from dotenv import load_dotenv

load_dotenv()

jobs_scraped = []
url = os.getenv('RANDSTAD_URL')
chromedriver = os.getenv('SELENIUM_DRIVER_PATH')

driver = webdriver.Chrome(chromedriver)
driver.get(url)

time.sleep(5)
cookies_alert = driver.find_element(By.XPATH, '//button[@id="onetrust-accept-btn-handler"]')
if cookies_alert:
    cookies_alert.click()

has_next_page = True
while has_next_page:
    try:
        next_page_button = driver.find_element(By.XPATH, '//button[@class="button button--m bluex-button--preloader"]')
        driver.execute_script("arguments[0].click();", next_page_button)
    except NoSuchElementException:
        has_next_page = False

jobs_list = driver.find_element(By.XPATH, '//ul[@class="cards__list cards__list--format-grid"]').find_elements(By.XPATH, './/li[@class="cards__item"]');

for job in jobs_list:
    header = job.find_element(By.XPATH, './/div[@class="cards__header"]').find_element(By.XPATH, './/h3[@class="cards__title"]')
    job_url = header.find_element(By.XPATH, './/a[@class="cards__link"]').get_attribute('href');

    job_details = scrap_job_page_by_url(job_url)
    jobs_scraped.append(job_details)

driver.quit()

export_to_json(jobs_scraped)
print('Randstad jobs scraped :D')