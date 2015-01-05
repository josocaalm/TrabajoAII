#encoding: utf-8

from selenium import webdriver

def performConversion(amount, conversionFactor):
    return amount*conversionFactor

def createWebdriver(url):
    driver = webdriver.Chrome()
    driver.get(url)
    
    return driver
    
def quitWebdriver(driver):
    driver.quit()
    pass