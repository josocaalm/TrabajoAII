#encoding: utf-8

import tf2outpost.loginThroughSteam as login
import tf2outpost.gameSearch as gamesearch
import tf2outpost.outpostPriceSearcher as pricesearch

driver = login.loginAndRedirectToSearchPage()
driver = gamesearch.prepareSearchForm("terraria", driver)
driver = gamesearch.fromTF2OutpostIDToSteamID(driver, '753,0,82,6')[0]
driver = gamesearch.enterToSearchPage(driver)

foundOffers = pricesearch.findOutpostOffers(driver, "Terraria", 20, 1, [])
results = pricesearch.extractKeysAndRefsPrice(foundOffers)
sortedResults = pricesearch.sortSearchResults(results)
finalResults = pricesearch.convertUSDToSpecifiedCurrency(sortedResults, "EUR")

for res in finalResults:
    print(res)