# Four in a Row Bot

This project is a Discord bot that lets Discord users play the popular two-player game 
Four in a Row (called Connect Four by Hasbro) against each other. THe bot uses a Flask backend API to store past games and retrieve player stats. The application has two parts—the bot code (in the [bot](/bot) directory and a backend API (in the [server](/server) directory) that interacts with a MongoDB database)

## Features


* The bot supports multiple simultaneous games across different servers and channels. However, 
only one game can be played at a time in a single channel.
* The standard Four in a Row board has 6 rows and 7 columns. Games are won by achieving 4 pieces in a row. The bot 
  supports games with custom board sizes (users can specify the number of rows and columns they want when creating  a new game).
  Users can also specify a custom number of pieces in a row to win the game.
* By default, the bot randomly chooses which players starts first, but there is also support for the player 
  initiating the game to chose whether they want to start first or second.
* A player can resign a game at any time. This will end the game and give the win to the other player.
* The bot detects and correctly handles invalid moves (such as a move by a player when it's not their turn, a move 
  in a column that's full, a move by a user who's not a participant in an active game)
* The project includes a Flask backend API that accepts requests to save every game after it has completed. For each game, the bot makes a request to the backend stores, in a MongoDB database, the Discord User IDs of the two players, the server and channel IDs in which the game was played, the board configuration for the game (number of rows, columns, and pieces in a row to win), the moves played in the game, the result of the game, and the date and time when the game was completed.
* The Flask backend also allows any player's stats (the number of games they have won, lost, and drawn) to be requested. The backend also allows the stats to be filtered by a specific opponent, Discord server or channel and by a date and time range. The bot uses this functionality to allow users to see their stats, filtered or unfiltered.
* To protect user data, the backend is secured using an API key that must be sent as an authorization header with every request. A hashed version of the API key is stored on the MongoDB database. If you want to use the run the backend code yourself, you will have to generate an API key and store it in the database yourself.

## Video demo

https://github.com/NikhilSDate/FourInARowBot/assets/47920034/8dfe280b-bb10-4135-884b-9693179681fe

## Screenshots

### A user initiating a game
![game start](media/game_start.png)

### A game in progress

![game in progress](media/game_in_progress.png)

### A player resigning a game

![resign](media/resign.png)

### A player initiating a game and choosing to start second
![starting second](media/starting_second.png)

### A game with a custom board size (8 rows and 8 columns)

![8x8 board](media/custom_board.png)




