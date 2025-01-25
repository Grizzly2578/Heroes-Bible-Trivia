import json
import nextcord

from nextcord import Interaction
from nextcord.ui import Button, View
from nextcord.ext import commands

class help_buttons(View):
    def __init__(self):
        super().__init__(timeout=600)
        self.current_page = 0

    async def on_timeout(self):
        self.back_button.disabled = True
        self.next_button.disabled = True
        await self.message.edit(view=self)

    @nextcord.ui.button(emoji="<:ArrowLeft:980082242955132948>")
    async def back_button(self, button: Button, interaction: Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                "This Button is not for you.", ephemeral=True)
            return
        self.current_page -= 1
        await interaction.response.edit_message(
            embed=self.bot.create_embed(self.bot, self.ctx, self.current_page))

    @nextcord.ui.button(emoji="<:arrowright:958961607554248735>")
    async def next_button(self, button: Button, interaction: Interaction):
        if interaction.user.id != self.ctx.author.id:
            await interaction.response.send_message(
                "This Button is not for you.", ephemeral=True)
            return
        self.current_page += 1
        await interaction.response.edit_message(
            embed=self.bot.create_embed(self.bot, self.ctx, self.current_page))


class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="help")
    async def help(self, ctx: commands.Context):
        view = help_buttons()
        view.ctx = ctx
        view.bot = self.bot
        view.message = await ctx.reply(embed=self.bot.create_embed(self.bot, ctx),
                                       view=view)


#   @commands.command(name='help1', description="Shows The List of Commands.", aliases=['h'])
#   @commands.cooldown(1, 5, commands.BucketType.user)
#   async def help1(self, ctx: commands.Context):

#       #First Page
#       help1 = nextcord.Embed(
#           title=f"THE COMMANDS",
#           description="These are the commands you can use to \nactivate the features of this discord bot.",
#           color=0xFFD500)

#     #Commands List (1)

#       #Game Command
#       help1.add_field(
#         name=f"`{self.bot.get_msg_prefix(self.bot, ctx)}`GAME",
#         value=f"<:GUI:953128943974776913>Shows The Game Description.",
#         inline=False
#       )
#       #Help Command
#       help1.add_field(
#         name=f"`{self.bot.get_msg_prefix(self.bot, ctx)}`HELP",
#         value=f"<:GUI:953128943974776913>Shows The List of Commands.",
#         inline=False
#       )
#       #Ping Command
#       help1.add_field(
#         name=f"`{self.bot.get_msg_prefix(self.bot, ctx)}`PING",
#         value=f"<:GUI:953128943974776913>Shows The Bot's Latency Rate.",
#         inline=False
#       )
#       #Porifle Command
#       help1.add_field(
#         name=f"`{self.bot.get_msg_prefix(self.bot, ctx)}`PROFILE",
#         value=f"<:GUI:953128943974776913>Shows The User's Profile.",
#         inline=False
#       )
#       help1.set_thumbnail(url=f"https://i.imgur.com/n2Fba9e.png")
#       help1.set_footer(text="PHILIPPIANS 4:13")

#       #Second Page
#       help2 = nextcord.Embed(
#           title=f"THE COMMANDS",
#           description=f"These are the commands you can use to \nactivate the features of this discord bot.",
#           color=0xFFD500)

#     #Commands List (2)

#       #Trivia Command
#       help2.add_field(
#         name=f"`{self.bot.get_msg_prefix(self.bot, ctx)}`TRIVIA",
#         value=f"<:GUI:953128943974776913>Shows The Quiz Interface.",
#         inline=False
#       )
#       #Effects Command
#       help2.add_field(
#         name=f"`{self.bot.get_msg_prefix(self.bot, ctx)}`EFFECTS",
#         value=f"<:GUI:953128943974776913>Shows The Effects Interface.",
#         inline=False
#       )
#       #Manna Command
#       help2.add_field(
#         name=f"`{self.bot.get_msg_prefix(self.bot, ctx)}`MANNA",
#         value=f"<:GUI:953128943974776913>Shows The Manna Interface.",
#         inline=False
#       )
#       help2.set_thumbnail(url=f"https://i.imgur.com/n2Fba9e.png")
#       help2.set_footer(text="PHILIPPIANS 4:13")

