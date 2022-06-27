import json
from config import discord, owners, new_user, on_cooldown, add_command_count, zero_effect_fix, zero_fix
from nextcord.ext import commands

class effect(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.group(name="effect", aliases=["effects", "fx"], invoke_without_command=True)
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def effect(self, ctx, user: discord.Member = None):
    await zero_effect_fix()
    with open("save.json", "r") as f:
      users = json.load(f)
      
    if user != None:
      
      if str(user.id) in users:
        
        embed=discord.Embed(
          title="THE EFFECTS THEY HAVE", 
          description="We see that you have discovered the effects panel. \nIn here you can mainly see the effects that you own, \nalong with a bunch of other subcommands under this panel. \n")

        #Invisible Embed
        embed.add_field(
          name=f"\u200b ", 
          value=f"\u200b ",
          inline=False)
        
        if users[str(user.id)]['effects'] == "":
          return
        else:
          for effect in list(users[str(user.id)]['effects'].keys()):
            with open("effect_shop.json", "r") as f2:
              shop = json.load(f2)
            effect_name = shop[effect]['name']
            effect_count = users[str(user.id)]['effects'][effect]['count']
            effect_desc = shop[effect]['description']
            effect_icon = shop[effect]['icon']
            effect_image = shop[effect]['image']
            if effect_count != 0:
  
              #Main Embed
              embed.add_field(
                name=f"`{effect_count}`{effect_icon} - {effect_name}",
                value=f"<:GUI:953128943974776913> *{effect_desc}*",
                inline = False)
            
        await ctx.reply(embed=embed)
        
      else:
        
        embed = discord.Embed(
          title="WHO AGAIN?",
          description=f"Unknown User.\nI've Never Met This Man My Entire Life.",
          color=0xb0c1e0)
        embed.set_thumbnail(url="https://i.imgur.com/3QiQAfL.png")
        await ctx.reply(embed=embed, delete_after=7)
        
    else:
      
      user = ctx.author
      if str(user.id) not in users:
        await new_user(user)
        embed=discord.Embed(
          title="THE EFFECTS YOU HAVE", 
          description="We see that you have discovered the effects panel. \nIn here you can mainly see the effects that you own, \nalong with a bunch of other subcommands under this panel. \n")
        
        #Invisible Embed
        embed.add_field(
          name=f"\u200b ", 
          value=f"\u200b ",
          inline=False)
            
        await ctx.reply(embed=embed)
        
      else:
        
        embed=discord.Embed(
          title="THE EFFECTS YOU HAVE", 
          description="We see that you have discovered the effects panel. \nIn here you can mainly see the effects that you own, \nalong with a bunch of other subcommands under this panel. \n")
        
        #Invisible Embed
        embed.add_field(
          name=f"\u200b ", 
          value=f"\u200b ",
          inline=False)
        if users[str(user.id)]['effects'] == "":
          return
        else:
          for effect in list(users[str(user.id)]['effects'].keys()):
            with open("effect_shop.json", "r") as f2:
              shop = json.load(f2)
            effect_name = shop[effect]['name']
            effect_count = users[str(user.id)]['effects'][effect]['count']
            effect_desc = shop[effect]['description']
            effect_icon = shop[effect]['icon']
            effect_image = shop[effect]['image']
            if effect_count != 0:
  
              #Main Embed
              embed.add_field(
                name=f"`{effect_count}`{effect_icon} - {effect_name}",
                value=f"<:GUI:953128943974776913> *{effect_desc}*",
                inline = False)
            
        await ctx.reply(embed=embed)
  
  @effect.command(name="shop", aliases=['item', 'help'])
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def effect_shop(self, ctx:commands.context, *, item=None):
    if item == None:
      with open("effect_shop.json", "r") as f:
        shop = json.load(f)
      embed = discord.Embed(
        title = "WELCOME TO THE SHOP",
        description = "In here, you can buy and sell different effects",
        color = 0xFFCC4D
      )
  
      for item in list(shop):
        name = shop[item]['name']
        price = shop[item]['price']
        icon = shop[item]['icon']
        if shop[item]['status'] == "unusable":
          description = "**Work in Progress**"
        else:
          description = shop[item]['description']
        embed.add_field(name=f"{icon} {name}", value=f"> 🌾`{price}`\n> *{description}*", inline=True)
      await ctx.reply(embed=embed)
    else:
      with open("effect_shop.json", "r") as f:
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
        if item in list(users[str(ctx.author.id)]['effects']):
          count = users[str(ctx.author.id)]['effects'][item]['count']
          embed = discord.Embed(
            title=f"{name} ({count} owned)", 
            description=f"> {description}\n\n<:GUI:953128943974776913> ID `{id}`\n**Buy** - 🌾`{price}`",
            color = 0xF7D600
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
          embed.set_thumbnail(url=image)
          await zero_fix()
          await ctx.reply(embed=embed)
      else:
        unknown=discord.Embed(
          title = "WHICH ONE?",
          description = "We Don't Think That Effect Is In Our List, Sorry.",
          color = 0x5BB5BA
        )
        await zero_fix()
        await ctx.reply(embed=unknown)

  @effect.command(name="buy")
  @commands.cooldown(1, 5, commands.BucketType.user)
  async def effect_buy(self, ctx, count, *, item):
    with open("save.json", "r") as f:
      users = json.load(f)
    if str(ctx.author.id) not in users:
      await new_user(ctx.author)
      await ctx.reply("Not Enough Manna")
    else:
      if count != None:
        with open("effect_shop.json", "r") as f:
          shop = json.load(f)
        item = item.upper()
        if int(count)<0:
            await ctx.reply("Amount Must Be A Positive Number!")
        else:
          if int(count) == 0:
              await ctx.reply("Ammount Cannot Be 0")
          else:
            if item in shop.keys():
                print(shop[item]['price'])
                with open("save.json", "r") as f:
                  users = json.load(f)
                user = ctx.author
                if users[str(user.id)]['manna'] < shop[item.upper()]['price'] * int(count):
                  await ctx.reply("Not Enough Manna")
                else:
                  with open("save.json", "r") as f:
                    users = json.load(f)
                  if item in users[str(user.id)]['effects']:
                    users[str(user.id)]['effects'][item]['count'] += int(count)
                    users[str(user.id)]['manna'] -= shop[item]['price'] * int(count)
                    with open("save.json", "w") as f:
                      json.dump(users, f, indent=4, sort_keys=True)
                    jollibee = discord.Embed(
                      title = "TRADE SUCCESSFUL",
                      description = f"`{count}` **{shop[item]['name']}** \n*Sucessfully Bought For* `{shop[item]['price'] * int(count)}`🌾!",
                      color = 0xF7D600
                    )
                    await ctx.reply(embed=jollibee)
                  else:
                    users[str(user.id)]['effects'][item] = {}
                    users[str(user.id)]['effects'][item]['count'] = 0
                    users[str(user.id)]['effects'][item]['count'] += int(count)
                    users[str(user.id)]['manna'] -= shop[item]['price'] * int(count)
                    with open("save.json", "w") as f:
                      json.dump(users, f, indent=4, sort_keys=True)
                    jollibee = discord.Embed(
                      title = "TRADE SUCCESSFUL",
                      description = f"`{count}` **{shop[item]['name']}** \n*Sucessfully Bought For* `{shop[item]['price'] * int(count)}`🌾!",
                      color = 0xF7D600
                    )
                    await ctx.reply(embed=jollibee)

            else:
              unknown=discord.Embed(
                title = "WHICH ONE?",
                description = "We Don't Think That Effect Is In Our List, Sorry.",
                color = 0x5BB5BA
              )
              await zero_fix()
              await ctx.reply(embed=unknown)












































  
  @effect.error
  async def effect_error(self, ctx:commands.Context, error):
    await on_cooldown(ctx, error)

  @effect.after_invoke
  async def effect_cooldown(self, ctx):
    await add_command_count(ctx.author)
    for id in owners:
      if id == ctx.author.id:
        ctx.command.reset_cooldown(ctx)
  
  @effect_buy.error
  async def effect_buy_error(self, ctx:commands.Context, error):
    await on_cooldown(ctx, error)

  @effect_buy.after_invoke
  async def effect_buy_cooldown(self, ctx):
    await add_command_count(ctx.author)
    for id in owners:
      if id == ctx.author.id:
        ctx.command.reset_cooldown(ctx)

  @effect_shop.error
  async def effect_shop_error(self, ctx:commands.Context, error):
    await on_cooldown(ctx, error)
  
  @effect_shop.after_invoke
  async def effect_shop_cooldown(self, ctx):
    await add_command_count(ctx.author)
    for id in owners:
      if id == ctx.author.id:
        ctx.command.reset_cooldown(ctx)

def setup(bot):
  bot.add_cog(effect(bot))