import sys
import platform
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime, time

TIME = '11:30'

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
driver.get('https://sisprod.psft.ust.hk/psc/SISPROD/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A&ACAD_CAREER=CAR&EMPLID=20520422&ENRL_REQUEST_ID=&INSTITUTION=INST&STRM=TERM')
driver.find_element_by_id('SSR_DUMMY_RECV1$sels$1$$0').click()
driver.find_element_by_id('DERIVED_SSS_SCT_SSR_PB_GO').click()

WebDriverWait(driver, 120).until(EC.presence_of_element_located((By.ID, 'DERIVED_REGFRM1_LINK_ADD_ENRL$82$')))
button = driver.find_element_by_id('DERIVED_REGFRM1_LINK_ADD_ENRL$82$')

startTime = time(*(map(int, TIME.split(':'))))
WebDriverWait(driver, 1000, 0.002).until(lambda s: datetime.today().time() > startTime)
button.click()

WebDriverWait(driver, 300, 0.002).until(EC.presence_of_element_located((By.ID, 'DERIVED_REGFRM1_SSR_PB_SUBMIT')))
driver.find_element_by_id('DERIVED_REGFRM1_SSR_PB_SUBMIT').click()

print('Good luck and have fun!')
