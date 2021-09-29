from random import randint
import discord
import json
from discord.ext import commands


class Moves(commands.Cog):
    "Various moves for the bot"

    def __init__(self, client):
        self.client = client

    @commands.command(help="Hit or strike with the palm of the hand or a flat object")
    async def slap(self, ctx, member: discord.User):
        if ctx.message.author.id != member.id:
            quotes = json.load(open("./data/slap_templates.json"))
            content = quotes[randint(
                0, len(quotes) - 1)].format(f"<@!{ctx.message.author.id}>", f"<@{member.id}>")
            await ctx.send(content)
        else:
            await ctx.send(f"<@!{ctx.message.author.id}> why r u slapping urself???")


def setup(client):
    client.add_cog(Moves(client))
