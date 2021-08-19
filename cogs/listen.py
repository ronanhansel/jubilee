from discord.ext import commands
from data.note import check_table, get_note

#from triggers import triggers, triggers_replies
class Listen(commands.Cog):
  def __init__(self, client):
    self.client = client
  @commands.Cog.listener()
  async def on_ready(self):
    print('Logged in as {0.user}'. format(self.client))
  async def on_message(self, ctx, message):
    _id = "_" + str(ctx.message.guild.id)
    msg = message.content
    if message.author == self.client.user: 
      return
    if msg.startswith('>'):
      if check_table(_id, msg[1:])[0]:
        await message.channel.send(get_note(_id, msg[1:])[1])
      else:
        await message.channel.send('Welp no such note, try `-notes` to see all available keys')
    # for i in msg.split():
    #   for a in triggers:
    #     for b in a:
    #       if i.lower() == b:
    #         matched = triggers.index(a)
    #         await message.channel.send(triggers_replies[matched][random.randint(0, len(triggers_replies[matched]) - 1)])
    # if (message.author.bot): pass

    # if ("@here" in message.content) or ("@everyone" in message.content): pass
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
    else: 
      await ctx.send(error)
      print(error)

def setup(client):
  client.add_cog(Listen(client))