import discord
from discord.ext import commands
import data.note

note = data.note


class Admin(commands.Cog):
    "Admin-permitted commands"

    def __init__(self, client):
        self.client = client
    @commands.command(help="Give someone a role")
    @commands.has_permissions(administrator=True)
    async def promote(self, ctx, member: discord.Member, *, name):
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role:
            await member.add_roles(role)
            await ctx.send(f"Added role for {member} - {role}")
        else:
            await ctx.send("The role does not exist")

    @commands.command(help="Remove someone from a role")
    @commands.has_permissions(administrator=True)
    async def demote(self, ctx, member: discord.Member, *, name):
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role:
            await member.remove_roles(role)
            await ctx.send(f"Removed role from {member} - {role}")
        else:
            await ctx.send("The role does not exist")

    @commands.command(help="Create a role")
    @commands.has_permissions(administrator=True)
    async def create(self, ctx, colour='#1cebe1', *, name):
        col = discord.Colour(value=int(colour[1:], 16))
        role = discord.utils.get(ctx.guild.roles, name=name)
        if not role:
            guild = ctx.guild
            await guild.create_role(name=name, colour=col)
            await ctx.send(f"Created role {name}")
        else:
            await ctx.send("The role is there")

    @commands.command(help="Remove a role")
    @commands.has_permissions(administrator=True)
    async def destroy(self, ctx, *, name):
        role = discord.utils.get(ctx.guild.roles, name=name)
        if role:
            await role.delete()
            await ctx.send(f"Role {name} is now gone muahahaha")
        else:
            await ctx.send("The role is not there")

    @commands.command(help="Delete messages")
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, val, silence=True):
        await dl(self, ctx, int(val))
        if not silence:
            await ctx.send(f'Purged {val} message(s)')

    @commands.command(help="Using bot to message")
    @commands.has_permissions(administrator=True)
    async def speak(self, ctx, *, word):
        await ctx.message.delete()
        await ctx.send(word)
    @commands.command(help="Add note for server")
    @commands.has_permissions(administrator=True)
    async def note_server(self, ctx, key, *, val):
        _id = "_s" + str(ctx.message.guild.id)
        try:
            note.create_table(_id)
            if not note.check_table(_id, key)[0]:
                note.insert_note(_id, key, val)
                await ctx.send('Got it!')
            else:
                await ctx.send('Note existed, to change value use `change`')
        except Exception:
            note.create_table(_id)
            await ctx.send('I have just created a storage for this instance, try again')
    @commands.command(help="Delete note server")
    @commands.has_permissions(administrator=True)
    async def forget_server(self, ctx, key):
        _id = "_s" + str(ctx.message.guild.id)
        if not note.check_table(_id, key):
            await ctx.send(key + ' This key does not exist, use command `note` to create note')
        else:
            note.remove_note(_id, key)
            await ctx.send('Ooops i forgot it, server edition')

# Functions


async def dl(self, ctx, val):
    await ctx.channel.purge(limit=val+1)


def setup(client):
    client.add_cog(Admin(client))
