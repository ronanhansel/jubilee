from discord.ext import commands
import os
from app_placeholder import tracker

#Import and load all files
client = commands.Bot(command_prefix= "-")
client.remove_command('remove')
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

tracker()
client.run(os.getenv('discord_token'))