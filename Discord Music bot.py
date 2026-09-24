import discord
from discord.ext import commands
from collections import deque
import yt_dlp
import asyncio

intents = discord.Intents.default()
intents.message_content = True
song_que = deque()
is_playing = False
ffmpeg_path = "E:\\ffmpeg-7.1.1-essentials_build\\ffmpeg-7.1.1-essentials_build\\bin\\ffmpeg.exe"

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


@bot.command()
async def join(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

    if ctx.author.voice:
        await ctx.author.voice.channel.connect()
        await ctx.send('Who is ready for some music?')
    else:
        await ctx.send('You must be in a voice channel!')


@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Good bye!")
    else:
        await ctx.send("I'm not in a voice channel!")


@bot.command()
async def play(ctx, *, query):
    global is_playing

    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True,
        'default_search': 'ytsearch',
        'noplaylist': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(query, download=False)
            if 'entries' in info:
                info = info['entries'][0]
            title = info.get('title', 'Unknown Title')
            url = info['url']
        except Exception as e:
            await ctx.send(f"Error fetching audio: {e}")
            return

    song = {
        'title': title,
        'url': url,
        'ctx': ctx
    }

    song_que.append(song)
    await ctx.send(f"Added to queue: {title}")

    if not is_playing and not ctx.voice_client.is_playing():
        await play_next()


async def play_next():
    global is_playing

    if not song_que:
        is_playing = False
        return

    song = song_que.popleft()
    ctx = song.get('ctx')
    if ctx is None:
        is_playing = False
        return

    url = song['url']
    title = song['title']
    voice_client = ctx.voice_client

    # Ensure the bot is connected to the voice channel
    if voice_client is None or not voice_client.is_connected():
        if ctx.author.voice:
            try:
                voice_client = await ctx.author.voice.channel.connect()
            except discord.ClientException:
                voice_client = ctx.voice_client  # Reuse
            except Exception as e:
                await ctx.send(f"Failed to connect to voice: {e}")
                is_playing = False
                return
        else:
            await ctx.send("You're not in a voice channel.")
            is_playing = False
            return

    ffmpeg_opts = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 1 -reconnect_at_eof 1',
        'options': '-vn'
    }

    try:
        source = await discord.FFmpegOpusAudio.from_probe(
            url, **ffmpeg_opts, method='fallback', executable=ffmpeg_path
        )

        def after_playing(error):
            fut = asyncio.run_coroutine_threadsafe(play_next(), bot.loop)
            try:
                fut.result()
            except Exception as e:
                print(f"Error in after_playing: {e}")

        voice_client.play(source, after=after_playing)
        await ctx.send(f"Now playing: {title}")
        is_playing = True  # Set playing state
    except Exception as e:
        await ctx.send(f"Error playing audio: {e}")
        is_playing = False


@bot.command()
#FIX ME MAKE IT END QUE
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Stopped the music.")


@bot.command()
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Skipping song.")

    elif song_que:
        await play_next()
    else:
        await ctx.send("End of queue.")


@bot.command()
async def queue(ctx):
    if not song_que:
        await ctx.send("The queue is empty.")
        return

    msg = "\n".join(
        [f"{i+1}. {song['title']}" for i, song in enumerate(song_que)]
    )
    await ctx.send("Queue:\n" + msg)


bot.run()