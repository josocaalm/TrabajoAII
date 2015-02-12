#encoding: utf-8

from bs4 import BeautifulSoup
from TrabajoAII_app.models import Game, Genre, SteamTag
from utilities import auxFunctions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common import by
from django.core.exceptions import ObjectDoesNotExist


def obtainSteamTopGamesIDs(driver, maxSearchDepth, currentSearchDepth, gamesIDs):
    if currentSearchDepth <= maxSearchDepth:
        WebDriverWait(driver,60).until(EC.presence_of_element_located((by.By.CLASS_NAME, "search_pagination")))
        soup = BeautifulSoup(driver.find_element_by_id("search_result_container").get_attribute("innerHTML"))
        
        for game in soup.findAll("a"):
            try:
                gameID = game["data-ds-appid"]
                gamesIDs.append(gameID)
            except:
                pass
            
        currentSearchDepth += 1
        driver.get("http://store.steampowered.com/search/?sort_by=_ASC&category1=998&page=" + str(currentSearchDepth))
        return obtainSteamTopGamesIDs(driver, maxSearchDepth, currentSearchDepth, gamesIDs)
    else:
        auxFunctions.quitWebdriver(driver)
        return gamesIDs
    

def getSteamTopGamesInfo(gamesIDs):
    baseUrl = "http://store.steampowered.com/app/"
    driver = auxFunctions.createWebdriver(baseUrl)
    games = list()
    
    for gameID in gamesIDs:
        try:
            driver.get(baseUrl + gameID + "?l=en")
            infoDict = dict()
            
            gameName = driver.find_element_by_xpath("//span[@itemprop='name']").text
            gameCoverHTML = driver.find_element_by_xpath("//div[@class='game_header_image_ctn']").get_attribute("innerHTML")
            coverHTMLSoup = BeautifulSoup(gameCoverHTML)
            gameCover = coverHTMLSoup.find("img")["src"]
            
            gameGenres = driver.find_element_by_xpath('//div[@class="details_block"]').find_element_by_tag_name("a").text.split(",")
            gameUserTagsElem = driver.find_element_by_xpath('//div[@class="glance_tags popular_tags"]')
            
            gameUserTags = list()
            for tag in gameUserTagsElem.find_elements_by_tag_name("a"):
                gameUserTags.append(tag.text)
                
            gameUserTags = [tag for tag in gameUserTags if tag != '']
            
            infoDict = {"name": gameName, "cover": gameCover, "genres": gameGenres, "tags": gameUserTags, "steamID": gameID}
            games.append(infoDict)
        except:
            pass
    
    auxFunctions.quitWebdriver(driver)
        
    return games


def loadMySQLDatabase(games):
    for game in games:
        newGame = Game(name = game["name"], coverString = game["cover"], steamID = game["steamID"])
        
        try:
            gameDB = Game.objects.get(steamID = game["steamID"])
            newGame = gameDB
        except ObjectDoesNotExist:
            newGame.save()
            
        for tag in game["tags"]:
            try:
                tagDB = SteamTag.objects.get(tagName = tag)
                tagDB.games.add(newGame)
            except ObjectDoesNotExist:
                newGameTag = SteamTag(tagName = tag)
                newGameTag.save()
                newGameTag.games.add(newGame)
            
        for genre in game["genres"]:
            try:
                genreDB = Genre.objects.get(name = genre)
                genreDB.games.add(newGame)
            except ObjectDoesNotExist:
                newGameGenre = Genre(name = genre)
                newGameGenre.save()
                newGameGenre.games.add(newGame)
