import discord
from discord.ext import commands

class Admins(commands.Cog):
  def __init__(self, client):
    self.client = client
  # try:
  #   admin = db['admin']
  # except Exception as e: 
  admin = 'Bee boo peep'
    # print(e)
  #For admins
  @commands.command()
  @commands.has_role(admin)
  async def promote(self, ctx, member: discord.Member, *, name):
    role = discord.utils.get(ctx.guild.roles, name=name)
    if role:
      await member.add_roles(role)
      await ctx.send(f"Added role for {member} - {role}")
    else: await ctx.send("The role does not exist")
  @commands.command()
  @commands.has_role(admin)
  async def demote(self, ctx, member: discord.Member, *, name):
    role = discord.utils.get(ctx.guild.roles, name=name)
    if role:
      await member.remove_roles(role)
      await ctx.send(f"Removed role from {member} - {role}")
    else: await ctx.send("The role does not exist")
  @commands.command()
  @commands.has_role(admin)
  async def create(self, ctx, colour='#1cebe1', *,name):
    col = discord.Colour(value= int(colour[1:], 16))
    role = discord.utils.get(ctx.guild.roles, name=name)
    if not role:  
      guild = ctx.guild
      await guild.create_role(name=name, colour=col)
      await ctx.send(f"Created role {name}")
    else:
      await ctx.send("The role is there")
  @commands.command()
  @commands.has_role(admin)
  async def destroy(self, ctx, *, name):
    role = discord.utils.get(ctx.guild.roles, name=name)
    if role:
      await role.delete()
      await ctx.send(f"Role {name} is now gone muahahaha")
    else:
      await ctx.send("The role is not there")
  @commands.command()
  @commands.has_role(admin)
  async def purge(self, ctx, val, silence=True):
    await dl(self, ctx, int(val))
    if not silence: await ctx.send(f'Purged {val} message(s)')
  @commands.command()
  @commands.has_role(admin)
  async def speak(self, ctx, *, word):
    await ctx.message.delete()
    await ctx.send(word)
    
#Functions
async def dl(self, ctx, val):
  await ctx.channel.purge(limit=val+1)


def setup(client):
  client.add_cog(Admins(client))