from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from datetime import datetime, time
from time import sleep

TIME = '22:40' # input your timeslot here

driver = webdriver.Chrome(executable_path='./chromedriver.exe')
driver.get('https://sisprod.psft.ust.hk/psp/SISPROD/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?pslnkid=Z_HC_SSS_STUDENT_CENTER_LNK&FolderPath=PORTAL_ROOT_OBJECT.Z_HC_SSS_STUDENT_CENTER_LNK&IsFolder=false&IgnoreParamTempl=FolderPath%2cIsFolder')
WebDriverWait(driver, 60).until(EC.title_contains("Student Center"))

driver.get('https://sisprod.psft.ust.hk/psc/SISPROD/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES_2.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART&Action=A&ExactKeys=Y&TargetFrameName=None')
driver.find_element_by_link_text('Plan').click()

for i in range(driver.find_element_by_id('SSR_REGFORM_VW$scroll$0').get_attribute('innerHTML').count('tr id')):
    driver.find_element_by_xpath(f'//*[@id="P_SELECT${i}"]').click()

startTime = time(*(map(int, TIME.split(':'))))
while startTime > datetime.today().time():
    sleep(0.01)

driver.find_element_by_link_text('enroll').click()
driver.find_element_by_link_text('Finish Enrolling').click()
