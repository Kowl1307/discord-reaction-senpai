import discord
from discord.ext import commands
from const import *
from cmds import CmdsCog


bot = commands.Bot(command_prefix=CMDPREFIX, description=DESCRIPTION)

bot.add_cog(CmdsCog(bot))

bot.run(TOKEN)