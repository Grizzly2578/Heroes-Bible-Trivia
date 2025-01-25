import nextcord
from nextcord.ext import commands
import openai

client = openai.OpenAI(
  api_key='sk-proj-0wI0PQF3mf0Uf9MHXvgZT3BlbkFJve3NhK95lgaVzXp8rA9z'
)

class chat_filter(commands.Cog):
    def __init__(self, bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.id == self.bot.user.id: return
        if msg.channel.id != 972095551971655711:
            resp = await client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": f"Does the following sentence contain a curse word? \"{msg}\" Answer with true or false."}])
            

            print(resp)




def setup(bot):
    bot.add_cog(chat_filter(bot))