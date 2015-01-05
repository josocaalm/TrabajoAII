#encoding: utf-8

from selenium.webdriver.support.select import Select
from selenium.common.exceptions import NoSuchElementException 

def findConversion(inputCurrency, outputCurrency, webdriver):    
    formInput = Select(webdriver.find_element_by_name("from"))
    formOutput = Select(webdriver.find_element_by_name("to"))
        
    formInput.select_by_value(inputCurrency)
    formOutput.select_by_value(outputCurrency)
        
    webdriver.find_element_by_name("f").submit()
        
    try:
        conversionElem = webdriver.find_element_by_xpath("//span[@class='bld']")
        currency1To2Value = conversionElem.text
        currency1To2Value = currency1To2Value.replace(" " + outputCurrency, "")
        currency1To2Value = float(currency1To2Value)
    except NoSuchElementException:
        currency1To2Value = 0
    
    return currency1To2Value   