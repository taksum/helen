import sys
import platform
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime, time

TIME = '00:00'

webdriver_path = {
    'Linux'  : './chrome_driver/chromedriver_linux',
    'Darwin' : './chrome_driver/chromedriver_mac',
    'Windows': './chrome_driver/chromedriver.exe'
}

system = platform.system()
if system not in webdriver_path.keys():
    sys.exit('Your operating system is not supported!')

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])

# login logic
driver = webdriver.Chrome(executable_path=webdriver_path[system], options=options)
driver.get('https://sisprod.psft.ust.hk/psp/SISPROD/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?pslnkid=Z_HC_SSS_STUDENT_CENTER_LNK&FolderPath=PORTAL_ROOT_OBJECT.Z_HC_SSS_STUDENT_CENTER_LNK&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder')
WebDriverWait(driver, 120).until(EC.title_contains("Student Center"))

# enrollment logic
driver.get('https://sisprod.psft.ust.hk/psc/SISPROD/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES_2.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A&ExactKeys=Y&TargetFrameName=None')
driver.find_element_by_link_text('Plan').click()

payload = driver.find_element_by_id('SSR_REGFORM_VW$scroll$0').get_attribute('innerHTML').count('P_SELECT')

if not payload:
    sys.exit('Nothing is in your shopping cart.')

for i in range(payload):
    driver.find_element_by_xpath(f'//*[@id="P_SELECT${i}"]').click()

button = driver.find_element_by_link_text('enroll')
startTime = time(*(map(int, TIME.split(':'))))

WebDriverWait(driver, 1000, 0.002).until(lambda s: datetime.today().time() > startTime)
button.click()

WebDriverWait(driver, 300, 0.002).until(EC.presence_of_element_located((By.ID, 'DERIVED_REGFRM1_SSR_PB_SUBMIT')))
driver.find_element_by_link_text('Finish Enrolling').click()         # TODO: migrate link_text to id

print('Good luck and have fun!')
