import time
import base64
import aiohttp
from io import BytesIO

import nextcord as discord
from nextcord.ext import commands


class Dropdown(discord.ui.Select):
    def __init__(self, message, images, user):
        self.message = message
        self.images = images
        self.user = user

        options = []
        for i in range(9):
            i = i + 1
            item = discord.SelectOption(label=str(i))
            options.append(item)

        super().__init__(placeholder="Choose the image you want to see!",
                         min_values=1,
                         max_values=1,
                         options=options)

    async def callback(self, interaction: discord.Interaction):
        selection = int(self.values[0]) - 1
        image = BytesIO(
            base64.decodebytes(self.images[selection].encode("utf-8")))
        if not self.user == int(interaction.user.id):
            await interaction.response.send_message(file=discord.File(
                image, "generatedImage.png"),
                                                    ephemeral=True)
        view = DropdownView(message=self.message,
                            images=self.images,
                            user=self.user)
        return await self.message.edit(file=discord.File(
            image, "generatedImage.png"),
                                       view=view)


class DropdownView(discord.ui.View):
    def __init__(self, message, images, user):
        super().__init__(timeout=120)
        self.message = message
        self.images = images
        self.user = user
        self.dropdown = Dropdown(self.message, self.images, self.user)
        self.add_item(self.dropdown)

    async def on_timeout(self):
        self.dropdown.disabled = True
        await self.message.edit(view=self)


class ai_images(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name="generate",
        description="An experimental feature!, returns an ai generated image")
    async def generate(self, ctx: commands.Context, *, prompt: str):
        ETA = int(time.time() + 60)
        msg = await ctx.reply(
            f"Go grab a coffee, this may take some time... ETA: <t:{ETA}:R>")
        async with aiohttp.request("POST",
                                   "https://backend.craiyon.com/generate",
                                   json={"prompt": prompt}) as resp:
            r = await resp.json()
            images = r['images']
            image = BytesIO(base64.decodebytes(images[0].encode("utf-8")))
            return await msg.edit(content="Image generated!",
                                  file=discord.File(image,
                                                    "generatedImage.png"),
                                  view=DropdownView(msg, images,
                                                    ctx.author.id))


def setup(bot):
    bot.add_cog(ai_images(bot))
