import json
import nextcord
from nextcord import Interaction, ButtonStyle
from nextcord.ui import View, Button
from config import discord, owners, new_user, on_cooldown, add_command_count, zero_effect_fix, zero_fix
from nextcord.ext import commands

not_enough = discord.Embed(
    title="NOT ENOUGH MANNA",
    description="You Don't Have Enough Manna To Buy This Item",
    color=0x6CBA74)


async def shop_embed(user, item):
    with open("effect_shop.json", "r") as f:
        shop = json.load(f)
    with open("save.json", "r") as k:
        users = json.load(k)

    if str(user.id) not in users:
        await new_user(user)
    name = shop[item]['name']
    icon = shop[item]['icon']
    image = shop[item]['image']
    id = shop[item]['id']
    price = shop[item]['price']
    description = shop[item]['description']

    if item in list(users[str(user.id)]['effects']):
        count = users[str(user.id)]['effects'][item]['count']
    else:
        count = 0
    if shop[item]['status'] == "unusable":
        description = "**Work in Progress**"
    embed = discord.Embed(
        title=f"{name} ({count} owned)",
        description=
        f"> {description}\n\n<:GUI:953128943974776913> ID `{id}`\n**Buy** - 🌾`{price}`",
        color=0xF7D600)
    embed.set_thumbnail(url=image)
    return embed


