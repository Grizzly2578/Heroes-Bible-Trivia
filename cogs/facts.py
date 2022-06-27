import json
import random

from config import discord, add_command_count, owners, on_cooldown
from nextcord.ext import commands

from nextcord import SlashOption, Interaction, slash_command

class facts(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="fact", aliases=['facts'])
  @commands.cooldown(1, 3, commands.BucketType.user)
  async def fact(self, ctx:commands.Context):
    with open("facts.json", "r") as f:
      fax = json.load(f)
    randomnum = random.randint(1, len(fax))

    
    fact = fax[randomnum - 1]

    embed = discord.Embed(
      title="Fact!",
      description=f"{fact}"
    )

    await ctx.reply(embed=embed)
  
  @fact.after_invoke
  async def fact_invoke(self, ctx):
    await add_command_count(ctx.author)
    for id in owners:
      if id == ctx.author.id:
        ctx.command.reset_cooldown(ctx)

  @fact.error
  async def fact_error(self, ctx:commands.Context, error):
    await on_cooldown(ctx, error)




  
  @slash_command(
    name="add_fact",
    description="Add's a fact to the facts list",
    guild_ids=[944155967011041340]
  )
  async def add_fact(self, interaction:Interaction,
                    fact_input: str = SlashOption(
                            name="fact",
                            description="The Fact You want to add",
                            required=True
                          )):
    with open("facts.json", "r") as f:
      fax = json.load(f)
      fax.append(fact_input)
    with open("facts.json", "w") as f:
      json.dump(fax, f, indent=4)
    await interaction.response.send_message(content=f"sucessfully added\n{fact_input}")


def setup(bot):
  bot.add_cog(facts(bot))