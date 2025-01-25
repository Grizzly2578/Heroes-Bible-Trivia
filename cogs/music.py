import nextcord
import yt_dlp as youtube_dl

from nextcord.ext import commands
from discord import FFmpegPCMAudio

class music(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot=bot

    @commands.command(
        name="join"
    )
    async def join(self, ctx:commands.Context):
        channel = ctx.message.author.voice.channel
        voice = nextcord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()

    @commands.command(
        name="leave"
    )
    async def leave(self, ctx:commands.Context):
        channel = ctx.message.author.voice.channel
        voice = nextcord.utils.get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await ctx.guild.voice_client.disconnect()
        else:
            await ctx.reply("I'm not in a voice channel, use the join command to make me join", mention_author=False)

    @commands.command(
        name="play"
    )
    async def play(self, ctx:commands.Context, url):
        YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
        FFMPEG_OPTIONS = {
            'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        voice = nextcord.utils.get(self.bot.voice_clients, guild=ctx.guild)

        if not voice.is_playing():
            with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(url, download=False)
            URL = info['url']
            voice.play(FFmpegPCMAudio(URL, **FFMPEG_OPTIONS))
            voice.is_playing()
            await ctx.send('Bot is playing')

        else:
            await ctx.send("Bot is already playing")
            return

    

def setup(bot):
    bot.add_cog(music(bot))