#Class And Buttons
class shop_view(nextcord.ui.View):
    def __init__(self):
        super().__init__(timeout=120)
        self.value = None
        self.ammount = 0
        self.current_item = None
        self.ammount_callback.disabled = True
        self.cost_callback.disabled = True

    async def on_timeout(self):
        self.abraham_callback.disabled = True
        self.daniel_callback.disabled = True
        self.elijah_callback.disabled = True
        self.plus1.disabled = True
        self.friday_callback.disabled = True
        self.jonah_callback.disabled = True
        self.joshua_callback.disabled = True
        self.buy_callback.disabled = True
        self.jesus_callback.disabled = True
        self.lazarus_callback.disabled = True
        self.revelation_callback.disabled = True
        self.minus1.disabled = True
        await self.message.edit(view=self)

    #Button Abraham
    @nextcord.ui.button(emoji="<:Abraham:985787855588704256>", row=0)
    async def abraham_callback(self, button: nextcord.ui.Button,
                               interaction: nextcord.Interaction):
        item = 'ABRAHAM'
        if interaction.user.id != self.ctx.author.id:
            steal = discord.Embed(title="THOU SHALT NOT STEAL",
                                  description="This Button Is Not For You",
                                  color=0xFF002F)
            await interaction.response.send_message(embed=steal,
                                                    ephemeral=True)
        else:
            self.current_item = item
            with open("effect_shop.json", "r") as f:
                shop = json.load(f)
            self.cost = shop[self.current_item]['price'] * self.ammount
            if self.cost == 0:
                self.cost_callback.label = "ㅤㅤㅤㅤㅤ      ㅤㅤPRICEㅤㅤㅤ  ㅤㅤㅤㅤㅤ "
                self.ammount_callback.label = "ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNTㅤㅤㅤㅤㅤㅤㅤ  "
            else:
                self.ammount_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNT:{self.ammount}ㅤㅤㅤㅤㅤㅤㅤ"
                self.cost_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤPRICE:{self.cost}ㅤㅤㅤㅤㅤㅤ  ㅤ"
            await interaction.response.edit_message(embed=await shop_embed(
                interaction.user, item),
                                                    view=self)

    #Button Daniel
    @nextcord.ui.button(emoji="<:Daniel:985787847799889930", row=0)
    async def daniel_callback(self, button: nextcord.ui.Button,
                              interaction: nextcord.Interaction):
        item = 'DANIEL'
        if interaction.user.id != self.ctx.author.id:
            steal = discord.Embed(title="THOU SHALT NOT STEAL",
                                  description="This Button Is Not For You",
                                  color=0xFF002F)
            await interaction.response.send_message(embed=steal,
                                                    ephemeral=True)
        else:
            self.current_item = item
            with open("effect_shop.json", "r") as f:
                shop = json.load(f)
            self.cost = shop[self.current_item]['price'] * self.ammount
            if self.cost == 0:
                self.cost_callback.label = "ㅤㅤㅤㅤㅤ      ㅤㅤPRICEㅤㅤㅤ  ㅤㅤㅤㅤㅤ "
                self.ammount_callback.label = "ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNTㅤㅤㅤㅤㅤㅤㅤ  "
            else:
                self.ammount_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNT:{self.ammount}ㅤㅤㅤㅤㅤㅤㅤ"
                self.cost_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤPRICE:{self.cost}ㅤㅤㅤㅤㅤㅤ  ㅤ"
            await interaction.response.edit_message(embed=await shop_embed(
                interaction.user, item),
                                                    view=self)

    #Button Elijah
    @nextcord.ui.button(emoji="<:Elijah:985787839268651110>", row=0)
    async def elijah_callback(self, button: nextcord.ui.Button,
                              interaction: nextcord.Interaction):
        item = 'ELIJAH'
        if interaction.user.id != self.ctx.author.id:
            steal = discord.Embed(title="THOU SHALT NOT STEAL",
                                  description="This Button Is Not For You",
                                  color=0xFF002F)
            await interaction.response.send_message(embed=steal,
                                                    ephemeral=True)
        else:
            self.current_item = item
            with open("effect_shop.json", "r") as f:
                shop = json.load(f)
            self.cost = shop[self.current_item]['price'] * self.ammount
            if self.cost == 0:
                self.cost_callback.label = "ㅤㅤㅤㅤㅤ      ㅤㅤPRICEㅤㅤㅤ  ㅤㅤㅤㅤㅤ "
                self.ammount_callback.label = "ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNTㅤㅤㅤㅤㅤㅤㅤ  "
            else:
                self.ammount_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNT:{self.ammount}ㅤㅤㅤㅤㅤㅤㅤ"
                self.cost_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤPRICE:{self.cost}ㅤㅤㅤㅤㅤㅤ  ㅤ"
            await interaction.response.edit_message(embed=await shop_embed(
                interaction.user, item),
                                                    view=self)

    #Plus 1 Button
    @nextcord.ui.button(label="   ➕   ",
                        row=0,
                        style=discord.ButtonStyle.blurple)
    async def plus1(self, button: nextcord.ui.Button,
                    interaction: nextcord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            steal = discord.Embed(title="THOU SHALT NOT STEAL",
                                  description="This Button Is Not For You",
                                  color=0xFF002F)
            await interaction.response.send_message(embed=steal,
                                                    ephemeral=True)
        else:
            self.ammount += 1
            with open("effect_shop.json", "r") as f:
                shop = json.load(f)
            if self.current_item == None:
                self.cost_callback.label = f"ㅤㅤㅤㅤㅤ      ㅤㅤPRICEㅤㅤㅤ  ㅤㅤㅤㅤㅤ "
                if self.ammount != 0:
                    self.ammount_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNT:{self.ammount}ㅤㅤㅤㅤㅤㅤㅤ"
            else:
                self.cost = shop[self.current_item]['price'] * self.ammount
                if self.cost == 0:
                    self.cost_callback.label = "ㅤㅤㅤㅤㅤ      ㅤㅤPRICEㅤㅤㅤ  ㅤㅤㅤㅤㅤ "
                    self.ammount_callback.label = "ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNTㅤㅤㅤㅤㅤㅤㅤ  "
                else:
                    self.ammount_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNT:{self.ammount}ㅤㅤㅤㅤㅤㅤㅤ"
                    self.cost_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤPRICE:{self.cost}ㅤㅤㅤㅤㅤㅤ  ㅤ"
            await interaction.response.edit_message(view=self)

    #Button Friday
    @nextcord.ui.button(emoji="<:Friday:985787835481206804>", row=1)
    async def friday_callback(self, button: nextcord.ui.Button,
                              interaction: nextcord.Interaction):
        item = 'FRIDAY'
        if interaction.user.id != self.ctx.author.id:
            steal = discord.Embed(title="THOU SHALT NOT STEAL",
                                  description="This Button Is Not For You",
                                  color=0xFF002F)
            await interaction.response.send_message(embed=steal,
                                                    ephemeral=True)
        else:
            self.current_item = item
            with open("effect_shop.json", "r") as f:
                shop = json.load(f)
            self.cost = shop[self.current_item]['price'] * self.ammount
            if self.cost == 0:
                self.cost_callback.label = "ㅤㅤㅤㅤㅤ      ㅤㅤPRICEㅤㅤㅤ  ㅤㅤㅤㅤㅤ "
                self.ammount_callback.label = "ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNTㅤㅤㅤㅤㅤㅤㅤ  "
            else:
                self.ammount_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNT:{self.ammount}ㅤㅤㅤㅤㅤㅤㅤ"
                self.cost_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤPRICE:{self.cost}ㅤㅤㅤㅤㅤㅤ  ㅤ"
            await interaction.response.edit_message(embed=await shop_embed(
                interaction.user, item),
                                                    view=self)

    #Button Jonah
    @nextcord.ui.button(emoji="<:Jonah:985787823812657203>", row=1)
    async def jonah_callback(self, button: nextcord.ui.Button,
                             interaction: nextcord.Interaction):
        item = 'JONAH'
        if interaction.user.id != self.ctx.author.id:
            steal = discord.Embed(title="THOU SHALT NOT STEAL",
                                  description="This Button Is Not For You",
                                  color=0xFF002F)
            await interaction.response.send_message(embed=steal,
                                                    ephemeral=True)
        else:
            self.current_item = item
            with open("effect_shop.json", "r") as f:
                shop = json.load(f)
            self.cost = shop[self.current_item]['price'] * self.ammount
            if self.cost == 0:
                self.cost_callback.label = "ㅤㅤㅤㅤㅤ      ㅤㅤPRICEㅤㅤㅤ  ㅤㅤㅤㅤㅤ "
                self.ammount_callback.label = "ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNTㅤㅤㅤㅤㅤㅤㅤ  "
            else:
                self.ammount_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNT:{self.ammount}ㅤㅤㅤㅤㅤㅤㅤ"
                self.cost_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤPRICE:{self.cost}ㅤㅤㅤㅤㅤㅤ  ㅤ"
            await interaction.response.edit_message(embed=await shop_embed(
                interaction.user, item),
                                                    view=self)

    #Button Joshua
    @nextcord.ui.button(emoji="<:Joshua:985787817173069834>", row=1)
    async def joshua_callback(self, button: nextcord.ui.Button,
                              interaction: nextcord.Interaction):
        item = 'JOSHUA'
        if interaction.user.id != self.ctx.author.id:
            steal = discord.Embed(title="THOU SHALT NOT STEAL",
                                  description="This Button Is Not For You",
                                  color=0xFF002F)
            await interaction.response.send_message(embed=steal,
                                                    ephemeral=True)
        else:
            self.current_item = item
            with open("effect_shop.json", "r") as f:
                shop = json.load(f)
            self.cost = shop[self.current_item]['price'] * self.ammount
            if self.cost == 0:
                self.cost_callback.label = "ㅤㅤㅤㅤㅤ      ㅤㅤPRICEㅤㅤㅤ  ㅤㅤㅤㅤㅤ "
                self.ammount_callback.label = "ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNTㅤㅤㅤㅤㅤㅤㅤ  "
            else:
                self.ammount_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNT:{self.ammount}ㅤㅤㅤㅤㅤㅤㅤ"
                self.cost_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤPRICE:{self.cost}ㅤㅤㅤㅤㅤㅤ  ㅤ"
            await interaction.response.edit_message(embed=await shop_embed(
                interaction.user, item),
                                                    view=self)

    #Confirm Button
    @nextcord.ui.button(label="CONFIRM",
                        row=1,
                        style=discord.ButtonStyle.blurple)
    async def buy_callback(self, button: nextcord.ui.Button,
                           interaction: nextcord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            steal = discord.Embed(title="THOU SHALT NOT STEAL",
                                  description="This Button Is Not For You",
                                  color=0xFF002F)
            await interaction.response.send_message(embed=steal,
                                                    ephemeral=True)
        else:
            if self.ammount < 1:
                await interaction.response.send_message(
                    "Amount Cannot Be Zero", ephemeral=True)
                return
            if self.current_item == None:
                await interaction.response.send_message("No Item Selected",
                                                        ephemeral=True)
                return
            else:
                with open("save.json", "r") as f:
                    users = json.load(f)
                user = interaction.user
                if str(user.id) not in users:
                    await new_user(user)
                    pass
                if users[str(user.id)]['manna'] < self.cost:
                    await interaction.response.edit_message(embed=not_enough,
                                                            view=None)
                    return
                if 'SATCHEL' not in users[str(user.id)]['bag']:
                    embed = discord.Embed(
                        title="OH I DROPPED IT",
                        description="You Can't Buy This Item Without A Satchel",
                        color=0xF7D600)
                    await interaction.response.edit_message(embed=embed,
                                                            view=None)
                else:
                    with open("save.json", "r") as f:
                        users = json.load(f)
                    with open("effect_shop.json", "r") as f:
                        shop = json.load(f)
                    if self.current_item in users[str(user.id)]['effects']:
                        users[str(user.id)]['effects'][
                            self.current_item]['count'] += self.ammount
                        users[str(user.id)]['manna'] -= self.cost
                        users[str(983916041384112168)]['manna'] += self.cost
                        with open("save.json", "w") as f:
                            json.dump(users, f, indent=4)
                        jollibee = discord.Embed(
                            title="TRADE SUCCESSFUL",
                            description=
                            f"`{self.ammount}` **{shop[self.current_item]['name']}** \n*Sucessfully Bought For* `{self.cost}`🌾!",
                            color=0xF7D600)
                        await interaction.response.edit_message(embed=jollibee,
                                                                view=None)
                    else:
                        users[str(user.id)]['effects'][self.current_item] = {}
                        users[str(user.id)]['effects'][
                            self.current_item]['count'] = self.ammount
                        users[str(user.id)]['manna'] -= self.cost
                        users[str(983916041384112168)]['manna'] += self.cost
                        with open("save.json", "w") as f:
                            json.dump(users, f, indent=4)
                        jollibee = discord.Embed(
                            title="TRADE SUCCESSFUL",
                            description=
                            f"`{self.ammount}` **{shop[self.current_item]['name']}** \n*Sucessfully Bought For* `{self.cost}`🌾!",
                            color=0xF7D600)
                        await interaction.response.edit_message(embed=jollibee,
                                                                view=None)

    #Button Jesus
    @nextcord.ui.button(emoji="<:Jesus:985787828665475073>", row=2)
    async def jesus_callback(self, button: nextcord.ui.Button,
                             interaction: nextcord.Interaction):
        item = 'JESUS'
        if interaction.user.id != self.ctx.author.id:
            steal = discord.Embed(title="THOU SHALT NOT STEAL",
                                  description="This Button Is Not For You",
                                  color=0xFF002F)
            await interaction.response.send_message(embed=steal,
                                                    ephemeral=True)
        else:
            self.current_item = item
            with open("effect_shop.json", "r") as f:
                shop = json.load(f)
            self.cost = shop[self.current_item]['price'] * self.ammount
            if self.cost == 0:
                self.cost_callback.label = "ㅤㅤㅤㅤㅤ      ㅤㅤPRICEㅤㅤㅤ  ㅤㅤㅤㅤㅤ "
                self.ammount_callback.label = "ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNTㅤㅤㅤㅤㅤㅤㅤ  "
            else:
                self.ammount_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNT:{self.ammount}ㅤㅤㅤㅤㅤㅤㅤ"
                self.cost_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤPRICE:{self.cost}ㅤㅤㅤㅤㅤㅤ  ㅤ"
            await interaction.response.edit_message(embed=await shop_embed(
                interaction.user, item),
                                                    view=self)

    #Button Lazarus
    @nextcord.ui.button(emoji="<:Lazarus:985787807949803540>", row=2)
    async def lazarus_callback(self, button: nextcord.ui.Button,
                               interaction: nextcord.Interaction):
        item = 'LAZARUS'
        if interaction.user.id != self.ctx.author.id:
            steal = discord.Embed(title="THOU SHALT NOT STEAL",
                                  description="This Button Is Not For You",
                                  color=0xFF002F)
            await interaction.response.send_message(embed=steal,
                                                    ephemeral=True)
        else:
            self.current_item = item
            with open("effect_shop.json", "r") as f:
                shop = json.load(f)
            self.cost = shop[self.current_item]['price'] * self.ammount
            if self.cost == 0:
                self.cost_callback.label = "ㅤㅤㅤㅤㅤ      ㅤㅤPRICEㅤㅤㅤ  ㅤㅤㅤㅤㅤ "
                self.ammount_callback.label = "ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNTㅤㅤㅤㅤㅤㅤㅤ  "
            else:
                self.ammount_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNT:{self.ammount}ㅤㅤㅤㅤㅤㅤㅤ"
                self.cost_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤPRICE:{self.cost}ㅤㅤㅤㅤㅤㅤ  ㅤ"
            await interaction.response.edit_message(embed=await shop_embed(
                interaction.user, item),
                                                    view=self)

    #Button Revelation
    @nextcord.ui.button(emoji="<:Revelation:985787800832069632>", row=2)
    async def revelation_callback(self, button: nextcord.ui.Button,
                                  interaction: nextcord.Interaction):
        item = 'REVELATION'
        if interaction.user.id != self.ctx.author.id:
            steal = discord.Embed(title="THOU SHALT NOT STEAL",
                                  description="This Button Is Not For You",
                                  color=0xFF002F)
            await interaction.response.send_message(embed=steal,
                                                    ephemeral=True)
        else:
            self.current_item = item
            with open("effect_shop.json", "r") as f:
                shop = json.load(f)
            self.cost = shop[self.current_item]['price'] * self.ammount
            if self.cost == 0:
                self.cost_callback.label = "ㅤㅤㅤㅤㅤ      ㅤㅤPRICEㅤㅤㅤ  ㅤㅤㅤㅤㅤ "
                self.ammount_callback.label = "ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNTㅤㅤㅤㅤㅤㅤㅤ  "
            else:
                self.ammount_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNT:{self.ammount}ㅤㅤㅤㅤㅤㅤㅤ"
                self.cost_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤPRICE:{self.cost}ㅤㅤㅤㅤㅤㅤ  ㅤ"
            await interaction.response.edit_message(embed=await shop_embed(
                interaction.user, item),
                                                    view=self)

    #Minus 1 Button
    @nextcord.ui.button(label="   ➖   ",
                        row=2,
                        style=discord.ButtonStyle.blurple)
    async def minus1(self, button: nextcord.ui.Button,
                     interaction: nextcord.Interaction):
        if interaction.user.id != self.ctx.author.id:
            steal = discord.Embed(
                title="THOU SHALT NOT STEAL",
                description="This Menu Isn't For You \nUse `+effects shop`",
                color=0xFF002F)
            await interaction.response.send_message(embed=steal,
                                                    ephemeral=True)
        else:
            if self.ammount < 1:
                await interaction.response.send_message(
                    "Amount Cannot Be Zero", ephemeral=True)
            else:
                self.ammount -= 1
                with open("effect_shop.json", "r") as f:
                    shop = json.load(f)
                if self.current_item == None:
                    self.cost_callback.label = f"ㅤㅤㅤㅤㅤ      ㅤㅤPRICEㅤㅤㅤ  ㅤㅤㅤㅤㅤ "
                    if self.ammount != 0:
                        self.ammount_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNT:{self.ammount}ㅤㅤㅤㅤㅤㅤㅤ"
                else:
                    self.cost = shop[self.current_item]['price'] * self.ammount
                    if self.cost == 0:
                        self.cost_callback.label = "ㅤㅤㅤㅤㅤ      ㅤㅤPRICEㅤㅤㅤ  ㅤㅤㅤㅤㅤ "
                        self.ammount_callback.label = "ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNTㅤㅤㅤㅤㅤㅤㅤ  "
                    else:
                        self.ammount_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNT:{self.ammount}ㅤㅤㅤㅤㅤㅤㅤ"
                        self.cost_callback.label = f"ㅤㅤㅤㅤㅤㅤㅤㅤPRICE:{self.cost}ㅤㅤㅤㅤㅤㅤ  ㅤ"
                await interaction.response.edit_message(view=self)

    @nextcord.ui.button(label=f"ㅤㅤㅤㅤㅤㅤㅤㅤAMOUNTㅤㅤㅤㅤㅤㅤㅤ  ",
                        row=3,
                        style=discord.ButtonStyle.green)
    async def ammount_callback(self, button: nextcord.ui.Button,
                               interaction: nextcord.Interaction):
        button.disabled = True

    @nextcord.ui.button(label=f"ㅤㅤㅤㅤㅤ      ㅤㅤPRICEㅤㅤㅤ  ㅤㅤㅤㅤㅤ ",
                        row=4,
                        style=discord.ButtonStyle.green)
    async def cost_callback(self, button: nextcord.ui.Button,
                            interaction: nextcord.Interaction):
        button.disabled = True


class effect(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(name="effect",
                    aliases=["effects", "fx"],
                    invoke_without_command=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def effect(self, ctx, user: discord.Member = None):
        await zero_effect_fix()
        with open("save.json", "r") as f:
            users = json.load(f)

        if user != None:

            if str(user.id) in users:

                embed = discord.Embed(
                    title="THEIR SATCHEL",
                    description=
                    "We see that you have discovered the effects panel. \nIn here you can mainly see the effects that you own, \nalong with a bunch of other subcommands under \nthis panel. \nㅤ"
                )
                embed.add_field(
                    name=f"SUB-COMMANDS",
                    value=
                    f"`{self.bot.get_msg_prefix(self.bot, ctx)}effects` **shop** \n`{self.bot.get_msg_prefix(self.bot, ctx)}effects` **buy** \nㅤ",
                    inline=False)
                embed.set_thumbnail(url='https://i.imgur.com/8ktFYeO.png')
                embed.set_footer(text="\nTHE EFFECTS ARE EFFECTIVE")

                if users[str(user.id)]['effects'] == {}:
                    return
                else:
                    for effect in list(users[str(user.id)]['effects'].keys()):
                        with open("effect_shop.json", "r") as f2:
                            shop = json.load(f2)
                        effect_name = shop[effect]['name']
                        effect_count = users[str(
                            user.id)]['effects'][effect]['count']
                        effect_desc = shop[effect]['description']
                        effect_icon = shop[effect]['icon']
                        effect_image = shop[effect]['image']
                        if effect_count != 0:

                            #Main Embed
                            embed.add_field(
                                name=
                                f"`{effect_count}`{effect_icon} - {effect_name}",
                                value=
                                f"<:GUI:953128943974776913> *{effect_desc}*",
                                inline=False)

                await ctx.reply(embed=embed)

            else:

                embed = discord.Embed(
                    title="WHO AGAIN?",
                    description=
                    f"Unknown User.\nI've Never Met This Man My Entire Life.",
                    color=0xb0c1e0)
                embed.set_thumbnail(url="https://i.imgur.com/3QiQAfL.png")
                await ctx.reply(embed=embed, delete_after=7)

        else:

            user = ctx.author
            if str(user.id) not in users:
                await new_user(user)
                embed = discord.Embed(
                    title="WHERE SHOULD I PUT IT?",
                    description="You Don't Have A Satchel, Buy `1` At The Shop",
                )
                embed.set_footer(text="\nTHE EFFECTS ARE EFFECTIVE")
                embed.set_thumbnail(url='https://i.imgur.com/8ktFYeO.png')
                await ctx.reply(embed=embed)

            else:
                with open("save.json", "r") as f:
                    users = json.load(f)
                if "SATCHEL" not in users[str(user.id)]['bag']:
                    embed = discord.Embed(
                        title="WHERE SHOULD I PUT IT?",
                        description=
                        "You Don't Have A Satchel, Buy `1` At The Shop",
                    )
                    embed.set_footer(text="\nTHE EFFECTS ARE EFFECTIVE")
                    embed.set_thumbnail(url='https://i.imgur.com/8ktFYeO.png')
                    await ctx.reply(embed=embed)

                else:
                    embed = discord.Embed(
                        title="YOUR SATCHEL",
                        description=
                        "We see that you have discovered the effects panel. \nIn here you can mainly see the effects that you own, \nalong with a bunch of other subcommands under \nthis panel. \nㅤ"
                    )
                    embed.add_field(
                        name=f"SUB-COMMANDS",
                        value=
                        f"`{self.bot.get_msg_prefix(self.bot, ctx)}effects` **shop** \n`{self.bot.get_msg_prefix(self.bot, ctx)}effects` **buy** \nㅤ",
                        inline=False)
                    embed.set_thumbnail(url='https://i.imgur.com/8ktFYeO.png')
                    embed.set_footer(text="\nTHE EFFECTS ARE EFFECTIVE")

                    if users[str(user.id)]['effects'] == "":
                        return
                    else:
                        for effect in list(users[str(
                                user.id)]['effects'].keys()):
                            with open("effect_shop.json", "r") as f2:
                                shop = json.load(f2)
                            effect_name = shop[effect]['name']
                            effect_count = users[str(
                                user.id)]['effects'][effect]['count']
                            effect_desc = shop[effect]['description']
                            effect_icon = shop[effect]['icon']
                            effect_image = shop[effect]['image']
                            if effect_count != 0:

                                #Main Embed
                                embed.add_field(
                                    name=
                                    f"`{effect_count}`{effect_icon} - {effect_name}",
                                    value=
                                    f"<:GUI:953128943974776913> *{effect_desc}*",
                                    inline=False)

                    await ctx.reply(embed=embed)

    @effect.command(name="shop", aliases=['item', 'help', 'buy'])
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def effect_shop(self, ctx: commands.context, *, item=None):
        if item == None:
            with open("effect_shop.json", "r") as f:
                shop = json.load(f)
            embed = discord.Embed(
                title="WELCOME TO THE SHOP",
                description="In here, you can buy and sell different effects",
                color=0xFFCC4D)

            for item in list(shop):
                name = shop[item]['name']
                price = shop[item]['price']
                icon = shop[item]['icon']
                if shop[item]['status'] == "unusable":
                    description = "**Work in Progress**"
                else:
                    description = shop[item]['description']
                embed.add_field(name=f"{icon} {name}",
                                value=f"> 🌾`{price}`\n> *{description}*",
                                inline=True)
            view = shop_view()
            view.ctx = ctx
            view.cog = self
            view.message = await ctx.reply(embed=embed, view=view)
        else:
            with open("effect_shop.json", "r") as f:
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
                if item in list(users[str(ctx.author.id)]['effects']):
                    count = users[str(ctx.author.id)]['effects'][item]['count']
                    embed = discord.Embed(
                        title=f"{name} ({count} owned)",
                        description=
                        f"> {description}\n\n<:GUI:953128943974776913> ID `{id}`\n**Buy** - 🌾`{price}`",
                        color=0xF7D600)
                    embed.set_thumbnail(url=image)
                    await zero_fix()
                    await ctx.reply(embed=embed)
                else:
                    count = 0
                    embed = discord.Embed(
                        title=f"{name} ({count} owned)",
                        description=
                        f"> {description}\n\n<:GUI:953128943974776913> ID `{id}`\n**Buy** - 🌾`{price}`",
                        color=0xF7D600)
                    embed.set_thumbnail(url=image)
                    await zero_fix()
                    await ctx.reply(embed=embed)
            else:
                unknown = discord.Embed(
                    title="WHICH ONE?",
                    description=
                    "We Don't Think That Effect Is In Our List, Sorry.",
                    color=0x5BB5BA)
                await zero_fix()
                await ctx.reply(embed=unknown)

    @effect.error
    async def effect_error(self, ctx: commands.Context, error):
        await on_cooldown(ctx, error)

    @effect.after_invoke
    async def effect_cooldown(self, ctx):
        await add_command_count(ctx.author)
        for id in owners:
            if id == ctx.author.id:
                ctx.command.reset_cooldown(ctx)

    @effect_shop.error
    async def effect_shop_error(self, ctx: commands.Context, error):
        await on_cooldown(ctx, error)

    @effect_shop.after_invoke
    async def effect_shop_cooldown(self, ctx):
        await add_command_count(ctx.author)
        for id in owners:
            if id == ctx.author.id:
                ctx.command.reset_cooldown(ctx)


def setup(bot):
    bot.add_cog(effect(bot))
