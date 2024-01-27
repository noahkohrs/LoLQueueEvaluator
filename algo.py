from riotwatcher import LolWatcher, ApiError
import pandas as pd
import json
import time
from termcolor import colored, cprint
from colorama import Fore as c
from datetime import datetime
import requests

# Load env variables
import os
from dotenv import load_dotenv
def load_api_key():
    load_dotenv()
    return os.getenv('YOUR_LOL_API_KEY')

def init_Calc() :
    """Initialize the global variables"""
    global api_key, watcher, my_region, CallCounter, debug, database
    api_key = load_api_key()
    watcher = LolWatcher(api_key)
    my_region = "europe"
    CallCounter = 0
    debug = False
    database = {}
def Call():
    """Avoid overloading the API"""
    global CallCounter, watcher, debug
    CallCounter += 1
    if CallCounter%120==0 :
        time.sleep(60)
        if debug : print("Waiting 60 seconds")
    elif CallCounter%20==0 :
        time.sleep(2)
        if debug : print("Waiting 2 seconds")


def DataIsUnknown(arg) :
    global database
    return not (arg in database.keys())

# Getters
def getSoloQueueListByPuuid(puuid):
    global database
    id = "SoloQueues:"+puuid
    if DataIsUnknown(id) :
        database[id] = watcher.match.matchlist_by_puuid("europe", puuid, queue=420)
        Call()
    return database[id]

def getMatchDetailsById(match):
    global database
    id = "MatchDetails:"+match
    if DataIsUnknown(id) :
        database[id] = watcher.match.by_id("europe", match)
        Call()
    return database[id]

def watcher_accounts_by_riot_id(region, name, tag):
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
    response = requests.get(url, headers={"X-Riot-Token": api_key})
    return response.json()

def getSummonerByRiotID(name, tag):
    global database
    id = "Summoner:"+name
    if DataIsUnknown(id) :
        database[id] = watcher_accounts_by_riot_id("europe", name, tag)
        Call()
    return database[id]

def getSummonerByPuuid(puuid):
    global database
    id = "Summoner:"+puuid
    if DataIsUnknown(id) :
        database[id] = watcher.summoner.by_puuid("euw1", puuid)
        Call()
    return database[id]

