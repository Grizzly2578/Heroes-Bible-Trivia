import json, os
from nextcord.ext import commands



with open("save.json", "r") as f:
  users = json.load(f)



class test(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command(
    name="test"
  )
  @commands.is_owner()
  async def test(self, ctx:commands.Context):
    pass


def setup(bot):
  bot.add_cog(test(bot))