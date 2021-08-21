import discord
from discord.ext import commands
from data.note import check_table, get_note


class Listen(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Bee boo peep"))
        print('Logged in as {0.user}'. format(self.client))

    @commands.Cog.listener()
    async def on_message(self, message):
        _id = "_" + str(message.author.id)
        _id_s = "_s" + str(message.guild.id)
        msg = message.content
        if message.author == self.client.user:
            return
        if msg.startswith('>'):
            try:
                await message.channel.send(get_note(_id, msg[1:])[1])
            except Exception:
                await message.channel.send('Welp no such note, try `-notes` to see all available keys')
        
        if msg.startswith('.'):
            try:
                await message.channel.send(get_note(_id_s, msg[1:])[1])
            except Exception:
                await message.channel.send('Welp no such note, try `-notes` to see all available keys')
        if message.mentions and (self.client.get_user(self.client.user.id) == message.mentions[0]):
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


def setup(client):
    client.add_cog(Listen(client))
