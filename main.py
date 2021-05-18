import discord
from discord.ext import commands
from const import *
from embeds.embedCmds import CmdsCog as embedCmds
from reactionRoles.listeners import ReactionListenerCog
from reactionRoles.dbFunctions import initDB
from reactionRoles.rolesCmds import CmdsCog as roleCmds
from xyz import TOKEN

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=CMDPREFIX, description=DESCRIPTION, intents=intents)

initDB()

bot.add_cog(embedCmds(bot))
bot.add_cog(roleCmds(bot))
bot.add_cog(ReactionListenerCog(bot))


bot.run(TOKEN)