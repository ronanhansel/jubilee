import discord
from discord.ext import commands
import data.note
import asyncio

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
    @commands.command(help="Be SPAMMY but you don't have to pay for it")
    @commands.has_permissions(administrator=True)
    async def spam(self, ctx, times, *, message):
        try:
            for i in range(0, int(times)):
                await ctx.send(message)
                await asyncio.sleep(1)
        except Exception:
            await ctx.send('Please specify number of messages')

    @commands.command(help="Mute annoying members")
    @commands.has_permissions(administrator=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        if member.permissions_in(ctx.message.channel).administrator:
            await ctx.message.channel.send("Sorry, I can't mute admins")
            return
        guild = ctx.guild
        muted_role = discord.utils.get(guild.roles, name="Muted")

        if not muted_role:
            muted_role = await guild.create_role(name="Muted")
            await muted_role.edit(position=2)
            for channel in guild.channels:
                await channel.set_permissions(muted_role, speak=False, send_messages=False, read_message_history=True, read_messages=True)
        embed = discord.Embed(title="Muted", description=f"{member.mention} was muted ", colour=discord.Colour.red())
        embed.add_field(name="Reason:", value=reason, inline=False)
        await ctx.send(embed=embed)
        await member.add_roles(muted_role, reason=reason)
        await member.send(f" you have been muted from: {guild.name} reason: {reason}")

    @commands.command(description="Unmutes a specified user")
    @commands.has_permissions(administrator=True)
    async def unmute(self, ctx, member: discord.Member):
        muted_role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(muted_role)
        await member.send(f" you have unmuted from: {ctx.guild.name}")
        embed = discord.Embed(title="Unmute", description=f" unmuted {member.mention}",colour=discord.Colour.green())
        await ctx.send(embed=embed)


    # @commands.command(help="Mute annoying members", aliases=["stfu"])
    # @commands.has_permissions(administrator=True)
    # async def mute(self, message, member: discord.Member):
    #     if member.permissions_in(message.channel).administrator:
    #         await message.channel.send("Sorry, I can't mute admins")
    #         return
    #     import json
    #     muted = json.load(open("./data/muted.json"))
    #     serverid = message.guild.id
    #     if not f"{serverid}" in muted.keys():
    #         muted[f"{serverid}"] = []
    #     if member.id in muted[f"{serverid}"]:
    #         await message.channel.send("User is already muted")
    #     else:
    #         muted[f"{serverid}"].append(member.id)
    #         json.dump(muted, open("./data/muted.json", "w"))
    #         await message.channel.send(f"Muted {member}")

    # @commands.command(help="Unmute someone")
    # @commands.has_permissions(administrator=True)
    # async def unmute(self, ctx, member: discord.Member):
    #     import json
    #     muted = json.load(open("./data/muted.json"))
    #     if member.id in muted[f"{ctx.message.guild.id}"]:
    #         muted[f"{ctx.message.guild.id}"].remove(member.id)
    #         json.dump(muted, open("./data/muted.json", "w"))
    #         await ctx.send(f"Unmuted {member}")
    #     else:
    #         await ctx.send("This member is not muted")

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member : discord.Member, *, reason):
        await member.ban(reason = reason)
        await ctx.send("Banned {} for \"{}\"".format(member.display_name(), reason))

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split("#")

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return
    
    @commands.command()
    @commands.has_permissions(administrator = True)
    async def kick(self, ctx, member: discord.User):
        await self.client.kick(member)
        await ctx.send("Kicked {}".format(member.display_name()))

def setup(client):
    client.add_cog(Admin(client))
