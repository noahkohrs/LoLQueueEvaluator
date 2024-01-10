# Importing file algo.py
from algo import PlayersWinratesLastGames, ColorChoicer, TotalPingsLastGames, FinalColorChoicer
from colorama import Fore as c
from scipy.stats import binom

player = input("Player to analyze: ")
# Number of games on which the winrate is calculated
n = int(input("Number of games to calculate the winrates on: "))

wanted_game = int(input("Game from which to start calculating the winrate series (starting from the most recent): "))

# Coloring the below print in red/blue depending on the team
# Set the parameters of the binomial distribution
p = 0.5  # probability of success in each trial

# Calculate the probability of X <= 5


WinLoss = PlayersWinratesLastGames(player, n, wanted_game)
if WinLoss[0] >= 50:
    AllyC = FinalColorChoicer(
        binom.cdf(int((WinLoss[0]/100)*4*n*n-1), 4*n*n, 0.5)*100)
else:
    AllyC = FinalColorChoicer(
        binom.cdf(int((WinLoss[0]/100)*4*n*n), 4*n*n, 0.5)*100)

if WinLoss[1] >= 50:
    EnemyC = FinalColorChoicer(
        binom.cdf(int((WinLoss[1]/100)*5*n*n-1), 5*n*n, 0.5)*100)
else:
    EnemyC = FinalColorChoicer(
        binom.cdf(int((WinLoss[1]/100)*5*n*n), 5*n*n, 0.5)*100)

BinAlly = min(binom.cdf(int((WinLoss[0]/100)*4*n*n), 4*n*n, 0.5),
              1 - binom.cdf(int((WinLoss[0]/100)*4*n*n-1), 4*n*n, 0.5))
BinEnemy = min(binom.cdf(int((WinLoss[1]/100)*5*n*n), 5*n*n, 0.5),
               1 - binom.cdf(int((WinLoss[1]/100)*5*n*n-1), 5*n*n, 0.5))

print("Evaluating winrate of %s on his last %d games starting from his %dth game" %
      (player, n, wanted_game))
print()
print(AllyC+"Winrate of your allies in the last %d games: %.2f%% (%.2f%% binomial chance)" %
      (n, WinLoss[0], BinAlly*100))
print(EnemyC+"Winrate of your enemies in the last %d games: %.2f%% (%.2f%% binomial chance)" %
      (n, WinLoss[1], BinEnemy*100))
print(c.RESET)
TotalPingsLastGames(player, n, wanted_game)
