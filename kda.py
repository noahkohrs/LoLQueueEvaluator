def getRatioKDAwithoutPlayer(player):
    """Return the ratio of the KDA of the player in the last N games"""
    my_region = "euw1"
    N = 20 # nombre de parties à analyser
    me = watcher.summoner.by_name(my_region, player)
    data = json.dumps(me, indent=4)
    fp.write(data)
    puuid = me['puuid']
    YourTeam = []
    TheirTeam = []
    my_matches = watcher.match.matchlist_by_puuid('europe', me['puuid'], queue=420)
    for i in range(0, N):
        (blue,red) = getMatchKDA(my_matches[i], puuid)


        if len(red) == 4:
            YourTeam.append(sum(red)/len(red))
            TheirTeam.append(sum(blue)/len(blue))
        else :
            YourTeam.append(sum(blue)/len(blue))
            TheirTeam.append(sum(red)/len(red))

    print("Ta Team : %.2f\nL'autre : %.2f" %(sum(YourTeam)/len(YourTeam), sum(TheirTeam)/len(TheirTeam)))



def getMatchKDA(match, puuid):
    """Return the KDA of the players in the match"""
    match_detail = watcher.match.by_id(my_region, match)
    red_kda = []
    blue_kda = []
    for j in range(0, 10): # 10 joueurs
        kda = match_detail["info"]["participants"][j]["challenges"]["kda"]
        if not (match_detail["metadata"]["participants"][j] == puuid) :
            if j < 5:
                blue_kda.append(kda)
            else:
                red_kda.append(kda)
    return (blue_kda, red_kda)