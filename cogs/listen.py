import asyncio
import discord, json
from discord.ext import commands
from data.note import get_note


class Listen(commands.Cog):
    "Bot listeners"
    def __init__(self, client):
        self.client = client 
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening,
                                                                   name="Bee boo peep"))
        print('Logged in as {0.user}'. format(self.client))

    @commands.Cog.listener()
    async def on_message(self, message):
        # NOTING PART
        _id = "_" + str(message.author.id)
        msg = message.content
        time_warns = 0
        if message.author == self.client.user:
            return
        if msg.startswith('>'):
            try:
                await message.channel.send(get_note(_id, msg[1:])[1])
            except Exception:
                await message.channel.send('Welp no such note, try `-notes` to see all available keys')
        for i in msg.split():
            for a in json.load(open("./data/no_say_words.json")):
                if i.lower() == a:
                    time_warns += 10
        member = message.author
        role = discord.utils.get(message.guild.roles, name='member')
        if role:
            await member.remove_roles(role)
            await message.channel.send(f"Muted {member} for {time_warns} seconds for saying `{i}`")
            await asyncio.sleep(time_warns)
            await member.add_roles(role)

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
