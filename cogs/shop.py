import json

from nextcord.ext import commands
from config import discord, add_command_count, zero_fix, owners, new_user

class shop(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group(name="shop", aliases=['item'], invoke_without_command=True)
  @commands.cooldown(1, 3, commands.BucketType.user)
  async def shop(self, ctx:commands.context, *, item=None):
    if item == None:
      with open("save.json", "r") as f2:
        users = json.load(f2)
      if str(ctx.author.id) not in users:
        await new_user(ctx.author)
      with open("shop.json", "r") as f:
        shop = json.load(f)
      embed = discord.Embed(
        title = "WELCOME TO THE SHOP",
        description = "In here, you can buy and sell different items such \nas manna packs, effects packs, and so much more.",
        color = 0xF7AD00
      )
  
      for item in list(shop):
        if shop[item]['price'] == None:
          pass
        else:
          name = shop[item]['name']
          id = shop[item]['id']
          price = shop[item]['price']
          description = shop[item]['description']
          icon = shop[item]['icon']
          embed.add_field(name=f"{icon} - {name}", value=f"> *ID*`{id}`\n> 🌾`{price}`\n> {description}")
      await zero_fix()
      await ctx.reply(embed=embed)
    else:
      with open("shop.json", "r") as f:
        shop = json.load(f)
      with open("save.json", "r") as f1:
        users = json.load(f1)
      item = item.upper()
      if item in shop.keys():
        name = shop[item]['name']
        icon = shop[item]['icon']
        image = shop[item]['image']
        id = shop[item]['id']
        price = shop[item]['price']
        description = shop[item]['description']
        rarity = shop[item]['rarity']
        if price == None:
          price = "Unable to be bought"
        if item in list(users[str(ctx.author.id)]['bag']):
          count = users[str(ctx.author.id)]['bag'][item]['count']
          embed = discord.Embed(
            title=f"{name} ({count} owned)", 
            description=f"> {description}\n\n<:GUI:953128943974776913> ID `{id}`\n**Buy** - 🌾`{price}`",
            color = 0xF7D600
          )
          embed.add_field(
            name="Rarity",
            value=f"`{rarity}`"
          )
          embed.set_thumbnail(url=image)
          await zero_fix()
          await ctx.reply(embed=embed)
        else:
          count = 0
          embed = discord.Embed(
            title=f"{name} ({count} owned)", 
            description=f"> {description}\n\n<:GUI:953128943974776913> ID `{id}`\n**Buy** - 🌾`{price}`",
            color = 0xF7D600
          )
          embed.add_field(
            name="Rarity",
            value=f"`{rarity}`"
          )
          embed.set_thumbnail(url=image)
          await zero_fix()
          await ctx.reply(embed=embed)
      else:
        await zero_fix()
        await ctx.reply("unknown item")


  
  @shop.command(name="buy")
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def buy(self, ctx, count=1, *, item):
    with open("shop.json", "r") as f1:
      shop = json.load(f1)
    with open("save.json", "r") as f:
      users = json.load(f)
    item = item.upper()
    if int(count)<0:
        await ctx.reply("Amount Must Have A Positive Number!")
    user = ctx.author
    if str(user.id) not in users:
      await new_user(user)
      await ctx.reply("Not Enough Manna")
    else:
      if int(count) == 0:
          await ctx.reply("Ammount cannot be 0")
      else:
        if item in shop.keys():
          with open("save.json", "r") as f:
            users = json.load(f)
          user = ctx.author
          price = shop[item.upper()]['price']
          if price == None:
            await ctx.reply("That Item is not available in this shop")
          if users[str(user.id)]['manna'] < price * int(count):
            await ctx.reply("Not Enough Manna")
          else:
            with open("save.json", "r") as f:
              users = json.load(f)

            if item in users[str(user.id)]['bag']:
              users[str(user.id)]['manna'] -= shop[item]['price'] * int(count)
              users[str(self.bot.user.id)]['manna'] += shop[item]['price'] * int(count)
              users[str(user.id)]['bag'][item]['count'] += int(count)
              with open("save.json", "w") as f:
                json.dump(users, f, indent=4, sort_keys=True)
              jollibee = discord.Embed(
                title = "TRADE SUCCESSFUL",
                description = f"`{count}` **{shop[item]['name']}** *Sucessfully Bought For* 🌾`{shop[item]['price'] * int(count)}`!",
                color = 0xF7D600
              )
              await zero_fix()
              await ctx.reply(embed=jollibee)
            else:
              with open("save.json", "r") as f:
                users = json.load(f)
              users[str(user.id)]['bag'][item] = {}
              users[str(user.id)]['bag'][item]['count'] = 0
              users[str(user.id)]['bag'][item]['count'] += int(count)
              users[str(user.id)]['manna'] -= shop[item]['price'] * int(count)
              users[str(self.bot.user.id)]['manna'] += shop[item]['price'] * int(count)
              with open("save.json", "w") as f:
                users = json.dump(users, f, indent=4, sort_keys=True)
              jollibee = discord.Embed(
                title = "TRADE SUCCESSFUL",
                description = f"`{count}` **{shop[item]['name']}** *Sucessfully Bought For* 🌾`{shop[item]['price'] * int(count)}`!",
                color = 0xF7D600
              )
              await zero_fix()
              await ctx.reply(embed=jollibee)
      
        else:
          await zero_fix()
          await ctx.reply("Unknown Item")

  @commands.command(name="buy")
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def buy1(self, ctx, count=1, *, item):
    with open("shop.json", "r") as f1:
      shop = json.load(f1)
    with open("save.json", "r") as f:
      users = json.load(f)
    item = item.upper()
    if int(count)<0:
        await ctx.reply("Amount Must Have A Positive Number!")
    user = ctx.author
    if str(user.id) not in users:
      await new_user(user)
      await ctx.reply("Not Enough Manna")
    else:
      if int(count) == 0:
          await ctx.reply("Ammount cannot be 0")
      else:
        if item in shop.keys():
          with open("save.json", "r") as f:
            users = json.load(f)
          user = ctx.author
          price = shop[item.upper()]['price']
          if price == None:
            await ctx.reply("That Item is not available in this shop")
          if users[str(user.id)]['manna'] < price * int(count):
            await ctx.reply("Not Enough Manna")
          else:
            with open("save.json", "r") as f:
              users = json.load(f)

            if item in users[str(user.id)]['bag']:
              users[str(user.id)]['manna'] -= shop[item]['price'] * int(count)
              users[str(self.bot.user.id)]['manna'] += shop[item]['price'] * int(count)
              users[str(user.id)]['bag'][item]['count'] += int(count)
              with open("save.json", "w") as f:
                json.dump(users, f, indent=4, sort_keys=True)
              jollibee = discord.Embed(
                title = "TRADE SUCCESSFUL",
                description = f"`{count}` **{shop[item]['name']}** *Sucessfully Bought For* 🌾`{shop[item]['price'] * int(count)}`!",
                color = 0xF7D600
              )
              await zero_fix()
              await ctx.reply(embed=jollibee)
            else:
              with open("save.json", "r") as f:
                users = json.load(f)
              users[str(user.id)]['bag'][item] = {}
              users[str(user.id)]['bag'][item]['count'] = 0
              users[str(user.id)]['bag'][item]['count'] += int(count)
              users[str(user.id)]['manna'] -= shop[item]['price'] * int(count)
              users[str(self.bot.user.id)]['manna'] += shop[item]['price'] * int(count)
              with open("save.json", "w") as f:
                users = json.dump(users, f, indent=4, sort_keys=True)
              jollibee = discord.Embed(
                title = "TRADE SUCCESSFUL",
                description = f"`{count}` **{shop[item]['name']}** *Sucessfully Bought For* 🌾`{shop[item]['price'] * int(count)}`!",
                color = 0xF7D600
              )
              await zero_fix()
              await ctx.reply(embed=jollibee)
      
        else:
          await zero_fix()
          await ctx.reply("Unknown Item")






























          
  # @buy.error
  # async def buy_error(self, ctx:commands.Context, error):
  #   await on_cooldown(ctx, error)
  #   if isinstance(error, commands.MissingRequiredArgument):
  #     await ctx.reply("Missing Arguemnts!")

  @buy.after_invoke
  async def buy_cooldown(self, ctx):
    await add_command_count(ctx.author)
    for id in owners:
      if id == ctx.author.id:
        ctx.command.reset_cooldown(ctx)

  # @buy1.error
  # async def buy1_error(self, ctx:commands.Context, error):
  #   await on_cooldown(ctx, error)
  #   if isinstance(error, commands.MissingRequiredArgument):
  #     await ctx.reply("Missing Arguemnts!")

  @buy1.after_invoke
  async def buy1_cooldown(self, ctx):
    await add_command_count(ctx.author)
    for id in owners:
      if id == ctx.author.id:
        ctx.command.reset_cooldown(ctx)
        
  # @shop.error
  # async def shop_error(self, ctx:commands.Context, error):
  #   await on_cooldown(ctx, error)

  @shop.after_invoke
  async def shop_cooldown(self, ctx):
    await add_command_count(ctx.author)
    for id in owners:
      if id == ctx.author.id:
        ctx.command.reset_cooldown(ctx)

def setup(bot):
  bot.add_cog(shop(bot))