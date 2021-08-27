from discord.ext import commands
import os

from data.note import autocommit, rollback
from discord.ext import commands
import psutil
import math

# Import and load all files
client = commands.Bot(command_prefix="-")
client.remove_command('help')

@client.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Loaded: {extension}')


@client.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send(f'Unloaded: {extension}')


@client.command(hidden=True)
@commands.is_owner()
async def reload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    client.load_extension(f'cogs.{extension}')
    await ctx.send(f'Reloaded: {extension}')

for filename in os.listdir('./cogs'):
    if filename.endswith('py'):
        client.load_extension(f'cogs.{filename[:-3]}')

# Owner commands only
@client.command(hidden=True)
@commands.is_owner()
async def cpu_usage(ctx, sec=1):
    await ctx.send(f'The CPU usage is: {psutil.cpu_percent(int(sec))}%')

@client.command(hidden=True)
@commands.is_owner()
async def ram_usage(ctx):
    mess = f'total: {round(psutil.virtual_memory()[0]/(math.pow(10, 9)), 2)}GB\navailable: {round(psutil.virtual_memory()[1]/(math.pow(10, 9)), 2)}GB\npercent: {psutil.virtual_memory()[2]}%\nused: {round(psutil.virtual_memory()[3]/(math.pow(10, 9)), 2)}GB\nfree: {round(psutil.virtual_memory()[4]/(math.pow(10, 9)), 2)}GB'
    await ctx.send(mess)
@client.command(hidden=True)
@commands.is_owner()
async def rollback(self, ctx):
    await ctx.send('Rolling back SQL data...')
    rollback()
    await ctx.send('Done!')
@client.command(hidden=True)
@commands.is_owner()
async def autocommit_sql(ctx, cmd):
    int(cmd)
    await ctx.send('Setting Autocommit to: {}'.format(cmd))
    autocommit(cmd)
    await ctx.send('Done!')

# Run the bot
client.run(os.getenv('discord_token'))
