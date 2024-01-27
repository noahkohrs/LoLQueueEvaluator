# LoL Queue Calculator

## Overview
This Python tool is designed for League of Legends (LoL) players to analyze the concept of winner and loser queues. It calculates and interprets history to determine if a player is likely in a winner's queue (where the chances of winning are higher due to various factors) or a loser's queue (where the opposite is true). By assessing recent game statistics such as win rates, team performance, and player behaviors, the tool aims to provide insights into a player's current matchmaking status.

## Features
- **Winrate Analysis:** Calculates and displays the winrate of allies and enemies in the player's last few games.

- **Player Death Analysis:** Identifies whether the player had the teammate who died the most in recent matches.

- **API Call Management:** Efficiently manages API calls to avoid overloading with built-in sleep timers.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/noahkohrs/LoLQueueEvaluator
   ```
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up `.env` file with your Riot Games API key:
   ```
   YOUR_LOL_API_KEY='<your-api-key-here>'
   ```

## Credits

Thanks to [Riot Games](https://developer.riotgames.com/) for providing the API used in this project.

## Usage

Run the script and follow the on-screen prompts to input the player's name, the number of games for analysis, and the starting game number for calculation.

Example:
```python
python main.py
```

## Authors
- [Arthur Mermet](https://github.com/DNSJambon)
- [Noah Kohrs](https://github.com/noahkohrs)



## Disclaimers

This is a prototype and is not intended for serious use.

This is a personal project and is not endorsed by Riot Games. It is created for educational purposes.
