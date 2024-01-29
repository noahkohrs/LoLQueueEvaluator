import requests
from time import sleep

debug = False

# queues :
# 420: soloQ
# 440: flexQ
# 700: clash

# /riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}
def account_by_riot_id(api_key:str, region:str, name:str, tag:str):
    global debug
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{name}/{tag}"
    response = requests.get(url, headers={"X-Riot-Token": api_key}).json()
    while "status" in response.keys():
        sleep(1)
        response = requests.get(url, headers={"X-Riot-Token": api_key}).json()
    if debug:
        print("account_by_riot_id request")
    return response

# /lol/match/v5/matches/by-puuid/{puuid}/ids
def matchlist_by_puuid(api_key:str, region:str, puuid:str, from_timestamp:int = None, count = 20):
    global debug
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}&queue=420"
    if from_timestamp is not None:
        url += f"&startTime={from_timestamp}"
    response = requests.get(url, headers={"X-Riot-Token": api_key}).json()
    if debug:
        print("matchlist_by_puuid request")
    try :
        while "status" in response.keys():
            sleep(1)
            response = requests.get(url, headers={"X-Riot-Token": api_key}).json()
    except AttributeError:
        return response
    return response

# /lol/match/v5/matches/{matchId}
def match_by_id(api_key:str, region:str, match_id:str):
    global debug
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}"
    response = requests.get(url, headers={"X-Riot-Token": api_key}).json()
    while "status" in response.keys():
        sleep(1)
        response = requests.get(url, headers={"X-Riot-Token": api_key}).json()
    if debug:
        print("match_by_id request")
    return response

# /riot/account/v1/accounts/by-puuid/{puuid}
def account_by_puuid(api_key:str, region:str, puuid:str):
    global debug
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-puuid/{puuid}"
    response = requests.get(url, headers={"X-Riot-Token": api_key}).json()
    while "status" in response.keys():
        sleep(1)
        response = requests.get(url, headers={"X-Riot-Token": api_key}).json()
    if debug:
        print("account_by_puuid request")
    return response
