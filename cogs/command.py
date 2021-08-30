import discord
import json
import random
import requests
import data.note
from discord.ext import commands

note = data.note

class Command(commands.Cog):
    "The commands anyone can use"

    def __init__(self, client):
        self.client = client
    # Commands

    @commands.command(help="Get entertained by memes on reddit")
    async def meme(self, ctx):
        data = requests.get("https://meme-api.herokuapp.com/gimme/1").json()
        await ctx.send(data["memes"][0]["url"])

    @commands.command(help="Flirt!")
    async def flirt(self, ctx):
        data = json.load(open("./data/quotes.json"))
        await ctx.send(data[random.randint(0,len(data))])

    @commands.command(help="Add note for yourself")
    async def note(self, ctx, key, *, val):
        _id = "_" + str(ctx.message.author.id)
        note.create_table(_id)
        if not note.check_table(_id, key)[0]:
            note.insert_note(_id, key, val)
            await ctx.send('Got it!')
        else:
            await ctx.send('Note existed, to change value use `change`')

    @commands.command(help="Change note")
    async def change(self, ctx, key, *, val):
        _id = "_" + str(ctx.message.author.id)
        if not note.check_table(_id, key):
            await ctx.send(key + ' This key does not exist, use command `note` to create note')
        else:
            note.change_note(_id, key, val)
            await ctx.send('Overridden note')

    @commands.command(help="List all notes")
    async def notes(self, ctx, option='me'):
        _id = "_" + str(ctx.message.author.id)
        _prefix = ">"
        try:
            line = "Soooo, here are the notes I remember, to use them, type '{}key': \n".format(_prefix)
            keys = [i[0] for i in note.get_note_all(_id)]
            if len(keys) >= 1:
              for i in sorted(keys):
                  line += '\t' + _prefix + i
                  line += '\n'
              await ctx.send(line)
            else:
              await ctx.send('Empty note')
        except Exception:
            await ctx.send('Empty note')

    @commands.command(help="Delete note")
    async def forget(self, ctx, key):
        _id = "_" + str(ctx.message.author.id)
        if not note.check_table(_id, key):
            await ctx.send(key + ' This key does not exist, use command `note` to create note')
        else:
            note.remove_note(_id, key)
            await ctx.send('Ooops i forgot it')

    @commands.command(help="Make your voice heard")
    async def shout(self, ctx, *, word):
        msg = word
        e = ''
        space = ' '
        for a in msg:
            e += a + '   '
        e += '\n'
        index = 1
        for i in msg[1:]:
            e += i + space*index*4 + i + '\n'
            index += 1
        await ctx.channel.send(e)

    @commands.command(help="Be annoying and blame it to the bot")
    async def ping(self, ctx, member: discord.User, *, word):
        await member.send(f'{ctx.author} pinged you: {word}')
        await ctx.send('Pinged, I\'m annoying')


# Functions
async def dl(self, ctx, val):
    await ctx.channel.purge(limit=val+1)

def setup(client):
    client.add_cog(Command(client))
