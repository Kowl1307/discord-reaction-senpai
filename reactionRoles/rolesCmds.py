from reactionRoles.dbFunctions import addReactionRole
from discord.ext import commands
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
                print(user.name)
                print(reaction.message.id)
                print(reactmsg.id)
                return user == ctx.author and reaction.message.id == reactmsg.id

            reaction, user = await self.bot.wait_for("reaction_add", timeout=TIMEOUT, check=reactCheck)
            await ctx.send("Noted.")
            addReactionRole(ctx.message.reference.message_id, str(reaction.emoji), ctx.message.role_mentions[0].id)
            await ctx.message.reference.resolved.add_reaction(reaction.emoji)
        except asyncio.TimeoutError:
            await ctx.send("Sorry, you took too long to react! (I waited {} seconds)".format(TIMEOUT))
            return
        return

    #Command to remove a reaction role
    @commands.command(aliases=["removereactionrole", "removerole", "removeRole","removereaction"])
    @commands.has_permissions(administrator=True)
    def removeReactionRole(self, ctx):
        return