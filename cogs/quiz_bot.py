import json
import nextcord
import random
import asyncio
from nextcord import Interaction
from nextcord.ext import commands

from nextcord import SlashOption, slash_command

from config import discord, owners, add_command_count, new_user, on_cooldown, zero_fix, update_name

from nextcord.ui import Button, View

with open("questions.json", "r") as f:
  questions = json.load(f)

with open("choices.json", "r") as f:
  choices = json.load(f)

async def correct_answer(user):
  await zero_fix()
  await update_name(user)
  with open("save.json", "r") as f:
    users = json.load(f)
  if str(user.id) not in users:
    await new_user(user)
  with open("save.json", "r") as f:
    users = json.load(f)
  if users[str(user.id)]['streak'] <=0:
    users[str(user.id)]['streak'] += users[str(user.id)]['streak'] * -1
    with open("save.json", "w") as f:
      users = json.dump(users, f, indent=4, sort_keys=True)
  with open("save.json", "r") as f:
    users = json.load(f)
  users[str(user.id)]['name'] = str(user)
  users[str(user.id)]['points'] += 25
  users[str(user.id)]['streak'] += 1
  users[str(user.id)]['manna'] += 75
  with open("save.json", "w") as f:
    users = json.dump(users, f, indent=4, sort_keys=True)

async def incorrect_answer(user):
  await zero_fix()
  await update_name(user)
  with open("save.json", "r") as f:
    users = json.load(f)
  if str(user.id) not in users:
    await new_user(user)
  with open("save.json", "r") as f:
    users = json.load(f)
  users[str(user.id)]['name'] = str(user)
  users[str(user.id)]['streak'] = 0
  users[str(user.id)]['manna'] -= 25
  with open("save.json", "w") as f:
    users = json.dump(users, f, indent=4, sort_keys=True)
  with open("save.json", "r") as f:
    users = json.load(f)
  if users[str(user.id)]['streak'] <=0:
    users[str(user.id)]['streak'] += users[str(user.id)]['streak'] * -1
    with open("save.json", "w") as f:
      users = json.dump(users, f, indent=4, sort_keys=True)

with open("heroes.json", "r") as f:
  heroes = json.load(f)

