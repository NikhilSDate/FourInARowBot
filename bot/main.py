import json
import re
import os
import random
from datetime import datetime

from discord import Intents
from discord.ext import commands
from discord.ext.commands import Context

from dotenv import load_dotenv
from disc.discord_game_manager import DiscordGameManager
from game.statuses import Status, StatusType
from api_wrapper.data_api import DataAPI
from disc.utils import stat_dict_to_message, parse_colon_arguments, user_id_from_mention, channel_id_from_mention

load_dotenv()

if __name__ == "__main__":

    intents = Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)
    game_manager = DiscordGameManager()
    data_api = DataAPI()

    error_messages = {Status.CHANNEL_BUSY: 'A game is currently in progress in this channel.',
                      Status.NO_ACTIVE_GAME: 'You are not a participant in an active game in this channel.',
                      Status.WRONG_TURN: 'Please wait for the other player to complete his turn.',
                      Status.INVALID_INDEX: 'Please enter a valid column index.',
                      Status.COLUMN_FULL: 'The column you are trying to play your piece in is full.',
                      }


    @bot.command()
    async def newgame(ctx: Context, other_player: str, mode='random', rows: int = 6, columns: int = 7,
                      winning_length: int = 4):
        id_regex = re.compile('^<@(.+)>$')
        author_id = str(ctx.author.id)
        other_player_id = id_regex.match(other_player).group(1)

        if mode == 'first':
            ids = [author_id, other_player_id]
        elif mode == 'second':
            ids = [other_player_id, author_id]
        elif mode == 'random':
            ids = [author_id, other_player_id]
            random.shuffle(ids)
        else:
            await ctx.send('The second argument of newgame must be \'random\', \'first\', or \'second\'')
            return

        status = await game_manager.new_game(channel=ctx.channel, guild=ctx.guild, first_player_id=ids[0],
                                             second_player_id=ids[1], dims=(rows, columns),
                                             winning_length=winning_length)

        if status != Status.OK:
            await ctx.send(error_messages[status])
        else:
            await game_manager.print_board(ctx.channel)


    @bot.command()
    async def move(ctx: Context, one_indexed_column: int):
        zero_indexed_column = one_indexed_column - 1
        status = game_manager.do_move(channel=ctx.channel, player_id=str(ctx.author.id), column=zero_indexed_column)
        if status in StatusType.ERROR:
            await ctx.send(error_messages[status])
        else:
            await game_manager.print_board(channel=ctx.channel)

        if status in StatusType.GAME_OVER:
            await game_manager.handle_game_over(ctx.channel)


    @bot.command()
    async def resign(ctx: Context):
        status = await game_manager.handle_resign(ctx.channel, str(ctx.author.id))
        if status in StatusType.ERROR:
            await ctx.send(error_messages[status])


    @bot.command()
    async def stats(ctx: Context, *, arg=''):
        user_id = str(ctx.author.id)
        filters = parse_colon_arguments(arg, options=['against', 'server', 'from', 'to', 'channel', 'mode'])
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
