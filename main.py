from bot import discord, bot

import os
import json

from api import keep_alive

from aiohttp import ClientSession


@bot.event
async def on_guild_join(guild):  #when the bot joins the guild
    with open('prefixes.json', 'r') as f:  #read the prefix.json file
        prefixes = json.load(f)  #load the json file

    prefixes['prefixes'][str(guild.id)] = '+'  #default prefix

    with open('prefixes.json',
              'w') as f:  #write in the prefix.json "message.guild.id": "bl!"
        json.dump(
            prefixes, f,
            indent=4)  #the indent is to make everything look a bit neater

    channel = bot.get_channel(991657740525129768)

    total_text_channels = len(guild.text_channels)
    total_voice_channels = len(guild.voice_channels)

    embed = discord.Embed(title="Alert!",
                          description="Another Server Added Me! Wooo!")
    embed.add_field(name=f"Guild ID:", value=f"{guild.id}")
    embed.add_field(name=f"Guild Name:", value=f"{guild.name}")
    embed.add_field(name="Description:", value=f"{guild.description}")
    embed.add_field(
        name="Created at:",
        value=f"{guild.created_at.strftime('%A %B %d %Y% %M:%S %p')}")
    embed.add_field(name=f"Guild Owner:", value=f"{guild.owner}")
    embed.add_field(name="Roles:", value=f"{len(guild.roles)}")
    embed.add_field(name="Emojis:", value=f"{len(guild.emojis)}")
    embed.add_field(name="Member Count:", value=f"{guild.member_count}")
    embed.add_field(name="Text Channels:", value=f"{total_text_channels}")
    embed.add_field(name="Voice Channels:", value=f"{total_voice_channels}")
    embed.set_thumbnail(url=guild.icon.url)
    await channel.send(embed=embed)


@bot.event
async def on_guild_remove(guild):  #when the bot is removed from the guild
    with open('prefixes.json', 'r') as f:  #read the file
        prefixes = json.load(f)

    prefixes['prefixes'].pop(str(guild.id))  #find the guild.id that bot was removed from

    with open('prefixes.json',
              'w') as f:  #deletes the guild.id as well as its prefix
        json.dump(prefixes, f, indent=4)
    channel = bot.get_channel(991657740525129768)

    total_text_channels = len(guild.text_channels)
    total_voice_channels = len(guild.voice_channels)

    embed = discord.Embed(title="Alert!",
                          description="Another Server Kicked Me! Noooo!")
    embed.add_field(name=f"Guild ID:", value=f"{guild.id}")
    embed.add_field(name=f"Guild Name:", value=f"{guild.name}")
    embed.add_field(name="Description:", value=f"{guild.description}")
    embed.add_field(
        name="Created at:",
        value=f"{guild.created_at.strftime('%A %B %d %Y% %M:%S %p')}")
    embed.add_field(name=f"Guild Owner:", value=f"{guild.owner}")
    embed.add_field(name="Roles:", value=f"{len(guild.roles)}")
    embed.add_field(name="Emojis:", value=f"{len(guild.emojis)}")
    embed.add_field(name="Member Count:", value=f"{guild.member_count}")
    embed.add_field(name="Text Channels:", value=f"{total_text_channels}")
    embed.add_field(name="Voice Channels:", value=f"{total_voice_channels}")
    if guild.icon != None:
        embed.set_thumbnail(url=guild.icon.url)
    await channel.send(embed=embed)
    with open("global_chat.json", "r") as f:
        global_chat_data = json.load(f)
    guild_ids = list(global_chat_data.keys())
    # if str(guild.id) in guild_ids:
    #     async with ClientSession() as session:
    #         hook = discord.Webhook.from_url(db['webhooks'][str(
    #             guild.id)]['webhook']['url'],
    #                                         session=session,
    #                                         bot_token=token)
    #         del db['webhooks'][str(guild.id)]
    #         guild_id = str(guild.id)
    #         with open("global_chat.json", "r") as f:
    #             global_chat = json.load(f)

    #         global_chat.pop(guild_id)

    #         with open("global_chat.json", "w") as f:
    #             json.dump(global_chat, f, indent=4)
    #         await hook.delete()


@bot.event
async def on_ready():
    print("We Have Been Summoned!")
    await bot.change_presence(activity=discord.Streaming(
        name="The Great Battle",
        platform=str,
        url='https://www.youtube.com/watch?v=zi_vZLjg_3o'))


initial_extensions = []

for filename in os.listdir('./cogs'):
    if filename.endswith('.py') and not filename.startswith("_"):
        initial_extensions.append("cogs." + filename[:-3])
        bot.load_extension(f"cogs.{filename[:-3]}")

token = "OTgzOTE2MDQxMzg0MTEyMTY4.GN5ZrW.4NxQqDMfGcBAbDRk0dOtoi3xLWGdqctXj6haHU"
keep_alive()
bot.run(token, reconnect=True)
