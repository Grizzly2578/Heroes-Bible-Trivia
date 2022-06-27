import nextcord, json, random
from nextcord.ext import commands

discord = nextcord

def get_prefix(bot, message):
    try:
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)
            return prefixes[str(message.guild.id)]
        
    except KeyError: # if the guild's prefix cannot be found in 'prefixes.json'
        with open('prefixes.json', 'r') as k:
            prefixes = json.load(k)
        prefixes[str(message.guild.id)] = '+'

        with open('prefixes.json', 'w') as j:
            json.dump(prefixes, j, indent = 4)

        with open('prefixes.json', 'r') as t:
            prefixes = json.load(t)
            return prefixes[str(message.guild.id)]
        
    except: # I added this when I started getting dm error messages
        return '+' # This will return "+" as a prefix. You can change it to any default prefix.

intents = discord.Intents.default()
intents.members = True
intents.presences = True



owners = [
  908234266301829132,
  829619198544183327
]

bot = commands.Bot(
  command_prefix=get_prefix,
  owner_ids=set(
    owners
  ),
  help_command=None,
  case_insensitive=True,
  intents=intents
)

async def load_json():
  with open("save.json", "r") as f:
    users = json.load(f)
  return users

async def update_name(user):
  with open("save.json", "r") as f:
    users = json.load(f)
    users[str(user.id)]['name'] = str(user)
    with open("save.json", "w") as f:
      json.dump(users, f, indent=4, sort_keys=True)

async def new_user(user):
  with open("save.json", "r") as f:
    users = json.load(f)
    users[str(user.id)] = {}
    users[str(user.id)]['name'] = str(user)
    users[str(user.id)]['points'] = 0
    users[str(user.id)]['level'] = 0
    users[str(user.id)]['manna'] = 0
    users[str(user.id)]['streak'] = 0
    users[str(user.id)]['cmds_ran'] = 0
    users[str(user.id)]['bag'] = {}
    users[str(user.id)]['effects'] = {}
    with open("save.json", "w") as f:
      users = json.dump(users, f, indent=4, sort_keys=True)
      
async def add_effect(user, effect, ammount):
  with open("save.json", "r") as f:
    users = json.load(f)
    effect_name = effect.upper()
    users[str(user.id)]['effects'][effect_name]['count'] += ammount
    with open("save.json", "w") as f:
      users = json.dump(users, f, indent=4, sort_keys=True)

async def remove_effect(user, effect, ammount):
  with open("save.json", "r") as f:
    users = json.load(f)
    effect_name = effect.upper()
    users[str(user.id)]['effects'][effect_name]['count'] -= ammount
    with open("save.json", "w") as f:
      users = json.dump(users, f, indent=4, sort_keys=True)

async def add_command_count(user):
  with open("save.json", "r") as f:
    users = json.load(f)
  if str(user.id) not in users:
    await new_user(user)
  else:
    with open("save.json", "r") as f:
      users = json.load(f)
      users[str(user.id)]['name'] = str(user)
      users[str(user.id)]['cmds_ran'] += 1
    with open("save.json", "w") as f:
      users = json.dump(users, f, indent=4, sort_keys=True)
    

async def get_commands_ran(user):
  with open("save.json", "r") as f:
    users = json.load(f)
    if str(user.id) not in users:
      return 'None'
    else:
      with open("save.json", "r") as f:
        users = json.load(f)
      return users[str(user.id)]['cmds_ran']

