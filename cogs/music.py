import asyncio
import discord
from discord.ext import commands
import DiscordUtils
from discord.ext.commands.core import command
from youtubesearchpython import VideosSearch
from types import SimpleNamespace

music = DiscordUtils.Music()

players = {}

search_q = []


class MusicInfo():
    name = ''
    img_url = ''
    duration = ''
    url = ''
    view = ''
    channel = ''
    requester = ''


m = MusicInfo()


def d_embed(song_name, view, channel, duration, requester, img,
            color=discord.Color.dark_gold(), command='Playing'):
    embed = discord.Embed(title=f'{command} **{song_name}**', color=color,
                          description=f'{view} - {channel} | {duration}\n' + f'Requested by {requester}')
    embed.set_author(name='YouTube')
    embed.set_thumbnail(url=img)
    return embed


async def playm(ctx, songname):
    try:
        video_search = VideosSearch(songname, limit=1)
        result = SimpleNamespace(**video_search.result()).result
        url = result[0]['link']
        img = result[0]['thumbnails'][0]['url']
        title = result[0]['accessibility']['title']
        title = title[:title.index("by")]
        view = result[0]['viewCount']['short']
        dur = result[0]['duration']
        channel_name = result[0]['channel']['name']
        requester = ctx.message.author.name
        player = music.get_player(guild_id=ctx.guild.id)

        try:
            if not player:
                player = music.create_player(ctx,
                                             ffmpeg_error_betterfix=True)
            if not ctx.voice_client.is_playing():
                await player.queue(url, search=True)
                player.on_play(setmusic(name=title, img_url=img, duration=dur,
                                        view=view, channel=channel_name, requester=requester, url=url))
                # player.on_stop()
                await player.play()
                embed = d_embed(m.name, m.view, m.channel, m.duration, m.requester,
                                m.img_url, color=discord.Color.blue())
                await ctx.send(embed=embed)
            else:
                await player.queue(url, search=True)
                embed = d_embed(title, view, channel_name, dur, requester,
                                img, command='Queued', color=discord.Color.blurple())
                await ctx.send(embed=embed)
        except DiscordUtils.NotConnectedToVoice:
            try:
                await ctx.author.voice.channel.connect()
                await playm(ctx=ctx, songname=songname)
            except AttributeError:
                await ctx.send("You have to join a voice channel first")
    except Exception as e:
        await ctx.send(e)


