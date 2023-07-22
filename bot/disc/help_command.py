from typing import Mapping, Optional, List, Any

import discord
from discord import Embed
from discord.ext.commands import HelpCommand, MinimalHelpCommand, Cog, Command, DefaultHelpCommand


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
        embed.add_field(name='', value='Use `!help [command]` for more info on a command.')
        await self.get_destination().send(embed=embed)

    # async def send_command_help(self, command: Command[Any, ..., Any], /) -> None:


