import discord
from discord import guild
from discord.errors import Forbidden, HTTPException
from discord.ext import commands
from reactionRoles.dbFunctions import addReactionRole, getRoleOfReaction, removeReactionRole, isReactionRole

class ReactionListenerCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener(name="on_ready")
    async def on_ready(self):
        print("Im ready!")

    @commands.Cog.listener(name="on_raw_reaction_add")
    async def on_raw_reaction_add(self, payload):
        emoji = payload.emoji
        user = payload.member

        if(not isReactionRole(payload.message_id, str(emoji))):
            return
        role = self.bot.get_guild(payload.guild_id).get_role(getRoleOfReaction(payload.message_id, str(emoji)))
        try:
            await user.add_roles(role)
        except Forbidden:
            print("I do not have permission to add roles! {}".format(user.guild.name))
            await user.guild.owner.send("I do not have the permission to give the {} role on {}!".format(role.name, user.guild.name))

    
    @commands.Cog.listener(name="on_raw_reaction_remove")
    async def on_raw_reaction_remove(self, payload):
        emoji = payload.emoji
        self.bot.get_guild(payload.guild_id).fetch_members()
        user = self.bot.get_guild(payload.guild_id).get_member(payload.user_id)
        print(user)
        print(self.bot.get_guild(payload.guild_id))
        if(not isReactionRole(payload.message_id, str(emoji))):
            return

        role = self.bot.get_guild(payload.guild_id).get_role(getRoleOfReaction(payload.message_id, str(emoji)))
        try:
            await user.remove_roles(role)
        except Forbidden:
            print("I do not have permission to remove roles! {}".format(user.guild.name))
            await user.guild.owner.send("I do not have the permission to remove the {} role on {}!".format(role.name, user.guild.name))

    #TBD: Remove all reactionroles to a message on delete