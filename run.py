import sys
import platform
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime, time
from time import sleep
from tkinter import messagebox
import tkinter as tk

TIME = '00:00'

webdriver_path = {
    'Linux': './chrome_driver/chromedriver_linux',
    'Darwin': './chrome_driver/chromedriver_mac',
    'Windows': './chrome_driver/chromedriver.exe'
}

system = platform.system()
if system not in webdriver_path.keys():
    sys.exit('Your operating system is not supported!')

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# Preflight briefing
root = tk.Tk()
root.withdraw()
messagebox.showinfo(
    title='Before we begin...',
    message="After you login, don't touch the browser window. Sit back and enjoy while I work my magic~",
)

# login logic
driver = webdriver.Chrome(
    executable_path=webdriver_path[system], options=options)
driver.get('https://sisprod.psft.ust.hk/psp/SISPROD/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?pslnkid=Z_HC_SSS_STUDENT_CENTER_LNK&FolderPath=PORTAL_ROOT_OBJECT.Z_HC_SSS_STUDENT_CENTER_LNK&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder')
WebDriverWait(driver, 120).until(EC.title_contains("Student Center"))

# enrollment logic
driver.get('https://sisprod.psft.ust.hk/psc/SISPROD/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES_2.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A&ExactKeys=Y&TargetFrameName=None')
driver.find_element_by_link_text('Plan').click()

for i in range(driver.find_element_by_id('SSR_REGFORM_VW$scroll$0').get_attribute('innerHTML').count('tr id')):
    try:
        driver.find_element_by_xpath(f'//*[@id="P_SELECT${i}"]').click()
    except:
        root.focus_set()
        messagebox.showinfo(
            title='Oops...',
            message='Nothing is in your shopping cart.'
        )
        sys.exit()

startTime = time(*(map(int, TIME.split(':'))))
while startTime > datetime.today().time():
    sleep(0.001)

driver.find_element_by_link_text('enroll').click()
WebDriverWait(driver, 300).until(EC.presence_of_element_located(
    (By.ID, 'DERIVED_REGFRM1_SSR_PB_SUBMIT')))
driver.find_element_by_link_text('Finish Enrolling').click()

print('Good luck and have fun!')