class Music(commands.Cog):
    "Chillin' commands"

    def __init__(self, client):
        self.client = client

    @commands.command(help="Join the audio server from which the user called")
    async def join(self, ctx):
        try:
            await ctx.author.voice.channel.connect()
        except discord.ClientException:
            await ctx.send("I'm already in...")
        except AttributeError:
            await ctx.send("You have to join a voice channel first")

    @commands.command(help="Leave the previously joined audio server")
    async def leave(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        if player:
            await ctx.send("Stopping song...")
            await player.stop()
        try:
            await ctx.voice_client.disconnect()
            await ctx.send("I'm out, what a nice music session")
        except AttributeError:
            await ctx.send("I'm not in any channel")

    @commands.command(help="Play the first song with specified name on YouTube", aliases=["p"])
    async def play(self, ctx, *, songname):
        try:
            n = int(songname)
            title = search_q[n-1]
            title = title[:title.index("by")]
            await playm(ctx=ctx, songname=title)
        except Exception:
            await playm(ctx=ctx, songname=songname)

    @commands.command(help="Pause currently playing song")
    async def pause(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        if player:
            song = await player.pause()
            await ctx.send(f"Paused {song.name}")
        else:
            await ctx.send("Not playing anything")

    @commands.command(help="Resume currently playing song")
    async def resume(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        if player:
            song = await player.resume()
            await ctx.send(f"Resumed {song.name}")
        else:
            await ctx.send("Not playing anything")

    @commands.command(help="Stop the player")
    async def stop(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        if player:
            await player.stop()
            await ctx.send("Stopped")
        else:
            await ctx.send("Not playing anything")

    @commands.command(help="Loop currently playing song")
    async def loop(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        if player:
            song = await player.toggle_song_loop()
            if song.is_looping:
                await ctx.send(f"Enabled loop for {song.name}")
            else:
                await ctx.send(f"Disabled loop for {song.name}")
        else:
            await ctx.send("Not playing anything")

    @commands.command(help="Show queued songs", aliases=["q"])
    async def queue(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        if player:
            songs = ''
            i = 0
            for song in player.current_queue():
                songs += f"{i + 1}. " + song.name + '\n'
                i += 1
            try:
                await ctx.send(songs)
            except Exception:
                await ctx.send("Empty queue")
        else:
            await ctx.send("Not playing anything")

    @commands.command(help="Info of currently playing song", aliases=['np'])
    async def now_playing(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        if player:
            try:
                now = player.current_queue()[0]
                await ctx.send(now.name)
            except Exception:
                await ctx.send("Not playing anything")
        else:
            await ctx.send("Not playing anything")

    @commands.command(help="Skip currently playing song", aliases=["sk"])
    async def skip(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        if player:
            data = await player.skip(force=True)
            await ctx.send(f"Skipped {data[0].name}")
        else:
            await ctx.send("Not playing anything")

    @commands.command(help="Change the volume of song", aliases=['vol'])
    async def volume(self, ctx, vol):
        player = music.get_player(guild_id=ctx.guild.id)
        if player:
            song, volume = await player.change_volume(
                float(vol) / 100)  # volume should be a float between 0 to 1
            await ctx.send(f"Changed volume for `{song.name}` to {volume*100}%")
        else:
            await ctx.send("Not playing anything")

    @commands.command(help="Remove queued song corresponding to the index", aliases=['rm'])
    async def remove(self, ctx, *, index):
        player = music.get_player(guild_id=ctx.guild.id)
        if player:
            index = int(index)
            song = await player.remove_from_queue(index - 1)
            await ctx.send(f"Removed {song.name}\n from queue")
        else:
            await ctx.send("Not playing anything")

    @commands.command(help="Return first 10 songs from YouTube")
    async def song(self, ctx, *, keyword='NULL'):
        n = 10
        search_q.clear()
        video_search = VideosSearch(keyword, limit=n)
        result = SimpleNamespace(**video_search.result()).result
        try:
            pages = len(result)
            cur_page = 1
            i = 0
            img = result[i]['thumbnails'][0]['url']
            title = result[i]['accessibility']['title']
            view = result[i]['viewCount']['short']
            dur = result[i]['duration']
            search_q.append(title)
            channel_name = result[i]['channel']['name']
            embed = discord.Embed(title=f'**{title[:title.index("by")]}**', color=discord.Color.dark_gold(),
                                  description=f'{view} - {channel_name} | {dur} Page {i + 1}/{pages}')
            embed.set_author(name='YouTube')
            embed.set_thumbnail(url=img)
            message = await ctx.send(embed=embed)
            # getting the message object for editing and reacting

            await message.add_reaction("◀️")
            await message.add_reaction("▶️")

            def check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ["◀️", "▶️"]
                # This makes sure nobody except the command sender can interact with the "menu"

            while True:
                try:
                    reaction, user = await self.client.wait_for("reaction_add", timeout=60, check=check)
                    # waiting for a reaction to be added - times out after x seconds, 60 in this
                    # example

                    if str(reaction.emoji) == "▶️" and cur_page != pages:
                        cur_page += 1
                        i = cur_page-1
                        img = result[i]['thumbnails'][0]['url']
                        title = result[i]['accessibility']['title']
                        view = result[i]['viewCount']['short']
                        dur = result[i]['duration']
                        search_q.append(title)
                        channel_name = result[i]['channel']['name']
                        embed = discord.Embed(title=f'**{title[:title.index("by")]}**', color=discord.Color.dark_gold(),
                                              description=f'{view} - {channel_name} | {dur} Page {i + 1}/{pages}')
                        embed.set_author(name='YouTube')
                        embed.set_thumbnail(url=img)
                        await message.edit(embed=embed)
                        await message.remove_reaction(reaction, user)

                    elif str(reaction.emoji) == "◀️" and cur_page > 1:
                        cur_page -= 1
                        i = cur_page-1
                        img = result[i]['thumbnails'][0]['url']
                        title = result[i]['accessibility']['title']
                        view = result[i]['viewCount']['short']
                        dur = result[i]['duration']
                        search_q.append(title)
                        channel_name = result[i]['channel']['name']
                        embed = discord.Embed(title=f'**{title[:title.index("by")]}**', color=discord.Color.dark_gold(),
                                              description=f'{view} - {channel_name} | {dur} Page {i + 1}/{pages}')
                        embed.set_author(name='YouTube')
                        embed.set_thumbnail(url=img)
                        await message.edit(embed=embed)
                        await message.remove_reaction(reaction, user)

                    else:
                        await message.remove_reaction(reaction, user)
                        # removes reactions if the user tries to go forward on the last page or
                        # backwards on the first page
                except asyncio.TimeoutError:
                    await message.delete()
                    break
        # ending the loop if user doesn't react after x seconds
        except IndexError:
            await ctx.send('Error')


def setmusic(name, img_url, duration, view, channel, requester, url):
    m.img_url = img_url
    m.duration = duration
    m.view = view
    m.channel = channel
    m.requester = requester
    m.url = url
    m.name = name


def setup(client):
    client.add_cog(Music(client))
