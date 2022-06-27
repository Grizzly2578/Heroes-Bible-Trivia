import json, datetime
from config import discord, owners, add_command_count, get_commands_ran, new_user, on_cooldown, level_fix, zero_fix, random_fact, update_name
from nextcord.ext import commands

class profile(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @commands.cooldown(1, 5, commands.BucketType.user)
  @commands.command(name="profile", aliases=['p', 'xp'])
  async def profile(self, ctx, member: discord.Member = None):
    await level_fix()
    await zero_fix()
    await random_fact(ctx)
    await update_name(ctx.author)
    if member != None:
      with open("save.json", "r") as f:
        users = json.load(f)
      if str(member.id) in users:
        await update_name(member)
        with open("save.json", "r") as f:
          users = json.load(f)
          with open("save.json", "r") as f:
            users = json.load(f)
          manna = users[str(member.id)]['manna']
          xp = users[str(member.id)]['points']
          streak = users[str(member.id)]['streak']
          level = users[str(member.id)]['level']
          #Profile Embed
          jomama=discord.Embed(
            color=0xDE52B2
          )
          if member.avatar != None:
            jomama.set_thumbnail(url=member.avatar.url)
          jomama.add_field(name="Level:", value=f"**{level}**", inline=True)
          jomama.add_field(name="Experience:", value=f"🔹`{xp}`", inline=True)
          jomama.add_field(name="Manna:", value=f"🌾`{manna}`", inline=True)
          jomama.add_field(name="Streak:", value=f"✅`{streak}`", inline=True)
          jomama.add_field(name="Commands Ran", value=f"🖥️`{await get_commands_ran(member)}`", inline=True)
          jomama.timestamp = datetime.datetime.utcnow()
          if member.avatar != None:
            jomama.set_author(
              name=f"{member}", 
              icon_url=member.avatar.url, 
              url=f"https://discordapp.com/users/{member.id}")
          else:
            jomama.set_author(
              name=f"{member}",
              url=f"https://discordapp.com/users/{member.id}")
          await ctx.reply(embed=jomama)
      else:
          with open("save.json", "r") as f:
            users = json.load(f)
            with open("save.json", "r") as f:
              users = json.load(f)
            manna = "None"
            xp = "None"
            streak = "None"
            level = "None"
            
            #Profile Embed
            jomama=discord.Embed(
              color=0xDE52B2
            )
            if member.avatar != None:
              jomama.set_thumbnail(url=member.avatar.url)
            jomama.add_field(name="Level:", value=f"**{level}**", inline=True)
            jomama.add_field(name="Experience:", value=f"🔹`{xp}`", inline=True)
            jomama.add_field(name="Manna:", value=f"🌾`{manna}`", inline=True)
            jomama.add_field(name="Streak:", value=f"✅`{streak}`", inline=True)
            jomama.add_field(name="Commands Ran", value=f"🖥️`{await get_commands_ran(member)}`", inline=True)
            jomama.timestamp = datetime.datetime.utcnow()
            if member.avatar != None:
              jomama.set_author(
                name=f"{member}", 
                icon_url=member.avatar.url, 
                url=f"https://discordapp.com/users/{member.id}")
            else:
              jomama.set_author(
                name=f"{member}",
                url=f"https://discordapp.com/users/{member.id}")
            await ctx.reply(embed=jomama)
    else:
      member = ctx.author
      with open("save.json", "r") as f:
        users = json.load(f)
      if str(member.id) not in users:
        await new_user(member)
        await add_command_count(member)
      else:
        with open("save.json", "r") as f:
          users = json.load(f)
        manna = users[str(member.id)]['manna']
        xp = users[str(member.id)]['points']
        streak = users[str(member.id)]['streak']
        level = users[str(member.id)]['level']
        
        #Profile Embed
        jomama=discord.Embed(
          color=0xDE52B2
        )
        if member.avatar != None:
          jomama.set_thumbnail(url=member.avatar.url)
        jomama.add_field(name="Level:", value=f"**{level}**", inline=True)
        jomama.add_field(name="Experience:", value=f"🔹`{xp}`", inline=True)
        jomama.add_field(name="Manna:", value=f"🌾`{manna}`", inline=True)
        jomama.add_field(name="Streak:", value=f"✅`{streak}`", inline=True)
        jomama.add_field(name="Commands Ran", value=f"🖥️`{await get_commands_ran(member)}`", inline=True)
        jomama.timestamp = datetime.datetime.utcnow()
        if member.avatar != None:
          jomama.set_author(
            name=f"{member}", 
            icon_url=member.avatar.url, 
            url=f"https://discordapp.com/users/{member.id}")
        else:
          jomama.set_author(
            name=f"{member}",
            url=f"https://discordapp.com/users/{member.id}")
        await ctx.reply(embed=jomama)






  
  @profile.after_invoke
  async def reset_cooldown(self, ctx):
    await random_fact(ctx)
    await add_command_count(ctx.author)
    await update_name(ctx.author)
    for id in owners:
      if id == ctx.author.id:
        ctx.command.reset_cooldown(ctx)

  @profile.error
  async def profile_error(self, ctx: commands.Context, error):
      await on_cooldown(ctx, error)
      if isinstance(error, commands.MemberNotFound):
          await random_fact(ctx)
          embed = discord.Embed(
              title="WHO AGAIN?",
              description=f"Unknown User.\nI've Never Met This Man My Entire Life.",
              color=0xb0c1e0)
          embed.set_thumbnail(url="https://i.imgur.com/3QiQAfL.png")
          await ctx.reply(embed=embed, delete_after=7)

def setup(bot):
  bot.add_cog(profile(bot))