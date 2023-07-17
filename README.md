# Four in a Row Bot

This project is a Discord bot that lets Discord users play the popular two-player game 
Four in a Row (called Connect Four by Hasbro) against each other. 

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

## Screenshots

### A user initiating a game
![](media/game_start.png)

### A game in progress

![](media/game_in_progress.png)

### A player resigning a game

![](media/resign.png)

### A player initiating a game and choosing to start second
![](media/starting_second.png)

### A game with a custom board size (8 rows and 8 columns)

![](media/custom_board.png)

## Video demo





