import json, datetime, random, nextcord
from nextcord.ext import commands

l = [
    ("0", ":zero:"),
    ("1", ":one:"),
    ("2", ":two:"),
    ("3", ":three:"),
    ("4", ":four:"),
    ("5", ":five:"),
    ("6", ":six:"),
    ("7", ":seven:"),
    ("8", ":eight:"),
    ("9", ":nine:"),
]


class profile(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def embed_builder(
        self, 
        ctx,
        member
    ):
        users = json.load(open("save.json", "r"))
        config = json.load(open("database/config.json", "r"))
        profiles = json.load(open("assets/profiles.heroes", "r"))
        
        if str(member.id) in users:
            manna = users[str(member.id)]['manna']
            xp = users[str(member.id)]['points']
            streak = users[str(member.id)]['streak']
            for int, emoji in l:
                level = str(users[str(member.id)]['level']).replace(int, emoji)
            correct_answers = users[str(member.id)]['correct_answers']
            badge_icons = []
            if users[str(member.id)]['badges']:
                for i in users[str(member.id)]['badges']:
                    badge_icons.append(config['badges'][i]['icon'])
            badges = "".join(badge_icons)
            
        else:
            manna = "None"
            xp = "None"
            streak = "None"
            level = "None"
            correct_answers = "None"
            badges = ""
        
        embed=nextcord.Embed(color=0xDE52B2)
        if member.avatar != None:
            if str(member.id) in profiles:
                if profiles[str(member.id)]['selected'] == None:
                    avatar_url = random.choice(profiles[str(member.id)]["avatar_url"])
                else:
                    avatar_url = profiles[str(member.id)]['avatar_url'][profiles[str(member.id)]['selected']]
            avatar_url = member.avatar.url
        elif member.avatar == None:
            if str(member.id) in profiles:
                if profiles[str(member.id)]['selected'] == None:
                    avatar_url = random.choice(profiles[str(member.id)]["avatar_url"])
                else:
                    avatar_url = profiles[str(member.id)]['avatar_url'][profiles[str(member.id)]['selected']]
            avatar_url = "https://i.imgur.com/YvDEKHf.png"
        embed.set_thumbnail(avatar_url)
        embed.set_author(
            name=member,
            icon_url=avatar_url,
            url=f"https://discordapp.com/users/{member.id}"
        )
        if badges != "":
            embed.add_field(name="Badges:", value=badges)
        embed.add_field(name="Level:", value=f"`{level}`", inline=True)
        embed.add_field(name="Experience:", value=f"🔹`{xp}`", inline=True)
        embed.add_field(name="Manna:", value=f"🌾`{manna}`", inline=True)
        embed.add_field(name="Streak:", value=f"✅`{streak}`", inline=True)
        embed.add_field(name="Correct Answers:",
                         value=f"✅`{correct_answers}`",
                         inline=True)
        embed.add_field(name="Commands Ran",
                         value=f"🖥️`{await self.bot.get_commands_ran(member)}`",
                         inline=True)
        embed.timestamp = datetime.datetime.utcnow()
        
        
        return embed
    
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.command(name="profile", aliases=['p', 'xp'])
    async def profile(self,
                      ctx: commands.Context,
                      member: nextcord.Member = None):
        await self.bot.level_fix()
        await self.bot.zero_fix()
        await self.bot.random_fact(ctx)
        if not member:
            member = ctx.author

        await self.bot.update_name(member)
        await ctx.reply(embed=await self.embed_builder(ctx=ctx, member=member))

        # if str(member.id) in users:
        #     manna = users[str(member.id)]['manna']
        #     xp = users[str(member.id)]['points']
        #     streak = users[str(member.id)]['streak']
        #     level = users[str(member.id)]['level']
        #     correct_answers = users[str(member.id)]['correct_answers']
        # else:
        #     manna = "None"
        #     xp = "None"
        #     streak = "None"
        #     level = "None"
        #     correct_answers = "None"

        # with open("save.json", "r") as f:
        #     users = json.load(f)
        #     with open("save.json", "r") as f:
        #         users = json.load(f)
        #     for int, emoji in l:
        #         level = str(level).replace(int, emoji)
        #     #Profile Embed
        #     jomama = nextcord.Embed(color=0xDE52B2)
        #     avatar_url = member.avatar.url
        #     if member.avatar != None:
        #         jomama.set_thumbnail(url=member.avatar.url)
        #     with open("assets/profiles.heroes", "r") as f:
        #         profiles = json.load(f)
        #     if str(member.id) in profiles:
        #         if profiles[str(member.id)]['selected'] == None:
        #             avatar_url = random.choice(profiles[str(
        #                 member.id)]["avatar_url"])
        #             jomama.set_thumbnail(url=avatar_url)
        #         else:
        #             selected = profiles[str(member.id)]['selected']
        #             avatar_url = profiles[str(
        #                 member.id)]['avatar_url'][selected]
        #             jomama.set_thumbnail(url=avatar_url)
        #     jomama.add_field(name="Level:", value=f"**{level}**", inline=True)
        #     jomama.add_field(name="Experience:", value=f"🔹`{xp}`", inline=True)
        #     jomama.add_field(name="Manna:", value=f"🌾`{manna}`", inline=True)
        #     jomama.add_field(name="Streak:", value=f"✅`{streak}`", inline=True)
        #     jomama.add_field(name="Correct Answers:",
        #                      value=f"✅`{correct_answers}`",
        #                      inline=True)
        #     jomama.add_field(name="Commands Ran",
        #                      value=f"🖥️`{await self.bot.get_commands_ran(member)}`",
        #                      inline=True)
        #     jomama.timestamp = datetime.datetime.utcnow()
        #     if member.avatar != None:
        #         jomama.set_author(
        #             name=f"{member}",
        #             icon_url=avatar_url,
        #             url=f"https://discordapp.com/users/{member.id}")
        #     else:
        #         jomama.set_author(
        #             name=f"{member}",
        #             url=f"https://discordapp.com/users/{member.id}")
        #     await ctx.reply(embed=jomama)

    @profile.after_invoke
    async def reset_cooldown(self, ctx):
        await self.bot.random_fact(ctx)
        await self.bot.add_command_count(ctx.author)
        await self.bot.update_name(ctx.author)
        for id in list(self.bot.owner_ids):
            if id == ctx.author.id:
                ctx.command.reset_cooldown(ctx)

    @profile.error
    async def profile_error(self, ctx: commands.Context, error):
        await self.bot.on_cooldown(ctx, error)
        if isinstance(error, commands.MemberNotFound):
            await self.bot.random_fact(ctx)
            embed = nextcord.Embed(
                title="WHO AGAIN?",
                description=f"Unknown User.\nI've Never Met This Man My Entire Life.",
                color=0xb0c1e0)
            embed.set_thumbnail(url="https://i.imgur.com/3QiQAfL.png")
            await ctx.reply(embed=embed, delete_after=7)
        else:
          print(error)


def setup(bot):
    bot.add_cog(profile(bot))
