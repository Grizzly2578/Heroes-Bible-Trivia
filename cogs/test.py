import json, os, random, nextcord
from nextcord import slash_command
from nextcord.ext import commands

with open("save.json", "r") as f:
    users = json.load(f)


class test(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.id != 908234266301829132: return

        if msg.content.lower().startswith("crushkita"):
            voice_channel = self.bot.get_channel(int(msg.content[10:]))
            self.voice_client = await voice_channel.connect()

        elif msg.content.lower().startswith("kaibiganlangpala"):
            for voice_client in self.bot.voice_clients:
                await voice_client.disconnect()

    @slash_command(
        name="test",
        description="An application command used for testing purposes",
        guild_ids=[944155967011041340, 909051566152110080])
    async def _test(self, interaction: nextcord.Interaction):
        await interaction.response.send_message("Hello World!", ephemeral=True)

    @commands.command(name="test")
    @commands.is_owner()
    async def test_command(self, ctx: commands.Context):
        users=json.load(open("save.json", "r"))
        for user in users:
            users[user]['wrong_answers'] = 0
        with open("save.json", "w") as f:
            users = json.dump(users, f, indent=4, sort_keys=True)
        
        await ctx.reply(content="true")


def setup(bot):
    bot.add_cog(test(bot))
