#encoding: utf-8

from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import re
import utilities.auxFunctions as utilsFuncs
import currency.currencies as curr

def currentRefPrice():
    request = Request("http://backpack.tf", headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"})
    html = urlopen(request)
    soup = BeautifulSoup(html)
        
    for elem in soup.findAll("p", {"class": "value"}):
        if "$" in elem.text:
            formatedText = elem.text.replace("$", "")
            if "–" in formatedText:
                hyphenIndex = formatedText.index("–")
                formatedText = formatedText[hyphenIndex+1:]
            break
    
    return float(formatedText)


def currentKeyToRefsEquivalence():
    request = Request("http://backpack.tf", headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/534.30 (KHTML, like Gecko) Ubuntu/11.04 Chromium/12.0.742.112 Chrome/12.0.742.112 Safari/534.30"})
    html = urlopen(request)
    soup = BeautifulSoup(html)
    
    regExp = "(\d)?\d–.* ref"
        
    for elem in soup.findAll("p", {"class": "value"}):
        if re.search(regExp, elem.text):
            formatedText = elem.text.replace(" ref", "")
            if "–" in formatedText:
                hyphenIndex = formatedText.index("–")
                formatedText = formatedText[hyphenIndex+1:]
            break
    
    return int(float(formatedText))


def currentKeyUSDPrice():
    return currentRefPrice()*currentKeyToRefsEquivalence()


def keyUSDPriceToSpecifiedCurrency(outputCurr):
    driver = utilsFuncs.createWebdriver("https://www.google.com/finance/converter")
    pricePerKey = curr.findConversion('USD', outputCurr, driver)*currentKeyUSDPrice()
    utilsFuncs.quitWebdriver(driver)
    return pricePerKey