async def level_fix():
  with open("save.json", "r") as f:
    users = json.load(f)
    for user in list(users):
      #Level 1
      if users[str(user)]['points'] > 0:
        users[str(user)]['level'] = 1
      #Level 2
      if users[str(user)]['points'] > 250:
        users[str(user)]['level'] = 2
      #Level 3
      if users[str(user)]['points'] > 500:
        users[str(user)]['level'] = 3
      #Level 4
      if users[str(user)]['points'] > 750:
        users[str(user)]['level'] = 4
      #Level 5
      if users[str(user)]['points'] > 1000:
        users[str(user)]['level'] = 5
      #Level 6
      if users[str(user)]['points'] > 1500:
        users[str(user)]['level'] = 6
      #Level 7
      if users[str(user)]['points'] > 1750:
        users[str(user)]['level'] = 7
      #Level 8
      if users[str(user)]['points'] > 2000:
        users[str(user)]['level'] = 8
      #Level 9
      if users[str(user)]['points'] > 2250:
        users[str(user)]['level'] = 9
      #Level 10
      if users[str(user)]['points'] > 2500:
        users[str(user)]['level'] = 10
      #Level 11
      if users[str(user)]['points'] > 2750:
        users[str(user)]['level'] = 11
      #Level 12
      if users[str(user)]['points'] > 3000:
        users[str(user)]['level'] = 12
      #Level 13
      if users[str(user)]['points'] > 3250:
        users[str(user)]['level'] = 13
      #Level 14
      if users[str(user)]['points'] > 3500:
        users[str(user)]['level'] = 14
      #Level 15
      if users[str(user)]['points'] > 3750:
        users[str(user)]['level'] = 15
      #Level 16
      if users[str(user)]['points'] > 4000:
        users[str(user)]['level'] = 16
      #Level 17
      if users[str(user)]['points'] > 4250:
        users[str(user)]['level'] = 17
      #Level 18
      if users[str(user)]['points'] > 4500:
        users[str(user)]['level'] = 18
      #Level 19
      if users[str(user)]['points'] > 4750:
        users[str(user)]['level'] = 19
      #Level 20
      if users[str(user)]['points'] > 5000:
        users[str(user)]['level'] = 20
      #Level 21
      if users[str(user)]['points'] > 5250:
        users[str(user)]['level'] = 21
      #Level 22
      if users[str(user)]['points'] > 5500:
        users[str(user)]['level'] = 22
      #Level 23
      if users[str(user)]['points'] > 5750:
        users[str(user)]['level'] = 23
      #Level 24
      if users[str(user)]['points'] > 6000:
        users[str(user)]['level'] = 24
      #Level 25
      if users[str(user)]['points'] > 6250:
        users[str(user)]['level'] = 25
      #Level 26
      if users[str(user)]['points'] > 6500:
        users[str(user)]['level'] = 26
      #Level 27
      if users[str(user)]['points'] > 6750:
        users[str(user)]['level'] = 27
      #Level 28
      if users[str(user)]['points'] > 7000:
        users[str(user)]['level'] = 28
      #Level 29
      if users[str(user)]['points'] > 7250:
        users[str(user)]['level'] = 29
      #Level 30
      if users[str(user)]['points'] > 7500:
        users[str(user)]['level'] = 30
      #Level 31
      if users[str(user)]['points'] > 7750:
        users[str(user)]['level'] = 31
      #Level 32
      if users[str(user)]['points'] > 8000:
        users[str(user)]['level'] = 32
      #Level 33
      if users[str(user)]['points'] > 8250:
        users[str(user)]['level'] = 33
      #Level 34
      if users[str(user)]['points'] > 8500:
        users[str(user)]['level'] = 34
      #Level 35
      if users[str(user)]['points'] > 8750:
        users[str(user)]['level'] = 35
      #Level 36
      if users[str(user)]['points'] > 9000:
        users[str(user)]['level'] = 36
      #Level 37
      if users[str(user)]['points'] > 9250:
        users[str(user)]['level'] = 37
      #Level 38
      if users[str(user)]['points'] > 9500:
        users[str(user)]['level'] = 38
      #Level 39
      if users[str(user)]['points'] > 9750:
        users[str(user)]['level'] = 39
      #Level 40
      if users[str(user)]['points'] > 10000:
        users[str(user)]['level'] = 40
    with open("save.json", "w") as f:
      users = json.dump(users, f, indent=4, sort_keys=True)

async def zero_fix():
  with open("save.json", "r") as f:
    users = json.load(f)
    for user in list(users):
      #Level 1
      if users[str(user)]['manna'] < 0:
        users[str(user)]['manna'] = 0
    with open("save.json", "w") as f:
      users = json.dump(users, f, indent=4, sort_keys=True)

