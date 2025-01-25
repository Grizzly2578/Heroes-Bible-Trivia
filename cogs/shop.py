import json
import nextcord

from nextcord.ext import commands

unknown_item = nextcord.Embed(title="Where's The Item?",
                             description="We Can't Find That Item",
                             color=0x6CBA74)

no_item = nextcord.Embed(title="What Item?",
                        description="You Didn't Provide An Item",
                        color=0x6CBA74)

zero_ammount = nextcord.Embed(
    title="How Many What?",
    description="The Item Number Shouldn't Be Zero or Negative",
    color=0x6CBA74)

not_enough = nextcord.Embed(
    title="Not Enough Manna",
    description="You don't have enough manna to buy this item",
    color=0x6CBA74)


def jollibee(count, item):
    with open("shop.json", "r") as f:
        shop = json.load(f)
    embed = nextcord.Embed(
        title="TRADE SUCCESSFUL",
        description=
        f"`{count}` **{shop[item]['name']}** *Sucessfully Bought For* 🌾`{shop[item]['price'] * int(count)}`!",
        color=0xF7D600)
    return embed





class shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def buy_mycrate(self, ctx, user, count, item):
        with open("save.json", "r") as f:
            users = json.load(f)
        with open("shop.json", "r") as g:
            shop = json.load(g)
        if "SATCHEL" not in users[str(user.id)]['bag']:
            embed = nextcord.Embed(
                title="OH I DROPPED IT",
                description="You Can't Buy This Item Without A Satchel",
                color=0xF7D600)
            await ctx.reply(embed=embed)
        else:
            item = "MYCRATE"
            if item in users[str(user.id)]['bag']:
                users[str(
                    user.id)]['manna'] -= shop[item]['price'] * int(count)
                users['983916041384112168'][
                    'manna'] += shop[item]['price'] * int(count)
                users[str(user.id)]['bag'][item]['count'] += int(count)
                with open("save.json", "w") as f:
                    json.dump(users, f, indent=4, sort_keys=True)
                await self.bot.zero_fix()
                await ctx.reply(embed=jollibee(count, item))
            else:
                with open("save.json", "r") as f:
                    users = json.load(f)
                users[str(user.id)]['bag'][item] = {}
                users[str(user.id)]['bag'][item]['count'] = 0
                users[str(user.id)]['bag'][item]['count'] += int(count)
                users[str(
                    user.id)]['manna'] -= shop[item]['price'] * int(count)
                users['983916041384112168'][
                    'manna'] += shop[item]['price'] * int(count)
                with open("save.json", "w") as f:
                    users = json.dump(users, f, indent=4, sort_keys=True)
                await self.bot.zero_fix()
                await ctx.reply(embed=jollibee(count, item))

    async def buy_satchel(self, ctx, user, count, item):
        with open("save.json", "r") as f:
            users = json.load(f)
        with open("shop.json", "r") as g:
            shop = json.load(g)
        item = "SATCHEL"
        if item in users[str(user.id)]['bag']:
            nauur = nextcord.Embed(title="WHY THOUGH?",
                                  description="You Already Have A Satchel",
                                  color=0xF7D600)
            await ctx.reply(embed=nauur)
        else:
            if int(count) > 1:
                more1 = nextcord.Embed(
                    title="WHY BUY MORE?",
                    description="You Can Only Have `1` Satchel",
                    color=0xF7D600)
                await ctx.reply(embed=more1)
                count = 1
                pass
            with open("save.json", "r") as f:
                users = json.load(f)
            users[str(user.id)]['bag'][item] = {}
            users[str(user.id)]['bag'][item]['count'] = 0
            users[str(user.id)]['bag'][item]['count'] += int(count)
            users[str(user.id)]['manna'] -= shop[item]['price'] * int(count)
            users['983916041384112168']['manna'] += shop[item]['price'] * int(
                count)
            with open("save.json", "w") as f:
                users = json.dump(users, f, indent=4, sort_keys=True)
            await self.bot.zero_fix()
            await ctx.reply(embed=jollibee(count, item))

    async def buy_item(self, ctx, user, count, item):
        if item == "MYCRATE":
            await self.buy_mycrate(ctx, user, count, item)
            return
        if item == "SATCHEL":
            await self.buy_satchel(ctx, user, count, item)
            return
        else:
            await ctx.reply(embed=unknown_item)

    @commands.group(name="shop", aliases=['item'], invoke_without_command=True)
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def shop(self, ctx: commands.context, *, item=None):
        if item == None:
            with open("save.json", "r") as f2:
                users = json.load(f2)
            if str(ctx.author.id) not in users:
                await self.bot.new_user(ctx.author)
            with open("shop.json", "r") as f:
                shop = json.load(f)
            embed = nextcord.Embed(
                title="WELCOME TO THE SHOP",
                description=
                "In here, you can buy and sell different items such \nas manna packs, effects packs, and so much more.",
                color=0xF7AD00)

            for item in list(shop):
                if shop[item]['price'] == None:
                    pass
                else:
                    name = shop[item]['name']
                    id = shop[item]['id']
                    price = shop[item]['price']
                    description = shop[item]['description']
                    icon = shop[item]['icon']
                    embed.add_field(
                        name=f"{icon} - {name}",
                        value=f"> *ID*`{id}`\n> 🌾`{price}`\n> {description}")
            await self.bot.zero_fix()
            await ctx.reply(embed=embed)
        else:
            with open("shop.json", "r") as f:
                shop = json.load(f)
            with open("save.json", "r") as f1:
                users = json.load(f1)
            item = item.upper()
            if item in shop.keys():
                name = shop[item]['name']
                icon = shop[item]['icon']
                image = shop[item]['image']
                id = shop[item]['id']
                price = shop[item]['price']
                description = shop[item]['description']
                rarity = shop[item]['rarity']
                if price == None:
                    price = "Unable to be bought"
                if item in list(users[str(ctx.author.id)]['bag']):
                    count = users[str(ctx.author.id)]['bag'][item]['count']
                    embed = nextcord.Embed(
                        title=f"{name} ({count} owned)",
                        description=
                        f"> {description}\n\n<:GUI:953128943974776913> ID `{id}`\n**Buy** - 🌾`{price}`",
                        color=0xF7D600)
                    embed.add_field(name="Rarity", value=f"`{rarity}`")
                    embed.set_thumbnail(url=image)
                    await self.bot.zero_fix()
                    await ctx.reply(embed=embed)
                else:
                    count = 0
                    embed = nextcord.Embed(
                        title=f"{name} ({count} owned)",
                        description=
                        f"> {description}\n\n<:GUI:953128943974776913> ID `{id}`\n**Buy** - 🌾`{price}`",
                        color=0xF7D600)
                    embed.add_field(name="Rarity", value=f"`{rarity}`")
                    embed.set_thumbnail(url=image)
                    await self.bot.zero_fix()
                    await ctx.reply(embed=embed)
            else:
                await self.bot.zero_fix()
                await ctx.reply("unknown item")

    async def buy(self, ctx, item=None, count=None):
        with open("save.json", "r") as f:
            users = json.load(f)
        with open("shop.json", "r") as f:
            shop = json.load(f)
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
                    if str(user.id) not in users:
                        await self.bot.new_user(user)
                        pass
                    if users[str(
                            user.id
                    )]['manna'] < shop[item]['price'] * int(count):
                        await ctx.reply(embed=not_enough)
                        return
                    await self.buy_item(ctx, user, count, item)

    @shop.command(name="buy")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def buy_cmd(self, ctx, item=None, count=None):
        await self.buy(ctx=ctx, item=item, count=count)

    @commands.command(name="buy")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def buy1_cmd(self, ctx, item=None, count=None):
        await self.buy(ctx=ctx, item=item, count=count)

    @buy_cmd.error
    async def buy_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = nextcord.Embed(title="Invalid Usage!", color=0xED4245)
            embed.add_field(
                name="Syntax:",
                value=
                f"<:GUI:953128943974776913> `{self.bot.get_msg_prefix(self.bot, ctx)}buy` `item` `ammount`",
                inline=False)
            embed.add_field(
                name="Examples:",
                value=
                f"`{self.bot.get_msg_prefix(self.bot, ctx)}buy donut 1`\n<:GUI:953128943974776913> You will be given a Donut for a certain ammount of Manna.",
                inline=False)
            await ctx.reply(embed=embed)

    @buy1_cmd.error
    async def buy1_error(self, ctx: commands.Context, error):
        if isinstance(error, commands.CommandInvokeError):
            embed = nextcord.Embed(title="Invalid Usage!", color=0xED4245)
            embed.add_field(
                name="Syntax:",
                value=
                f"<:GUI:953128943974776913> `{self.bot.get_msg_prefix(self.bot, ctx)}buy` `item` `ammount`",
                inline=False)
            embed.add_field(
                name="Examples:",
                value=
                f"`{self.bot.get_msg_prefix(self.bot, ctx)}buy donut 1`\n<:GUI:953128943974776913> You will be given a Donut for a certain ammount of Manna.",
                inline=False)
            await ctx.reply(embed=embed)

    @buy_cmd.after_invoke
    async def buy_cooldown(self, ctx):
        await self.bot.add_command_count(ctx.author)
        for id in list(self.bot.owner_ids):
            if id == ctx.author.id:
                ctx.command.reset_cooldown(ctx)

    @buy1_cmd.after_invoke
    async def buy1_cooldown(self, ctx):
        await self.bot.add_command_count(ctx.author)
        for id in list(self.bot.owner_ids):
            if id == ctx.author.id:
                ctx.command.reset_cooldown(ctx)

    @shop.error
    async def shop_error(self, ctx: commands.Context, error):
        await self.bot.on_cooldown(ctx, error)

    @shop.after_invoke
    async def shop_cooldown(self, ctx):
        await self.bot.add_command_count(ctx.author)
        for id in list(self.bot.owner_ids):
            if id == ctx.author.id:
                ctx.command.reset_cooldown(ctx)


def setup(bot):
    bot.add_cog(shop(bot))
