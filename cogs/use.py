import json
import random
import nextcord
from nextcord.ext import commands

no_item = nextcord.Embed(title="What Item?",
                        description="You Didn't Provide An Item",
                        color=0x6CBA74)

no_item1 = nextcord.Embed(title="Which Item?",
                         description="You Don't Have This Item",
                         color=0x6CBA74)

unknown_item = nextcord.Embed(title="Where's The Item?",
                             description="We Can't Find That Item",
                             color=0x6CBA74)

unsusable_item = nextcord.Embed(title="How Do You Do It Again?",
                               description="The Item You Provided Is Unusable",
                               color=0x6CBA74)

zero_ammount = nextcord.Embed(
    title="How Many What?",
    description="The Item Number Shouldn't Be Zero or Negative",
    color=0x6CBA74)

with open("save.json", "r") as f:
    users = json.load(f)

with open("effect_shop.json", "r") as f1:
    effects = json.load(f1)

with open("shop.json", "r") as f2:
    shop = json.load(f2)


async def use_mycrate(ctx, user, count):
    with open("save.json", "r") as f:
        users = json.load(f)
    if "SATCHEL" not in users[str(user.id)]['bag']:
        embed = nextcord.Embed(
            title="OH I DROPPED IT",
            description="You Can't Buy This Item Without A Satchel",
            color=0xF7D600)
        await ctx.reply(embed=embed)
        return
    random_manna = random.randint(750, 1000) * int(count)
    effect = random.choices(list(effects.keys()), k=3 * int(count))
    with open("save.json", "r") as f:
        users = json.load(f)
    users[str(user.id)]['bag']['MYCRATE']['count'] -= int(count)
    users[str(user.id)]['manna'] += random_manna
    if 'MYCRATE' not in users['983916041384112168']['bag']:
        users['983916041384112168']['bag']['MYCRATE'] = {}
        users['983916041384112168']['bag']['MYCRATE']['count'] = int(count)
    else:
        users['983916041384112168']['bag']['MYCRATE']['count'] += int(count)

    for effects1 in effect:
        if effects1 in users[str(user.id)]['effects']:
            users[str(user.id)]['effects'][effects1]['count'] += int(count)
        else:
            users[str(user.id)]['effects'][effects1] = {}
            users[str(user.id)]['effects'][effects1]['count'] = int(count)
    with open("save.json", "w") as f:
        json.dump(users, f, indent=4, sort_keys=True)

    #Embed For Mystery Crate Use
    embed = nextcord.Embed(title=f"You Used `{count}` **Mystery Crate**!",
                          description=f"You Received 🌾{random_manna}",
                          color=0xFFD500)
    one_out_of_1k = random.randint(1, 100)
    if one_out_of_1k == 7:
        dev_items = ['DONUT', 'CHICKEN', 'BREAD']
        item = random.choice(dev_items)
        if item not in users[str(user.id)]['bag']:
            users[str(user.id)]['bag'][item] = {}
            users[str(user.id)]['bag'][item]['count'] = 1
            embed.add_field(
                name=
                f"{int(count)}`{shop[item]['icon']}** - {shop[item]['name']}**",
                value=f"*{shop[item]['description']}*",
                inline=False)
    for effects2 in effect:
        embed.add_field(
            name=
            f"`{int(count)}`{effects[effects2]['icon']}** - {effects[effects2]['name']}**",
            value=f"*{effects[effects2]['description']}*",
            inline=False)
    await self.bot.zero_item_fix()
    await ctx.reply(embed=embed)


