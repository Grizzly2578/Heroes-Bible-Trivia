import json
import os
import random
import nextcord

from aiohttp import ClientSession

from nextcord.ext import commands

token = os.environ['token']

filt = ["@everyone", "@here"]


class global_chat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            if msg.author.id == self.bot.user.id:
                return
            else:
                return

        if isinstance(msg.channel, nextcord.channel.DMChannel): return
        for i in filt:
            if i in msg.content.lower():
                await msg.reply("Message was not sent!", delete_after=7)
                return
        if not msg.content.startswith(self.bot.get_msg_prefix(self.bot, msg)):
            if str(msg.guild.id) in list(db['webhooks']):
                with open("global_chat.json", "r") as f:
                    global_chat_data = json.load(f)
                channel_id = list(global_chat_data.values())

                # message sender
                if msg.channel.id in channel_id:
                    # Unsuported message content
                    if not msg.content: print("not content")
                    # message reveiver
                    for ids in channel_id:
                        if msg.channel.id == ids:
                            for guild_ids in list(db['webhooks']):
                                if str(msg.guild.id) != guild_ids:
                                    if msg.author.avatar == None:
                                        avatar_url = "https://i.imgur.com/xaMxJFw.jpg"
                                    else:
                                        avatar_url = msg.author.avatar.url
                                    with open("assets/profiles.heroes",
                                              "r") as f:
                                        profiles = json.load(f)
                                    if str(msg.author.id) in profiles:
                                        if profiles[str(msg.author.id
                                                        )]['selected'] == None:
                                            avatar_url = random.choice(
                                                profiles[str(msg.author.id)]
                                                ["avatar_url"])
                                        else:
                                            selected = profiles[str(
                                                msg.author.id)]['selected']
                                            avatar_url = profiles[str(
                                                msg.author.id
                                            )]['avatar_url'][selected]
                                    async with ClientSession() as session:
                                        webhook = nextcord.Webhook.from_url(
                                            db['webhooks'][guild_ids]
                                            ['webhook']['url'],
                                            session=session,
                                            bot_token=token)
                                        await webhook.send(
                                            content=msg.content,
                                            username=f"{msg.author}",
                                            avatar_url=avatar_url)


def setup(bot):
    bot.add_cog(global_chat(bot))
