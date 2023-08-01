import json
import os
import random
from datetime import datetime

from discord import Intents
from discord.ext import commands
from discord.ext.commands import Context

from dotenv import load_dotenv

from disc.discord_manager import DiscordManager
from disc.discord_two_player_game_manager import DiscordTwoPlayerGameManager
from disc.help_command import MyHelp
from game.statuses import Status, StatusType
from api_wrapper.data_api import DataAPI
from disc.utils import stat_dict_to_message, parse_colon_arguments, user_id_from_mention, channel_id_from_mention

load_dotenv()

if __name__ == "__main__":

    intents = Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents, help_command=MyHelp())
    discord_manager = DiscordManager()
    data_api = DataAPI()

    error_messages = {Status.CHANNEL_BUSY: 'A game is currently in progress in this channel.',
                      Status.NO_ACTIVE_GAME: 'You are not a participant in an active game in this channel.',
                      Status.WRONG_TURN: 'Please wait for the other player to complete his turn.',
                      Status.INVALID_INDEX: 'Please enter a valid column index.',
                      Status.COLUMN_FULL: 'The column you are trying to play your piece in is full.',
                      }


    @bot.command(help="Create a new game."
                      "\n\nThe `mode` argument controls which player starts first and must be either `first`,`second`, or `random`."
                      "\n\nExample usage: `!newgame @foobar second 8 8 4`")
    async def newgame(ctx: Context, other_player_mention: str, mode: str = 'random', rows: int = 6, columns: int = 7, winning_length: int = 4):

        author_id = str(ctx.author.id)
        other_player_id = 'ai' if other_player_mention == 'ai' else user_id_from_mention(other_player_mention)

        if mode == 'first':
            ids = [author_id, other_player_id]
        elif mode == 'second':
            ids = [other_player_id, author_id]
        elif mode == 'random':
            ids = [author_id, other_player_id]
            random.shuffle(ids)
        else:
            await ctx.send('The second argument of newgame \nmust be \'random\', \'first\', or \'second\'')
            return

        status = await discord_manager.new_game(channel=ctx.channel, guild=ctx.guild, first_player_id=ids[0],
                                             second_player_id=ids[1], dims=(rows, columns),
                                             winning_length=winning_length)

        if status != Status.OK:
            await ctx.send(error_messages[status])

    @bot.command(help='Play a move\nExample usage: `!move 4`')
    async def move(ctx: Context, column: int):
        zero_indexed_column = column - 1
        status = await discord_manager.do_move(channel=ctx.channel, player_id=str(ctx.author.id), column=zero_indexed_column)
        if status in StatusType.ERROR:
            await ctx.send(error_messages[status])


    @bot.command(help='Resign the game\n Example usage: !resign')
    async def resign(ctx: Context):
        status = await discord_manager.handle_resign(ctx.channel, str(ctx.author.id))
        if status in StatusType.ERROR:
            await ctx.send(error_messages[status])


    @bot.command(help="Get your stats"
                      "\n\nAllowed filters are `against: @user`, `server: current` (for games played in the current server only),`from: YYYY-MM-DD`, `to: YYYY-MM-DD` and `channel: #channel`"
                      "\n\nExample usage: `!stats against: @foobar server: current from: 2023-01-01 channel: #general`")
    async def stats(ctx: Context, *, filters=''):
        user_id = str(ctx.author.id)
        filters = parse_colon_arguments(filters, options=['against', 'server', 'from', 'to', 'channel', 'mode'])
        against = filters.get('against', None)
        guild = filters.get('server', None)
        channel = filters.get('channel', None)
        from_date = filters.get('from', None)
        to_date = filters.get('to', None)
        mode = filters.get('mode', 'concise')
        if against is not None:
            against = user_id_from_mention(against)
        if guild == 'current':
            guild = str(ctx.guild.id)
        if channel is not None:
            channel = channel_id_from_mention(channel)
        if from_date is not None:
            from_date = datetime.fromisoformat(from_date)
        if to_date is not None:
            to_date = datetime.fromisoformat(to_date)

        response, status = await data_api.get_stats(user_id, other_player_id=against, guild_id=guild,
                                                    channel_id=channel, from_date=from_date, to_date=to_date)
        stat_dict = json.loads(response)

        await ctx.send(stat_dict_to_message(stat_dict, mode=mode))


    token = os.getenv('DISCORD_TOKEN')
    bot.run(token)
