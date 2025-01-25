#!/usr/bin/env python3

import nextcord
import random
import json
import os

# from replit import db
from nextcord.ext import commands
from aiohttp import ClientSession

class Bot(commands.Bot):

    def __init__(self, **kwargs):
        super().__init__(
            owner_ids=set([908234266301829132,829619198544183327]),
            command_prefix=self.get_msg_prefix,
            case_insensitive=True,
            help_command=None,
            intents=nextcord.Intents.all(),
            **kwargs
        )
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py') and not filename.startswith("_"):
                try:
                    self.load_extension(f"cogs.{filename[:-3]}")
                except Exception as exc:
                    print(
                        f'Could not load extension {filename[:-3]} due to {exc.__class__.__name__}: {exc}'
                    )

    def get_msg_prefix(self,bot, message):
        try:
            with open('config.json', 'r') as f:
                config = json.load(f)
                return config['prefixes'][str(message.guild.id)]

        except KeyError:  # if the guild's prefix cannot be found in 'prefixes.json'
            with open('config.json', 'r') as k:
                config = json.load(k)
            config['prefixes'][str(
                message.guild.id)] = config['prefixes']['default']

            with open('config.json', 'w') as j:
                json.dump(config, j, indent=4)

            with open('config.json', 'r') as t:
                config = json.load(t)
                return config['prefixes'][str(message.guild.id)]

        except:
            return config['prefixes']['default']



    async def on_ready(self):
        print(f'Logged on as {self.user} (ID: {self.user.id})')
        await bot.change_presence(activity=nextcord.Streaming(
            name="The Great Battle",
            platform=str,
            url='https://www.youtube.com/watch?v=zi_vZLjg_3o'))

    async def on_guild_join(self, guild):
        with open('config.json', 'r') as k:
            config = json.load(k)
        config['prefixes'][str(guild.id)] = config['prefixes']['default']

        with open('config.json', 'w') as j:
            json.dump(config, j, indent=4)

        channel = bot.get_channel(991657740525129768)

        total_text_channels = len(guild.text_channels)
        total_voice_channels = len(guild.voice_channels)

        embed = nextcord.Embed(title="Alert!",
                              description="Another Server Added Me! Wooo!")
        embed.add_field(name="Guild ID:", value=f"{guild.id}")
        embed.add_field(name="Guild Name:", value=f"{guild.name}")
        embed.add_field(name="Description:", value=f"{guild.description}")
        embed.add_field(
            name="Created at:",
            value=f"{guild.created_at.strftime('%A %B %d %Y% %M:%S %p')}")
        embed.add_field(name="Guild Owner:", value=f"{guild.owner}")
        embed.add_field(name="Roles:", value=f"{len(guild.roles)}")
        embed.add_field(name="Emojis:", value=f"{len(guild.emojis)}")
        embed.add_field(name="Member Count:", value=f"{guild.member_count}")
        embed.add_field(name="Text Channels:", value=f"{total_text_channels}")
        embed.add_field(name="Voice Channels:", value=f"{total_voice_channels}")
        embed.set_thumbnail(url=guild.icon.url)
        await channel.send(embed=embed)

    async def on_guild_remove(guild):
        with open('config.json', 'r') as f:  #read the file
            config = json.load(f)

        config['prefixes'].pop(str(guild.id))  #find the guild.id that bot was removed from

        with open('config.json',
                  'w') as f:  #deletes the guild.id as well as its prefix
            json.dump(config, f, indent=4)
        channel = bot.get_channel(991657740525129768)

        total_text_channels = len(guild.text_channels)
        total_voice_channels = len(guild.voice_channels)

        embed = nextcord.Embed(title="Alert!",
                              description="Another Server Kicked Me! Noooo!")
        embed.add_field(name="Guild ID:", value=f"{guild.id}")
        embed.add_field(name="Guild Name:", value=f"{guild.name}")
        embed.add_field(name="Description:", value=f"{guild.description}")
        embed.add_field(
            name="Created at:",
            value=f"{guild.created_at.strftime('%A %B %d %Y% %M:%S %p')}")
        embed.add_field(name="Guild Owner:", value=f"{guild.owner}")
        embed.add_field(name="Roles:", value=f"{len(guild.roles)}")
        embed.add_field(name="Emojis:", value=f"{len(guild.emojis)}")
        embed.add_field(name="Member Count:", value=f"{guild.member_count}")
        embed.add_field(name="Text Channels:", value=f"{total_text_channels}")
        embed.add_field(name="Voice Channels:", value=f"{total_voice_channels}")
        if guild.icon != None:
            embed.set_thumbnail(url=guild.icon.url)
        await channel.send(embed=embed)
        # with open("global_chat.json", "r") as f:
        #     global_chat_data = json.load(f)
        # guild_ids = list(global_chat_data.keys())
        # if str(guild.id) in guild_ids:
        #     async with ClientSession() as session:
        #         hook = nextcord.Webhook.from_url(db['webhooks'][str(
        #             guild.id)]['webhook']['url'],
        #                                         session=session,
        #                                         bot_token=os.environ['token'])
        #         del db['webhooks'][str(guild.id)]
        #         guild_id = str(guild.id)
        #         with open("global_chat.json", "r") as f:
        #             global_chat = json.load(f)

        #         global_chat.pop(guild_id)

        #         with open("global_chat.json", "w") as f:
        #             json.dump(global_chat, f, indent=4)
        #         await hook.delete()

    async def new_user(self, user):
        with open("save.json", "r") as f:
            users = json.load(f)
            users[str(user.id)] = {}
            users[str(user.id)]['name'] = str(user)
            users[str(user.id)]['points'] = 0
            users[str(user.id)]['level'] = 0
            users[str(user.id)]['manna'] = 0
            users[str(user.id)]['streak'] = 0
            users[str(user.id)]['cmds_ran'] = 1
            users[str(user.id)]['correct_answers'] = 0
            users[str(user.id)]['bag'] = {}
            users[str(user.id)]['effects'] = {}
            with open("save.json", "w") as f:
                users = json.dump(users, f, indent=4, sort_keys=True)

    async def zero_item_fix(self):
        with open("save.json", "r") as f:
            users = json.load(f)
        with open("shop.json", "r") as f1:
            shop = json.load(f1)
            for user in list(users.keys()):
                for item in list(shop.keys()):
                    if item in users[user]['bag']:
                        if users[user]['bag'][item]['count'] == 0:
                            users[user]['bag'].pop(item)
            with open("save.json", "w") as f:
                users = json.dump(users, f, indent=4, sort_keys=True)

    async def update_user_manna(self, user, mode, value):
        with open("save.json", "r") as f: users = json.load(f)
        if mode.lower() == 'add':
            users[str(user.id)]['manna'] += value
        elif mode.lower() == 'subtract':
            users[str(user.id)]['manna'] -= value
        with open("save.json", "w") as f:
            users = json.dump(users, f, indent=4, sort_keys=True)
        return mode, value

    async def update_user_item(self, user, mode, item, value):
        with open("save.json", "r") as f: users = json.load(f)
        user_bag = users[str(user.id)]['bag']
        if mode == 'add':
            user_bag[item]['count'] += value
        elif mode == 'subtract':
            user_bag[item]['count'] -= value
        with open("save.json", "w") as f:
            users = json.dump(users, f, indent=4, sort_keys=True)
        await self.zero_item_fix()
        return mode, item, value

    async def add_command_count(self, user):
        with open("save.json", "r") as f:
            users = json.load(f)
        if str(user.id) not in users:
            await self.new_user(user)
        else:
            with open("save.json", "r") as f:
                users = json.load(f)
                users[str(user.id)]['name'] = str(user)
                users[str(user.id)]['cmds_ran'] += 1
            with open("save.json", "w") as f:
                users = json.dump(users, f, indent=4, sort_keys=True)

    async def zero_fix(self):
        with open("save.json", "r") as f:
            users = json.load(f)
            for user in list(users):
                #Level 1
                if users[str(user)]['manna'] < 0:
                    users[str(user)]['manna'] = 0
            with open("save.json", "w") as f:
                users = json.dump(users, f, indent=4, sort_keys=True)

    async def update_name(self, user):
        try:
            with open("save.json", "r") as f:
                users = json.load(f)
                users[str(user.id)]['name'] = str(user)
                with open("save.json", "w") as f:
                    json.dump(users, f, indent=4, sort_keys=True)
        except KeyError:
            return

    async def on_cooldown(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            cooldown_embed = nextcord.Embed(
                title="PEACE BE STILL, BRO...",
                description=
                f"Jesus Slept In The Boat, Why Not Allow Me In My Own Bed? \nWait For `{error.retry_after:.2f}` Seconds.",
                color=0xF70036)
            await ctx.reply(embed=cooldown_embed)

    async def get_commands_ran(self, user):
        with open("save.json", "r") as f:
            users = json.load(f)
            if str(user.id) not in users:
                return 'None'
            else:
                with open("save.json", "r") as f:
                    users = json.load(f)
                return users[str(user.id)]['cmds_ran']

    async def level_fix(self):
        with open("save.json", "r") as f:
            users = json.load(f)
        for user in users.keys():
            result = users[user]['points'] / 250
            if result < 1:
                result = 0
            result = int(f"{result:.0f}")
            users[user]['level'] = result
        with open("save.json", "w") as f:
            users = json.dump(users, f, indent=4, sort_keys=True)

    async def random_fact(self, ctx):
        with open("facts.json", "r") as f:
            fax = json.load(f)
        randomnum = random.randint(1, len(fax))

        fact = fax[randomnum - 1]

        embed = nextcord.Embed(title="Fact!", description=f"{fact}")

        if (random.randint(0, 500) == 42) and (ctx.author != bot.user):
            await ctx.reply(embed=embed)

        elif (random.randint(0, 500) == 69) and (ctx.author != bot.user):
            await ctx.reply(embed=embed)

        elif (random.randint(0, 500) == 99) and (ctx.author != bot.user):
            await ctx.reply(embed=embed)

        elif (random.randint(0, 500) == 76) and (ctx.author != bot.user):
            await ctx.reply(embed=embed)

        elif (random.randint(0, 500) == 25) and (ctx.author != bot.user):
            await ctx.reply(embed=embed)

        elif (random.randint(0, 500) == 56) and (ctx.author != bot.user):
            await ctx.reply(embed=embed)

        elif (random.randint(0, 500) == 420) and (ctx.author != bot.user):
            await ctx.reply(embed=embed)

        elif (random.randint(0, 500) == 70) and (ctx.author != bot.user):
            await ctx.reply(embed=embed)

        elif (random.randint(0, 500) == 71) and (ctx.author != bot.user):
            await ctx.reply(embed=embed)

        elif (random.randint(0, 500) == 72) and (ctx.author != bot.user):
            await ctx.reply(embed=embed)

        elif (random.randint(0, 500) == 73) and (ctx.author != bot.user):
            await ctx.reply(embed=embed)

        elif (random.randint(0, 500) == 74) and (ctx.author != bot.user):
            await ctx.reply(embed=embed)

        elif (random.randint(0, 500) == 7) and (ctx.author != bot.user):
            await ctx.reply(embed=embed)

        elif (random.randint(0, 500) == 6) and (ctx.author != bot.user):
            await ctx.reply(embed=embed)

        else:
            return

    def create_embed(self, bot, ctx, page=0, inline=False):
        help_commands = json.load(open("commands.json"))
        page = page % len(list(help_commands['default']))
        pageNum = list(help_commands['default'])[page]
        embed = nextcord.Embed(
            title=f"THE COMMANDS",
            description=
            "These are the commands you can use to \nactivate the features of this discord bot.",
            color=0xFFD500)
        embed.set_thumbnail(url=f"https://i.imgur.com/n2Fba9e.png")
        embed.set_footer(text="PHILIPPIANS 4:13")
        for key, val in help_commands['default'][pageNum].items():
            embed.add_field(name=f"`{self.get_msg_prefix(bot, ctx)}`{key}",
                            value=val,
                            inline=inline)
        return embed



bot = Bot()

from flask import Flask, render_template
from threading import Thread

with open("save.json", "r") as f:
  users = json.load(f)



app = Flask('')



@app.route('/', methods=['GET'])
def home():
  return "Rise You Monstrosity!!"

# @app.route("/interactions")
# @app.route("/interactions/")
# def interactions_():
#   data = request.form.get()
#   print(data)
#   return data

# Website Endpoints

@app.route('/shop')
@app.route('/shop/')
def shop():
  return "Hello This website is still work in progress"

# API Endpoints
@app.route('/api/')
@app.route('/api')
def api():
  return render_template("index.html")

# @app.route('/api/interactions')
# def interactions():
#     print(flask.request.data)
#     return ""

@app.route('/api/test')
def test():
  return render_template("_index.html")

@app.route('/api/user/', methods=['GET'])
@app.route('/api/user', methods=['GET'])
def api_users():
  with open("save.json", "r") as f:
    users = json.load(f)
  return users

@app.route('/api/user/<user>/', methods=['GET'])
@app.route('/api/user/<user>', methods=['GET'])
def api_user(user):
  with open("save.json", "r") as f:
    users = json.load(f)
  if user not in users:
    return "Unkown User"
  else:
    return {user:users[user]}

@app.route('/api/shop/', methods=['GET'])
@app.route('/api/shop', methods=['GET'])
def api_shop():
  with open("shop.json", "r") as f:
    shop = json.load(f)
  return shop

@app.route('/api/shop/<item>/', methods=['GET'])
@app.route('/api/shop/<item>', methods=['GET'])
def api_shop2(item):
  with open("shop.json", "r") as f:
    shop = json.load(f)
  if item.upper() not in shop:
    return shop
  else:
    return {item.upper():shop[item.upper()]}

def run():
  app.run(host='0.0.0.0',port=8082)



def keep_alive():
    t = Thread(target=run)
    t.start()

# keep_alive()
bot.run("OTgzOTE2MDQxMzg0MTEyMTY4.GN5ZrW.4NxQqDMfGcBAbDRk0dOtoi3xLWGdqctXj6haHU")
