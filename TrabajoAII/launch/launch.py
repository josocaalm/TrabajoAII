#encoding: utf-8

from tf2outpost.loginThroughSteam import loginAndRedirectToSearchPage
from tf2outpost.gameSearch import prepareSearchForm
from tf2outpost.gameSearch import retrieveListOfGames

def launch_game_list_search(query):
    driver = loginAndRedirectToSearchPage()
    driver = prepareSearchForm(query, driver)
    driverAndGameList = retrieveListOfGames(driver)
    
    return driverAndGameList