async def use_donut(ctx, user, count):
    random_xp = random.randint(2500, 5000)
    users[str(user.id)]['points'] += random_xp
    users[str(user.id)]['bag']['DONUT']['count'] -= int(count)

    #Embed For Donut Use
    embed = nextcord.Embed(title=f"You used {count} Donut!",
                          description=f"You Received 🔹`{random_xp}`")
    if 'DONUT' not in users['983916041384112168']['bag']:
        users['983916041384112168']['bag']['DONUT'] = {}
        users['983916041384112168']['bag']['DONUT']['count'] = int(count)
    else:
        users['983916041384112168']['bag']['DONUT']['count'] += int(count)
    with open("save.json", "w") as f:
        json.dump(users, f, indent=4)
    await ctx.reply(embed=embed)


async def use_bread(ctx, user, count):
    random_xp = random.randint(2500, 5000)
    users[str(user.id)]['points'] += random_xp
    users[str(user.id)]['bag']['BREAD']['count'] -= int(count)

    #Embed For Bread Use
    embed = nextcord.Embed(title=f"You used {count} Bread!",
                          description=f"You recived 🔹{random_xp}")
    if 'BREAD' not in users['983916041384112168']['bag']:
        users['983916041384112168']['bag']['BREAD'] = {}
        users['983916041384112168']['bag']['BREAD']['count'] = int(count)
    else:
        users['983916041384112168']['bag']['BREAD']['count'] += int(count)
    with open("save.json", "w") as f:
        json.dump(users, f, indent=4)
    await ctx.reply(embed=embed)


async def use_chicken(ctx, user, count):
    random_xp = random.randint(2500, 5000)
    users[str(user.id)]['points'] += random_xp
    users[str(user.id)]['bag']['CHICKEN']['count'] -= int(count)

    #Embed For Bread Use
    embed = nextcord.Embed(title=f"You used {count} Chicken!",
                          description=f"You recived 🔹{random_xp}")
    if 'CHICKEN' not in users['983916041384112168']['bag']:
        users['983916041384112168']['bag']['CHICKEN'] = {}
        users['983916041384112168']['bag']['CHICKEN']['count'] = int(count)
    else:
        users['983916041384112168']['bag']['CHICKEN']['count'] += int(count)
    with open("save.json", "w") as f:
        json.dump(users, f, indent=4)
    await ctx.reply(embed=embed)


async def use_item(ctx, user, count, item):
    item = item.upper()
    if item == "MYCRATE":
        await use_mycrate(ctx, user, count)
        return
    if item == "DONUT":
        await use_donut(ctx, user, count)
        return
    if item == "BREAD":
        await use_bread(ctx, user, count)
        return
    if item == "CHICKEN":
        await use_chicken(ctx, user, count)
        return
    else:
        await ctx.reply(embed=unsusable_item)


class use(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="use")
    async def use(self, ctx, item=None, count=None):
        with open("save.json", "r") as f:
            users = json.load(f)
        user = ctx.author
        if count == None:
            count = 1
        if int(count) < 1:
            await ctx.reply(embed=zero_ammount)
        else:
            if item == None:
                await ctx.reply(embed=no_item)
            else:
                item = item.upper()
                with open("shop.json", "r") as f:
                    shop = json.load(f)
                if item not in shop.keys():
                    await ctx.reply(embed=unknown_item)
                else:
                    with open("save.json", "r") as f:
                        users = json.load(f)
                    if item not in users[str(user.id)]['bag']:
                        await self.bot.new_user(user)
                        await ctx.reply(embed=no_item1)
                    else:
                        await use_item(ctx, user, count, item)

    @use.error
    async def use_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = nextcord.Embed(title="Invalid Usage!", color=0xED4245)
            embed.add_field(
                name="Syntax:",
                value=
                f"<:GUI:953128943974776913> `{self.bot.get_msg_prefix(self.bot, ctx)}use` `item` `ammount`",
                inline=False)
            embed.add_field(
                name="Examples:",
                value=
                f"`{self.bot.get_msg_prefix(self.bot, ctx)}use donut 1`\n<:GUI:953128943974776913> One of your donut will be used.",
                inline=False)
            await ctx.reply(embed=embed)


def setup(bot):
    bot.add_cog(use(bot))
