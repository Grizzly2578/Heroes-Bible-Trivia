import os
import traceback
import asyncio
import requests
import json
import nextcord

from nextcord import Interaction
from nextcord.ext import commands
from nextcord.ui import button, View
from config import discord, add_command_count, on_cooldown, zero_fix, owners


class prefix_modal(nextcord.ui.Modal):
    def __init__(self, bot):
        self.bot = bot
        super().__init__("Change Prefix")
        self.prefix = nextcord.ui.TextInput(label="New Prefix",
                                            min_length=1,
                                            max_length=10,
                                            required=True)
        self.add_item(self.prefix)

    async def callback(self, interaction: Interaction) -> None:
        with open("config.json", "r") as f:
            config = json.load(f)

        if self.bot.get_msg_prefix(self.bot,
                      interaction) in interaction.guild.me.display_name:
            await interaction.guild.me.edit(
                nick=interaction.guild.me.display_name.replace(
                    self.bot.get_msg_prefix(self.bot, interaction), self.prefix.value))

        config['prefixes'][str(interaction.guild.id)] = self.prefix.value

        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)
        embed = discord.Embed(
            title="Prefix",
            description=f"The prefix has been changed to `{self.prefix.value}`",
            color=0xDA37A1)
        embed.set_footer(text=interaction.user.name)
        view = prefix_button(self.bot)
        view.change_button.disabled = True
        view.message = await interaction.response.edit_message(embed=embed,
                                                               view=view)


class prefix_button(View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=600)

    async def on_timeout(self):
        self.change_button.disabled = True
        await self.message.edit(view=self)

    @button(label="Change Prefix", style=nextcord.ButtonStyle.green)
    async def change_button(self, button: nextcord.ui.Button,
                            interaction: Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                content="This button is not for you.", ephemeral=True)
        else:
            if not interaction.user.guild_permissions.manage_messages:
                await interaction.response.send_message(
                    content="You do not have permissions to do this!",
                    ephemeral=True)
            else:
                await interaction.response.send_modal(
                    prefix_modal(bot=self.bot))


class ping_view(View):
    def __init__(self):
        super().__init__()

    @button(label="Sheesh")
    async def sheesh_button(self, button: button, interaction: Interaction):
        button.disabled = True
        sembed = discord.Embed(
            title="SHEESH",
            description=f"Sheesh \n**{round(self.bot.latency * 1000)}ms**",
            color=0xDA37A1)
        await interaction.response.edit_message(embed=sembed, view=self)


