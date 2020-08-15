import sys
import platform
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime, time
from time import sleep

TIME = '00:00'
HEADLESS = True

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

# login logic
url = 'https://sisprod.psft.ust.hk/psp/SISPROD/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?pslnkid=Z_HC_SSS_STUDENT_CENTER_LNK&FolderPath=PORTAL_ROOT_OBJECT.Z_HC_SSS_STUDENT_CENTER_LNK&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder'
driver = webdriver.Chrome(
    executable_path=webdriver_path[system], options=options)
driver.get(url)
WebDriverWait(driver, 180).until(EC.title_contains("Student Center"))
cookies = driver.get_cookies()
driver.quit()

# enrollment logic
url = 'https://sisprod.psft.ust.hk/psc/SISPROD/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES_2.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A&ExactKeys=Y&TargetFrameName=None'
if HEADLESS:
    options.add_argument("--headless")
driver = webdriver.Chrome(
    executable_path=webdriver_path[system], options=options)
driver.get(url)
for cookie in cookies:
    driver.add_cookie(cookie)
driver.get(url)

driver.find_element_by_link_text('Plan').click()

for i in range(driver.find_element_by_id('SSR_REGFORM_VW$scroll$0').get_attribute('innerHTML').count('tr id')):
    try:
        driver.find_element_by_xpath(f'//*[@id="P_SELECT${i}"]').click()
    except:
        sys.exit('Nothing is in your shopping cart.')

startTime = time(*(map(int, TIME.split(':'))))
while startTime > datetime.today().time():
    sleep(0.001)

WebDriverWait(driver, 180).until(EC.presence_of_element_located(
    (By.ID, 'DERIVED_REGFRM1_LINK_ADD_ENRL')))
driver.find_element_by_link_text('enroll').click()
WebDriverWait(driver, 180).until(EC.presence_of_element_located(
    (By.ID, 'DERIVED_REGFRM1_SSR_PB_SUBMIT')))
driver.find_element_by_link_text('Finish Enrolling').click()

print('Good luck and have fun!')
