from discord.ext import commands
import data.note
import psutil
import math
import discord

note = data.note


class Owner(commands.Cog):
    "Owner's commands"

    def __init__(self, client):
        self.client = client

    # Owner commands only
    @commands.command()
    @commands.is_owner()
    async def cpu_usage(self, ctx, sec=1):
        await ctx.send(f'The CPU usage is: {psutil.cpu_percent(int(sec))}%')

    @commands.command()
    @commands.is_owner()
    async def ram_usage(self, ctx):
        mess = f'total: {round(psutil.virtual_memory()[0]/(math.pow(10, 9)), 2)}GB\navailable: {round(psutil.virtual_memory()[1]/(math.pow(10, 9)), 2)}GB\npercent: {psutil.virtual_memory()[2]}%\nused: {round(psutil.virtual_memory()[3]/(math.pow(10, 9)), 2)}GB\nfree: {round(psutil.virtual_memory()[4]/(math.pow(10, 9)), 2)}GB'
        await ctx.send(mess)

    @commands.command()
    @commands.is_owner()
    async def speak(self, ctx, *, word):
        await ctx.message.delete()
        await ctx.send(word)

    @commands.command()
    @commands.is_owner()
    async def message_count(self, ctx, channel: discord.TextChannel = None):
        channel = channel or ctx.channel
        count = 0
        async for _ in channel.history(limit=None):
            count += 1
        await ctx.send("There were {} messages in {}".format(count, channel.mention))

    @commands.command()
    @commands.is_owner()
    async def server_info(self, ctx):
        import cpuinfo
        cpu = cpuinfo.get_cpu_info()
        s = ""
        flags = ['python_version', 'arch', 'vendor_id_raw',
                 'brand_raw', 'hz_actual_friendly', 'family']
        for a in flags:
            s += f"{a}: {cpu[a]}\n"
        await ctx.send(s)

    @commands.command()
    @commands.is_owner()
    async def sh(self, ctx, *, command="echo Hello World"):
        try:
            from subprocess import Popen, PIPE, STDOUT
            cmd = command
            event = Popen(cmd, shell=True, stdin=PIPE,
                          stdout=PIPE, stderr=STDOUT)
            output = event.communicate()[0].decode("utf-8")
            if len(output) <= 1:
                await ctx.send("Executed")
            else:
                await ctx.send(output)
        except Exception as e:
            await ctx.send(e)


def setup(client):
    client.add_cog(Owner(client))
