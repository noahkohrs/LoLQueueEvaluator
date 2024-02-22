# LoL Queue Calculator

## Overview
This Python tool is designed for League of Legends (LoL) players to analyze the concept of winner and loser queues. It calculates and interprets history to determine if a player is likely in a winner's queue (where the chances of winning are higher due to unknown factors) or a loser's queue. By assessing recent game win rates the tool aims to provide insights into a player's current matchmaking status.


## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/noahkohrs/LoLQueueEvaluator
   ```
2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up `.env` file with your Riot Games API key
   
   First, create a file named `.env` in the root directory of the project.
   Then, add the following line to the file, replacing `<your-api-key-here>` with your Riot Games API key :
   ```
   YOUR_LOL_API_KEY='<your-api-key-here>'
   ```

   *Note* : You can get your API key from [Riot Games](https://developer.riotgames.com/)

   *Warning* : The standard api key lasts for 24 hours, so you will need to replace it every day. 

## Usage

Run the script.

Example :
```python
python main.py
```

This will open a GUI that looks like this:

![GUI](UI_img.png)


## Credits

Thanks to [Riot Games](https://developer.riotgames.com/) for providing the API used in this project.



## Authors
- [Arthur Mermet](https://github.com/DNSJambon)
- [Noah Kohrs](https://github.com/noahkohrs)


## Disclaimers

- This is a prototype and is not intended for serious use.

- The analysis could take several minutes to run due to the rate limits of the Riot Games API.

- This project only currently works for EUW players. Feel free to fork and add support for other regions.

- This is a personal project and is not endorsed by Riot Games. It is created for educational purposes.
