import nextcord
import json
import os

# from replit import db
from nextcord.ext import commands
from nextcord import Interaction, slash_command, SlashOption
from aiohttp import ClientSession

guild_ids = [
  944155967011041340,
  909051566152110080
]
shop = json.load(open("shop.json", "r"))
config = json.load(open("database/config.json", "r"))

class slash(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @slash_command(
    name="ban_item_from_give_command",
    description="Bans an item from the give command",
    guild_ids=guild_ids
  )
  async def ban_item_from_give_command(
    self,
    interaction:Interaction,
    item: str = SlashOption(
      name="item",
      description="The item you want to ban",
      choices=shop.keys(),
      required=True
    )
  ):
    config["ungivable_items"][item.lower()] = "banned from give command"
    with open("database/config.json", "w") as f:
      json.dump(config, f, indent=4)
    await interaction.response.send_message(
      content=f"{item} has been banned from the give command"
    )


  
  @slash_command(
    name="unban_item_from_give_command",
    description="Bans an item from the give command",
    guild_ids=guild_ids
  )
  async def unban_item_from_give_command(
    self,
    interaction:Interaction,
    item: str = SlashOption(
      name="item",
      description="The item you want to unban",
      choices=config["ungivable_items"].keys(),
      required=True
    )
  ):
    config["ungivable_items"].pop(item)
    
    with open("database/config.json", "w") as f:
      json.dump(config, f, indent=4)
    await interaction.response.send_message(
      content=f"{item} has been unbanned from the give command"
    )



  
  # @slash_command(
  #   name="global_chat",
  #   description="A Command To Setup The Global Chat Channel."
  # )
  # async def global_chat(
  #   self, 
  #   interaction:Interaction,
  #   channel: nextcord.abc.GuildChannel = SlashOption(
  #     channel_types=[nextcord.ChannelType.text],
  #     description="The Text Channel You Want The Messages To Be Sent.",
  #     required=True
  #   )
  # ):
  #   if not interaction.user.guild_permissions.manage_messages:
  #     if interaction.user.id not in list(self.bot.owner_ids):
  #       await interaction.response.send_message(content="You do not have permissions to use this command", ephemeral=True)
  #     else:
  #       if str(interaction.guild.id) in db["webhooks"]:
  #           await interaction.response.send_message(
  #             content="This server already have a global channel", 
  #             ephemeral=True
  #           )
  #       else:
  #           with open("global_chat.json", "r") as f:
  #             global_chat = json.load(f)
  #             global_chat[str(interaction.guild.id)] = channel.id
  #             with open("global_chat.json", "w") as f:
  #               json.dump(global_chat, f, indent=4)  
  #           webhook = await channel.create_webhook(
  #             name="Heroes Bible Trivia"
  #           )
  #           db["webhooks"][str(interaction.guild.id)] = {}
  #           db["webhooks"][str(interaction.guild.id)]['webhook'] = {}
  #           db["webhooks"][str(interaction.guild.id)]['webhook']['channel_id'] = interaction.channel.id
  #           db["webhooks"][str(interaction.guild.id)]['webhook']['url'] = webhook.url
  #           await interaction.response.send_message(
  #               content=f"Sucessfully Registered {channel.mention} to global chat\nUse /remove_global_chat to unregister you text channel as a global chat", 
  #               ephemeral=True
  #           )
  #   else:
  #     if str(interaction.guild.id) in db["webhooks"]:
  #       await interaction.response.send_message(
  #         content="This server already have a global channel", 
  #         ephemeral=True
  #       )
  #     else:
        
  #       with open("global_chat.json", "r") as f:
  #         global_chat = json.load(f)
  #         global_chat[str(interaction.guild.id)] = channel.id
  #         with open("global_chat.json", "w") as f:
  #           json.dump(global_chat, f, indent=4)
          
  #       webhook = await channel.create_webhook(
  #         name="Heroes Bible Trivia"
  #       )
  #       db["webhooks"][str(interaction.guild.id)] = {}
  #       db["webhooks"][str(interaction.guild.id)]['webhook'] = {}
  #       db["webhooks"][str(interaction.guild.id)]['webhook']['channel_id'] = interaction.channel.id
  #       db["webhooks"][str(interaction.guild.id)]['webhook']['url'] = webhook.url
  #       await interaction.response.send_message(
  #           content=f"Sucessfully Registered {channel.mention} to global chat\nUse /remove_global_chat to unregister you text channel as a global chat", 
  #           ephemeral=True
  #       )

  # @global_chat.error
  # async def global_chat_error(self, interaction: Interaction, error):
  #   if isinstance(error, commands.CommandInvokeError):
  #     await interaction.response.send_message(
  #       content="Error: I am missing the `Manage Webhooks` Permission\nThis command will not work"
  #     )
  
  # @slash_command(
  #   name="remove_global_chat",
  #   description="A Command To Remove The Global Chat Channel."
  # )
  # async def remove_global_chat(self, interaction:Interaction):
  #   with open("global_chat.json", "r") as f:
  #     global_chat = json.load(f)
  #   if not interaction.user.guild_permissions.manage_messages:
  #     if interaction.user.id not in list(self.bot.owner_ids):
  #       await interaction.response.send_message(content="You do not have permissions to use this command", ephemeral=True)
  #     else:
  #       if str(interaction.guild.id) not in global_chat:
  #         await interaction.response.send_message(
  #           content="This server doesnt have a global channel to unregister", 
  #           ephemeral=True
  #         )
  #       else:
  #         async with ClientSession() as session:
  #           hook = nextcord.Webhook.from_url(db['webhooks'][str(interaction.guild.id)]['webhook']['url'], session=session, bot_token=token)
  #           del db['webhooks'][str(interaction.guild.id)]
  #           guild_id = str(interaction.guild.id)
  #           with open("global_chat.json", "r") as f:
  #             global_chat = json.load(f)
    
  #           global_chat.pop(guild_id)
    
  #           with open("global_chat.json", "w") as f:
  #             json.dump(global_chat, f, indent=4)
  #           await hook.delete()
  #           await interaction.response.send_message(
  #             content="Sucessfully Removed The Global Chat!",
  #             ephemeral=True
  #           )
  #   else:
  #     if str(interaction.guild.id) not in global_chat:
  #       await interaction.response.send_message(
  #         content="This server doesnt have a global channel to unregister", 
  #         ephemeral=True
  #       )
  #     else:
  #       async with ClientSession() as session:
  #         hook = nextcord.Webhook.from_url(db['webhooks'][str(interaction.guild.id)]['webhook']['url'], session=session, bot_token=token)
  #         del db['webhooks'][str(interaction.guild.id)]
  #         guild_id = str(interaction.guild.id)
  #         with open("global_chat.json", "r") as f:
  #           global_chat = json.load(f)
  
  #         global_chat.pop(guild_id)
  
  #         with open("global_chat.json", "w") as f:
  #           json.dump(global_chat, f, indent=4)
  #         await hook.delete()
  #         await interaction.response.send_message(
  #           content="Sucessfully Removed The Global Chat!",
  #           ephemeral=True
  #         )
  

  # @remove_global_chat.error
  # async def remove_global_chat_error(self, interaction: Interaction, error):
  #   if isinstance(error, commands.CommandInvokeError):
  #     await interaction.response.send_message(
  #       content="Error: I am missing the `Manage Webhooks` Permission\nThis command will not work"
  #     )

def setup(bot):
  bot.add_cog(slash(bot))