async def zero_item_fix():
  with open("save.json", "r") as f:
    users = json.load(f)
  with open("shop.json", "r") as f1:
    shop = json.load(f1)
    for user in list(users.keys()):
      for item in list(shop.keys()):
        if item in users[user]['bag']:
          if users[user]['bag'][item]['count'] == 0:
            users[user]['bag'].pop(item)
    with open("save.json", "w") as f:
      users = json.dump(users, f, indent=4, sort_keys=True)
      
async def zero_effect_fix():
  with open("effect_shop.json", "r") as f:
    shop = json.load(f)
  with open("save.json", "r") as f1:
    users = json.load(f1)
    for user in list(users.keys()):
      for item in list(shop.keys()):
        if item in users[user]['effects']:
          if users[user]['effects'][item]['count'] == 0:
            users[user]['effects'].pop(item)
    with open("save.json", "w") as f:
      users = json.dump(users, f, indent=4, sort_keys=True)
      
def clean_code(content):
    if content.startswith("```") and content.endswith("```"):
        return "\n".join(content.split("\n")[1:])[:-3]
    else:
        return content

async def random_fact(ctx):
  with open("facts.json", "r") as f:
      fax = json.load(f)
  randomnum = random.randint(1, len(fax))

  
  fact = fax[randomnum - 1]

  embed = discord.Embed(
    title="Fact!",
    description=f"{fact}"
  )

  if (random.randint(0,500) == 42) and (ctx.author != bot.user):
        await ctx.reply(embed=embed)
    
  elif (random.randint(0,500) == 69) and (ctx.author != bot.user):
      await ctx.reply(embed=embed)

  elif (random.randint(0,500) == 99) and (ctx.author != bot.user):
      await ctx.reply(embed=embed)

  elif (random.randint(0,500) == 76) and (ctx.author != bot.user):
      await ctx.reply(embed=embed)

  elif (random.randint(0,500) == 25) and (ctx.author != bot.user):
      await ctx.reply(embed=embed)
  
  elif (random.randint(0,500) == 56) and (ctx.author != bot.user):
      await ctx.reply(embed=embed)
    
  elif (random.randint(0,500) == 420) and (ctx.author != bot.user):
      await ctx.reply(embed=embed)
    
  elif (random.randint(0,500) == 70) and (ctx.author != bot.user):
      await ctx.reply(embed=embed)

  elif (random.randint(0,500) == 71) and (ctx.author != bot.user):
      await ctx.reply(embed=embed)

  elif (random.randint(0,500) == 72) and (ctx.author != bot.user):
      await ctx.reply(embed=embed)

  elif (random.randint(0,500) == 73) and (ctx.author != bot.user):
      await ctx.reply(embed=embed)

  elif (random.randint(0,500) == 74) and (ctx.author != bot.user):
      await ctx.reply(embed=embed)

  elif (random.randint(0,500) == 7) and (ctx.author != bot.user):
      await ctx.reply(embed=embed)

  elif (random.randint(0,500) == 6) and (ctx.author != bot.user):
      await ctx.reply(embed=embed)

  elif (random.randint(0,500) == 101) and (ctx.author != bot.user):
      await ctx.reply(embed=embed)

  elif (random.randint(0,500) == 211) and (ctx.author != bot.user):
      await ctx.reply(embed=embed)

  elif (random.randint(0,500) == 312) and (ctx.author != bot.user):
      await ctx.reply(embed=embed)

  elif (random.randint(0,500) == 212) and (ctx.author != bot.user):
      await ctx.reply(embed=embed)

  elif (random.randint(0,500) == 53) and (ctx.author != bot.user):
      await ctx.reply(embed=embed)
  
  else:
      return




















async def on_cooldown(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    cooldown_embed = discord.Embed(
      title = "PEACE BE STILL, BRO...",
      description = f"Jesus Slept In The Boat, Why Not Allow Me In My Own Bed? \nWait For `{error.retry_after:.2f}` Seconds.",
      color = 0xF70036
    )
    await ctx.reply(embed=cooldown_embed)