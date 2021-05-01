import discord
from discord.ext import commands
from const import *
from cmds import CmdsCog
from listeners import ReactionListenerCog
from xyz import TOKEN


bot = commands.Bot(command_prefix=CMDPREFIX, description=DESCRIPTION)

bot.add_cog(CmdsCog(bot))
bot.add_cog(ReactionListenerCog(bot))

bot.run(TOKEN)