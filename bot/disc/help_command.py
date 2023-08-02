from typing import Mapping, Optional, List

import discord
from discord import Embed
from discord.ext.commands import MinimalHelpCommand, Cog, Command


class MyHelp(MinimalHelpCommand):

    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = Embed(title='Command help', description=page, color=discord.Color.blurple())
            await destination.send(embed=embed)

    async def send_bot_help(self, mapping: Mapping[Optional[Cog], List[Command]], /) -> None:
        embed = Embed(title='Help', description='', color = discord.Color.blurple())
        for cog, commands in mapping.items():
            names = [self.context.clean_prefix + c.name for c in commands]
            if names:
                embed.add_field(name="All commands", value="\n".join(names), inline=False)
        embed.add_field(name='', value="Use `!help [command]` for more info on a command."
                                       "\n\nIn command help, angle brackets indicate a required parameter. "
                                       "Square brackets indicate an optional parameter. "
                                       "A value for an optional parameter, if given, indicates the default value for that parameter. "
                                       "For example, 'rows=6' means that the default value for the 'rows' parameter is 6. "
                                       "Only the values of parameters should be specified when running commands, not the names. "
                                       "See the example usage for each command for examples of this.")
        await self.get_destination().send(embed=embed)

    # async def send_command_help(self, command: Command[Any, ..., Any], /) -> None:


