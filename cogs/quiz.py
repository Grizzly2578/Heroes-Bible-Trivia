import json
import time
import random
import asyncio
import nextcord
from nextcord import Interaction, ButtonStyle
from nextcord.ext import commands

from nextcord import SlashOption, slash_command

from nextcord.ui import Button, View, button

with open("database/quiz.json", "r") as f:
    quiz = json.load(f)

correct = nextcord.Embed(title="YOU ANSWERED CORRECTLY",
                         description="*You Gained* 🔹`25` and 🌾`75`",
                         color=0x31C14C)

incorrect = nextcord.Embed(title="YOU ANSWERED INCORRECTLY",
                           description="*You Lost* 🌾**25**",
                           color=0xC23030)

class get_embed:
    def __init__(self, embed:str, user, time_taken):
        super().__init__()
        self.embed = embed
        self.user = user
        self.time_taken = time_taken

class trivia_buttons(View):

    def __init___(self):
        super().__init__()

    async def on_timeout(self):
        await self.disabled_button()

    async def correct_answer(self, user):
        await self.bot.zero_fix()
        await self.bot.update_name(user)
        with open("save.json", "r") as f:
            users = json.load(f)
        if str(user.id) not in users:
            await self.bot.new_user(user)
        with open("save.json", "r") as f:
            users = json.load(f)
        if users[str(user.id)]['streak'] <= 0:
            users[str(user.id)]['streak'] += users[str(user.id)]['streak'] * -1
            with open("save.json", "w") as f:
                users = json.dump(users, f, indent=4, sort_keys=True)
        with open("save.json", "r") as f:
            users = json.load(f)
        users[str(user.id)]['name'] = str(user)
        users[str(user.id)]['points'] += 25
        users[str(user.id)]['streak'] += 1
        users[str(user.id)]['manna'] += 75
        users[str(user.id)]['correct_answers'] += 1
        with open("save.json", "w") as f:
            users = json.dump(users, f, indent=4, sort_keys=True)

    async def incorrect_answer(self, user):
        users = json.load(open("save.json"))
        await self.bot.zero_fix()
        await self.bot.update_name(user)
        user_streak = users[str(user.id)]['streak']
        _time_taken = self.start - time.time()
        time_taken = _time_taken * -1
        embed = nextcord.Embed(
            title=
            "Uh oh. Looks like someone got something wrong.\nCome on it wasnt that hard.",
            description=f"UserID: {self.user.id}",
            color=0xC23030)
        embed.add_field(name="They lost an answer streak of:",
                        value=f"{user_streak}")
        embed.add_field(name="It took them this long to answer:",
                        value=f"{time_taken:.2f}")
        embed.add_field(name=f"Question:", value=f" {self.question}")
        embed.add_field(name="Correct Answer:", value=f"{self.answer}")
        embed.add_field(name="Their answer:", value=f"{self.userAns}")
        embed.set_author(name=self.user)
        embed.add_field(name=f"Choices:", value=f"{self.choice_sep}")
        if self.user.avatar.url:
            embed.set_thumbnail(url=self.user.avatar.url)
        channel = self.bot.get_channel(985404112982118431)
        await channel.send(embed=embed)

        with open("save.json", "r") as f:
            users = json.load(f)
        if str(user.id) not in users:
            await self.bot.new_user(user)
        with open("save.json", "r") as f:
            users = json.load(f)
        users[str(user.id)]['name'] = str(user)
        users[str(user.id)]['streak'] = 0
        users[str(user.id)]['wrong_answers'] += 1
        users[str(user.id)]['manna'] -= 25
        with open("save.json", "w") as f:
            users = json.dump(users, f, indent=4, sort_keys=True)
        with open("save.json", "r") as f:
            users = json.load(f)
        if users[str(user.id)]['streak'] <= 0:
            users[str(user.id)]['streak'] += users[str(user.id)]['streak'] * -1
            with open("save.json", "w") as f:
                users = json.dump(users, f, indent=4, sort_keys=True)

    async def green_button(self):
        self.button_a.style = ButtonStyle.green
        self.button_b.style = ButtonStyle.green
        self.button_c.style = ButtonStyle.green
        self.button_d.style = ButtonStyle.green
        self.button_a.disabled = True
        self.button_b.disabled = True
        self.button_c.disabled = True
        self.button_d.disabled = True
        self.add_item(self.next_button)
        await self.message.edit(view=self)

    async def red_button(self):
        self.button_a.style = ButtonStyle.red
        self.button_b.style = ButtonStyle.red
        self.button_c.style = ButtonStyle.red
        self.button_d.style = ButtonStyle.red
        self.button_a.disabled = True
        self.button_b.disabled = True
        self.button_c.disabled = True
        self.button_d.disabled = True
        self.add_item(self.next_button)
        await self.message.edit(view=self)

    async def gray_button(self):
        self.button_a.style = ButtonStyle.gray
        self.button_b.style = ButtonStyle.gray
        self.button_c.style = ButtonStyle.gray
        self.button_d.style = ButtonStyle.gray
        self.button_a.disabled = False
        self.button_b.disabled = False
        self.button_c.disabled = False
        self.button_d.disabled = False
        await self.message.edit(view=self)

    async def disabled_button(self):
        self.button_a.style = ButtonStyle.gray
        self.button_b.style = ButtonStyle.gray
        self.button_c.style = ButtonStyle.gray
        self.button_d.style = ButtonStyle.gray
        self.button_a.disabled = True
        self.button_b.disabled = True
        self.button_c.disabled = True
        self.button_d.disabled = True
        self.next_button.disabled = True
        await self.message.edit(view=self)

    async def check_answer(self, interaction):
        user = interaction.user
        if self.userAns == self.answer:
            await self.correct_answer(user)

            if interaction.user.avatar != None:
                correct.set_author(
                    name=f"Answered By: {interaction.user.display_name}",
                    icon_url=interaction.user.avatar.url)
            else:
                correct.set_author(
                    name=f"Answered By: {interaction.user.display_name}")

            correct.remove_field(0)
            correct.add_field(name="Time taken:",
                              value=f"🕙 `{self.time_taken - 1:.2f}`")
            await self.green_button()
            await interaction.response.edit_message(embed=correct, view=self)
        else:
            await self.incorrect_answer(user)

            if interaction.user.avatar != None:
                incorrect.set_author(
                    name=f"Answered By: {interaction.user.display_name}",
                    icon_url=interaction.user.avatar.url)
            else:
                incorrect.set_author(
                    name=f"Answered By: {interaction.user.display_name}")
            incorrect.remove_field(0)
            incorrect.add_field(name="Time taken:",
                                value=f"🕙 `{self.time_taken - 1:.2f}`")
            await self.red_button()
            await interaction.response.edit_message(embed=incorrect, view=self)

    @button(label="A", custom_id="A0", style=nextcord.ButtonStyle.blurple)
    async def button_a(self, button: Button, interaction: Interaction):
        self.userAns = "A"
        self.user = interaction.user
        self.user_name = interaction.user.display_name
        _time_taken = self.start - time.time()
        self.time_taken = _time_taken * -1
        await self.check_answer(interaction=interaction)

    @button(label="B", style=nextcord.ButtonStyle.blurple)
    async def button_b(self, button: Button, interaction: Interaction):
        self.userAns = "B"
        self.user = interaction.user
        self.user_name = interaction.user.display_name
        _time_taken = self.start - time.time()
        self.time_taken = _time_taken * -1
        await self.check_answer(interaction=interaction)

    @button(label="C", style=nextcord.ButtonStyle.blurple)
    async def button_c(self, button: Button, interaction: Interaction):
        self.userAns = "C"
        self.user = interaction.user
        self.user_name = interaction.user.display_name
        _time_taken = self.start - time.time()
        self.time_taken = _time_taken * -1
        await self.check_answer(interaction=interaction)

    @button(label="D", style=nextcord.ButtonStyle.blurple)
    async def button_d(self, button: Button, interaction: Interaction):
        self.userAns = "D"
        self.user = interaction.user
        self.user_name = interaction.user.display_name
        _time_taken = self.start - time.time()
        self.time_taken = _time_taken * -1
        await self.check_answer(interaction=interaction)

    @button(emoji="<:arrowright:988005642881085471>",
            style=nextcord.ButtonStyle.green,
            row=1)
    async def next_button(self, button: Button, interaction: Interaction):
        self.remove_item(self.next_button)
        randomnum = random.randint(1, len(quiz["questions"]))
        question_list = list(quiz["questions"].keys())
        question = question_list[randomnum - 1]
        choice = quiz["questions"][question]["choices"]
        choice_sep = '\n'.join(choice)
        hero = quiz["questions"][question]["hero"]
        question_image = quiz["heroes"][hero]["image"]
        colour = quiz["heroes"][hero]["color"]
        self.answer = quiz["questions"][question]["answer"]

        # Image Embed
        embed0 = nextcord.Embed(color=int(colour, 16))
        embed0.set_image(url=question_image)

        # Question Embed
        embed1 = nextcord.Embed(title=f"{question}",
                                description=f"**{choice_sep}**",
                                color=int(colour, 16))
        embed1.set_author(name=f"{hero}")

        embeds = []
        embeds.append(embed0)
        embeds.append(embed1)

        view = trivia_buttons()
        await self.bot.zero_fix()
        self.question = question
        self.cog.answer = self.answer
        self.hero = hero
        self.choice_sep = choice_sep
        self.question_image = question_image
        self.colour = colour
        self.start = time.time()
        self.remove_item(view.next_button)

        await self.gray_button()
        self.message = await interaction.response.edit_message(embeds=embeds,
                                                               view=self)


