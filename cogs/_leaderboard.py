import json



from nextcord.ext import commands
from config import discord, get_prefix, zero_fix, owners, on_cooldown, add_command_count



class leaderboard(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group(name="top", aliases=["leaderboard", "lb"], invoke_without_command=True)
  async def top(self, ctx):
    await ctx.reply(
      f"The top command, commands: \n{get_prefix(self.bot, ctx)}top manna\n{get_prefix(self.bot, ctx)}top xp"
    )


    
  @top.command(name="manna", aliases=["m"], pass_context=True)
  @commands.cooldown(1, 3, commands.BucketType.user)
  async def top_manna(self, ctx):
    with open("save.json", "r") as f:
      users = json.load(f)
    x=10
    leaderboard = {}
    total=[]
    for user in list(users):
      name = users[str(user)]['name']
      total_amt = users[str(user)]['manna']
      leaderboard[total_amt] = name
      total.append(total_amt)

    total = sorted(total,reverse=True)
    em = discord.Embed(
    title = f'Top {x} Highest Manna Count',
    description = 'The Highest Manna Count Recorded',
    color = 0xFFCC4D)
    index = 1
    for amt in total:
      if amt != 0:
        id_ = leaderboard[amt]
        
        em.add_field(name = f'{index}: {id_}', value = f'  🌾`{amt}`', inline=False)      
        
        if index == x:
          break
        else:
          index += 1
    await zero_fix()
    await ctx.send(embed = em)
  
  @top.command(name="xp", aliases=["experience"], pass_context=True)
  @commands.cooldown(1, 3, commands.BucketType.user)
  async def top_xp(self, ctx):
    with open("save.json", "r") as f:
      users = json.load(f)
    x=10
    leaderboard = {}
    total=[]
    for user in list(users):
      name = users[str(user)]['name']
      total_amt = users[str(user)]['points']
      leaderboard[total_amt] = name
      total.append(total_amt)

    total = sorted(total,reverse=True)
    em = discord.Embed(
    title = f'Top {x} Highest Experience Count',
    description = 'The Highest Experience Count Recorded',
    color = 0x55ACEE)
    index = 1
    for amt in total:
      if amt != 0:
        id_ = leaderboard[amt]
        
        em.add_field(name = f'{index}: {id_}', value = f'  🔹`{amt}`', inline=False)      
        
        if index == x:
          break
        else:
          index += 1
    await zero_fix()
    await ctx.send(embed = em)

  @top.command(name="lvl", aliases=["level"], pass_context=True)
  @commands.is_owner()
  @commands.cooldown(1, 3, commands.BucketType.user)
  async def top_lvl(self, ctx):
    with open("save.json", "r") as f:
      users = json.load(f)
    x=10
    leaderboard = {}
    total=[]
    for user in list(users):
      name = users[str(user)]['name']
      total_amt = users[str(user)]['level']
      leaderboard[total_amt] = name
      total.append(total_amt)

    total = sorted(total,reverse=True)
    em = discord.Embed(
    title = f'Top {x} Highest Experience Count',
    description = 'The Highest Experience Count Recorded',
    color = 0x55ACEE)
    index = 1
    for amt in total:
      if amt != 0:
        id_ = leaderboard[amt]
        
        em.add_field(name = f'{index}: {id_}', value = f'  🔹`{amt}`', inline=False)      
        
        if index == x:
          break
        else:
          index += 1
    await zero_fix()
    await ctx.send(embed = em)

  @top.after_invoke
  async def top_cooldown(self, ctx):
    await add_command_count(ctx.author)
    for id in owners:
      if id == ctx.author.id:
        ctx.command.reset_cooldown(ctx)

  @top.error
  async def top_error(self, ctx:commands.Context, error):
    await on_cooldown(ctx, error)
  
  @top_manna.after_invoke
  async def top_cooldown(self, ctx):
    await add_command_count(ctx.author)
    for id in owners:
      if id == ctx.author.id:
        ctx.command.reset_cooldown(ctx)

  @top_manna.error
  async def top_manna_error(self, ctx:commands.Context, error):
    await on_cooldown(ctx, error)
  
  @top_xp.after_invoke
  async def top_xp_cooldown(self, ctx):
    await add_command_count(ctx.author)
    for id in owners:
      if id == ctx.author.id:
        ctx.command.reset_cooldown(ctx)

  @top_xp.error
  async def top_xp_error(self, ctx:commands.Context, error):
    await on_cooldown(ctx, error)
  
  @top_lvl.error
  async def top_lvl_error(self, ctx:commands.Context, error):
    await on_cooldown(ctx, error)

def setup(bot):
  bot.add_cog(leaderboard(bot))