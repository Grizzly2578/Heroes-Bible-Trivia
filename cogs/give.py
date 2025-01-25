import json
import nextcord

from nextcord.ui import button
from nextcord import Interaction
from nextcord import ButtonStyle
from nextcord.ext import commands
from nextcord.ui import View

config = json.load(open("database/config.json", "r"))
shop = json.load(open("shop.json", "r"))
users = json.load(open("save.json", "r"))
class give_view(View):
  def __init__(self):
    super().__init__()

  async def on_timeout(self):
    self.confirm.disabled = True
    self.cancel.disanled = True
    await self.message.edit(view=self)
  
  @button(
    label="Confirm"
  )
  async def confirm(self, button:button, interaction:Interaction):
    user = self.reciever
    item = self.item
    count = self.count
    with open("save.json", "r") as f:
      users = json.load(f)
    if interaction.user.id != self.ctx.author.id:
      await interaction.response.send_message("This Button is not for you.", ephemeral=True)
    else:
      if item == "🌾":
        users[str(self.ctx.author.id)]["manna"] -= count
        users[str(self.reciever.id)]["manna"] += count
        with open("save.json", "w") as f:
          users = json.dump(users, f, indent=4, sort_keys=True)
        self.confirm.style = ButtonStyle.green
        self.confirm.disabled = True
        self.cancel.disabled = True
        embed=nextcord.Embed(
          title="Give",
          description=f"Sucessfully gave `{count}` 🌾 to {user.mention}"
        )
        await self.message.edit(
          embed=embed,
          view=self
        )
        return
        
      users[str(self.ctx.author.id)]['bag'][item.upper()]['count'] -= int(count)
      if item.upper() in users[str(user.id)]['bag']:
        users[str(user.id)]['bag'][item.upper()]['count'] += int(count)
        with open("save.json", "w") as f:
          users = json.dump(users, f, indent=4, sort_keys=True)
        embed=nextcord.Embed(
          title="Give",
          description=f"Sucessfully gave {count} {item.upper()} to {user.mention}"
        )
        self.confirm.style = ButtonStyle.green
        self.confirm.disabled = True
        self.cancel.disanled = True
        await self.bot.zero_item_fix()
        await self.message.edit(
          embed=embed,
          view=self
        )
      else:
        users[str(user.id)]['bag'][item.upper()] = {}
        users[str(user.id)]['bag'][item.upper()]['count'] = int(count)
        with open("save.json", "w") as f:
          users = json.dump(users, f, indent=4, sort_keys=True)
        embed=nextcord.Embed(
          title="Give",
          description=f"Sucessfully gave `{count}` {item} to {user.mention}"
        )
        self.confirm.style = ButtonStyle.green
        self.confirm.disabled = True
        self.cancel.disanled = True
        await self.bot.zero_item_fix()
        await self.message.edit(
          embed=embed,
          view=self
        )

  @button(
    label="Cancel"
  )
  async def cancel(self, button:button, interaction:Interaction):
    if interaction.user.id != self.ctx.author.id:
      await interaction.response.send_message("This Button is not for you.", ephemeral=True)
    else:
      self.confirm.disabled = True
      self.cancel.disanled = True
      await self.message.edit(view=self)
      await self.message.edit(self)



