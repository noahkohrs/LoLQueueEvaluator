import tkinter as tk
from tkinter import messagebox
from algo import PlayersWinsLastGames, FinalColorChoicer
from scipy.stats import binom
from colorama import Fore as c
from tkinter import ttk
import pickle

try:
    with open('history.pkl', 'rb') as f:
        history = pickle.load(f)
except FileNotFoundError:
    history = {}

def calculateWins(player, n, wanted_game):
    riotID = player.split('#')
    playerName = riotID[0]
    try :
        playerTag = riotID[1]
    except IndexError:
        playerTag = "EUW"
    return PlayersWinsLastGames(playerName, playerTag, n, wanted_game)


def calculateBinomialProbability(success, n):
    return min(binom.cdf(success, n, 0.5),
               1 - binom.cdf(success-1, n, 0.5))

def onSelect(evt):
    w = evt.widget
    index = int(w.curselection()[0])
    value = w.get(index)
    messagebox.showinfo("Results", history[value])


def calculateAction():
    player_name: str = player_name_entry.get()
    n: int = int(sessions_spinbox.get())
    starting_game: int = int(starting_game_spinbox.get())
    tag = player_name + "-" + str(n) + "-" + str(starting_game)
    # try:
    WinLoss = calculateWins(player_name, n, starting_game)
    # except:
    #     messagebox.showerror("Error", "Please verify that you have entered a valid key in the .env file and that the player name is correct")
    #     return
    AllyWinrate = WinLoss[0]/(n*n*4)*100
    EnemyWinrate = WinLoss[1]/(n*n*5)*100
    BinAlly = calculateBinomialProbability(WinLoss[0], n*n*4)
    BinEnemy = calculateBinomialProbability(WinLoss[1], n*n*5)
    cumulativeSuccesses = WinLoss[0]+(n*n*5-WinLoss[1])
    totalNumberOfGames = n*n*9
    FinalResult = calculateBinomialProbability(cumulativeSuccesses, totalNumberOfGames)

    Conclusion = "\n"
    if FinalResult < 0.006:
        if cumulativeSuccesses >= (n*n*9)*0.5:
            Conclusion = "You litteraly can't lose next game"
        else:
            Conclusion = "Wtf these game were wild 💀💀💀"
    elif FinalResult < 0.07:
        if cumulativeSuccesses >= (n*n*9)*0.5:
            Conclusion = "You're surely in winner's queue"
        else:
            Conclusion = "You're surely in looser's queue"
    elif FinalResult < 0.2:
        if cumulativeSuccesses >= (n*n*9)*0.5:
            Conclusion = "You're probably in winner's queue"
        else:
            Conclusion = "You're probably in looser's queue"
    else :
        Conclusion = "You're probably in neutral queue"


    if tag in history:
        # Remove the old entry
        for (i, item) in enumerate(results_list.get(0, tk.END)):
            if item == tag:
                results_list.delete(i)
                break

    result  = f"Evaluating winrate of {player_name} on his last {n} games starting from his {starting_game}th game\n"
    result += f"Winrate of your allies in the last {n} games: {AllyWinrate:.2f}% ({BinAlly*100:.2f}% binomial chance)\n"
    result += f"Winrate of your enemies in the last {n} games: {EnemyWinrate:.2f}% ({BinEnemy*100:.2f}% binomial chance)"
    result += f"\nFinal result: {FinalResult*100:.2f}% binomial chance"
    result += "\n\n" + Conclusion
    history[tag] = result
    
    results_list.insert(0, tag)
    with open('history.pkl', 'wb') as f:
        pickle.dump(history, f)
    messagebox.showinfo("Results", result)






root = tk.Tk()
root.title("LoL Queue Calculator")


main_frame = tk.Frame(root)
main_frame.pack(fill=tk.BOTH, expand=True)

# PanedWindow
paned_window = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
paned_window.pack(fill=tk.BOTH, expand=True)

# Input section (left side)
input_frame = tk.LabelFrame(
    paned_window, text="LoL Queue Calculator", padx=10, pady=10)
input_frame.pack(fill=tk.BOTH, expand=True)

# Player name input
player_name_label = tk.Label(input_frame, text="Player name :")
player_name_label.pack()
player_name_entry = tk.Entry(input_frame)
player_name_entry.pack()

# Number of sessions input
sessions_label = tk.Label(input_frame, text="Number of game recursions :")
sessions_label.pack()
sessions_spinbox = tk.Spinbox(input_frame, from_=1, to=5)
sessions_spinbox.pack()

# Starting game input
starting_game_label = tk.Label(input_frame, text="From which game :")
starting_game_label.pack()
starting_game_spinbox = tk.Spinbox(input_frame, from_=0, to=10)
starting_game_spinbox.pack()

# Calculate button
calculate_button = tk.Button(input_frame, text="Calculate", command=calculateAction)
calculate_button.pack()

paned_window.add(input_frame)

# Results section (right side)
results_frame = tk.LabelFrame(
    paned_window, text="List of Results", padx=10, pady=10)
results_frame.pack(fill=tk.BOTH, expand=True)

# Results
results_list = tk.Listbox(results_frame)
results_list.bind('<<ListboxSelect>>', onSelect)
results_list.pack()
for tag in history:
    results_list.insert(0, tag)

# Add the results frame to the paned window
paned_window.add(results_frame)

# Run the main loop
root.mainloop()