#       #Third Page
#       help3 = nextcord.Embed(
#           title=f"THE COMMANDS",
#           description="These are the commands you can use to \nactivate the features of this discord bot.",
#           color=0xFFD500)

#     #Commands List (3)

#       #Shop Command
#       help3.add_field(
#         name=f"`{self.bot.get_msg_prefix(self.bot, ctx)}`SHOP",
#         value=f"<:GUI:953128943974776913>Shows The Shop Interface",
#         inline=False
#       #Top Command
#       )
#       help3.add_field(
#         name=f"`{self.bot.get_msg_prefix(self.bot, ctx)}`TOP",
#         value=f"<:GUI:953128943974776913>Shows The Leaderboard",
#         inline=False
#       )
#       #Prefix Command
#       help3.add_field(
#         name=f"`{self.bot.get_msg_prefix(self.bot, ctx)}`PREFIX",
#         value=f"<:GUI:953128943974776913>Shows The Bot's Current Prefix.",
#         inline=False
#       )
#       help3.set_thumbnail(url=f"https://i.imgur.com/n2Fba9e.png")
#       help3.set_footer(text="PHILIPPIANS 4:13")

#     #Menu Not For You!
#       menudo = nextcord.Embed(
#           title="NOT FOR ME?",
#           description="Sorry, But This Menu Isn't For You.",
#           color=0xFFD500
#         )

# # Bintana

#       view1 = View()
#       back1 = Button(emoji="<:ArrowLeft:980082242955132948>", style=nextcord.ButtonStyle.gray)
#       next1 = Button(emoji="<:arrowright:958961607554248735>", style=nextcord.ButtonStyle.gray)
#       back1.disabled = True
#       view1.add_item(back1)
#       view1.add_item(next1)

#       view2 = View()
#       back2 = Button(emoji="<:ArrowLeft:980082242955132948>", style=nextcord.ButtonStyle.gray)
#       next2 = Button(emoji="<:arrowright:958961607554248735>", style=nextcord.ButtonStyle.gray)
#       view2.add_item(back2)
#       view2.add_item(next2)

#       view3 = View()
#       back3 = Button(emoji="<:ArrowLeft:980082242955132948>", style=nextcord.ButtonStyle.gray)
#       next3 = Button(emoji="<:arrowright:958961607554248735>", style=nextcord.ButtonStyle.gray)
#       next3.disabled = True
#       view3.add_item(back3)
#       view3.add_item(next3)

# # Callbacks

#       async def next1_callback(interaction):
#         if interaction.user.id == ctx.author.id:
#           await interaction.response.edit_message(embed=help2, view=view2)
#         else:
#           await interaction.response.send_message(embed=menudo, ephemeral=True)
#       next1.callback = next1_callback

#       async def back2_callback(interaction):
#         if interaction.user.id == ctx.author.id:
#           await interaction.response.edit_message(embed=help1, view=view1)
#         else:
#           await interaction.response.send_message(embed=menudo, ephemeral=True)
#       back2.callback = back2_callback

#       async def back3_callback(interaction):
#         if interaction.user.id == ctx.author.id:
#           await interaction.response.edit_message(embed=help2, view=view2)
#         else:
#           await interaction.response.send_message(embed=menudo, ephemeral=True)
#       back3.callback = back3_callback

#       async def next2_callback(interaction):
#         if interaction.user.id == ctx.author.id:
#           await interaction.response.edit_message(embed=help3, view=view3)
#         else:
#           await interaction.response.send_message(embed=menudo, ephemeral=True)
#       next2.callback = next2_callback

#       # Sends the main message.
#       with open("save.json", "r") as f:
#         users = json.load(f)
#       if str(ctx.author.id) not in users:
#         await new_user(ctx.author)
#         await ctx.send(embed=help1, view=view1)
#       else:
#         await ctx.send(embed=help1, view=view1)

    @help.after_invoke
    async def reset_cooldown(self, ctx):
        await self.bot.add_command_count(ctx.author)
        for id in list(self.bot.owner_ids):
            if id == ctx.author.id:
                ctx.command.reset_cooldown(ctx)

    @help.error
    async def help_error(self, ctx: commands.Context, error):
        await self.bot.on_cooldown(ctx, error)


def setup(bot):
    bot.add_cog(help(bot))