def getSoloQueueListByPuuidAndTimestamp(puuid, timestamp):
    global database
    id = "SoloQueuesList:"+puuid+str(timestamp)
    if DataIsUnknown(id) :
        database[id] = watcher.match.matchlist_by_puuid("europe", puuid, queue=420, end_time=(timestamp//1000))
        Call()
    return database[id]



# Aux functions 
def PlayerHasThePlayerWhoDiedTheMost(match, puuid):
    match_detail = watcher.match.by_id(my_region, match)
    playerIndex = match_detail["metadata"]["participants"].index(puuid)
    maxDeaths = 0
    for j in range(0, 10): # 10 players
        deaths = match_detail["info"]["participants"][j]["deaths"]
        if deaths > maxDeaths and not (match_detail["metadata"]["participants"][j] == puuid) :
            maxDeaths = deaths
            maxDeathsIndex = j
    return (maxDeathsIndex < 5) == (playerIndex < 5)
    # B B = True
    # B R = False
    # R B = False
    # R R = True

def PlayerInBlueTeam(match_detail, puuid):
    return match_detail["metadata"]["participants"].index(puuid)<5

def PlayerWonTheGame(match_detail, puuid):
    if PlayerInBlueTeam(match_detail, puuid):
        return match_detail["info"]["teams"][0]["win"]
    else:
        return match_detail["info"]["teams"][1]["win"]

def PlayerNumberOfWins(player, n, timing): # player = player watcher
    matches = getSoloQueueListByPuuidAndTimestamp(player['puuid'], timing)
    win = 0
    for i in range(0,min(len(matches),n)) : 
        match_detail = getMatchDetailsById(matches[i])
        if PlayerWonTheGame(match_detail, player['puuid']):
            win+=1


    return win

def ColorChoicer(winrate):
    #4 stats : 0-25, 25-50, 50-75, 75-100
    if winrate<40:
        return c.RED
    elif winrate<45:
        return c.YELLOW
    elif winrate<=55:
        return c.WHITE
    elif winrate<60:
        return c.GREEN
    else:
        return c.BLUE

def FinalColorChoicer(winrate):
    #4 stats : 0-25, 25-50, 50-75, 75-100
    if winrate<=5:
        return c.RED
    elif winrate<=10:
        return c.YELLOW
    elif winrate<=90:
        return c.WHITE
    elif winrate<=95:
        return c.GREEN
    else:
        return c.BLUE

def TotalPings(match_detail, player_j):
    l=match_detail["info"]["participants"][player_j]
    return l["allInPings"]+l["assistMePings"]+l["baitPings"]+l["basicPings"]+l["commandPings"]+l["dangerPings"]+l["enemyVisionPings"]+l["getBackPings"]+l["holdPings"]+l["needVisionPings"]+l["onMyWayPings"]+l["pushPings"]+l["visionClearedPings"]


# Main functions
def PlayersWinsLastGames(playerName, playerTag, N : int, wantedGameNumber : int):
    init_Calc()

    start_time = time.time()
    debug = True
    me = getSummonerByRiotID(playerName, playerTag)
    matches = getSoloQueueListByPuuid(me['puuid'])
    
    wins_allies=0
    wins_enemies=0


    for i in range(wantedGameNumber, N+wantedGameNumber):
        win_b=[]
        win_r=[]

        match_detail = getMatchDetailsById(matches[i])
        me_index = match_detail["metadata"]["participants"].index(me['puuid'])
        timingOfTheGame = match_detail["info"]["gameEndTimestamp"]

        for j in range(0, 5):
            if j != me_index:
                p = getSummonerByPuuid(match_detail["metadata"]["participants"][j])
                x=PlayerNumberOfWins(p, N, timingOfTheGame)
                win_b.append(x)

        for j in range(5, 10):
            if j != me_index:
                p = getSummonerByPuuid(match_detail["metadata"]["participants"][j])              
                x=PlayerNumberOfWins(p, N,timingOfTheGame)
                win_r.append(x)              
        
        if debug: print("Game %d" % i)

        if PlayerInBlueTeam(match_detail,me["puuid"]):
            ActualAllyWins =sum(win_b)
            ActualEnemyWins=sum(win_r)
        else:
            ActualAllyWins=sum(win_r)
            ActualEnemyWins=sum(win_b)
        
        wins_allies+=ActualAllyWins
        wins_enemies+=ActualEnemyWins

        ActualAllyWinrate = (ActualAllyWins/(N*4))*100
        ActualEnemyWinrate = (ActualEnemyWins/(N*5))*100

        AllyC=ColorChoicer(ActualAllyWinrate)
        EnemyC=ColorChoicer(ActualEnemyWinrate)

        if debug : print(AllyC+"Your team's winrate: %.2f" % ActualAllyWinrate)
        if debug : print(EnemyC+"Enemy team's winrate: %.2f\n" % ActualEnemyWinrate + c.RESET)

    if debug :
        print("Number of API calls: %d" % CallCounter)
        print("Execution time: %s seconds" % (time.time() - start_time))

    return (wins_allies, wins_enemies)




def TotalPingsLastGames(playerName, playerTag, N : int, wantedGameNumber : int):

    me = getSummonerByRiotID(playerName, playerTag)
    matches = getSoloQueueListByPuuid(me['puuid'])
    pings_allies=0
    pings_enemies=0

    for i in range(wantedGameNumber, N+wantedGameNumber):
        pings_b=0
        pings_r=0
        
        
        match_detail = getMatchDetailsById(matches[i])
        me_index = match_detail["metadata"]["participants"].index(me['puuid'])

        for j in range(0, 5):
            if j != me_index:
                pings_b += TotalPings(match_detail, j)
        
        for j in range(5, 10):
            if j != me_index:            
                pings_r += TotalPings(match_detail, j)


        if PlayerInBlueTeam(match_detail,me["puuid"]):
            pings_allies += pings_b/4
            pings_enemies += pings_r/5
            
        else:
            pings_allies += pings_r/4
            pings_enemies += pings_b/5
             
    print("Average number of pings per allies in targeted games: %.1f" % (pings_allies/N))
    print("Average number of pings per enemies in targeted games: %.1f" % (pings_enemies/N))
    return (pings_allies, pings_enemies)
                      

def PlayerHasThePlayerWhoDiedTheMostInLastsMatches(playerName, playerTag, N, wantedGameNumber):

    debug = True
    me = getSummonerByRiotID(playerName, playerTag)
    matches = getSoloQueueListByPuuid(me['puuid'])

    totalAlly = 0
    totalEnemy = 0

    for i in range(wantedGameNumber, N+wantedGameNumber):
        win_b = []
        win_r = []

        match_detail = getMatchDetailsById(matches[i])
        me_index = match_detail["metadata"]["participants"].index(me['puuid'])
        timingOfTheGame = match_detail["info"]["gameEndTimestamp"]

        for j in range(0, 5):
            if j != me_index:
                p = getSummonerByPuuid(
                    match_detail["metadata"]["participants"][j])
                if PlayerHasThePlayerWhoDiedTheMost(p, N, timingOfTheGame):
                    totalAlly += 1

        for j in range(5, 10):
            if j != me_index:
                p = getSummonerByPuuid(
                    match_detail["metadata"]["participants"][j])
                if PlayerHasThePlayerWhoDiedTheMost(p, N, timingOfTheGame):
                    totalEnemy += 1

        if debug:
            print("Game %d" % i)

    RatioAlly = (totalAlly/(totalAlly+totalEnemy))*100
    RatioEnemy = (totalEnemy/(totalAlly+totalEnemy))*100
    AllyC = ColorChoicer(RatioAlly)
    EnemyC = ColorChoicer(RatioEnemy)
    if debug:
        print(AllyC+"Winrate of your team: %.2f" % RatioAlly + c.RESET)
    if debug:
        print(EnemyC+"Winrate of the enemy team: %.2f\n" %
              RatioEnemy + c.RESET)

    if debug:
        print("Number of API calls: %d" % CallCounter)

    return (round(RatioAlly, 2), round(RatioEnemy, 2))


def LooserQueueDetector(player, n, wanted_game):
    PlayerHasThePlayerWhoDiedTheMostInLastsMatches(player, n, wanted_game)
