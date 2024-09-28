import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.alert import Alert
import pytesseract
import easyocr
from PIL import Image
import requests
from io import BytesIO
from bs4 import BeautifulSoup

def getWeb():
    global driver
    driver = webdriver.Firefox()
    driver.get('http://result.rgpv.ac.in/Result/ProgramSelect.aspx')
    btech_click = driver.find_element(By.XPATH,'//*[@id="radlstProgram_1"]').click()

def getImg():
    
    captcha_xp = '/html/body/form/div[3]/div/div[2]/table/tbody/tr[5]/td/div/table/tbody/tr[1]/td/div/img'
    captcha = driver.find_element(By.XPATH,captcha_xp)
    captcha_url = captcha.get_attribute('src')
    response = requests.get(captcha_url)
    captcha_img = Image.open(BytesIO(response.content))  
    reader = easyocr.Reader(['en'])
    result = reader.readtext(captcha_img)
    captcha_text = ' '.join([item[1] for item in result]) 
    global captcha_final
    captcha_final = captcha_text.replace(' ','')
    
def detailsInput():
    enroll_no = '0103IS221137'
    enroll_xp = '/html/body/form/div[3]/div/div[2]/table/tbody/tr[4]/td/table/tbody/tr/th[2]/input'
    enroll_input = driver.find_element(By.XPATH,enroll_xp)
    enroll_input.send_keys(enroll_no)

    sem_ddn_xp = '/html/body/form/div[3]/div/div[2]/table/tbody/tr[4]/td/table/tbody/tr/th[4]/select'
    sem_ddn = driver.find_element(By.XPATH,sem_ddn_xp).click()
    sem_sel_xp = '/html/body/form/div[3]/div/div[2]/table/tbody/tr[4]/td/table/tbody/tr/th[4]/select/option[4]'
    sem_sel = driver.find_element(By.XPATH, sem_sel_xp).click()

    captcha_input_xp = '/html/body/form/div[3]/div/div[2]/table/tbody/tr[5]/td/div/table/tbody/tr[2]/th/input'
    captcha_input = driver.find_element(By.XPATH, captcha_input_xp)
    captcha_input.send_keys(captcha_final) 

    submit_xp = '/html/body/form/div[3]/div/div[2]/table/tbody/tr[5]/td/div/table/tbody/tr[3]/th/input'
    time.sleep(3)
    submit_info = driver.find_element(By.XPATH, submit_xp).click()
    alert = driver.switch_to.alert
    alert.accept()


    

getWeb()
getImg()
detailsInput()