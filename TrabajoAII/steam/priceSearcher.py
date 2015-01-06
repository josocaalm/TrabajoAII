#encoding: utf-8

from urllib.request import urlopen
from urllib.error import HTTPError
import isoCurrenciesCountries.ISOCodes as iso
import currency.currencies as currency
import utilities.auxFunctions as utilsFuncs
import json
 
 
def findGamePriceAndDetailsByID(gameID):
    dictCurrencyAndGameDetails = dict()
    isoCountryCodesDict = iso.ISO3166CodeToCountry()
         
    for code in isoCountryCodesDict.keys():
        url = "http://store.steampowered.com/api/appdetails/?appids=" + str(gameID) + "&cc=" + code + "&l=english&v=1"
        
        try:
            html = urlopen(url).read()
    
            jsonData = json.loads(html.decode("utf-8"))
            
            gamePrice = str(jsonData[str(gameID)]["data"]["price_overview"]["initial"])
            priceCurrency = jsonData[str(gameID)]["data"]["price_overview"]["currency"]
            discount = jsonData[str(gameID)]["data"]["price_overview"]["discount_percent"]
            gamePriceDiscount = str(jsonData[str(gameID)]["data"]["price_overview"]["final"])
            gameName = jsonData[str(gameID)]["data"]["name"]
            
            gamePrice = float(gamePrice[:len(gamePrice)-2] + "." + gamePrice[len(gamePrice)-2:])
            gamePriceDiscount = float(gamePriceDiscount[:len(gamePriceDiscount)-2] + "." + gamePriceDiscount[len(gamePriceDiscount)-2:])
    
            res = (gameID, code, isoCountryCodesDict[code], gamePrice, discount, gamePriceDiscount, gameName)
              
            if priceCurrency in dictCurrencyAndGameDetails.keys() and gamePrice < dictCurrencyAndGameDetails[priceCurrency][3]:
                del dictCurrencyAndGameDetails[priceCurrency]
                dictCurrencyAndGameDetails[priceCurrency] = res
            if priceCurrency not in dictCurrencyAndGameDetails.keys():
                dictCurrencyAndGameDetails[priceCurrency] = res
                        
        except HTTPError:
            pass
     
    return dictCurrencyAndGameDetails
     
 
def priceConversion(outputCurrency, dictCurrencyAndGameDetails):
    convertedPriceList = list()
    
    driver = utilsFuncs.createWebdriver("https://www.google.com/finance/converter")
     
    for curr in dictCurrencyAndGameDetails.keys():
        if curr != outputCurrency:
            conversionValue = currency.findConversion(curr, outputCurrency, driver)
            convertedPrice = utilsFuncs.performConversion(dictCurrencyAndGameDetails[curr][3], conversionValue)
             
            gameID = dictCurrencyAndGameDetails[curr][0]
            gameRegionIsoCode = dictCurrencyAndGameDetails[curr][1]
            gameStore = dictCurrencyAndGameDetails[curr][2]
            gameOldPrice = dictCurrencyAndGameDetails[curr][3]
            gameTitle = dictCurrencyAndGameDetails[curr][4]
             
            elemList = [gameID, gameRegionIsoCode, gameStore, gameTitle, gameOldPrice, curr, convertedPrice, outputCurrency]
        else:
            elemList = [gameID, gameRegionIsoCode, gameStore, gameTitle, gameOldPrice, curr, gameOldPrice, curr]
     
        convertedPriceList.append(tuple(elemList))
    
    utilsFuncs.quitWebdriver(driver)
     
    return convertedPriceList


def findLowestPrice(convertedPriceList):
    priceSet = set()
    result = tuple()
    
    for infoTuple in convertedPriceList:
        priceSet.add(infoTuple[6])
        
    minimumPrice = min(priceSet)
    
    for infoTuple in convertedPriceList:
        if infoTuple[6] == minimumPrice:
            result = infoTuple
            break
    
    return result