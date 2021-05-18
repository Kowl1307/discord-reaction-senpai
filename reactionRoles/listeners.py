import discord
from discord.ext import commands

class ReactionListenerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener(name="on_ready")
    async def on_ready(self):
        print("Im ready!")

    @commands.Cog.listener(name="on_reaction_add")
    async def on_reaction_add(reaction, user):
        message = reaction.message
    
    @commands.Cog.listener(name="on_reaction_remove")
    async def on_reaction_add(reaction, user):
        message = reaction.message