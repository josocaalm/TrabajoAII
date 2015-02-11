#encoding: utf-8

import utilities.auxFunctions as utilsFuncs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common import by

def loginAndRedirectToSearchPage():
    driver = utilsFuncs.createWebdriver("http://www.tf2outpost.com/search")
    
    username = driver.find_element_by_xpath("//input[@name='username']")
    password = driver.find_element_by_xpath("//input[@name='password']")
    
    username.send_keys("tfgTest")
    password.send_keys("tfg123Test")
    
    driver.find_element_by_name("logon").submit()
    
    searchButton = WebDriverWait(driver, 60).until(EC.presence_of_element_located((by.By.XPATH, "//a[@href='/search']")))
    searchButton.click()
    
    return driver