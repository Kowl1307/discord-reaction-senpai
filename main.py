import discord
from discord.ext import commands
from const import *
from embeds.cmds import CmdsCog
from reactionRoles.listeners import ReactionListenerCog
from reactionRoles.dbFunctions import initDB
from xyz import TOKEN


bot = commands.Bot(command_prefix=CMDPREFIX, description=DESCRIPTION)

initDB()

bot.add_cog(CmdsCog(bot))
bot.add_cog(ReactionListenerCog(bot))

bot.run(TOKEN)