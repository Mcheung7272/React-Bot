import os

import discord
from discord import guild
from dotenv import load_dotenv
from discord.ext import commands
from discord import TextChannel
from discord import PartialEmoji
from typing import Union
import random

listOfKekws = []
listOfAnime = []

thisdir = os.getcwd()

for r, d, f in os.walk(thisdir):
    for file in f:
        if "kek" in file:
            listOfKekws.append(file)
        elif "weeb" in file:
            listOfAnime.append(file)


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix = '*')

@bot.command(name='kekw')
@commands.cooldown(1,15,commands.BucketType.channel)
async def getmsg(ctx):
    messages = await ctx.channel.history(limit=10).flatten()
    x = random.sample(listOfKekws,1)
    result = ", ".join(x)
    await ctx.send(file=discord.File(thisdir + "\\kekwFolder\\" + result))
    for word in messages:
        await word.add_reaction(":KEKW:696868795263746089")

@bot.command(name='weeb')
@commands.cooldown(1,15,commands.BucketType.channel)
async def getmsg(ctx):
    messages = await ctx.channel.history(limit=10).flatten()
    guildID = ctx.guild.id
    currentG = bot.get_guild(guildID)
    list = await currentG.fetch_emojis()
    animeList = []
    for a in list:
        if "anime" in a.name:
            animeList.append(a)
    results = random.sample(animeList, 2)
    x = random.sample(listOfAnime,1)
    result = ", ".join(x)
    await ctx.send(file=discord.File(thisdir + "\\animeFolder\\" + result))
    for word in messages:
        for emote in results:
            await word.add_reaction(emote)

@bot.command(name='react')
@commands.cooldown(1,15,commands.BucketType.channel)
async def differentEmotes(ctx, emoji: Union[discord.Emoji, discord.PartialEmoji]):
    messages = await ctx.channel.history(limit=10).flatten()
    await ctx.send(emoji)
    for word in messages:
        await word.add_reaction(emoji)

@bot.command(name="sock")
@commands.cooldown(1,15,commands.BucketType.channel)
async def listAllEmotes(ctx):
    guildID = ctx.guild.id
    currentG = bot.get_guild(guildID)
    list = await currentG.fetch_emojis()
    one = random.choice(list)
    await ctx.send(str(one) + str("\n:dress:") + str("\n<:Socks:755471011469852774>"))

@bot.command(name='helpme')
async def helpMenu(ctx):
    embedVar = discord.Embed(title="Commands:",  color=0x00ff00)
    embedVar.add_field(name="*kekw", value="reacts to past messages and uploads kekw meme", inline=False)
    embedVar.add_field(name="*react/space/<emote>", value="You can have the bot react to past messages with any emote from THIS server", inline=False)
    embedVar.add_field(name="*weeb", value="Weeb meme and reactions", inline=False)
    embedVar.add_field(name="*sock", value="Find out", inline=False)
    await ctx.send(embed=embedVar)
    
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("Command is on cooldown! Try again in " + (str)(round(error.retry_after)) + " seconds")
    
bot.run(TOKEN)
