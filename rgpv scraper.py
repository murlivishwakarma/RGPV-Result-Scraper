import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, ElementNotInteractableException 
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.alert import Alert
import easyocr
from PIL import Image
import requests
import json
from io import BytesIO
from bs4 import BeautifulSoup
from rgpv_xpath import *


def getWeb():

    global driver
    driver = webdriver.Firefox()
    driver.get('http://result.rgpv.ac.in/Result/ProgramSelect.aspx')
    btech_click = driver.find_element(By.XPATH,course_click_xp).click()


def getImg():
    
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
    
    enroll_no = '0103IS221001'
    enroll_input = driver.find_element(By.XPATH,enroll_xp)
    enroll_input.send_keys(enroll_no)
    
    sem_ddn = driver.find_element(By.XPATH,sem_ddn_xp).click()
    sem_sel = driver.find_element(By.XPATH, sem_sel_xp).click()

    captcha_input = driver.find_element(By.XPATH, captcha_input_xp)
    captcha_input.send_keys(captcha_final) 
    time.sleep(3)
    submit_info = driver.find_element(By.XPATH, submit_xp).click()


def resultExt():
    
    html_content = driver.page_source
    soup = BeautifulSoup(html_content,'html.parser')

    name = soup.find('span', {'id': name_id}).text.strip()
    roll_no = soup.find('span', {'id': roll_no_id}).text.strip()

    subjects_and_grades = []
    subject_tables = soup.find_all('table', class_='gridtable', style='width:100%')

    for table in subject_tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) == 4:
                subject = cells[0].text.strip()
                grade = cells[3].text.strip()
                subjects_and_grades.append({"subject": subject, "grade": grade})

    result = {
        "name": name,
        "roll_no": roll_no,
        "subjects_and_grades": subjects_and_grades
    }
    json_output = json.dumps(result, indent=2)

    with open('result.json', 'w') as f:
        f.write(json_output)
    
    

  

    


    

getWeb()
getImg()
detailsInput()
resultExt()