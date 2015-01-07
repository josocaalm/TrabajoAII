#encoding: utf-8

from bs4 import BeautifulSoup
from selenium.common.exceptions import NoSuchElementException
import utilities.auxFunctions as auxFuncs 
import backpackTF.tf2keysAndRefs as keysRefsFuncs
import currency.currencies as curr
import re

def findOutpostOffers(driver, gameName, maxSearchDepth, currentSearchDepth, foundOffers):
    if currentSearchDepth <= maxSearchDepth:
        try:
            regExp1 = ".*" + gameName + ".*\d?(,|\.|')?\d.*((x)?(T|t)(F|f)(2)?)?.*(K|k)ey(s)?.*(\d( )?((R|r)ef(s)?))?"
            regExp2 = ".*\d?(,|\.|')?\d.*((x)?(T|t)(F|f)(2)?)?.*(K|k)ey(s)?.*(\d.*((R|r)ef(s)?))?.*" + gameName + ".*"
            
            offers = driver.find_element_by_id('modules').get_attribute("innerHTML")
            soup = BeautifulSoup(offers)
            
            for offer in soup.find_all("div", {"class":"trade box module"}):
                searchResult = tuple()
                notes = offer.find("div", {"class":"notes preview"})
                tradeID = offer.find("a", {"class":"bookmark_toggle"})["data-tradeid"]
                tradeLink = "http://www.tf2outpost.com/trade/" + tradeID
                
                if notes != None:
                    match = re.match(regExp1, notes.text)
                    match2 = re.match(regExp2, notes.text)
                    if match != None:
                        searchResult = (match.group(0), tradeLink)
                        foundOffers.append(searchResult)
                    if match2 != None:
                        searchResult = (match2.group(0), tradeLink)
                        foundOffers.append(searchResult)
                            
            currentSearchDepth += 1
            nextPageElem = driver.find_element_by_xpath('//ul[@class="pages"]/descendant::li/descendant::a[text()="' + str(currentSearchDepth) + '"]')
            nextPageElem.click()
            
            return findOutpostOffers(driver, gameName, maxSearchDepth, currentSearchDepth, foundOffers)
        except NoSuchElementException:
            auxFuncs.quitWebdriver(driver)
            return foundOffers
    else:
        auxFuncs.quitWebdriver(driver)
        return foundOffers
    

def extractKeysAndRefsPrice(foundOffers):
    results = list()
    
    regExpKeys = "\d?\d((,|\.|')\d\d?)?( )?((x)?(T|t)(F|f)(2)?)?( )?(K|k)ey(s)?"
    regExpRefs = "\d((,|\.|')\d\d)?( )?(R|r)ef(s)?"
    
    regExpKeysPrice = "\d?\d((,|\.|')\d\d?)?"
    regExpRefsPrice = "\d((,|\.|')\d\d)?"
    
    refPriceOnUSD = keysRefsFuncs.currentRefPrice()
    refsPerKey = keysRefsFuncs.currentKeyToRefsEquivalence()
    
    for offer in foundOffers:
        try:
            keyOfferMatch = re.search(regExpKeys, offer[0])
            refOfferMatch = re.search(regExpRefs, offer[0])
            totalAmountOfRefs = 0
            numOfRefs = 0
            
            if keyOfferMatch != None:
                keyPrice = keyOfferMatch.group(0)
                numOfKeys = re.search(regExpKeysPrice, keyPrice).group(0)
                numOfKeys = numOfKeys.replace(",", ".")
                numOfKeys = numOfKeys.replace("'", ".")
                totalAmountOfRefs += float(numOfKeys) * float(refsPerKey)
            if refOfferMatch != None:
                refPrice = refOfferMatch.group(0)
                numOfRefs = re.search(regExpRefsPrice, refPrice).group(0)
                numOfRefs = numOfRefs.replace(",", ".")
                numOfRefs = numOfRefs.replace("'", ".")
                totalAmountOfRefs += float(numOfRefs)
            
            priceOnUSD = refPriceOnUSD * totalAmountOfRefs
            
            finalSearchResult = [float(numOfKeys), float(numOfRefs), round(priceOnUSD, 2), offer[1]]
            
            if finalSearchResult[2] != 0.0:
                results.append(tuple(finalSearchResult))
                
        except UnboundLocalError:
            pass
    
    return results


def sortSearchResults(results):
    return sorted(results, key=lambda res: res[2])


def convertUSDToSpecifiedCurrency(results, outputCurrency):
    updatedResults = list()
    driver = auxFuncs.createWebdriver("https://www.google.com/finance/converter")
    USDToOutputEquivalence = curr.findConversion("USD", outputCurrency, driver)
    auxFuncs.quitWebdriver(driver)
    
    for offer in results:
        priceOnUSD = offer[2]
        priceOnOutputCurrency = round(priceOnUSD * USDToOutputEquivalence, 2)
        newOffer = offer + (priceOnOutputCurrency,)
        updatedResults.append(newOffer)   
    
    return updatedResults
        