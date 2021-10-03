import asyncio
import discord
import json
from discord.ext import commands
from data.note import get_note


global muted
muted = []


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
        if message.author == self.client.user:
            return
        _id = "_" + str(message.author.id)
        msg = message.content
        time_warns = 0
        censored = False

        for i in msg.split():
            for a in json.load(open("./data/filtered_words.json")):
                if i.lower() == a:
                    censored = True
                    i = a
                    time_warns += 10

        if censored:
            await message.delete()
            member = message.author
            role = discord.utils.get(message.guild.roles, name='member')
            if role:
                await member.remove_roles(role)
                await message.channel.send(f"Muted {member} for {time_warns} seconds for saying `{i}`")
                await asyncio.sleep(time_warns)
                await member.add_roles(role)
                return
        if message.author.id in muted:
            await message.delete()

        if msg.startswith('>'):
            try:
                await message.channel.send(get_note(_id, msg[1:])[1])
                return
            except Exception:
                await message.channel.send('Welp no such note, try `-notes` to see all available keys')
                return

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
