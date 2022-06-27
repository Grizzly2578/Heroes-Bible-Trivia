import requests
import json

from nextcord.ext import commands
from config import discord, add_command_count, owners, zero_fix, on_cooldown

class verse(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  #Verse Command
  @commands.command(name="verse", aliases=['vers'])
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def verse(self, ctx, *args):
      if not args:
        results = requests.get(
            "https://labs.bible.org/api/?passage=random&type=json").json()
        bookname = results[0]['bookname']
        chapter = results[0]['chapter']
        verse = results[0]['verse']
        text = results[0]['text']
        embed = discord.Embed(color=0xF7CA00, title=f"VERSE GENERATOR")
        embed.description = "[Click Here for More Verses](https://www.biblegateway.com/)"
        embed.add_field(name="----------------------------------",
                        value=f" ***{text}***",
                        inline=False)
        embed.set_footer(text=f"{bookname} {chapter}:{verse}")
        embed.set_author(name="JESUS",icon_url="https://i.imgur.com/TH5oBkC.png")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/944155967011041343/984709410347688036/unknown.png?size=4096")  
        await zero_fix()
        await ctx.reply(embed=embed)
      elif args:
        items = " ".join(args)
        results = requests.get("https://labs.bible.org/api/?passage=" + items + '&type=json').json()
        if len(results) == 1:
          bookname = results[0]['bookname']
          chapter = results[0]['chapter']
          verse = results[0]['verse']
          text = results[0]['text']
          embed = discord.Embed(color=0xF7CA00, title=f"VERSE GENERATOR")
          embed.description = "[Click Here for More Verses](https://www.biblegateway.com/)"
          embed.add_field(name="----------------------------------",value=f" ***{text}***")
          embed.set_footer(text=f"{bookname} {chapter}:{verse}")
          embed.set_author(name="JESUS", icon_url="https://i.imgur.com/TH5oBkC.png")
          embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/944155967011041343/984709410347688036/unknown.png?size=4096")
          await zero_fix()
          await ctx.reply(embed=embed)
        elif len(results) > 1:
          bookname = results[0]['bookname']
          chapter = results[0]['chapter']
          text = requests.get("https://labs.bible.org/api/?passage=" + items + "&type=text"+"&formatting=plain")
          embed = discord.Embed(color=0xF7CA00, title=f"VERSE GENERATOR")
          embed.description = "[Click Here for More Verses](https://www.biblegateway.com/)"
          embed.add_field(name="----------------------------------",value=f" ***{str(text.content)[4:]}***")
          embed.set_footer(text=f"{args}")
          embed.set_author(name="JESUS", icon_url="https://i.imgur.com/TH5oBkC.png")
          embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/944155967011041343/984709410347688036/unknown.png?size=4096")
          await zero_fix()
          await ctx.reply(embed=embed)

  @verse.after_invoke
  async def verse_cooldown(self, ctx):
    await add_command_count(ctx.author)
    for id in owners:
        if id == ctx.author.id:
          ctx.command.reset_cooldown(ctx)

  # @verse.error
  # async def verse_error(self, ctx:commands.Context, error):
  #   await on_cooldown(ctx, error)

def setup(bot):
  bot.add_cog(verse(bot))