class comds(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='reload',
                      description="Reload all/one of the bots cogs!",
                      aliases=["r"])
    @commands.is_owner()
    async def reload(self, ctx, cog=None):
        if not cog:
            # No cog, means we reload all cogs
            async with ctx.typing():
                embed = discord.Embed(title="Reloading all cogs!",
                                      color=0x808080,
                                      timestamp=ctx.message.created_at)
                for ext in os.listdir("./cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.bot.unload_extension(f"cogs.{ext[:-3]}")
                            self.bot.load_extension(f"cogs.{ext[:-3]}")
                            embed.add_field(name=f"Reloaded: `{ext}`",
                                            value='\uFEFF',
                                            inline=False)
                        except Exception as e:
                            embed.add_field(name=f"Failed to reload: `{ext}`",
                                            value=e,
                                            inline=False)
                        await asyncio.sleep(0.5)
                await ctx.send(embed=embed)
        else:
            # reload the specific cog
            async with ctx.typing():
                embed = discord.Embed(title="Reloading all cogs!",
                                      color=0x808080,
                                      timestamp=ctx.message.created_at)
                ext = f"{cog.lower()}.py"
                if not os.path.exists(f"./cogs/{ext}"):
                    # if the file does not exist
                    embed.add_field(name=f"Failed to reload: `{ext}`",
                                    value="This cog does not exist.",
                                    inline=False)

                elif ext.endswith(".py") and not ext.startswith("_"):
                    try:
                        self.bot.unload_extension(f"cogs.{ext[:-3]}")
                        self.bot.load_extension(f"cogs.{ext[:-3]}")
                        embed.add_field(name=f"Reloaded: `{ext}`",
                                        value='\uFEFF',
                                        inline=False)
                    except Exception:
                        desired_trace = traceback.format_exc()
                        embed.add_field(name=f"Failed to reload: `{ext}`",
                                        value=desired_trace,
                                        inline=False)
                await ctx.send(embed=embed)

    @commands.command(name='load')
    @commands.is_owner()
    async def load(self, ctx: commands.context, cog=None):
        async with ctx.typing():
            embed = discord.Embed(title="Reloading all cogs!",
                                  color=0x808080,
                                  timestamp=ctx.message.created_at)
            ext = f"{cog.lower()}.py"
            if not os.path.exists(f"./cogs/{ext}"):
                # if the file does not exist
                embed.add_field(name=f"Failed to reload: `{ext}`",
                                value="This cog does not exist.",
                                inline=False)

            elif ext.endswith(".py") and not ext.startswith("_"):
                try:
                    self.bot.load_extension(f"cogs.{ext[:-3]}")
                    embed.add_field(name=f"Loaded: `{ext}`",
                                    value='\uFEFF',
                                    inline=False)
                except Exception:
                    desired_trace = traceback.format_exc()
                    embed.add_field(name=f"Failed to Load: `{ext}`",
                                    value=desired_trace,
                                    inline=False)
            await ctx.send(embed=embed)

    @commands.command(name='unload')
    @commands.is_owner()
    async def unload(self, ctx: commands.context, cog=None):
        async with ctx.typing():
            embed = discord.Embed(title="Reloading all cogs!",
                                  color=0x808080,
                                  timestamp=ctx.message.created_at)
            ext = f"{cog.lower()}.py"
            if not os.path.exists(f"./cogs/{ext}"):
                # if the file does not exist
                embed.add_field(name=f"Failed to reload: `{ext}`",
                                value="This cog does not exist.",
                                inline=False)

            elif ext.endswith(".py") and not ext.startswith("_"):
                try:
                    self.bot.unload_extension(f"cogs.{ext[:-3]}")
                    embed.add_field(name=f"Unloaded: `{ext}`",
                                    value='\uFEFF',
                                    inline=False)
                except Exception:
                    desired_trace = traceback.format_exc()
                    embed.add_field(name=f"Failed to Unload: `{ext}`",
                                    value=desired_trace,
                                    inline=False)
            await ctx.send(embed=embed)

    @commands.command(name="invite_ian")
    @commands.is_owner()
    async def invite_ian(self, ctx: commands.context):
        guild = self.bot.get_channel(988991633720746054)
        invite = await guild.create_invite()
        await ctx.reply(f"{invite}")

    @commands.command(name="reply", aliases=['send'])
    @commands.is_owner()
    async def reply(self, ctx: commands.context, channel, *, content):
        channel = self.bot.get_channel(int(channel))
        await channel.send(content)

    #Prefix Info
    @commands.group(name="prefix",
                    description="Shows You The Bot's Prefix",
                    invoke_without_command=True)
    @commands.guild_only()
    async def prefix(self, ctx: commands.Context):
        embed = discord.Embed(
            title="Prefix!",
            description=f"The Prefix Here Is: `{self.bot.get_msg_prefix(self.bot, ctx)}`",
            color=0xDA37A1)
        if ctx.author.guild_permissions.manage_messages:
            view = prefix_button(bot=self.bot)
            view.ctx = ctx
            view.message = await ctx.reply(embed=embed,
                                           mention_author=False,
                                           view=view)
        else:
            await ctx.reply(embed=embed, mention_author=False)

    #Ping Command
    @commands.command(name="ping", description=f"Show's the bot's latency.")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ping(self, ctx: commands.Context):
        embed = discord.Embed(
            title="PONG!",
            description=
            f" The Ping is:\n**{round(self.bot.latency * 1000)}ms**",
            color=0xDA37A1)
        view = ping_view()
        view.bot = self.bot
        await zero_fix()
        view.message = await ctx.reply(embed=embed,
                                       mention_author=True,
                                       view=view)

    @ping.after_invoke
    async def ping_cooldown(self, ctx):
        await add_command_count(ctx.author)
        for id in owners:
            if id == ctx.author.id:
                ctx.command.reset_cooldown(ctx)

    @ping.error
    async def ping_error(self, ctx: commands.context, error):
        await on_cooldown(ctx, error)

    @commands.command(name="game", aliases=["info"])
    async def game(self, ctx):
        heroes = discord.Embed(
            title="WELCOME TO THE GAME!",
            description=
            "Hi There! This is a Discord Bot created so that you could play and learn using\nHeroes 2 even in the comfort of your own groupchat.\n\nJust like the game, you can answer questions, use effects, earn manna, experience, and more.\n\nDownload The Original App Here!",
            color=0xF70094)
        heroes.add_field(
            name="IOS Download Link",
            value=
            "[IOS](https://apps.apple.com/us/app/heroes-2-the-bible-trivia-game/id1529609634)"
        )
        heroes.add_field(
            name="Android Download Link",
            value=
            "[Android](https://play.google.com/store/apps/details?id=org.adventist.heroes.ii)"
        )
        await zero_fix()
        await ctx.reply(embed=heroes)

    @commands.command(name="emojiinfo", aliases=["ei"])
    async def emoji_info(self, ctx, emoji: discord.Emoji = None):
        if not emoji:
            return await ctx.invoke(self.bot.get_command("help"),
                                    entity="emojiinfo")

        try:
            emoji = await emoji.guild.fetch_emoji(emoji.id)
        except discord.ext.commands.errors.EmojiNotFound:
            return await ctx.send(
                "I could not find this emoji in the given guild.")

        is_managed = "Yes" if emoji.managed else "No"
        is_animated = "Yes" if emoji.animated else "No"
        requires_colons = "Yes" if emoji.require_colons else "No"
        creation_time = emoji.created_at.strftime("%I:%M %p %B %d, %Y")
        can_use_emoji = ("Everyone" if not emoji.roles else " ".join(
            role.name for role in emoji.roles))

        description = f"""
      **General:**
      **- Name:** {emoji.name}
      **- Id:** {emoji.id}
      **- URL:** [Link To Emoji]({emoji.url})
      **- Author:** {emoji.user.mention}
      **- Time Created:** {creation_time}
      **- Usable by:** {can_use_emoji}
      
      **Other:**
      **- Animated:** {is_animated}
      **- Managed:** {is_managed}
      **- Requires Colons:** {requires_colons}
      **- Guild Name:** {emoji.guild.name}
      **- Guild Id:** {emoji.guild.id}
      """

        embed = discord.Embed(
            title=f"**Emoji Information for:** `{emoji.name}`",
            description=description,
            colour=0xADD8E6,
        )
        embed.set_thumbnail(url=emoji.url)
        await ctx.send(embed=embed)

    @commands.command(name="notif",
                      aliases=['notification', 'notifications', 'notifs'])
    async def notif(self, ctx: commands.command):
        embed = discord.Embed(title="Stuff from the devs")
        embed.add_field(
            name="Endpoints:",
            value=
            "Requesting a user:\nhttps://nextcord-heroes.norberto-noahno.repl.co/api/user/ discord user id\
    Requesting an item from the shop:\nhttps://nextcord-heroes.norberto-noahno.repl.co/api/shop/ item"
        )
        await ctx.reply(embed=embed, mention_author=False)

    @commands.command(name="global_chat", aliases=[
        'gchat',
    ])
    async def global_chat(self, ctx: commands.Context):
        embed = discord.Embed(title="Is tHiS aN EmBEd¿")
        await ctx.reply(embed=embed)

    @commands.command(name="stats")
    @commands.is_owner()
    async def stats(self, ctx: commands.context):
        with open("save.json", "r") as f:
            users = json.load(f)

        total_amt = []

        for user in users:

            amt = users[user]['manna']
            total_amt.append(amt)

        await ctx.reply(
            f"The Users have accumulated a total of **{(sum(total_amt))}**🌾")

    @commands.command(name="servers")
    async def _servers(self, ctx: commands.Context):
        embed = nextcord.Embed(
            title="Servers!",
            description="These are the servers that were generous enough to offer me refuge.",
            color=0x2b2d31
        )
        embed.add_field(
            name=self.bot.get_guild(470009654404055042).name,
            value=f"[Join](https://discord.com/invite/pdDzZRZb5r) | with {self.bot.get_guild(470009654404055042).member_count} members",
            inline=False
        )
        embed.add_field(
            name=self.bot.get_guild(817164113650253864).name,
            value=f"[Join](https://discord.com/invite/ZAbGrjv3AC) | with {self.bot.get_guild(817164113650253864).member_count} members",
            inline=False
        )
        embed.add_field(
            name=self.bot.get_guild(985298076669444157).name,
            value=f"[Join](https://discord.com/invite/BdWeHpZMrw) | with {self.bot.get_guild(985298076669444157).member_count} members",
            inline=False
        )
        await ctx.reply(embed=embed)
    
    @commands.command(name="cls")
    @commands.is_owner()
    async def clear_console(self, ctx:commands.Context):
        os.system("clear")
        await ctx.reply("Console cleared!")

def setup(bot):
    bot.add_cog(comds(bot))
