#encoding: utf-8

from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common import by
from bs4 import BeautifulSoup
from urllib.request import urlopen

def prepareSearchForm(inputText, driver):
    driver.execute_script("document.getElementById('gameid').setAttribute('style', '')")
    
    selectInventory = Select(driver.find_element_by_name("gameid"))
    selectInventory.select_by_value("753")

    searchField = driver.find_element_by_id("filter")
    searchField.clear()
    searchField.send_keys(inputText)
    
    action = ActionChains(driver);
    action.send_keys(Keys.ENTER).perform()
    
    return driver

def retrieveListOfGames(driver):
    searchMatches = list()
    
    try:
        WebDriverWait(driver,5).until(EC.presence_of_element_located((by.By.XPATH, "//li[@class='item it_753_6']")))
    except:
        pass
    
    for elem in driver.find_elements_by_xpath("//li[@class='item it_753_6']"):
        if elem.get_attribute("data-subtitle") == "Gift":
            name = elem.get_attribute("data-name")
            coverHTMLFragment = driver.find_element_by_xpath('//li[a[span[img[@alt="' + name + '"]]]]').get_attribute("innerHTML")
            coverHTMLSoup = BeautifulSoup(coverHTMLFragment)
            coverString = coverHTMLSoup.find("img")["src"]
            
            tf2outpostPartialID = elem.get_attribute("data-hash")
            firstCommaIndex = tf2outpostPartialID.index(",")
            tf2outpostFullID = tf2outpostPartialID[0:firstCommaIndex] + ",0," + tf2outpostPartialID[firstCommaIndex+1:]
            
            gameData = (name, coverString, tf2outpostPartialID, tf2outpostFullID)
            searchMatches.append(gameData)
    
    return [driver, searchMatches]


def fromTF2OutpostIDToSteamID(driver, tf2outpostFullID):
    driver.get("http://www.tf2outpost.com/item/" + tf2outpostFullID)
    steamFakeLinkElem = WebDriverWait(driver,10).until(EC.presence_of_element_located((by.By.XPATH, '//div[@class="summary box module"]/descendant::ul[@class="links"]/descendant::li/descendant::a[text()=" View on Steam"]')))
    steamFakeLink = steamFakeLinkElem.get_attribute("href")
    
    soup = BeautifulSoup(urlopen(steamFakeLink))
    
    try:
        steamTrueLinkElem = soup.find("link", {"rel" : "canonical"})
        if steamTrueLinkElem != None:
            steamTrueLink = steamTrueLinkElem["href"]
            steamID = steamTrueLink.replace("http://store.steampowered.com/app/", "")
            steamID = steamID.replace("/", "")   
        else:
            steamPossibleGamePackID = soup.find("input", {"name":"subid"})
            steamID = steamPossibleGamePackID["value"]
            
    except TypeError:
        steamCheckAgeForm = soup.find("form", {"id":"agecheck_form"})
        steamGameCoverLink = steamCheckAgeForm["action"]
        steamID = steamGameCoverLink.replace("http://store.steampowered.com/agecheck/app/", "")
        steamID = steamID.replace("/", "")    
    
    return [driver, int(steamID)]


def enterToSearchPage(driver):
    searchRedirectionButton = driver.find_element_by_xpath('//a[text()=" Sellers"]')
    searchRedirectionButton.click()
    
    return driver