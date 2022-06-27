import os
import traceback
import asyncio
import requests
import json

from nextcord.ext import commands
from nextcord.ui import Button, View
from config import discord, get_prefix, add_command_count, on_cooldown, zero_fix, owners


class comds(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(
      name='reload', description="Reload all/one of the bots cogs!"
  )
  @commands.is_owner()
  async def reload(self, ctx, cog=None):
      if not cog:
          # No cog, means we reload all cogs
          async with ctx.typing():
              embed = discord.Embed(
                  title="Reloading all cogs!",
                  color=0x808080,
                  timestamp=ctx.message.created_at
              )
              for ext in os.listdir("./cogs/"):
                  if ext.endswith(".py") and not ext.startswith("_"):
                      try:
                          self.bot.unload_extension(f"cogs.{ext[:-3]}")
                          self.bot.load_extension(f"cogs.{ext[:-3]}")
                          embed.add_field(
                              name=f"Reloaded: `{ext}`",
                              value='\uFEFF',
                              inline=False
                          )
                      except Exception as e:
                          embed.add_field(
                              name=f"Failed to reload: `{ext}`",
                              value=e,
                              inline=False
                          )
                      await asyncio.sleep(0.5)
              await ctx.send(embed=embed)
      else:
          # reload the specific cog
          async with ctx.typing():
              embed = discord.Embed(
                  title="Reloading all cogs!",
                  color=0x808080,
                  timestamp=ctx.message.created_at
              )
              ext = f"{cog.lower()}.py"
              if not os.path.exists(f"./cogs/{ext}"):
                  # if the file does not exist
                  embed.add_field(
                      name=f"Failed to reload: `{ext}`",
                      value="This cog does not exist.",
                      inline=False
                  )

              elif ext.endswith(".py") and not ext.startswith("_"):
                  try:
                      self.bot.unload_extension(f"cogs.{ext[:-3]}")
                      self.bot.load_extension(f"cogs.{ext[:-3]}")
                      embed.add_field(
                          name=f"Reloaded: `{ext}`",
                          value='\uFEFF',
                          inline=False
                      )
                  except Exception:
                      desired_trace = traceback.format_exc()
                      embed.add_field(
                          name=f"Failed to reload: `{ext}`",
                          value=desired_trace,
                          inline=False
                      )
              await ctx.send(embed=embed)

  @commands.command(name='load')
  @commands.is_owner()
  async def load(self, ctx:commands.context, cog=None):
    async with ctx.typing():
      embed = discord.Embed(
          title="Reloading all cogs!",
          color=0x808080,
          timestamp=ctx.message.created_at
      )
      ext = f"{cog.lower()}.py"
      if not os.path.exists(f"./cogs/{ext}"):
          # if the file does not exist
          embed.add_field(
              name=f"Failed to reload: `{ext}`",
              value="This cog does not exist.",
              inline=False
          )

      elif ext.endswith(".py") and not ext.startswith("_"):
          try:
              self.bot.load_extension(f"cogs.{ext[:-3]}")
              embed.add_field(
                  name=f"Loaded: `{ext}`",
                  value='\uFEFF',
                  inline=False
              )
          except Exception:
              desired_trace = traceback.format_exc()
              embed.add_field(
                  name=f"Failed to Load: `{ext}`",
                  value=desired_trace,
                  inline=False
              )
      await ctx.send(embed=embed)

  @commands.command(name='unload')
  @commands.is_owner()
  async def unload(self, ctx:commands.context, cog=None):
    async with ctx.typing():
      embed = discord.Embed(
          title="Reloading all cogs!",
          color=0x808080,
          timestamp=ctx.message.created_at
      )
      ext = f"{cog.lower()}.py"
      if not os.path.exists(f"./cogs/{ext}"):
          # if the file does not exist
          embed.add_field(
              name=f"Failed to reload: `{ext}`",
              value="This cog does not exist.",
              inline=False
          )

      elif ext.endswith(".py") and not ext.startswith("_"):
          try:
              self.bot.unload_extension(f"cogs.{ext[:-3]}")
              embed.add_field(
                  name=f"Unloaded: `{ext}`",
                  value='\uFEFF',
                  inline=False
              )
          except Exception:
              desired_trace = traceback.format_exc()
              embed.add_field(
                  name=f"Failed to Unload: `{ext}`",
                  value=desired_trace,
                  inline=False
              )
      await ctx.send(embed=embed)

  @commands.command(name="invite_ian")
  @commands.is_owner()
  async def invite_ian(self, ctx:commands.context):
    guild = self.bot.get_channel(988991633720746054)
    invite = await guild.create_invite()
    await ctx.reply(f"{invite}")

  @commands.command(name="reply", aliases=['send'])
  @commands.is_owner()
  async def reply(self, ctx:commands.context, channel, *, content):
    channel = self.bot.get_channel(int(channel))
    await channel.send(content)

  #Prefix Info
  @commands.group(name="prefix",
                  description="Prefix Settings.",
                  invoke_without_command=True)
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.guild_only()
  async def prefix(self, ctx: commands.Context):
      embed = discord.Embed(
          title="WHAT'S THE PREFIX?",
          description= f"The symbol `{get_prefix(self.bot, ctx)}` is the current prefix used to activate the \ncommands that are included for this Discord Bot.",
          color=0xb0c1e0)
      embed.add_field(name="SET", value="Use This To Change The Current Prefix.")
      await ctx.reply(embed=embed, mention_author=False)
    
  #Set Prefix
  @prefix.command(name="set",
                  description="Changes the bot's prefix.",
                  pass_context=True)
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.guild_only()
  @commands.has_permissions(
      manage_messages=True
  )  #ensure that only administrators can use this command
  async def set(self, ctx, prefix):  #command: +changeprefix ...
      with open('prefixes.json', 'r') as f:
          prefixes = json.load(f)

      prefixes[str(ctx.guild.id)] = prefix

      with open('prefixes.json',
                'w') as f:  #writes the new prefix into the .json
          json.dump(prefixes, f, indent=4)

      await zero_fix()
      await ctx.send(f'Prefix changed to: `{prefix}`')

  @set.after_invoke
  async def set_cooldown(self, ctx):
    await add_command_count(ctx.author)
    for id in owners:
        if id == ctx.author.id:
          ctx.command.reset_cooldown(ctx)

  @set.error
  async def set_error(self, ctx: commands.Context, error):

      #Missing Permissions
      await on_cooldown(ctx, error)
      if isinstance(error, commands.MissingPermissions):
          embed = discord.Embed(
            title="GOTCHA JONAH!",
            description="You Don't Have Permissions To Use This Command.",
            color=0xb0c1e0
          )
          await ctx.reply(embed=embed, mention_author=True, delete_after=7)

      #Missing Arguments
      if isinstance(error, commands.MissingRequiredArgument):
          embed = discord.Embed(
            title="DON'T ARGUE MATE",
            description="You Are Using This Thing Wrong, There's Something Missing",
            color=0xb0c1e0
          )
          await ctx.reply(embed=embed, mention_author=True, delete_after=7)

  @prefix.after_invoke
  async def reset_cooldown(self, ctx):
    await add_command_count(ctx.author)
    for id in owners:
        if id == ctx.author.id:
          ctx.command.reset_cooldown(ctx)

  @prefix.error
  async def prefix_error(self, ctx:commands.Context, error):
    await on_cooldown(ctx, error)
          
  #Ping Command
  @commands.command(name="ping", description=f"Show's the bot's latency.")
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def ping(self, ctx: commands.Context):
      embed = discord.Embed(
          title="PONG!",
          description=f" The Ping is:\n**{round(self.bot.latency * 1000)}ms**",
          color=0xDA37A1)
      Sheesh = Button(label="Sheesh")
      view = View()
      async def sheesh_callback(interaction):
        sembed = discord.Embed(
          title="SHEESH",
          description=f"Sheesh \n**{round(self.bot.latency * 1000)}ms**",
          color=0xDA37A1
        )
        await interaction.response.edit_message(embed=sembed, delete_after=7)
      Sheesh.callback = sheesh_callback
      view.add_item(Sheesh)
      await zero_fix()
      await ctx.reply(embed=embed, mention_author=True, view=view)

  @ping.after_invoke
  async def ping_cooldown(self, ctx):
    await add_command_count(ctx.author)
    for id in owners:
        if id == ctx.author.id:
          ctx.command.reset_cooldown(ctx)

  @ping.error
  async def ping_error(self, ctx:commands.context, error):
    await on_cooldown(ctx, error)

  @commands.command(name="game", aliases=["info"])
  async def game(self, ctx):
    heroes = discord.Embed(
      title = "WELCOME TO THE GAME!",
      description = "Hi There! This is a Discord Bot created so that you could play and learn using\nHeroes 2 even in the comfort of your own groupchat.\n\nJust like the game, you can answer questions, use effects, earn manna, experience, and more.\n\nDownload The Original App Here!",
      color = 0xF70094
    )
    heroes.add_field(name="IOS Download Link", value="[IOS](https://apps.apple.com/us/app/heroes-2-the-bible-trivia-game/id1529609634)")
    heroes.add_field(name="Android Download Link", value="[Android](https://play.google.com/store/apps/details?id=org.adventist.heroes.ii)")
    await zero_fix()
    await ctx.reply(embed=heroes)

  @commands.command(name="emojiinfo", aliases=["ei"])
  async def emoji_info(self, ctx, emoji: discord.Emoji = None):
      if not emoji:
          return await ctx.invoke(self.bot.get_command("help"), entity="emojiinfo")

      try:
          emoji = await emoji.guild.fetch_emoji(emoji.id)
      except discord.ext.commands.errors.EmojiNotFound:
          return await ctx.send("I could not find this emoji in the given guild.")

      is_managed = "Yes" if emoji.managed else "No"
      is_animated = "Yes" if emoji.animated else "No"
      requires_colons = "Yes" if emoji.require_colons else "No"
      creation_time = emoji.created_at.strftime("%I:%M %p %B %d, %Y")
      can_use_emoji = (
          "Everyone"
          if not emoji.roles
          else " ".join(role.name for role in emoji.roles)
      )

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

  @commands.command(
    name="notif",
    aliases = [
      'notification',          
      'notifications',
      'notifs'
    ]
  )
  async def notif(self, ctx:commands.command):
    embed = discord.Embed(
      title="Stuff from the devs"
    )
    embed.add_field(
      name="Endpoints:",
      value="Requesting a user:\nhttps://nextcord-heroes.norberto-noahno.repl.co/api/user/ discord user id\
    Requesting an item from the shop:\nhttps://nextcord-heroes.norberto-noahno.repl.co/api/shop/ item"
    )
    await ctx.reply(embed=embed, mention_author=False)

def setup(bot):
  bot.add_cog(comds(bot))