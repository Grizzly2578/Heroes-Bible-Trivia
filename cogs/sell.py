import json, nextcord
from nextcord.ext import commands


class confirm_view(nextcord.ui.View):
    def __init__(self, cog):
        super().__init__(timeout=300)
        self.cog = cog

    @nextcord.ui.button(label="Confirm", style=nextcord.ButtonStyle.green)
    async def confirm_button(self, button: nextcord.ui.Button,
                             interaction: nextcord.Interaction):
        if interaction.user.id != self.cog.user_id:
            return await interaction.response.send_message(
                content="This button is not for you!", ephemeral=True)
        with open("save.json", "r") as f:
            users = json.load(f)
        self.cog.user_bag = users[str(self.cog.user.id)]['bag']

        if self.cog.item not in self.cog.user_bag:
            button.disabled = True
            await self.msg.edit(view=self)
            return await interaction.response.send_message(
                content="You dont have this item")

        if self.cog.user_bag[self.cog.item]['count'] < self.cog.count:
            button.disabled = True
            await self.msg.edit(view=self)
            return await interaction.response.send_message(
                content="You don't have that much of this item.")
        await self.cog.bot.update_user_item(user=self.cog.user,
                                            mode='subtract',
                                            item=self.cog.item,
                                            value=self.cog.count)
        await self.cog.bot.update_user_manna(user=self.cog.user,
                                             mode='add',
                                             value=self.cog.item_sell_price *
                                             self.cog.count)
        button.disabled = True
        await self.msg.edit(view=self)
        await interaction.response.send_message(content="Cofirmed")


class sell_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="sell", description="sells a mentioned item")
    async def sell_cmd(self,
                       ctx: commands.Context,
                       count: str = None,
                       *,
                       item: str = None):
        self.ctx = ctx
        try:
            if count == None:
                self.count = 1
            else:
                self.count = int(count)
            self.item = item
        except ValueError:
            self.count = 1
            self.item = count

        self.user = ctx.author
        self.user_id = ctx.author.id
        self.shop = json.load(open("shop.json", "r"))
        self.sellable_items = {
            item_id: item
            for item_id, item in self.shop.items()
            if item.get("sell_price") is not None
        }
        self.data = json.load(open("save.json", "r"))
        if str(self.user_id) not in self.data:
            await self.bot.new_user(self.user)

        self.user_data = self.data[str(self.user_id)]
        self.user_bag = self.user_data['bag']
        self.user_sellable_items = {
            item_id: self.user_bag[item_id]['count']
            for item_id in self.user_bag.keys()
            if item_id in self.sellable_items
        }

        if self.item != None:
            self.item = self.item.upper()
            if self.item not in self.shop:
                x = False
                for item in self.shop:
                    if self.item.lower() in self.shop[item]['name'].lower():
                        self.item = item
                        x = True
                if x is False:
                    return await ctx.reply(embed=nextcord.Embed(
                        title="Hol Up!",
                        description=
                        f"I couldn't find an item called `{self.item}`",
                        color=0x2b2d31))

        else:
            self.user_sellable_items_embed = nextcord.Embed(
                title="Your Sellable Items", color=0x2b2d31)
            formatted_embed_desc = ""
            for item_id in self.user_sellable_items:
                formatted_embed_desc = formatted_embed_desc + f"\n{self.shop[item_id]['icon']} **{self.shop[item_id]['name']}** ({self.user_sellable_items[item_id]}) ─ 🌾 {format(self.shop[item_id]['sell_price'],',')}\n{self.shop[item_id]['description']}"
            if formatted_embed_desc != "":
                self.user_sellable_items_embed.description = formatted_embed_desc + f"\n\n `{self.bot.get_msg_prefix(self.bot, ctx)}sell 1 donut`\n<:GUI:953128943974776913> You will be given a Donut for a certain ammount of Manna."
            elif formatted_embed_desc == "":
                self.user_sellable_items_embed.description = f"**Looks like you don't have any items to sell**\n\n `{self.bot.get_msg_prefix(self.bot, ctx)}sell 1 donut`\n<:GUI:953128943974776913> You will be given a Donut for a certain ammount of Manna."
            return await ctx.reply(embed=self.user_sellable_items_embed)

        self.item_sell_price = self.shop[self.item]['sell_price']

        if self.item_sell_price is None:
            return await ctx.reply(embed=nextcord.Embed(
                title="Hold Your Horses!",
                description=
                f"** {self.shop[self.item]['icon']} - {self.shop[self.item]['name']}** is not sellable",
                color=0x2b2d31))

        if self.item not in self.user_bag:
            return await ctx.reply(embed=nextcord.Embed(
                title="Uh Oh!",
                description=
                f"It seems like you don't have a {self.item} in your bag.",
                color=0x2b2d31))

        self.view = confirm_view(cog=self)
        self.transaction_embed = nextcord.Embed(
            title="You are about to sell",
            description=
            f"{self.count} {self.shop[self.item]['icon']} **{self.shop[self.item]['name']}** for 🌾 {format((self.shop[self.item]['sell_price'] * self.count),',')}"
        )
        self.view.msg = await ctx.reply(embed=self.transaction_embed,
                                        view=self.view)


def setup(bot):
    bot.add_cog(sell_cog(bot))
