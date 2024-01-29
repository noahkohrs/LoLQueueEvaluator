import pandas as pd
import json
import time
from termcolor import colored, cprint
from colorama import Fore as c
from datetime import datetime
import lol_api_endpoints as api

# Load env variables
import os
from dotenv import load_dotenv
def load_api_key():
    load_dotenv()
    return os.getenv('YOUR_LOL_API_KEY')

def init_Calc() :
    """Initialize the global variables"""
    global api_key, my_region, CallCounter, debug, database
    api_key = load_api_key()
    my_region = "europe"
    CallCounter = 0
    debug = False
    database = {}



def DataIsUnknown(arg) :
    global database
    return not (arg in database.keys())

# Getters
def getSoloQueueListByPuuid(puuid, region="europe", from_timestamp = 0, count = 20):
    global api_key, CallCounter
    res = api.matchlist_by_puuid(api_key, region, puuid, 0)
    CallCounter+=1
    return res

def getMatchDetailsById(match):
    global api_key, CallCounter
    res = api.match_by_id(api_key, "europe", match)
    CallCounter+=1
    return res

def getSummonerByRiotID(name, tag):
    global api_key, CallCounter
    res = api.account_by_riot_id(api_key, "europe", name, tag)
    CallCounter+=1
    return res

def getSummonerByPuuid(puuid):
    global api_key, CallCounter
    res = api.account_by_puuid(api_key, "europe", puuid)
    CallCounter+=1
    return res

def PlayerInBlueTeam(match_detail, puuid):
    return match_detail["metadata"]["participants"].index(puuid)<5


def PlayerWonTheGame(match_detail, puuid):
    if PlayerInBlueTeam(match_detail, puuid):
        return match_detail["info"]["teams"][0]["win"]
    else:
        return match_detail["info"]["teams"][1]["win"]

def PlayerNumberOfWins(player_puuid, n, timing):
    matches = getSoloQueueListByPuuid(player_puuid, from_timestamp = timing, count = n)

    win = 0
    for i in range(0,min(len(matches),n)) : 
        match_detail = getMatchDetailsById(matches[i])
        if PlayerWonTheGame(match_detail, player_puuid):
            win+=1
    return win

def ColorChoicer(winrate):
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


def PlayersWinsLastGames(playerName, playerTag, N : int, wantedGameNumber : int):
    init_Calc()

    start_time = time.time()
    debug = True
    me = getSummonerByRiotID(playerName, playerTag)

    matches = getSoloQueueListByPuuid(me['puuid'], count = N+wantedGameNumber)

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
                currentPlayerPuuid = match_detail["metadata"]["participants"][j]

                x = PlayerNumberOfWins(currentPlayerPuuid, N, int(timingOfTheGame/1000))
                win_b.append(x)

        for j in range(5, 10):
            if j != me_index:
                currentPlayerPuuid = match_detail["metadata"]["participants"][j]
         
                x = PlayerNumberOfWins(currentPlayerPuuid, N, int(timingOfTheGame/1000))
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
