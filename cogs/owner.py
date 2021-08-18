import discord
from discord.ext import commands
from replit import db
from cogs.admins import Admins
import psutil
import math


class Owner(commands.Cog):
  def __init__(self, client):
    self.client = client
    #For owner ONLY
  @commands.command(hidden=True)
  @commands.is_owner()
  async def deleteallnotes(self, ctx):
    for i in db.keys():
      del db[i]
    await ctx.send('Deleted all keys')
  @commands.command(hidden=True)
  @commands.is_owner()
  async def helpop(self, ctx):
    embed = discord.Embed(
      colour = discord.Colour.orange()
    )
    embed.set_author(name='Hi Ronan here are some commands')
    embed.add_field(name='deleteallnotes', value='Delete **ALL** notes', inline=False)
    embed.add_field(name='deleteallnotes', value='Delete **ALL** notes', inline=False)
    await ctx.author.send(embed=embed)
    await ctx.message.delete()
  #DEBUG SECTION
  @commands.command(hidden=True)
  @commands.is_owner()
  async def cpu_usage(self, ctx, sec=1):
    await ctx.send(f'The CPU usage is: {psutil.cpu_percent(int(sec))}%')
  @commands.command(hidden=True)
  @commands.is_owner()
  async def ram_usage(self, ctx):
    mess = f'total: {round(psutil.virtual_memory()[0]/(math.pow(10, 9)), 2)}GB\navailable: {round(psutil.virtual_memory()[1]/(math.pow(10, 9)), 2)}GB\npercent: {psutil.virtual_memory()[2]}%\nused: {round(psutil.virtual_memory()[3]/(math.pow(10, 9)), 2)}GB\nfree: {round(psutil.virtual_memory()[4]/(math.pow(10, 9)), 2)}GB'
    await ctx.send(mess)
  @commands.command(hidden=True)
  @commands.is_owner()
  async def role_admin(self, ctx, *, role):
    db['admin'] = role
    Admins.admin = role
    await ctx.send(f'{role} is now the admin of me 👀')
    
    

def setup(client):
  client.add_cog(Owner(client))