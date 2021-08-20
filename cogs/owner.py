from discord.ext import commands
import psutil
import math


class Owner(commands.Cog):
    "For the owner of the bot"

    def __init__(self, client):
        self.client = client

    @commands.command(hidden=True)
    @commands.is_owner()
    async def cpu_usage(self, ctx, sec=1):
        await ctx.send(f'The CPU usage is: {psutil.cpu_percent(int(sec))}%')

    @commands.command(hidden=True)
    @commands.is_owner()
    async def ram_usage(self, ctx):
        mess = f'total: {round(psutil.virtual_memory()[0]/(math.pow(10, 9)), 2)}GB\navailable: {round(psutil.virtual_memory()[1]/(math.pow(10, 9)), 2)}GB\npercent: {psutil.virtual_memory()[2]}%\nused: {round(psutil.virtual_memory()[3]/(math.pow(10, 9)), 2)}GB\nfree: {round(psutil.virtual_memory()[4]/(math.pow(10, 9)), 2)}GB'
        await ctx.send(mess)


def setup(client):
    client.add_cog(Owner(client))
