from fileinput import filename
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from helpers import scrapSingleJobPage, exportJobsToJson

url = 'https://www.randstad.com.ar/trabajos/buenos-aires/bahia-blanca/'
driver = webdriver.Chrome(ChromeDriverManager().install())

data = []
driver.get(url)
jobs = driver.find_element(By.XPATH, '//ul[@class="cards__list cards__list--format-grid"]').find_elements(By.XPATH, './/li[@class="cards__item"]');

for job in jobs:
    header = job.find_element(By.XPATH, './/div[@class="cards__header"]').find_element(By.XPATH, './/h3[@class="cards__title"]')
    jobUrl = header.find_element(By.XPATH, './/a[@class="cards__link"]').get_attribute('href');

    data.append(scrapSingleJobPage(jobUrl))

driver.quit()

exportJobsToJson(data)
print('Randstad jobs scrapped :D')