import json
import nextcord
from nextcord.ext import commands

class leaderboard_cog(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    def generate_leaderboard(self, type):
        users = json.load(open("save.json", "r"))
        lb = sorted(users, key=lambda k: -users[k][type])
        place = 0
        raw_leaderbord = []
        for k in lb[:10]:
            place += 1
            name = users[k]['name']
            ammount = users[k][type]
            raw_leaderbord.append((place, users[k][type], users[k]['name']))
        formatted_leaderboard = []
        for place, ammount, name in raw_leaderbord:
            formatted_leaderboard.append(f"{place} `{ammount}`-{name}")
        return "\n".join(formatted_leaderboard)

    @commands.group(
        name="top",
        description="A command that show you the players that are on top of their league",
        invoke_without_command=True
    )
    async def top(self, ctx:commands.Context):
        await ctx.reply(
            f"The top command, commands: \n{self.bot.get_msg_prefix(self.bot, ctx)}top manna\n{self.bot.get_msg_prefix(self.bot, ctx)}top xp"
        )

    
    @top.command(
        name="manna",
        aliases=["m"]
    )
    async def top_manna(self, ctx:commands.Context):
        embed = nextcord.Embed()
        embed.add_field(name=f"Top 10 Manna Leaderboard",value=self.generate_leaderboard(type="manna"), inline=True)
        await ctx.reply(embed=embed, mention_author=False)

    @top.command(
        name="experience",
        aliases=["xp", "exp"]
    )
    async def top_xp(self, ctx:commands.Context):
        embed = nextcord.Embed()
        embed.add_field(name=f"Top 10 Experience Leaderboard",value=self.generate_leaderboard(type="points"), inline=True)
        await ctx.reply(embed=embed, mention_author=False)

    @top.command(
        name="correctanswers",
        aliases=["correct", "answers"]
    )
    async def top_correct_answers(self, ctx:commands.Context):
        embed = nextcord.Embed()
        embed.add_field(name=f"Top 10 Correct Answers Leaderboard",value=self.generate_leaderboard(type="correct_answers"), inline=True)
        await ctx.reply(embed=embed, mention_author=False)

    @top.command(
        name="streaks",
        aliases=["streak", "combo"]
    )
    async def streak(self, ctx:commands.Context):
        embed = nextcord.Embed()
        embed.add_field(name=f"Top 10 Answer Streak Leaderboard",value=self.generate_leaderboard(type="streak"), inline=True)
        await ctx.reply(embed=embed, mention_author=False)

def setup(bot):
    bot.add_cog(leaderboard_cog(bot))