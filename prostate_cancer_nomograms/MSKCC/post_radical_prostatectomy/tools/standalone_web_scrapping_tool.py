from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import os
from prostate_cancer_nomograms.root import ROOT

chrome_options = Options()
# chrome_options.add_argument("--headless")

driver = webdriver.Chrome(
    executable_path=os.path.join(ROOT, r"web_drivers\chromedriver.exe"),
    options=chrome_options
)

driver.get("https://www.mskcc.org/nomograms/prostate/post_op")

time.sleep(2)

try:
    pop_up = driver.find_element_by_xpath("/html/body/div[7]/div[1]/div[1]/div[2]/p[3]/button[1]")
    pop_up.click()
except NoSuchElementException:
    pass

time.sleep(0.5)
button = driver.find_element_by_xpath("/html/body/div[6]/div/div/div[2]/div[2]/form/input[1]")
button.click()

time.sleep(0.5)
button = driver.find_element_by_id("edit-neoadjuvant-hormone-therapy-false")
button.click()

time.sleep(0.5)
button = driver.find_element_by_id("edit-neoadjuvant-radiation-therapy-false")
button.click()

time.sleep(0.5)
text_input = driver.find_element_by_id("edit-pre-treatment-psa")
text_input.send_keys("0.08")

time.sleep(0.5)
text_input = driver.find_element_by_id("edit-age-at-surgery")
text_input.send_keys("50")

time.sleep(0.5)
text_input = driver.find_element_by_id("edit-months-disease-free")
text_input.send_keys("80")

time.sleep(0.5)
button = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/main/div/div[2]/div/div[1]/article/section/div/div/form/div[2]/div[2]/div[3]/div[2]/div/div[1]/div/div")
button.click()
time.sleep(0.5)
button = driver.find_element_by_id("choices--edit-primary-surgery-gleason-item-choice-3")
button.click()

time.sleep(0.5)
button = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/main/div/div[2]/div/div[1]/article/section/div/div/form/div[2]/div[2]/div[3]/div[3]/div/div[1]/div/div")
button.click()

time.sleep(0.5)
button = driver.find_element_by_id("choices--edit-secondary-surgery-gleason-item-choice-4")
button.click()

time.sleep(0.5)
button = driver.find_element_by_id("edit-surgical-margins-positive-false")
button.click()

time.sleep(0.5)
button = driver.find_element_by_id("edit-extracapsular-extension-false")
button.click()

time.sleep(0.5)
button = driver.find_element_by_id("edit-seminal-vesicle-involvement-true")
button.click()

time.sleep(0.5)
button = driver.find_element_by_id("edit-lymph-node-involvement-true")
button.click()

time.sleep(0.5)
button = driver.find_element_by_id("edit-submit")
button.click()

time.sleep(3)
output = driver.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/main/div/div[2]/div/div[1]/article/section/div/div/form/div[2]/div/div[1]/div[1]/div")
print(output.text)

driver.close()
