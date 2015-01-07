#encoding: utf-8

from tf2outpost.loginThroughSteam import loginAndRedirectToSearchPage
from tf2outpost.gameSearch import *
from tf2outpost.outpostPriceSearcher import *
from utilities.auxFunctions import *

def launch_game_list_search(query):
    driver = loginAndRedirectToSearchPage()
    driver = prepareSearchForm(query, driver)
    driverAndGameList = retrieveListOfGames(driver)
    
    return driverAndGameList

def launch_fast_offer_search(name, fullId, outputCurrency):
    driver = loginAndRedirectToSearchPage()
    driver = prepareSearchForm(name, driver)
    driver = retrieveListOfGames(driver)[0]
    driver = fromTF2OutpostIDToSteamID(driver, fullId)[0]
    driver = enterToSearchPage(driver)
    
    foundOffers = findOutpostOffers(driver, name, 20, 1, [])
    results = extractKeysAndRefsPrice(foundOffers)
    sortedResults = sortSearchResults(results)
    finalResults = convertUSDToSpecifiedCurrency(sortedResults, outputCurrency)
    
    return finalResults