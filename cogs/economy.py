import random
import json

from nextcord.ui import button

from nextcord import Interaction, ButtonStyle, SlashOption, slash_command

from nextcord.ui import Button, View

from nextcord.ext import commands
from config import discord, owners, add_command_count, new_user, on_cooldown, zero_fix, zero_item_fix

  

class bank(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  #Manna Command
  @commands.group(name="manna", aliases=['m'], invoke_without_command=True)
  @commands.cooldown(1, 3, commands.BucketType.user)
  async def manna(self, ctx):
    with open("save.json", "r") as f:
      users = json.load(f)
    elijah = discord.Embed(
      title="YOU GOT THAT MANNA",
      description=f"Just Like Moses And The Israelites Back Then,\nYou Can Also Earn Manna In The Game\n You Have 🌾`{users[str(ctx.author.id)]['manna']}`."
    )
    await ctx.reply(embed=elijah)

  #Harvest Sub-Command
  @manna.command(name="harvest", pass_context=True)
  @commands.cooldown(1, 2400, commands.BucketType.user)
  async def _harvest(self, ctx):
    randomnum = random.randint(150, 500)
    with open("save.json", "r") as f:
      users = json.load(f)
      if str(ctx.author.id) not in users:
        await new_user(ctx.autor)
        users[str(ctx.author.id)]['manna'] += randomnum
        with open("save.json", "w") as f:
          users = json.dump(users, f, indent=4, sort_keys=True)
        moses1=discord.Embed(
          title="WOW, WHAT IS IT?",
          description=f"You Harvested 🌾**{randomnum}** From The Ground",
          color=0xDA37A1
        )
        await ctx.reply(embed=moses1)
      else:
        with open("save.json", "r") as f:
          users = json.load(f)
          users[str(ctx.author.id)]['manna'] += randomnum
          with open("save.json", "w") as f:
            users = json.dump(users, f, indent=4, sort_keys=True)

        moses2=discord.Embed(
          title="WOW, WHAT IS IT?",
          description=f"You Harvested 🌾**{randomnum}** From The Ground",
          color=0xDA37A1
        )
        await zero_fix()
        await ctx.reply(embed=moses2)
    
  @commands.command(name="inventory", aliases=["inv"])
  @commands.cooldown(1, 3, commands.BucketType.user)
  async def inv(self, ctx, user: discord.Member = None):
    await zero_item_fix()
    with open("save.json", "r") as f:
      users = json.load(f)
    with open("shop.json", "r") as f1:
      shop = json.load(f1)
    if user != None:
      if str(user.id) in users:
        embed=discord.Embed(
          title = "THEIR PERSONAL INVENTORY",
          description = "\u200b ",
          color = 0xF78400
        )
        if users[str(user.id)]['bag'] == "":
          return
        else:
          for item in list(users[str(user.id)]['bag'].keys()):
            item_name = shop[item]['name']
            item_count = users[str(user.id)]['bag'][item]['count']
            item_id = shop[item]['id']
            icon = shop[item]['icon']
            if item_count != 0:
              embed.add_field(name=f"`{item_count}` {icon} - {item_name}", value=f"<:GUI:953128943974776913> *ID* `{item_id}`", inline=False)
        await zero_fix()
        await ctx.reply(embed=embed)
      else:
        await zero_fix()
        await ctx.reply("Member Not Found")
    else:
      
      user = ctx.author
      if str(user.id) not in users:
        await new_user(ctx.author)
        embed=discord.Embed(
          title = "YOUR PERSONAL INVENTORY",
          description = "\u200b ",
          color = 0xF78400
        )
        await zero_fix()
        await ctx.reply(embed=embed)
      else:
        embed=discord.Embed(
          title = "YOUR PERSONAL INVENTORY",
          description = "\u200b",
          color = 0xF78400
        )
        if users[str(user.id)]['bag'] == "":
          return
        else:
          for item in list(users[str(user.id)]['bag'].keys()):
            item_name = shop[item]['name']
            item_count = users[str(user.id)]['bag'][item]['count']
            item_id = shop[item]['id']
            icon = shop[item]['icon']
            if item_count != 0:
              embed.add_field(name=f"`{item_count}` {icon} - {item_name}", value=f"<:GUI:953128943974776913> *ID* `{item_id}`", inline=False)
        await zero_fix()
        await ctx.reply(embed=embed)




  
  @commands.command(name="_give")
  @commands.cooldown(1, 3, commands.BucketType.user)
  async def _give(self, ctx:commands.Context, user:discord.Member, count, item=None):
    await zero_item_fix()
    await zero_fix()

    confirm = Button(label="Confirm", style=ButtonStyle.green)

    confirm1 = Button(label="Confirm", style=ButtonStyle.green)
    view = View()
    view.add_item(confirm)

    view1 = View()
    view1.add_item(confirm1)
    
    disabled_confirm = Button(label="Confirm", style=ButtonStyle.green)
    disabled_confirm.disabled = True
    disabled = View()
    disabled.add_item(disabled_confirm)

    
    async def confirm_callback(interaction: Interaction):
      if interaction.user.id != ctx.author.id:
        await interaction.response.send_message("This Button is not for you.", ephemeral=True)
      else:
        with open("save.json", "r") as f:
          users = json.load(f)
        users[str(ctx.author.id)]['bag'][item.upper()]['count'] -= int(count)
        if item.upper() in users[str(user.id)]['bag']:
          users[str(user.id)]['bag'][item.upper()]['count'] += int(count)
          with open("save.json", "w") as f:
            users = json.dump(users, f, indent=4, sort_keys=True)
          embed=discord.Embed(
            title="Give",
            description=f"Sucessfully gave {count} {item.upper()} to {user.mention}"
          )
          await interaction.response.edit_message(embed=embed, view=disabled)
        else:
          users[str(user.id)]['bag'][item.upper()] = {}
          users[str(user.id)]['bag'][item.upper()]['count'] = int(count)
          with open("save.json", "w") as f:
            users = json.dump(users, f, indent=4, sort_keys=True)
          embed=discord.Embed(
            title="Give",
            description=f"Sucessfully gave {count} {item} to {user.mention}"
          )
          await interaction.response.edit_message(embed=embed, view=disabled)
    confirm.callback = confirm_callback
    
    async def confirm1_callback(interaction: Interaction):
      if interaction.user.id != ctx.author.id:
        await interaction.response.send_message("This Button is not for you.", ephemeral=True)
      else:
        with open("save.json", "r") as f:
          users = json.load(f)
        users[str(ctx.author.id)]['manna'] -= int(count)
        users[str(user.id)]['manna'] += int(count)
        with open("save.json", "w") as f:
          users = json.dump(users, f, indent=4, sort_keys=True)
        embed=discord.Embed(
          title="Give",
          description=f"Sucessfully gave {count} to {user.mention}"
        )
        await interaction.response.edit_message(embed=embed, view=disabled)
    confirm1.callback = confirm1_callback

    if item.upper() == "SATCHEL":
      whygive = discord.Embed(
        title = "No"
      )
      await ctx.reply(embed=whygive)
      return
    
    if int(count) < 1:
      await ctx.reply("Ammount cannot be negative or 0.")
    else:
      
      with open("save.json", "r") as f:
        users = json.load(f)
      if str(user.id) in users.keys():
        if str(ctx.author.id) not in users.keys():
          await new_user(ctx.author)
          if item != None:
            with open("shop.json", "r") as f1:
              shop = json.load(f1)
            if item in shop.keys():
              await ctx.reply("You dont have this item")
            else:
              await ctx.reply("Unknown Item")
          else:
            await ctx.reply("Not enough Mana")
        else:
          if item != None:
            item = item.upper()
            with open("shop.json", "r") as f1:
              shop = json.load(f1)
            if item in shop.keys():
              if item in users[str(ctx.author.id)]['bag']:
                embed=discord.Embed(
                  title="Give",
                  description=f"You are about to give {count}, {item} to {user.mention}\n Click the Button to Confirm"
                )
                await ctx.reply(embed=embed, view=view)
              else:
                await ctx.reply("You dont have this item")
            else:
              await ctx.reply("Unknown Item")
          else:
            if users[str(ctx.author.id)]['manna'] < int(count):
              await ctx.reply("Not enough Mana")
            else:
              embed=discord.Embed(
                title="Give",
                description=f"You are about to give {count}, to {user.mention}\n Click the Button to Confirm"
              )
              await ctx.reply(embed=embed, view=view1)
            
              
              
      else:
        await ctx.reply("Unknown User: User is not in our Database")
          
        



  

  
  













  
  



















  

  @manna.after_invoke
  async def mana_cooldown(self, ctx):
    await add_command_count(ctx.author)
    for id in owners:
      if id == ctx.author.id:
        ctx.command.reset_cooldown(ctx)

  @manna.error
  async def manna_error(self, ctx:commands.Context, error):
    await on_cooldown(ctx, error)
    
  @_harvest.after_invoke
  async def _harvest_cooldown(self, ctx):
    await add_command_count(ctx.author)
    for id in owners:
      if id == ctx.author.id:
        ctx.command.reset_cooldown(ctx)

  @_harvest.error
  async def harvest_error(self, ctx:commands.context, error):
    if isinstance(error, commands.CommandOnCooldown):
      mins = error.retry_after / 60
      famine = discord.Embed(
        title = "THERE'S A FAMINE! WAIT!",
        description = f"If Joseph And The Egyptians Can Wait For 7 Years, \nWe Believe You Can Wait For {mins:.1f} Minutes.",
        color = 0xF79400
      )
      await ctx.reply(embed=famine)

  @inv.after_invoke
  async def inv_cooldown(self, ctx):
    await add_command_count(ctx.author)
    for id in owners:
      if id == ctx.author.id:
        ctx.command.reset_cooldown(ctx)

  @inv.error
  async def inv_error(self, ctx:commands.Context, error):
    await on_cooldown(ctx, error)









  



  








  




  
  @slash_command(name="add_item", description="Adds An Item To The Shop", guild_ids=[944155967011041340])
  async def add_item(self, interaction:Interaction,
                    name: str=SlashOption(
                      name="item_name",
                      description="The Name Of The Item You Want To Add",
                      required=True
                    ),
                     id: str=SlashOption(
                      name="item_id",
                      description="The ID Of The Item You Want To Add",
                      required=True
                    ),
                     icon: str=SlashOption(
                      name="icon",
                      description="The Emoji/Icon Of The Item You Want To Add",
                      required=True
                    ),
                     image: str=SlashOption(
                      name="image",
                      description="The Imagen Of The Item You Want To Add MUST be an imgur link",
                      required=True
                    ),
                    description: str=SlashOption(
                      name="description",
                      description="The Description Of The Item You Want To Add",
                      required=True
                    ),
                    rarity: str=SlashOption(
                      name="rarity",
                      description="The Rarity Of The Item You Want To Add",
                      required=True
                    ),
                    price: int=SlashOption(
                      name="price",
                      description="The Price Of The Item You Want To Add"
  )):
    with open("shop.json", "r") as f:
      shop = json.load(f)
    shop[id.upper()] = {}
    shop[id.upper()]['name'] = name.upper()
    shop[id.upper()]['id'] = id.lower()
    shop[id.upper()]['icon'] = icon
    shop[id.upper()]['image'] = image
    shop[id.upper()]['price'] = price
    shop[id.upper()]['description'] = description
    shop[id.upper()]['rarity'] = rarity
    with open("shop.json", "w") as f:
      shop = json.dump(shop, f, indent=4, sort_keys=True)
      sellah = discord.Embed(
        title = "SUCCESSFUL TRADE",
        description = "The Item You Sold Was Added To The Shop Successfully!",
        color = 0xF7AD00
      )
      await interaction.response.send_message(embed=sellah)

def setup(bot):
  bot.add_cog(bank(bot))