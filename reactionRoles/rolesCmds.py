from discord.errors import HTTPException
from reactionRoles.dbFunctions import addReactionRole, isReactionRole, removeReactionRole
from discord.ext import commands
from discord import Message
from const import TIMEOUT
import asyncio

class CmdsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    #Command to add a reaction role
    @commands.command(aliases=["addreactionrole", "addrole", "addRole","addreaction"])
    @commands.has_permissions(administrator=True)
    async def addReactionRole(self, ctx):
        
        if(not ctx.message.reference):
            await ctx.send("Please reply to the message I should add a role-reaction to!")
            return
        if(len(ctx.message.role_mentions) != 1):
            await ctx.send("Please mention one role!")
            return
        
        #Wait for the user to react to this message
        try:
            reactmsg = await ctx.send("Please react to this message with your desired emoji!")
            
            def reactCheck(reaction, user):
                return user == ctx.author and reaction.message.id == reactmsg.id

            reaction, user = await self.bot.wait_for("reaction_add", timeout=TIMEOUT, check=reactCheck)
            await ctx.send("Noted.")
            addReactionRole(ctx.message.reference.message_id, str(reaction.emoji), ctx.message.role_mentions[0].id)
            await ctx.guild.fetch_emojis()
            try:
                await ctx.message.reference.resolved.add_reaction(reaction.emoji)
            except HTTPException:
                await ctx.send("Sorry, but i cant find that emoji... Possibly it's from another server?")
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you took too long to react! (I waited {} seconds)".format(TIMEOUT))
            return
        return

    #Command to remove a reaction role
    @commands.command(aliases=["removereactionrole", "removerole", "removeRole","removereaction"])
    @commands.has_permissions(administrator=True)
    async def removeReactionRole(self, ctx, arg):
        if(not ctx.message.reference):
            await ctx.send("Please reply to the message with the reaction role you want to delete!")
            return
        if(not isReactionRole(ctx.message.reference.message_id, str(arg))):
            await ctx.send("Sorry, but that does not seem to be a reacton role..")
            return

        removeReactionRole(ctx.message.reference.message_id, str(arg))
        if(type(ctx.message.reference.resolved == Message)):
            await ctx.message.reference.resolved.clear_reaction(str(arg))
        else:
            await ctx.send("I couldn't find the emoji.. Well, whatever :p It either stays there forever or the message does not exist anymore.")
        await ctx.send("I removed the reaction role! (At least out of my brain)")

    @removeReactionRole.error
    async def removeErrorHandler(self,ctx, arg):
        await ctx.send("Please specify the emoji of the reaction role!")