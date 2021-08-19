import os
import discord
from discord.ext import commands
from discord.ext.commands.core import check
import requests
import json
import data.note


note = data.note

class Commands(commands.Cog):
  def __init__ (self, client):
    self.client = client
  #Commands

  @commands.command()
  async def meme(self, ctx):
        data = requests.get("https://meme-api.herokuapp.com/gimme/1").json()
        await ctx.send(data["memes"][0]["url"])

  @commands.command()
  async def note(self, ctx, key, *, val):
    _id = "_" + str(ctx.message.guild.id)
    if os.path.exists('data/note.db'):
      try:
        if not note.check_table(_id, key)[0]:
          note.insert_note(_id, key, val)
          await ctx.send('Got it!')
        else: await ctx.send('Note existed, to change value use `change`')
      except Exception as e:
        note.create_table(_id)
        await ctx.send(e)
        await ctx.send('I have just created a storage for this server, try again')
    else:
      await ctx.send('Arghh, the database is not functioning, please give me some time, I will try to fix this ASAP')

  @commands.command()
  async def change(self, ctx, key, *,val): 
    _id = "_" + str(ctx.message.guild.id)
    if not note.check_table(_id, key):
      await ctx.send(key + ' This key does not exist, use command `note` to create note')
    else:
      note.change_note(_id, key, val)
      await ctx.send('Overridden note')
  @commands.command()
  async def notes(self, ctx):
    _id = "_" + str(ctx.message.guild.id)
    try:
      line = "Soooo, here are the notes I remember, to use them, type '>key': \n"
      keys = [i[0] for i in note.get_note_all(_id)]
      for i in sorted(keys):
        line += '\t' + '>' + i
        line += '\n'
      await ctx.send(line)
    except Exception as e:
      await ctx.send(e)
      await ctx.send('Empty notes')
  # @commands.command()
  # async def forget(self, ctx, key):
  #   _id = "_" + str(ctx.message.guild.id)
  #   if not note.check_table(_id, key):
  #     await ctx.send(key + ' This key does not exist, use command `note` to create note')
  #   else:
  #     note.remove_note(_id, key)
  #     await ctx.send('Ooops i forgot it')
  
  
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