#encoding: latin1

from steam.loadDatabase import obtainSteamTopGamesIDs, getSteamTopGamesInfo, loadMySQLDatabase
from utilities.auxFunctions import createWebdriver

def launchDBDataLoad():
    gamesIDs = obtainSteamTopGamesIDs(createWebdriver("http://store.steampowered.com/search/?sort_by=_ASC&category1=998&page=1"), 100, 1, [])
    games = getSteamTopGamesInfo(gamesIDs)
    loadMySQLDatabase(games)