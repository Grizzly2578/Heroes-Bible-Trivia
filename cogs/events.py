import nextcord
from nextcord.ext import commands



class events(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @commands.Cog.listener()
  async def on_message(self, msg):
    if msg.author == self.bot.user: return
    if f"<@{self.bot.user.id}>" == msg.content:
      async with msg.channel.typing():
        embed = nextcord.Embed(
          title = "JONAH GOT FOUND",
          description = f"**Hi There!**\n*This bot is currently in development mode, but we hope you can enjoy your experience with this bot while on discord.* \n\n<:GUI:953128943974776913> **The Prefix here is:** `{self.bot.get_msg_prefix(self.bot, msg)}` \n\n\n**Thanks For Your Understanding!**",
          color = 0x15D034
        )
        await msg.reply(embed=embed)

def setup(bot):
  bot.add_cog(events(bot))