import json
import nextcord
import requests
from nextcord.ext import commands
from nextcord.ui import Button, View

class meme(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  @commands.command(name="meme", aliases=['memes'])
  async def meme(self, ctx):
      content = requests.get("https://meme-api.com/gimme/memes").text
      data = json.loads(content)
      posttitle = data['title']
      postimg = data['url']
      postlink = data['postLink']
      upvotes = data['ups']
      author = data['author']

      async def button_callback(interaction):
          content = requests.get("https://meme-api.com/gimme/memes").text
          data = json.loads(content)
          posttitle = data['title']
          postimg = data['url']
          postlink = data['postLink']
          upvotes = data['ups']
          author = data['author']
          embed = nextcord.Embed(title=f"{posttitle}", url=f"{postlink}")
          embed.set_image(url=f"{postimg}")
          embed.set_footer(text=f"Posted by: {author} | 👍{upvotes}")

          async def button4_callback(interaction):
              await interaction.user.send(embed=embed)

          button3 = Button(label='Next Meme',
                           style=nextcord.ButtonStyle.green)
          button4 = Button(label='Save Post', style=nextcord.ButtonStyle.gray)
          button4.callback = button4_callback
          view1 = View()
          button3.callback = button_callback
          view1.add_item(button3)
          view1.add_item(button4)

          await interaction.response.edit_message(embed=embed, view=view1)

      async def button2_callback(interaction):
          await interaction.user.send(embed=embed)

      button1 = Button(label='Next Meme', style=nextcord.ButtonStyle.green)
      button2 = Button(label='Save Post', style=nextcord.ButtonStyle.gray)
      button2.callback = button2_callback
      view = View()
      button1.callback = button_callback
      view.add_item(button1)
      view.add_item(button2)

      embed = nextcord.Embed(title=f"{posttitle}", url=f"{postlink}")
      embed.set_image(url=f"{postimg}")
      embed.set_footer(text=f"Posted by: {author} | 👍{upvotes}")
      await ctx.reply(embed=embed, view=view)

def setup(bot):
  bot.add_cog(meme(bot))