import nextcord, json
from nextcord.ext import commands

class admin_cog(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_command(self, ctx:commands.Context):
        global_chat = json.load(open("global_chat.json", "r"))
        if str(ctx.guild.id) in global_chat.keys():
            if global_chat[str(ctx.guild.id)] == ctx.channel.id:
                print(True)
                return
            else:
                pass

def setup(bot):
    bot.add_cog(admin_cog(bot))