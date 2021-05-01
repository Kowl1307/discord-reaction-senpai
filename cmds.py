from discord import Embed, TextChannel, Colour
from discord.ext import commands
from const import TIMEOUT
import asyncio


currentPartners = set()
class CmdsCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    '''
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def testEmbed(self, ctx):
        embed = Embed(title="Test Embed", description="This is an embed! It looks nicer than regular text.")
        await ctx.send(embed=embed)
    '''
    
    @commands.command()
    @commands.has_permissions(administrator=True)
    async def createEmbed(self, ctx):
        partner = ctx.author

        if(partner in currentPartners):
            await ctx.send("Nice try, but no.")
            return

        currentPartners.add(partner)

        async def abortDialogue(abortMsg):
            await ctx.send(abortMsg)
            currentPartners.remove(partner)
        
        #Local functions needed for easier creation of the embed
        def partnerCheck(answer):
            return answer.author == partner and answer.channel == ctx.channel


        async def askPartner(question):
            await ctx.send(question)
            try:
                answer = await self.bot.wait_for("message", timeout=TIMEOUT, check=partnerCheck)
                return answer
            except asyncio.TimeoutError:
                await abortDialogue("You took too long, so I cancelled the creation. You took more than {0} seconds".format(TIMEOUT))
                

        async def askPartnerForText(question):
            answer = await askPartner(question)
            return answer.content
        
        async def askPartnerYesNo(question):
            answer = await askPartnerForText(question)
            if(answer.lower() == "yes" or answer.lower == "y"): 
                return True
            else:
                return False
        
        #Ask the partner for info about the embed
        title = await askPartnerForText("Give me a title!")
        if(len(title) >= 256):
            await abortDialogue("Sorry mate, that's too long! Maximum length of the title is 256 characters!")
            return

        #Description
        description = await askPartnerForText("Give me a small text!")
        thumbnail = Embed.Empty
        if(await askPartnerYesNo("Do you want to add a thumbnail? (Answer with Yes/No)")):
            thumbnail = await askPartnerForText("Send me the URL!")
        
        #Color
        desColor = await askPartnerForText("Which color should the embed have (Left side)? Send me the hex-code of the color! I.e. e91e63")
        color = Colour(int(desColor,16))

        

        #Ask in which channel the embed should go
        answer = await askPartner("Where should I send the embed to? Send the channel via #Channel!")
        channel = answer.channel_mentions[0] if answer.channel_mentions else ctx.channel
        if not(type(channel) is TextChannel):
            await ctx.send("Sorry, that is not a text channel? Im just going to pretend you didnt mean another channel")
            channel = ctx.channel

        #Actually create the embed
        embed = Embed(title=title, description=description, colour=color)
        embed.set_thumbnail(url=thumbnail)
        #Send the embed into the desired channel
        await channel.send(embed=embed)
        currentPartners.remove(partner)