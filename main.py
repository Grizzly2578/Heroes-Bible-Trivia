from config import discord, bot

import os
import json

from api import keep_alive



@bot.event
async def on_guild_join(guild): #when the bot joins the guild
    with open('prefixes.json', 'r') as f: #read the prefix.json file
        prefixes = json.load(f) #load the json file

    prefixes[str(guild.id)] = '+'#default prefix

    with open('prefixes.json', 'w') as f: #write in the prefix.json "message.guild.id": "bl!"
        json.dump(prefixes, f, indent=4) #the indent is to make everything look a bit neater

@bot.event
async def on_guild_remove(guild): #when the bot is removed from the guild
    with open('prefixes.json', 'r') as f: #read the file
        prefixes = json.load(f)

    prefixes.pop(str(guild.id)) #find the guild.id that bot was removed from

    with open('prefixes.json', 'w') as f: #deletes the guild.id as well as its prefix
        json.dump(prefixes, f, indent=4)

@bot.event
async def on_ready():
  print("We Have Been Summoned!")
  await bot.change_presence(
    activity=discord.Streaming(
      name="The Great Battle", 
      platform=str, 
      url='https://www.youtube.com/watch?v=zi_vZLjg_3o')
  ) 

initial_extensions = []



for filename in os.listdir('./cogs'):
  if filename.endswith('.py') and not filename.startswith("_"):
    initial_extensions.append("cogs." + filename[:-3])
    bot.load_extension(f"cogs.{filename[:-3]}")


    
token = os.environ['token']
keep_alive()
bot.run(token, reconnect=True)