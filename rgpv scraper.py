import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException 
from selenium.webdriver.firefox.options import Options
import pytesseract
from PIL import Image
import requests
from io import BytesIO
from bs4 import BeautifulSoup

def getWeb():
    global driver
    driver = webdriver.Firefox()
    driver.get("http://result.rgpv.ac.in/Result/BErslt.aspx")

def getImg():
    
    captcha_xp = '/html/body/form/div[3]/div/div[2]/table/tbody/tr[5]/td/div/table/tbody/tr[1]/td/div/img'
    captcha = driver.find_element(By.XPATH,captcha_xp)
    captcha_url = captcha.get_attribute('src')
   
    response = requests.get(captcha_url)
    captcha_img = Image.open(BytesIO(response.content))

    text = pytesseract.image_to_string(captcha_img)
    print(f"Extracted Text: {text}")


getWeb()
getImg()