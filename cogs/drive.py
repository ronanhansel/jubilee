from discord.ext import commands
from drive_get import create
# ↳


class Drive(commands.Cog):
    "For Google Drive intergration"

    def __init__(self, client):
        self.client = client

    @commands.command(help="Add folder to Google Drive")
    async def folder(self, ctx, *, folder):
        create(folder)
        mess = 'Created in Juvenile Project folder: \n Juvenile Project'
        d = 0
        for i in folder.split("/"):
            if i[0] == "&":
                for a in i[1:].split(".."):
                    mess += "\n" + "\t" * d + "↳" + a
            else:
                mess += "\n" + "\t" * d + "↳" + i
            d += 2
        await ctx.send(mess)


def setup(client):
    client.add_cog(Drive(client))