class quiz_cog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="trivia", aliases=['t'])
    @commands.max_concurrency(1, commands.BucketType.user, wait=True)
    async def trivia(self, ctx):
        randomnum = random.randint(1, len(quiz["questions"]))
        question_list = list(quiz["questions"].keys())
        question = question_list[randomnum - 1]
        choice = quiz["questions"][question]["choices"]
        choice_sep = '\n'.join(choice)
        hero = quiz["questions"][question]["hero"]
        question_image = quiz["heroes"][hero]["image"]
        colour = quiz["heroes"][hero]["color"]
        self.answer = quiz["questions"][question]["answer"]

        # Image Embed
        embed0 = nextcord.Embed(color=int(colour, 16))
        embed0.set_image(url=question_image)

        # Question Embed
        embed1 = nextcord.Embed(title=f"{question}",
                                description=f"**{choice_sep}**",
                                color=int(colour, 16))
        embed1.set_author(name=f"{hero}")

        embeds = []
        embeds.append(embed0)
        embeds.append(embed1)

        self.view = trivia_buttons(timeout=600)
        await self.bot.zero_fix()
        self.view.question = question
        self.view.answer = self.answer
        self.view.hero = hero
        self.view.choice_sep = choice_sep
        self.view.question_image = question_image
        self.view.colour = colour
        self.view.remove_item(self.view.next_button)
        self.view.bot = self.bot
        self.view.start = time.time()
        self.view.cog = self
        self.view.message = await ctx.send(embeds=embeds, view=self.view)

    @commands.command(name="ans")
    @commands.is_owner()
    async def ans(self, ctx: commands.Context):
        await ctx.reply(self.answer)

    @trivia.after_invoke
    async def reset_cooldown(self, ctx):
        await self.bot.add_command_count(ctx.author)
        await self.bot.update_name(ctx.author)
        for id in list(self.bot.owner_ids):
            if id == ctx.author.id:
                ctx.command.reset_cooldown(ctx)

    # @trivia.error
    # async def trivia_error(self, ctx:commands.Context, error):
    #   await on_cooldown(ctx, error)

    @slash_command(name="add_question",
                   description="Add's a question to the trivia command",
                   guild_ids=[944155967011041340])
    async def add_question(
        self,
        interaction: Interaction,
        question: str = SlashOption(name="question",
                                    description="The Question You want to add",
                                    required=True),
        answer: str = SlashOption(
            name="answer",
            description="The Letter of the correct answer, MUST be Capitalized",
            required=True),
        A: str = SlashOption(name="a",
                             description="Choice Letter A.",
                             required=True),
        B: str = SlashOption(name="b",
                             description="Choice Letter B.",
                             required=True),
        C: str = SlashOption(name="c",
                             description="Choice Letter C.",
                             required=True),
        D: str = SlashOption(name="d",
                             description="Choice Letter D.",
                             required=True),
        hero: str = SlashOption(name="hero",
                                description="The Hero That asked the question",
                                choices=quiz["heroes"].keys(),
                                required=True),
        verse: str = SlashOption(
            name="verse",
            description="The Bible Verse where the answer is found",
            required=False)):
        with open("database/quiz.json", "r") as f:
            quiz = json.load(f)

        A1 = f"A. {A}"
        B1 = f"B. {B}"
        C1 = f"C. {C}"
        D1 = f"D. {D}"

        l = [A1, B1, C1, D1]

        quiz["questions"][question] = {}
        quiz["questions"][question]['answer'] = answer.upper()
        quiz["questions"][question]["choices"] = l
        quiz["questions"][question]['hero'] = hero.upper()
        quiz["questions"][question]['verse'] = verse
        with open("database/quiz.json", "w") as f:
            json.dump(quiz, f, indent=4)

        color = quiz["heroes"][hero.upper()]['color']

        newquestion = nextcord.Embed(
            title=f"QUESTION ADDED\n{question}",
            description=f"**A.** {A}\n**B.** {B}\n**C.** {C}\n**D.** {D}\n",
            color=int(color, 16))
        newquestion.set_image(url=quiz["heroes"][hero.upper()]['image'])
        await interaction.response.send_message(embed=newquestion,
                                                ephemeral=True)

    @slash_command(name="add_hero",
                   description="Adds a hero to heroes.json",
                   guild_ids=[944155967011041340])
    async def add_hero(
        self,
        interaction: Interaction,
        hero: str = SlashOption(name="name",
                                description="The name of the Hero.",
                                required=True),
        image: str = SlashOption(name="image",
                                 description="The Image url of the Hero",
                                 required=True),
        colour: str = SlashOption(
            name="color",
            description="The Embed Color that will be shown with the hero",
            required=True)):
        with open("database/quiz.json", "r") as f:
            quiz = json.load(f)
        quiz["heroes"][hero.upper()] = {}
        quiz["heroes"][hero.upper()]['name'] = hero.upper()
        quiz["heroes"][hero.upper()]['image'] = image
        quiz["heroes"][hero.upper()]['color'] = colour
        with open("database/quiz.json", "w") as f:
            json.dump(quiz, f, indent=4, sort_keys=True)
        embed = nextcord.Embed(title="Successfully Added a Hero",
                               color=int(colour, 16))
        embed.set_image(url=image)
        await interaction.response.send_message(embed=embed)


def setup(bot):
    bot.add_cog(quiz_cog(bot))