# Four in a Row Bot

This project is an open-source Discord bot that lets Discord users play the popular two-player game Four in a Row (called Connect Four by Hasbro) against each other or against an AI.  

The project has three parts, all written in Python:

* **The Discord bot code** (located in the [bot](/bot) directory): The code for the bot uses the [discord.py](https://discordpy.readthedocs.io/en/stable/) library.
* **The Data API** (located in the [server](/server) directory): The Data API uses [Flask](https://flask.palletsprojects.com/en/2.3.x/quickstart/) framework. The Data API interacts with a [MongoDB](https://www.mongodb.com/) database that stores game data. The Discord bot uses the Data API to save completed games to the MongoDB database and to retrieve player stats from the database. 
* **The AI API** (located in the [ai_server](/ai_server) directory): The AI API also uses the Flask framework. The AI API uses the [minimax](https://en.wikipedia.org/wiki/Minimax) algorithm with alpha-beta pruning and iterative deepening to determine a minimax value and move suggestion given a board position. The Discord bot uses the AI API to let human players against the AI. 

**[Video Demos](#video-demos)**<br/>
**[Features](#features)**<br/> 
**[Self-hosting Instructions](#self-hosting-instructions)**<br/>
**[Screenshots](#screenshots)**<br/>
**[Bot Usage](#bot-usage)**<br/>

## Video Demos

### A game between two Discord users

https://github.com/NikhilSDate/FourInARowBot/assets/47920034/8dfe280b-bb10-4135-884b-9693179681fe

### A game between a Discord user and the AI

https://github.com/NikhilSDate/FourInARowBot/assets/47920034/b108a7cd-730a-472d-b9d4-30650663c70f

## Features
### Bot

* The bot supports multiple simultaneous games across different servers and channels. However, 
only one game can be played at a time in a single channel.
* The standard Four in a Row board has 6 rows and 7 columns. Games are won by achieving 4 pieces in a row. The bot 
  supports games with custom board sizes (users can specify the number of rows and columns they want when creating a new game).
  Users can also specify a custom number of pieces in a row to win the game.
* By default, the bot randomly chooses which players starts first, but the player 
  initiating the game can also chose whether they want to start first or second.
* A player can resign a game at any time. This will end the game and give the win to the other player.
* The bot detects and correctly handles invalid moves (such as a move by a player when it's not their turn, a move 
  in a column that's full, a move by a user who's not a participant in an active game)
* The bot saves each game to the MongoDB database after the game has completed by calling the Data API. 
* The bot allows users to view their stats (the number of games they have won, lost, and drawn). 
* The bot lets human players play against an AI. The AI is quite strong and offers a tough challenge to casual players. 

### Data API 
* The Data API exposes an API endpoint to save games to a MongoDB database. The API saves the following data in the database:
  - The Discord User IDs of the two players who played the game,
  - The IDs of the server and channel in which the game was played,
  - The game configuration (number of rows, columns, and pieces in a row to win),
  - The moves played in the game,
  - The result of the game, and
  - The date and time when the game was completed.
* The Data API exposes another API endpoint to retrieve stats for a user given their Discord User ID. Stats consist of the number of games the user has won, lost and drawn. Stats can also be queried for games played against a particular opponent, in a particular server or channel, and in a particular date and time range.
* To protect user data, the Data API is secured using an API key that must be sent as an authorization header with every request. A hashed version of the API key is stored in the MongoDB database. If you want to host this bot yourself, you will have to generate an API key and store it in the database manually (see the [Self-hosting Instructions](#self-hosting-instructions) section for more information).

### AI API

* The AI API exposes an API endpoint to get a minimax value and move suggestion for a given game position. A game position consists of the board state and the color whose turn it is to play. 
* The AI API uses [minimax](https://en.wikipedia.org/wiki/Minimax) with alpha-beta pruning and iterative deepening. Iterative deepening means that the AI will first search to depth 1, then depth 2, then depth 3, and so on, instead of directly searching to a preset depth. Iterative deepening offers a number of advantages:
  * The effectiveness of alpha-beta pruning depends on the order in which nodes at a particular depth are searched. Using iterative deepening, search to a depth $n$ can be sped up by examining nodes at the same level in order, from best to worst, of their minimax values calculated during the search to depth $n - 1$.
  * Iterative deepening allows a time limit to be set for the AI. If a time limit is set, the AI will return the results from the deepest search that completed before the time limit was hit. This means that, given the same time limit, the AI will automatically search deeper when it has more computing power available.
* The AI API can be configured with time and depth limits. The AI stops searching when it hits either the time limit or the depth limit and returns the result of the deepest completed search.


## Self-hosting Instructions

To run this bot, you will have to host it yourself. This will involve individually hosting three applications: the bot and a Flask backend application each for the Data API and the AI API. The bot can, however, run without any or both of the two APIs; it will simply lack the features that rely on the missing API or APIs. 

### A) Installing and running the bot without the backend APIs

* Clone this repository: `git clone https://github.com/NikhilSDate/FourInARowBot.git`
* Navigate to the `bot` directory. This is where the code for the bot is located
* Install the requirements: `pip install -r requirements.txt`
* Get a [Discord token](https://www.technobezz.com/how-to-get-a-discord-bot-token/). 
* Create a file with the name `.env` in the `bot` directory. Paste the following line into this file:
  ```
  DISCORD_TOKEN=<your_discord_token>
  ```
* Run the `main.py` script with `python main.py`. The bot should now be up and running.
* Create an invite link for the bot in the Discord Developer Portal. You will need to specify permissions for the bot when doing so. The bot needs only the 'Send Messages' permission. A server administrator can now use the invite link (by pasting it into a browser) to add the bot to their server. You can also test out the bot now by creating a test server and inviting the bot to it.

### B) Running the Data API 
Note: these instructions are for running the backend locally. If you want to run the backend on a cloud platform like Render or Vercel, you might have to manually add the `DB_URI` emvironment variable instead of using a `env` file. See the instructions below for the value of this environment variable.

* Create a MongoDB database (either locally or in the cloud) to store game data. The database will store game data in a collection named `games`. If you use MongoDB Atlas for this step, you will have to add the public IP address of the Flask backend to the IP Access List of the MongoDB Atlas project containing your database. 
* Navigate to the `server` directory.
* Install the requirements: `pip install -r requirements.txt`
* In the `server` directory, create a file named `.env`. Paste the following line into this file (note that the connection string should have the database name at its end):
  ```
  DB_URI=<your_monngodb_connection_string>
  ```
* The Flask application is contained in the `app.py` file in the `server` directory. You can run the application locally using Flask's development server using the following command from the `server` directory:
  ```
  flask run --cert=adhoc
  ```
  This runs the aplication over HTTPS using a self-signed certificate. HTTPS is needed since the application receives an API key and sends and receives Discord User IDs, which should both be encrypted.
* The Flask application for the Data API should be up and running. However, the bot won't be able to talk to the application just yet. [Section D](#d-integrating-the-bot-with-the-data-and-ai-apis) explains how to integrate the bot with the Data API.

### C) Running the AI API
Note: As with the previous section, the instructions in this section are for running the backend locally. Unlike the Data API, however, the AI API does not need access to any external resources (like a database), so there is no need to configure a `.env` file.

* Navigate to the `ai_server` directory.
* Install the requirements: `pip install -r requirements.txt`
* If you want to change the time and/or depth limit for the AI, edit the values for `TIME_LIMIT` and `MAX_DEPTH` in the `config.json` file in the `ai_server` directory. The `TIME_LIMIT` value is in seconds. The AI stops searching when it hits either the time limit or the depth limit and returns the result of the deepest completed search. The default value for `TIME_LIMIT` is `9.75` (for a 10-second limit with some margin for overheads). The default value for `MAX_DEPTH` is `20`
* The Flask application is contained in the `app.py` file in the `ai_server` directory. You can run the application locally by executing the following command from the `ai_server` directory:
  ```
  flask run
  ```
* The Flask application for the AI API should be up and running. However, the bot won't be able to talk to the application just yet. [Section D](#d-integrating-the-bot-with-the-data-and-ai-apis) explains how to integrate the bot with the Data API.

### D) Integrating the bot with the Data and AI APIs
* Generate an API key using a method of your choice. For example, you could use the `token_hex()` method of Python's `secrets` module to generate a random hexadecimal text string to use as the API key. Once you have an API key, use Python's `hashlib` module to hash the key using SHA256 as follows (where `key` is your API key and should be a string):
  ```python
  hashed_key = hashlib.sha256(key.enocode('utf-8')).hexdigest()
  ```
* Create a collection named `api_keys` in your database and insert the following document into it:
  ```javascript
  {
    key: "<your hashed key>"
  } 
  ```
  MongoDB should generate an `_id` field for this document automatically.
* Navigate to the `bot` directory.
* In the `.env` file you created in part A in the `bot` directory, add the following line:
  ```
  DATA_API_KEY=<your-unhashed-api-key>
  ```
  Make sure that you add the **unhashed** API key.
*  Open the `config.json` file in the bot directory and enter the following text:
  ```javascript
  {
    "DATA_API_URL": "<url_of_the_data_api>",
    "AI_API_URL": "<url_of_the_ai_api>"
  }
  ```
* Stop the `main.py` script if it is still running from when you ran it in Part A and run it again with `python main.py`. The bot should now be able to talk to the Data and AI APIs.

## Screenshots

### A user initiating a game
![game start](media/game_start.png)

### A game in progress

![game in progress](media/game_in_progress.png)

### A player resigning a game

![resign](media/resign.png)

### Viewing stats with and without filters

![stats](media/stats.png)

### A game with a custom board size (8 rows and 8 columns)

![8x8 board](media/custom_board.png)

### A player initiating a game and choosing to start second
![starting second](media/starting_second.png)

## Bot Usage

Angle brackets indicate a required parameter. Square brackets indicate an optional parameter. 
A value for an optional parameter, if given, indicates the default value for that parameter. 
For example, `rows=6` means that the default value for the `rows` parameter is `6`. 
Only the values of parameters should be specified when running commands, not the names. 
See the example usage for each command for examples of this. 

| Command                                                                                         | Description                                                                                                                                                                                                                                                                                                                                                                                                     |
|-------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| !newgame \<other_player_mention\> \[mode=random\] \[rows=6\] \[columns=7\] \[winning_length=4\] | Create a new game. <br/> To play against an AI, specify `ai` (no need for an @ symbol) for the `<other_player_mention>` argument. <br/> The `mode` argument controls which player starts first and must be either `first`, `second`, or `random`. <br/> Example usage for playing against another player: <br/> `!newgame @foobar second 8 8 4` <br/> Example usage for playing against AI: <br/> `!newgame ai` |
| !move \<column\>                                                                                | Play a move <br/> Example usage: <br/> `!move 4`                                                                                                                                                                                                                                                                                                                                                                |
| !resign                                                                                         | Resign the game <br/> Example usage: <br/> `!resign`                                                                                                                                                                                                                                                                                                                                                            |
| !stats \[filters\]                                                                              | Get your stats <br/> Allowed filters are `against: @user`, `server: current` (to get stats for games played in the current server), `from: YYYY-MM-DD`, `to: YYYY-MM-DD` and `channel: #channel`<br/> Example usage: <br/> `!stats against: @foobar server: current from: 2023-01-01 channel: #general`                                                                                                         |
| !help \[command=None\]                                                                          | Get a list of all the commands or get help on a specific command <br/>Example usage: <br/> `!help newgame`                                                                                                                                                                                                                                                                                                      |







