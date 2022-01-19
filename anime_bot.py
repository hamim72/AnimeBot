import os
import time

import discord
from discord import activity
from discord.ext import commands
from dotenv import load_dotenv

import mal
import embed_dict

load_dotenv()
token = os.getenv("DISCORD_TOKEN")
my_guild = os.getenv("DISCORD_GUILD")
PREFIX = '!'

activity = discord.Activity(type=discord.ActivityType.watching, name="One Piece")
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, activity=activity, help_command=None)

bot.search_results = []
bot.search_type = ''

@bot.event
async def on_ready():
    for guild in bot.guilds:
        if guild.name == my_guild:
            break
    print(
        f"{bot.user} is connected"
        )

@bot.command(name='help')
async def help(ctx):
    await ctx.send("""
**Commands**
**!anime [name]** - info of the anime
**!manga [name]** - info of the manga
**!person [name]**  - info of people like *VAs*, directors, animators etc.

**!search anime [name]** - list of anime search results
**!search manga [name]** - list of manga search results
**!get [index]** -  get the anime or manga info based on its index in the list
""")

@bot.command(name='anime')
async def anime(ctx, *, message: str):
    search_type = 'anime'
    results = mal.mal_search(search_type, message)
    first_result_id = results[0][0]
    anime_info = mal.get_info(search_type, first_result_id)
    embed = discord.Embed.from_dict(embed_dict.anime(anime_info))
    await ctx.send(embed=embed)

@bot.command(name='manga')
async def manga(ctx, *, message: str):
    search_type = 'manga'
    results = mal.mal_search(search_type, message)
    first_result_id = results[0][0]
    manga_info = mal.get_info(search_type, first_result_id)
    embed = discord.Embed.from_dict(embed_dict.manga(manga_info))
    await ctx.send(embed=embed)

@bot.command(name='person')
async def person(ctx, *, message: str):
    search_type = 'person'
    results = mal.mal_search(search_type, message)
    first_result_id = results[0][0]
    print(first_result_id)
    person_info = mal.get_info(search_type, first_result_id)
    embed = discord.Embed.from_dict(embed_dict.person(person_info))
    await ctx.send(embed=embed)

@bot.command(name='search')
async def search(ctx, *, message: str):
    search_type, query = message.split(' ',1)
    bot.search_type = search_type
    bot.search_results = mal.mal_search(search_type, query)

    embed = discord.Embed.from_dict(embed_dict.search_results)

    total_results_count = len(bot.search_results)
    results_per_page = 5
    start = 0
    end = results_per_page

    def page_format(results: list, start: int, end: int):
        page_output = ''
        for i in range(len(results[start:end])):
            page_output+=str((start+i+1))+'. '+results[start+i+1][1]+'\n'
        return page_output

    embed.add_field(name=None,value=page_format(bot.search_results, start, end), inline=False)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('◀️')
    await msg.add_reaction('▶️')

    def check(reaction, user):
            return user == ctx.message.author and (str(reaction.emoji) == '▶️' or str(reaction.emoji) == '◀️')
    
    try:
        while end<total_results_count or start>0:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
            if str(reaction.emoji) == '▶️':
                
                start+=results_per_page
                end+=results_per_page
                new_embed = discord.Embed.from_dict(embed_dict.search_results)
                new_embed.add_field(name=None,value=page_format(bot.search_results, start, end), inline=False)
            if str(reaction.emoji) == '◀️':
                start-=results_per_page
                end-=results_per_page
                new_embed = discord.Embed.from_dict(embed_dict.search_results)
                new_embed.add_field(name=None,value=page_format(bot.search_results, start, end), inline=False)
            await msg.edit(embed=new_embed)
    except Exception as e:
        print(e)

@bot.command(name='get')
async def get(ctx, message: str):
    position = int(message)
    mal_id = bot.search_results[position][0]
    info = mal.get_info(bot.search_type, mal_id)
    if bot.search_type=='anime':
        embed = discord.Embed.from_dict(embed_dict.anime(info))
    if bot.search_type=='manga':
        embed = discord.Embed.from_dict(embed_dict.manga(info))
    if bot.search_type=='person':
        embed = discord.Embed.from_dict(embed_dict.manga(info))
    if bot.search_type=='user':
        pass
    await ctx.send(embed=embed) 

bot.run(token)

