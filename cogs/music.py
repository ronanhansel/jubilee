import discord
from discord.ext import commands
import DiscordUtils
from youtubesearchpython import VideosSearch
from types import SimpleNamespace

music = DiscordUtils.Music()

players = {}

search_q = []

search_q_img = []

class Music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        try:
            await ctx.author.voice.channel.connect()
        except discord.ClientException: 
            await ctx.send("I'm already in...")
        except AttributeError:
            await ctx.send("You have to join a voice channel first")

    @commands.command()
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

    @commands.command()
    async def play(self, ctx, *, songname):
        await ctx.send("Gimme a sec...")
        try:
            videosSearch = VideosSearch(songname, limit=1)
            result = SimpleNamespace(**videosSearch.result())
            url = result.result[0]['link']
            img = result.result[0]['thumbnails'][1]['url']
            player = music.get_player(guild_id=ctx.guild.id)
            try:
                if not player:
                    player = music.create_player(ctx,
                                                 ffmpeg_error_betterfix=True)
                if not ctx.voice_client.is_playing():
                    await player.queue(url, search=True)
                    song = await player.play()
                    embed = discord.Embed(title=f'Playing **{song.name}**',
                                          description='As your request')
                    embed.set_author(name='YouTube')
                    embed.set_thumbnail(url=img)
                    await ctx.send(embed=embed)
                else:
                    song = await player.queue(url, search=True)
                    embed = discord.Embed(title=f'Queued **{song.name}**',
                                          description='As your request')
                    embed.set_author(name='YouTube')
                    embed.set_thumbnail(url=img)
                    await ctx.send(embed=embed)
            except DiscordUtils.NotConnectedToVoice:
                await ctx.send(
                    "Not connected to any voice channel, lemme join...")
                try:
                    await ctx.author.voice.channel.connect()
                    await ctx.send("Aight, try again")
                except AttributeError:
                    await ctx.send("You have to join a voice channel first")
        except Exception as e:
            print(e)
            await ctx.send('Error, try another keyword or song')

    @commands.command()
    async def pause(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        if player:
            song = await player.pause()
            await ctx.send(f"Paused {song.name}")
        else:
            await ctx.send("Not playing anything")

    @commands.command()
    async def resume(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        if player:
            song = await player.resume()
            await ctx.send(f"Resumed {song.name}")
        else:
            await ctx.send("Not playing anything")

    @commands.command()
    async def stop(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        if player:
            await player.stop()
            await ctx.send("Stopped")
        else:
            await ctx.send("Not playing anything")

    @commands.command()
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

    @commands.command()
    async def queue(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        if player:
            songs = ''
            i = 0
            for song in player.current_queue():
                songs += f"{i}. " + song.name + '\n'
                i += 1
            await ctx.send(songs)
        else:
            await ctx.send("Not playing anything")

    @commands.command()
    async def now_playing(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        if player:
            song = player.now_playing()
            await ctx.send(song.name)
        else:
            await ctx.send("Not playing anything")

    @commands.command()
    async def skip(self, ctx):
        player = music.get_player(guild_id=ctx.guild.id)
        if player:
            data = await player.skip(force=True)
            await ctx.send(f"Skipped {data[0].name}")
        else:
            await ctx.send("Not playing anything")

    @commands.command()
    async def volume(self, ctx, vol):
        player = music.get_player(guild_id=ctx.guild.id)
        if player:
            song, volume = await player.change_volume(
                float(vol) / 100)  # volume should be a float between 0 to 1
            await ctx.send(f"Changed volume for {song.name} to {volume*100}%")
        else:
            await ctx.send("Not playing anything")

    @commands.command()
    async def remove_q(self, ctx, index):
        player = music.get_player(guild_id=ctx.guild.id)
        if player:
            song = await player.remove_from_queue(int(index))
            await ctx.send(f"Removed {song.name} from queue")
        else:
            await ctx.send("Not playing anything")

    

    @commands.command()
    async def search(self, ctx, n=3, *, keyword):
      search_q.clear()
      search_q_img.clear()
      videosSearch = VideosSearch(keyword, limit=n)
      result = SimpleNamespace(**videosSearch.result()).result
      try:
        for i in range(0, len(result)):
            img = result[i]['thumbnails'][1]['url']
            title = result[i]['accessibility']['title']
            view = result[i]['viewCount']['short']
            url = result[i]['link']
            search_q.append(url)
            search_q_img.append(img)
            channel_name = result[0]['channel']['name']
            embed = discord.Embed(title=f'**{title[:title.index("by")]}**',
                                  description=f'{view} - {channel_name}')
            embed.set_author(name='YouTube')
            embed.set_thumbnail(url=img)
            await ctx.send(embed=embed)
      except IndexError:
        await ctx.send('That\'s it lol, did you search something ... oddly specific 🙄?')
    @commands.command()
    async def play_search(self, ctx, n):
      n = int(n)
      await ctx.send('Gimme me a sec...')
      url = search_q[n-1]
      img = search_q_img[n-1]
      player = music.get_player(guild_id=ctx.guild.id)
      try:
          if not player:
              player = music.create_player(ctx,
                                            ffmpeg_error_betterfix=True)
          if not ctx.voice_client.is_playing():
              await player.queue(url, search=True)
              song = await player.play()
              embed = discord.Embed(title=f'Playing **{song.name}**',
                                    description='As your request')
              embed.set_author(name='YouTube')
              embed.set_thumbnail(url=img)
              await ctx.send(embed=embed)
          else:
              song = await player.queue(url, search=True)
              embed = discord.Embed(title=f'Queued **{song.name}**',
                                    description='As your request')
              embed.set_author(name='YouTube')
              embed.set_thumbnail(url=img)
              await ctx.send(embed=embed)
      except DiscordUtils.NotConnectedToVoice:
          await ctx.send(
              "Not connected to any voice channel, lemme join...")
          try:
              await ctx.author.voice.channel.connect()
              await ctx.send("Aight, try again")
          except AttributeError:
              await ctx.send("You have to join a voice channel first")

  


def setup(client):
    client.add_cog(Music(client))
