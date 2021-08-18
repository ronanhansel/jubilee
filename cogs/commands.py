import discord
from discord.ext import commands
import requests
from replit import db

class Commands(commands.Cog):
  def __init__ (self, client):
    self.client = client
  #Commands

  @commands.command(aliases=['meme'])
  async def get_meme(self, ctx):
        data = requests.get("https://meme-api.herokuapp.com/gimme/1").json()
        await ctx.send(data["memes"][0]["url"])

  @commands.command(aliases=['save'])
  async def add_note(self, ctx, key, *, val):
    if key not in db.keys():
      db[key] = val
      await ctx.send('Added note')

    else:
      await ctx.send(key + ' Key existed, if you want to override, use command `-override`')

  @commands.command(aliases=['override'])
  async def override_note(self, ctx, key, *,val): 
    if key not in db.keys():
      await ctx.send(key + ' This key does not exist, use command `-save` to create note')
    else:
      db[key] = val
      await ctx.send('Overridden note')
  @commands.command()
  async def notes(self, ctx):
    try:
      line = "Soooo, here are the notes I remember, to use them, type '>key': \n"
      for i in sorted(db.keys()):
        line += '\t' + '>' + i
        line += '\n'
      await ctx.send(line)
    except:
      await ctx.send('Empty notes')
  @commands.command(aliases=['remove'])
  async def remove_note(self, ctx, key):
    if key in db.keys():
      del db[key]
      await ctx.send('Removed note')

    else:
      await ctx.send('I can\'t find that note, typo?')
  
  
  @commands.command()
  async def shout(self, ctx, *, word):
    msg = word
    e = ''
    space = ' '

    for a in msg:
        e += a + ' '
    e += '\n'
    index = 1
    for i in msg[1:]:
        e += i + space*index*4 + i + '\n'
        index += 1
    await ctx.channel.send(e) 
  @commands.command()
  async def ping(self, ctx, member:discord.User, *, word):
    await member.send(f'{ctx.author} pinged you: {word}')
    await ctx.send('Pinged, I\'m annoying')
#Functions
async def dl(self, ctx, val):
  await ctx.channel.purge(limit=val+1)

def setup(client):
  client.add_cog(Commands(client))