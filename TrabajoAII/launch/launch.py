#encoding: utf-8

from tf2outpost.loginThroughSteam import loginAndRedirectToSearchPage
from tf2outpost.gameSearch import retrieveListOfGames, prepareSearchForm, fromTF2OutpostIDToSteamID, enterToSearchPage
from tf2outpost.outpostPriceSearcher import findOutpostOffers, extractKeysAndRefsPrice, sortSearchResults, convertUSDToSpecifiedCurrency
from utilities.auxFunctions import createWebdriver, quitWebdriver
from steam.priceSearcher import findGamePriceAndDetailsByID, priceConversion, findLowestPrice

def launch_game_list_search(query):
    driver = loginAndRedirectToSearchPage()
    driver = prepareSearchForm(query, driver)
    driverAndGameList = retrieveListOfGames(driver)
    
    return driverAndGameList

def launch_tf2outpost_offer_search(name, fullId, outputCurrency):
    driver = loginAndRedirectToSearchPage()
    driver = prepareSearchForm(name, driver)
    driver = retrieveListOfGames(driver)[0]
    driverAndId = fromTF2OutpostIDToSteamID(driver, fullId)
    driver = enterToSearchPage(driverAndId[0])
    
    foundOffers = findOutpostOffers(driver, name, 20, 1, [])
    results = extractKeysAndRefsPrice(foundOffers)
    sortedResults = sortSearchResults(results)
    finalResults = convertUSDToSpecifiedCurrency(sortedResults, outputCurrency)
    
    return finalResults

def launch_steam_best_offer(fullId, outputCurrency):
    driver = createWebdriver("http://www.tf2outpost.com")
    steamId = fromTF2OutpostIDToSteamID(driver, fullId)[1]
    quitWebdriver(driver)
    
    dictGamesAndDetails = findGamePriceAndDetailsByID(steamId)
    priceConversions = priceConversion(outputCurrency, dictGamesAndDetails)
    lowestPriceInfo = findLowestPrice(priceConversions)
    
    return lowestPriceInfo