class give_cog(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="give")
  @commands.is_owner()
  async def give(
    self, ctx:commands.Context, user:nextcord.Member=None, count = 1, item=None
  ):
    self.count = int(count)
    error_embed = nextcord.Embed(
      title="Invalid Usage!",
      color=0xED4245
    )
    error_embed.add_field(
      name="Syntax:",
      value=f"<:GUI:953128943974776913> `{self.bot.get_msg_prefix(self.bot, ctx)}give` `user` `quantity` `item`",
      inline=False
    )
    error_embed.add_field(
      name="User Examples:",
      value=f"<:gui_1:1022056763371048981> 829619198544183327\n<:GUI:953128943974776913> <@{self.bot.user.id}>",
      inline=False
    )
    error_embed.add_field(
      name="Examples:",
      value=f"<:gui_1:1022056763371048981> `+give {self.bot.user.name} 1 donut`\n<:GUI:953128943974776913> Your donut will be given to <@{self.bot.user.id}>",
      inline=False
    )
    if not user:
      self.error = "No User Specified."
      error_embed.add_field(
        name="Error:",
        value=f"<:GUI:953128943974776913> `{self.error}`",
        inline=False
      )
      await ctx.send(embed=error_embed)
      return

    if user.id == ctx.author.id:
      self.error = "You cannot give yourself items."
      error_embed.add_field(
        name="Error:",
        value=f"<:GUI:953128943974776913> `{self.error}`",
        inline=False
      )
      await ctx.send(embed=error_embed)
      return

    if count < 1:
      self.error = "Quantity must not be zero or negative."
      error_embed.add_field(
        name="Error:",
        value=f"<:GUI:953128943974776913> `{self.error}`",
        inline=False
      )
      await ctx.send(embed=error_embed)
      return
    
    if item:
      if item.lower() in config["ungivable_items"].keys():
        self.error = "You cannot give this item."
        error_embed.add_field(
          name="Error:",
          value=f"<:GUI:953128943974776913> `{self.error}`",
          inline=False
        )
        await ctx.send(embed=error_embed)
        return
      elif item.upper() in shop.keys():
        item = item.upper()
        self.item = item
        self.item_description = shop[item]["description"]
        self.item_icon = shop[item]["icon"]
        self.item_id = shop[item]["id"]
        self.item_image = shop[item]["image"]
        self.item_name = shop[item]["name"]
        self.item_price = shop[item]["price"]
        self.item_rarity = shop[item]["rarity"]
        
    if not item:
      item = "🌾"
      if users[str(ctx.author.id)]["manna"] < self.count:
        self.error = "You don't have enough manna to give to this user."
        error_embed.add_field(
          name="Error:",
          value=f"<:GUI:953128943974776913> `{self.error}`",
          inline=False
        )
        await ctx.send(embed=error_embed)
        return
      embed=nextcord.Embed(
        title="Give",
        description=f"You are about to give:\n`{count}` 🌾\nto {user.mention}\n",
        color = 0x2F3136
      )
      embed.set_footer(text="Click the Button to Confirm")
      view = give_view()
      view.bot = self.bot
      view.ctx = ctx
      view.item = item
      view.count = count
      view.timeout = 25
      view.message = await ctx.reply(
        embed=embed,
        view=view
      )
      view.reciever = user
      return


    if str(ctx.author.id) not in users.keys():
      self.error = "You do not have this item."
      error_embed.add_field(
        name="Error:",
        value=f"<:GUI:953128943974776913> `{self.error}`",
        inline=False
      )
      await self.bot.new_user(ctx.author)
      await ctx.send(embed=error_embed)
      return

    if str(user.id) not in users.keys():
      self.error = "They have not used or registered on our bot yet."
      error_embed.add_field(
        name="Error:",
        value=f"<:GUI:953128943974776913> `{self.error}`",
        inline=False
      )
      await ctx.send(embed=error_embed)
      return

    if self.item not in users[str(ctx.author.id)]["bag"]:
      self.error = "You don't have this item."
      error_embed.add_field(
        name="Error:",
        value=f"<:GUI:953128943974776913> `{self.error}`",
        inline=False
      )
      await ctx.send(embed=error_embed)
      return

    if users[str(ctx.author.id)]["bag"][item]["count"] < count:
      self.error = "You don't have that much of this item."
      error_embed.add_field(
        name="Error:",
        value=f"<:GUI:953128943974776913> `{self.error}`",
        inline=False
      )
      await ctx.send(embed=error_embed)
      return
    
    embed=nextcord.Embed(
      title="Give",
      description=f"You are about to give:\n`{count}` | {self.item_icon} **{self.item_name}** \nto {user.mention}\n",
      color = 0x2F3136
    )
    embed.set_footer(text="Click the Button to Confirm")
    embed.set_thumbnail(url=self.item_image)
    view = give_view()
    view.bot = self.bot
    view.ctx = ctx
    view.item = item
    view.count = count
    view.timeout = 25
    view.message = await ctx.reply(
      embed=embed,
      view=view
    )
    view.reciever = user

















  

  @give.error
  async def give_error(self,ctx:commands.Context , error):
    error_embed = nextcord.Embed(
      title="Invalid Usage!",
      color=0xED4245
    )
    error_embed.add_field(
      name="Syntax:",
      value=f"<:GUI:953128943974776913> `{self.bot.get_msg_prefix(self.bot, ctx)}give` `user` `quantity` `item`",
      inline=False
    )
    error_embed.add_field(
      name="User Examples:",
      value=f"<:gui_1:1022056763371048981> 829619198544183327\n<:GUI:953128943974776913> <@{self.bot.user.id}>",
      inline=False
    )
    error_embed.add_field(
      name="Examples:",
      value=f"<:gui_1:1022056763371048981> `+give {self.bot.user.name} 1 donut`\n<:GUI:953128943974776913> Your donut will be given to <@{self.bot.user.id}>",
      inline=False
    )
    if isinstance(error, commands.MemberNotFound):
      self.error = "User not found"
      error_embed.add_field(
        name="Error:",
        value=f"<:GUI:953128943974776913> `{self.error}`",
        inline=False
      )
      await ctx.send(embed=error_embed)
      return
    elif isinstance(error, commands.BadArgument):
      self.error = """Invalid Arguments!

Possible Issues:
  Quantity must be in numbers.
  Quantity must not be negative."""
      error_embed.add_field(
        name="Error:",
        value=f"<:GUI:953128943974776913> `{self.error}`",
        inline=False
      )
      await ctx.send(embed=error_embed)
      return

def setup(bot):
  bot.add_cog(give_cog(bot))