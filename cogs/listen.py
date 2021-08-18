import discord
from discord.ext import commands
from replit import db


#from triggers import triggers, triggers_replies
class Listen(commands.Cog):
  def __init__(self, client):
    self.client = client
  @commands.Cog.listener()
  async def on_ready(self):
    print('Logged in as {0.user}'. format(self.client))
  @commands.Cog.listener()
  async def on_message(self, message):
    msg = message.content
    if message.author == self.client.user: 
      return
    if msg.startswith('>'):
      if msg[1:] in db.keys():
        await message.channel.send(db[msg[1:]])
      else:
        await message.channel.send('Welp no such note, try `-notes` to see all available keys')
    # for i in msg.split():
    #   for a in triggers:
    #     for b in a:
    #       if i.lower() == b:
    #         matched = triggers.index(a)
    #         await message.channel.send(triggers_replies[matched][random.randint(0, len(triggers_replies[matched]) - 1)])
    # if (message.author.bot): pass

    if ("@here" in message.content) or ("@everyone" in message.content): pass
    if message.mentions:
      if (self.client.get_user(self.client.user.id) == message.mentions[0]):
        await message.channel.send("I\'m awake!")
  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
      await ctx.send("Unknown command, see `-help` for more infomation")
    elif isinstance(error, commands.NotOwner):
      await ctx.send('''You aren't the owner buddy!''')
    elif isinstance(error, (commands.MissingRole, commands.MissingAnyRole)):
        await ctx.send('''You aren't authorised buddy!''')
    else: await ctx.send(error)

def setup(client):
  client.add_cog(Listen(client))