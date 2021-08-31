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
    async def create(self, ctx, *command):
        try:
            if (command[0] == "-c"):
                colour = command[1]
                if len(colour) != 6:
                    await ctx.send(len(colour))
                    await ctx.send('Please specify colour code after -c flag (without #)\n`-create -c "colour" "name"`')
                    await ctx.send('https://preview.redd.it/941j8bdlc6251.png?auto=webp&s=3e5b5c17beaf5c54d0b53c99483f308f8aaad663')
                    return
                name = ' '.join(command[2:])
            else:
                colour = '99aab5'
                name = ' '.join(command[0:])
        except IndexError:
            await ctx.send('Please specify colour code after -c flag (without #)\n`-create -c "colour" "name"`')
            await ctx.send('https://preview.redd.it/941j8bdlc6251.png?auto=webp&s=3e5b5c17beaf5c54d0b53c99483f308f8aaad663')
            return
        col = discord.Colour(value=int(colour, 16))
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
        val = int(val)
        await ctx.channel.purge(limit=val+1)
        if not silence:
            await ctx.send(f'Purged {val} message(s)')



def setup(client):
    client.add_cog(Admin(client))