class func(commands.Cog):
    def __init__(self, bot):
      self.bot = bot
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(name="trivia", aliases=['t'])
    async def trivia(self, ctx):
        randomnum = random.randint(1, len(questions))
        question_list = list(questions.keys())
        question = question_list[randomnum - 1]
        choice = choices[randomnum - 1]
        choice_sep = '\n'.join(choice)

        hero = questions[question]['hero']
        question_image = heroes[hero]['image']
        colour = heroes[hero]['color']

        #Question Embed
        embed1 = discord.Embed(title=f"{question}",
                               description=f"[**{choice_sep}**](https://discord.com/invite/aGKBcCxWdv)",
                               color = int(colour, 16))
        embed1.set_image(url=question_image)
        embed1.set_author(name=f"{hero}")

        #Correct Answer Embed
        correct = discord.Embed(title="YOU ANSWERED CORRECTLY",
                                description="*You Gained* 🔹`25` and 🌾`75`",
                                color=0x31C14C)

        #Incorrect Answer Embed
        incorrect = discord.Embed(title="YOU ANSWERED INCORRECTLY",
                                  description="*You Lost* 🌾**25**",
                                  color=0xC23030)

        A = Button(label="A", custom_id="A0", style=nextcord.ButtonStyle.blurple)

        B = Button(label="B", custom_id="B0", style=nextcord.ButtonStyle.blurple)

        C = Button(label="C", custom_id="C0", style=nextcord.ButtonStyle.blurple)

        D = Button(label="D", custom_id="D0", style=nextcord.ButtonStyle.blurple)

        view = View()
        view.add_item(A)
        view.add_item(B)
        view.add_item(C)
        view.add_item(D)

        A1 = Button(label="A", custom_id="A1", style=nextcord.ButtonStyle.red)
        A1.disabled = True

        B1 = Button(label="B", custom_id="B1", style=nextcord.ButtonStyle.red)
        B1.disabled = True

        C1 = Button(label="C", custom_id="C1", style=nextcord.ButtonStyle.red)
        C1.disabled = True

        D1 = Button(label="D", custom_id="D1", style=nextcord.ButtonStyle.red)
        D1.disabled = True

        Next = Button(emoji="<:arrowright:988005642881085471>", style=nextcord.ButtonStyle.green, row=1)

        disabled = View()
        disabled.add_item(A1)
        disabled.add_item(B1)
        disabled.add_item(C1)
        disabled.add_item(D1)
        disabled.add_item(Next)

        A2 = Button(label="A",
                    custom_id="A2",
                    style=nextcord.ButtonStyle.green)
        A2.disabled = True

        B2 = Button(label="B",
                    custom_id="B2",
                    style=nextcord.ButtonStyle.green)
        B2.disabled = True

        C2 = Button(label="C",
                    custom_id="C2",
                    style=nextcord.ButtonStyle.green)
        C2.disabled = True

        D2 = Button(label="D",
                    custom_id="D2",
                    style=nextcord.ButtonStyle.green)
        D2.disabled = True
        green = View()
        green.add_item(A2)
        green.add_item(B2)
        green.add_item(C2)
        green.add_item(D2)
        green.add_item(Next)

        A3 = Button(label="A", custom_id="A3", style=nextcord.ButtonStyle.gray)
        A3.disabled = True
        B3 = Button(label="B", custom_id="B3", style=nextcord.ButtonStyle.gray)
        B3.disabled = True
        C3 = Button(label="C", custom_id="C3", style=nextcord.ButtonStyle.gray)
        C3.disabled = True
        D3 = Button(label="D", custom_id="D3", style=nextcord.ButtonStyle.gray)
        D3.disabled = True

        gray = View()
        gray.add_item(A3)
        gray.add_item(B3)
        gray.add_item(C3)
        gray.add_item(D3)
      
        async def A_callback(interaction):
            userAns = "A"
            #Correct Answer
            if userAns == questions[question]['answer']:
                user = interaction.user
                await correct_answer(user)
              
                if interaction.user.avatar !=None:
                    correct.set_author(
                        name=f"Answered By: {interaction.user.display_name}",
                        icon_url=interaction.user.avatar.url)
                else:
                    correct.set_author(
                        name=f"Answered By: {interaction.user.display_name}")
                await interaction.response.edit_message(embed=correct,
                                                        view=green)
            else:
                user = interaction.user
                await incorrect_answer(user)
                  
                incorrect.set_author(
                    name=f"Answered By: {interaction.user.display_name}",
                    icon_url=interaction.user.avatar.url)
                await interaction.response.edit_message(embed=incorrect,
                                                        view=disabled)

        A.callback = A_callback

        async def B_callback(interaction):
            userAns = "B"
            if userAns == questions[question]['answer']:
                user = interaction.user
                await correct_answer(user)
              
                if interaction.user.avatar !=None:
                    correct.set_author(
                        name=f"Answered By: {interaction.user.display_name}",
                        icon_url=interaction.user.avatar.url)
                else:
                    correct.set_author(
                        name=f"Answered By: {interaction.user.display_name}")
                await interaction.response.edit_message(embed=correct,
                                                        view=green)
            else:
                user = interaction.user
                await incorrect_answer(user)
                  
                if interaction.user.avatar !=None:
                    incorrect.set_author(
                        name=f"Answered By: {interaction.user.display_name}",
                        icon_url=interaction.user.avatar.url)
                else:
                    incorrect.set_author(
                        name=f"Answered By: {interaction.user.display_name}")
                await interaction.response.edit_message(embed=incorrect,
                                                        view=disabled)

        B.callback = B_callback

        async def C_callback(interaction):
            userAns = "C"
            if userAns == questions[question]['answer']:
                user = interaction.user
                await correct_answer(user)
              
                if interaction.user.avatar !=None:
                    correct.set_author(
                        name=f"Answered By: {interaction.user.display_name}",
                        icon_url=interaction.user.avatar.url)
                else:
                    correct.set_author(
                        name=f"Answered By: {interaction.user.display_name}")
                await interaction.response.edit_message(embed=correct,
                                                        view=green)
            else:
                user = interaction.user
                await incorrect_answer(user)
                  
                if interaction.user.avatar !=None:
                    incorrect.set_author(
                        name=f"Answered By: {interaction.user.display_name}",
                        icon_url=interaction.user.avatar.url)
                else:
                    incorrect.set_author(
                        name=f"Answered By: {interaction.user.display_name}")
                await interaction.response.edit_message(embed=incorrect,
                                                        view=disabled)

        C.callback = C_callback

        async def D_callback(interaction):
            userAns = "D"
            if userAns == questions[question]['answer']:
                user = interaction.user
                await correct_answer(user)
                if interaction.user.avatar !=None:
                    correct.set_author(
                        name=f"Answered By: {interaction.user.display_name}",
                        icon_url=interaction.user.avatar.url)
                else:
                    correct.set_author(
                        name=f"Answered By: {interaction.user.display_name}")
                await interaction.response.edit_message(embed=correct,
                                                        view=green)
            else:
                user = interaction.user
                await incorrect_answer(user)
                  
                if interaction.user.avatar !=None:
                    incorrect.set_author(
                        name=f"Answered By: {interaction.user.display_name}",
                        icon_url=interaction.user.avatar.url)
                else:
                    incorrect.set_author(
                        name=f"Answered By: {interaction.user.display_name}")
                await interaction.response.edit_message(embed=incorrect,
                                                        view=disabled)

        D.callback = D_callback
      
        async def next_callback(interaction):
          randomnum = random.randint(1, len(questions))
          question_list = list(questions.keys())
          question = question_list[randomnum - 1]
          choice = choices[randomnum - 1]
          choice_sep = '\n'.join(choice)

          hero = questions[question]['hero']
          question_image = heroes[hero]['image']
          hero = questions[question]['hero']
          colour = heroes[hero]['color']
  
          #Question Embed
          embed1 = discord.Embed(title=f"{question}",
                                 description=f"[**{choice_sep}**](https://discord.com/invite/aGKBcCxWdv)",
                                 color = int(colour, 16))
          embed1.set_image(url=question_image)
          embed1.set_author(name=f"{hero}")
  
          #Correct Answer Embed
          correct = discord.Embed(title="YOU ANSWERED CORRECTLY",
                                  description="*You Gained* 🔹`25` and 🌾`75`",
                                  color=0x31C14C)
  
          #Incorrect Answer Embed
          incorrect = discord.Embed(title="YOU ANSWERED INCORRECTLY",
                                    description="*You Lost* 🌾**25**",
                                    color=0xC23030)
  
          A = Button(label="A", custom_id="A0", style=nextcord.ButtonStyle.blurple)
  
          B = Button(label="B", custom_id="B0", style=nextcord.ButtonStyle.blurple)
  
          C = Button(label="C", custom_id="C0", style=nextcord.ButtonStyle.blurple)
  
          D = Button(label="D", custom_id="D0", style=nextcord.ButtonStyle.blurple)
  
          view = View()
          view.add_item(A)
          view.add_item(B)
          view.add_item(C)
          view.add_item(D)
  
          A1 = Button(label="A", custom_id="A1", style=nextcord.ButtonStyle.red)
          A1.disabled = True
  
          B1 = Button(label="B", custom_id="B1", style=nextcord.ButtonStyle.red)
          B1.disabled = True
  
          C1 = Button(label="C", custom_id="C1", style=nextcord.ButtonStyle.red)
          C1.disabled = True
  
          D1 = Button(label="D", custom_id="D1", style=nextcord.ButtonStyle.red)
          D1.disabled = True
  
          Next = Button(emoji="<:arrowright:988005642881085471>", style=nextcord.ButtonStyle.green, row=1)
          Next.callback = next_callback
  
          disabled = View()
          disabled.add_item(A1)
          disabled.add_item(B1)
          disabled.add_item(C1)
          disabled.add_item(D1)
          disabled.add_item(Next)
  
          A2 = Button(label="A",
                      custom_id="A2",
                      style=nextcord.ButtonStyle.green)
          A2.disabled = True
  
          B2 = Button(label="B",
                      custom_id="B2",
                      style=nextcord.ButtonStyle.green)
          B2.disabled = True
  
          C2 = Button(label="C",
                      custom_id="C2",
                      style=nextcord.ButtonStyle.green)
          C2.disabled = True
  
          D2 = Button(label="D",
                      custom_id="D2",
                      style=nextcord.ButtonStyle.green)
          D2.disabled = True
          green = View()
          green.add_item(A2)
          green.add_item(B2)
          green.add_item(C2)
          green.add_item(D2)
          green.add_item(Next)
  
          A3 = Button(label="A", custom_id="A3", style=nextcord.ButtonStyle.gray)
          A3.disabled = True
          B3 = Button(label="B", custom_id="B3", style=nextcord.ButtonStyle.gray)
          B3.disabled = True
          C3 = Button(label="C", custom_id="C3", style=nextcord.ButtonStyle.gray)
          C3.disabled = True
          D3 = Button(label="D", custom_id="D3", style=nextcord.ButtonStyle.gray)
          D3.disabled = True
  
          gray = View()
          gray.add_item(A3)
          gray.add_item(B3)
          gray.add_item(C3)
          gray.add_item(D3)
        
          async def A_callback(interaction):
              userAns = "A"
              #Correct Answer
              if userAns == questions[question]['answer']:
                  user = interaction.user
                  await correct_answer(user)
                
                  if interaction.user.avatar !=None:
                    correct.set_author(
                        name=f"Answered By: {interaction.user.display_name}",
                        icon_url=interaction.user.avatar.url)
                  else:
                    correct.set_author(
                        name=f"Answered By: {interaction.user.display_name}")
                  await interaction.response.edit_message(embed=correct,
                                                          view=green)
              else:
                  user = interaction.user
                  await incorrect_answer(user)
                    
                  if interaction.user.avatar !=None:
                    incorrect.set_author(
                        name=f"Answered By: {interaction.user.display_name}",
                        icon_url=interaction.user.avatar.url)
                  else:
                    incorrect.set_author(
                        name=f"Answered By: {interaction.user.display_name}")
                  await interaction.response.edit_message(embed=incorrect,
                                                          view=disabled)
  
          A.callback = A_callback
  
          async def B_callback(interaction):
              userAns = "B"
              if userAns == questions[question]['answer']:
                  user = interaction.user
                  await correct_answer(user)
                
                  if interaction.user.avatar !=None:
                    correct.set_author(
                        name=f"Answered By: {interaction.user.display_name}",
                        icon_url=interaction.user.avatar.url)
                  else:
                    correct.set_author(
                        name=f"Answered By: {interaction.user.display_name}")
                  await interaction.response.edit_message(embed=correct,
                                                          view=green)
              else:
                  user = interaction.user
                  await incorrect_answer(user)
                    
                  if interaction.user.avatar !=None:
                    incorrect.set_author(
                        name=f"Answered By: {interaction.user.display_name}",
                        icon_url=interaction.user.avatar.url)
                  else:
                    incorrect.set_author(
                        name=f"Answered By: {interaction.user.display_name}")
                  await interaction.response.edit_message(embed=incorrect,
                                                          view=disabled)
  
          B.callback = B_callback
  
          async def C_callback(interaction):
              userAns = "C"
              if userAns == questions[question]['answer']:
                  user = interaction.user
                  await correct_answer(user)
                
                  if interaction.user.avatar !=None:
                    correct.set_author(
                        name=f"Answered By: {interaction.user.display_name}",
                        icon_url=interaction.user.avatar.url)
                  else:
                    correct.set_author(
                        name=f"Answered By: {interaction.user.display_name}")
                  await interaction.response.edit_message(embed=correct,
                                                          view=green)
              else:
                  user = interaction.user
                  await incorrect_answer(user)
                    
                  if interaction.user.avatar !=None:
                    incorrect.set_author(
                        name=f"Answered By: {interaction.user.display_name}",
                        icon_url=interaction.user.avatar.url)
                  else:
                    incorrect.set_author(
                        name=f"Answered By: {interaction.user.display_name}")
                  await interaction.response.edit_message(embed=incorrect,
                                                          view=disabled)
  
          C.callback = C_callback
  
          async def D_callback(interaction):
              userAns = "D"
              if userAns == questions[question]['answer']:
                  user = interaction.user
                  await correct_answer(user)
                  if interaction.user.avatar !=None:
                    correct.set_author(
                        name=f"Answered By: {interaction.user.display_name}",
                        icon_url=interaction.user.avatar.url)
                  else:
                    correct.set_author(
                        name=f"Answered By: {interaction.user.display_name}")
                  await interaction.response.edit_message(embed=correct,
                                                          view=green)
              else:
                  user = interaction.user
                  await incorrect_answer(user)
                  if interaction.user.avatar !=None:
                    incorrect.set_author(
                        name=f"Answered By: {interaction.user.display_name}",
                        icon_url=interaction.user.avatar.url)
                  else:
                    incorrect.set_author(
                        name=f"Answered By: {interaction.user.display_name}")
                  await interaction.response.edit_message(embed=incorrect,
                                                          view=disabled)
          D.callback = D_callback
          await interaction.response.edit_message(embed=embed1, view=view)
        Next.callback = next_callback
        # await ctx.message.delete()
        await zero_fix()
        await ctx.send(embed=embed1, view=view)

    @trivia.after_invoke
    async def reset_cooldown(self, ctx):
      await add_command_count(ctx.author)
      await update_name(ctx.author)
      for id in owners:
          if id == ctx.author.id:
            ctx.command.reset_cooldown(ctx)
  
    @trivia.error
    async def trivia_error(self, ctx:commands.Context, error):
      await on_cooldown(ctx, error)




    with open("heroes.json", "r") as f:
      heroes = json.load(f)
  
    @slash_command(
      name="add_question",
      description="Add's a question to the trivia command",
      guild_ids=[944155967011041340]
    )
    async def add_question(
      self, 
      interaction:Interaction,
      question: str = SlashOption(
        name="question",
        description="The Question You want to add",
        required=True
      ),
      answer: str = SlashOption(
        name="answer",
        description="The Letter of the correct answer, MUST be Capitalized",
        required=True
      ),
      A : str = SlashOption(
        name="a",
        description="Choice Letter A.",
        required=True
      ),
      B : str = SlashOption(
        name="b",
        description="Choice Letter B.",
        required=True
      ),
      C : str = SlashOption(
        name="c",
        description="Choice Letter C.",
        required=True
      ),
      D : str = SlashOption(
        name="d",
        description="Choice Letter D.",
        required=True
      ),
      hero: str = SlashOption(
        name="hero",
        description="The Hero That asked the question",
        choices = heroes.keys(),
        required=True
      )):
      with open("heroes.json", "r") as f:
        heroes = json.load(f)
      with open("questions.json", "r") as f:
        questions = json.load(f)
      questions[question] = {}
      questions[question]['answer'] = answer.upper()
      questions[question]['hero'] = hero.upper()
      with open("questions.json", "w") as f:
        json.dump(questions, f, indent=4)

      A1 = f"A. {A}"
      B1 = f"B. {B}"
      C1 = f"C. {C}"
      D1 = f"D. {D}"

      color = heroes[hero.upper()]['color']
      
      with open("choices.json", "r") as f:
        choices = json.load(f)
        l = [A1,B1,C1,D1]
        choices.append(l)
      with open("choices.json", "w") as f:
        json.dump(choices, f, indent=4)
      newquestion = discord.Embed(
        title = f"QUESTION ADDED\n{question}",
        description = f"**A.** {A}\n**B.** {B}\n**C.** {C}\n**D.** {D}\n",
        color = int(color, 16)
      )
      newquestion.set_image(url = heroes[hero.upper()]['image'])
      await interaction.response.send_message(embed=newquestion, ephemeral=True)


    @slash_command(
      name="add_hero",
      description="Adds a hero to heroes.json",
      guild_ids=[944155967011041340]
    )
    async def add_hero(
      self, 
      interaction:Interaction,
      hero: str = SlashOption(
        name = "name",
        description = "The name of the Hero.",
        required = True
      ),
      image: str = SlashOption(
        name = "image",
        description = "The Image url of the Hero",
        required = True
      ),
      colour: str = SlashOption(
        name = "color",
        description = "The Embed Color that will be shown with the hero",
        required = True
      )
    ):
      with open("heroes.json", "r") as f:
        heroes = json.load(f)
      heroes[hero.upper()] = {}
      heroes[hero.upper()]['name'] = hero.upper()
      heroes[hero.upper()]['image'] = image
      heroes[hero.upper()]['color'] = colour
      with open("heroes.json", "w") as f:
        json.dump(heroes, f, indent = 4, sort_keys=True)
      embed = discord.Embed(
        title="Successfully Added a Hero",
        color = int(colour, 16)
      )
      embed.set_image(url=image)
      await interaction.response.send_message(embed=embed)
def setup(bot):
  bot.add_cog(func(bot))