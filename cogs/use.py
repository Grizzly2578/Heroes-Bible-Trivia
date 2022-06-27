import json
import random
from nextcord.ext import commands
from config import discord, new_user, zero_item_fix



no_item = discord.Embed(
  title="What?",
  description="No item provided"
)

no_item1 = discord.Embed(
  title="No!",
  description="You dont have this item"
)

unknown_item = discord.Embed(
  title="Which one?",
  description="We dont have that item here"
)

with open("save.json", "r") as f:
  users = json.load(f)

with open("effect_shop.json", "r") as f1:
  effects = json.load(f1)

with open("shop.json", "r") as f2:
  shop = json.load(f2)

async def use_mycrate(ctx, user, count):
  random_manna = random.randint(750, 1000) * int(count)
  effect = random.choices(list(effects.keys()), k=3 * int(count))
  with open("save.json", "r") as f:
    users = json.load(f)
  users[str(user.id)]['bag']['MYCRATE']['count'] -= int(count)
  users[str(user.id)]['manna'] += random_manna
  if 'MYCRATE' not in users['983916041384112168']['bag']:
    users['983916041384112168']['bag']['MYCRATE'] = {}
    users['983916041384112168']['bag']['MYCRATE']['count'] = int(count)
  else:
    users['983916041384112168']['bag']['MYCRATE']['count'] += int(count)
  
  for effects1 in effect:
    if effects1 in users[str(user.id)]['effects']:
      users[str(user.id)]['effects'][effects1]['count'] += int(count)
    else:
      users[str(user.id)]['effects'][effects1] = {}
      users[str(user.id)]['effects'][effects1]['count'] = int(count)
  with open("save.json", "w") as f:
    json.dump(users, f, indent=4, sort_keys=True)
  embed = discord.Embed(
    title = f"You used {count} Mystery Crate!",
    description = f"You recived {random_manna}🌾"
  )
  one_out_of_1k = random.randint(1, 100)
  if one_out_of_1k == 7:
    dev_items = [
      'DONUT',
      'CHICKEN',
      'BREAD'
    ]
    item = random.choice(dev_items)
    if item not in users[str(user.id)]['bag']:
      users[str(user.id)]['bag'][item] = {}
      users[str(user.id)]['bag'][item]['count'] = 1
      embed.add_field(name=f"{int(count)}`{shop[item]['icon']}** - {shop[item]['name']}**", value=f"*{shop[item]['description']}*", inline=False)
  for effects2 in effect:
    embed.add_field(name=f"`{int(count)}`{effects[effects2]['icon']}** - {effects[effects2]['name']}**", value=f"*{effects[effects2]['description']}*", inline=False)
  await zero_item_fix()
  await ctx.reply(embed=embed)


  
async def use_donut(ctx, user, count):
  random_xp = random.randint(2500, 5000)
  users[str(user.id)]['points'] += random_xp
  users[str(user.id)]['bag']['DONUT']['count'] -= int(count)
  embed = discord.Embed(
    title = f"You used {count} Donut!",
    description = f"You recived {random_xp}🔹"
  )
  if 'DONUT' not in users['983916041384112168']['bag']:
    users['983916041384112168']['bag']['DONUT'] = {}
    users['983916041384112168']['bag']['DONUT']['count'] = int(count)
  else:
    users['983916041384112168']['bag']['DONUT']['count'] += int(count)
  with open("save.json", "w") as f:
    json.dump(users, f, indent=4)
  await ctx.reply(embed=embed)

  

async def use_item(ctx, user, count, item):
  if item == "MYCRATE":
    await use_mycrate(ctx, user, count)
  if item == "DONUT":
    await use_donut(ctx, user, count)
  

class use(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command(
    name="use"
  )
  async def use(self, ctx, item=None, count=None):
    with open("save.json", "r") as f:
      users = json.load(f)
    user = ctx.author
    if count == None:
      count = 1
    if int(count) < 1:
      await ctx.reply("Ammount must not be lower than 1")
    else:
      if item == None:
        await ctx.reply(embed=no_item)
      else:
        item = item.upper()
        with open("shop.json", "r") as f:
          shop = json.load(f)
        if item not in shop.keys():
          await ctx.reply(embed=unknown_item)
        else:
          with open("save.json", "r") as f:
            users = json.load(f)
          if item not in users[str(user.id)]['bag']:
            await new_user(user)
            await ctx.reply(embed=no_item1)
          else:
            await use_item(ctx, user, count, item)

def setup(bot):
  bot.add_cog(use(bot))