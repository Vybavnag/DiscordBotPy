from cProfile import label
from email import message
from operator import truediv
import queue
from aiohttp import ClientRequest
import discord
import os
import asyncio
import youtube_dl

# creating intents allowing the bot to perform its task
intent = discord.Intents.default()
intent.members = True
intent.message_content = True

# hidden token
token = "Hidden toke"

# creating the client for the bot
client = discord.Client(intents=intent)

# voice client
voice_clients = {}
yt_dl_opts = {'format': 'bestaudio/best'}
ytdl = youtube_dl.YoutubeDL(yt_dl_opts)

# importing ffmpeg
ffmpeg_options = {'options': "-vn"}

# words to delete from users
# can add any words that you dont want people to say or spam
block_words = ["Bad word", "http://", "https://"]


# starts up the bot
@client.event
async def on_ready():
    print(f"Bot logged in as {client.user}")


# responds to user messages
@client.event
async def on_message(msg):

    # displays all the functions the bot can do
    if msg.author != client.user and msg.content.startswith("?commands"):
        try:
            await msg.channel.send(f'''?hi says hi to you
?play https:// for playing youtube links only
?pause pauses the current song
?resume resumes the song
?stop stops the song and leaves
everything is CASE SENSITIVE''')
        except:
            print("error")

    # command for playing a song
    if msg.author != client.user and msg.content.startswith("?play"):

        # connects the bot to the voice chat can play mutliple songs
        try:
            voice_client = await msg.author.voice.channel.connect()
            voice_clients[voice_client.guild.id] = voice_client
        except:
            print("error")

        # plays the song
        try:
            url = msg.content.split()[1]
            loop = asyncio.get_event_loop()

            data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=False))

            song = data['url']
            player = discord.FFmpegPCMAudio(
                song, **ffmpeg_options, executable="C:\\ffmpeg\\bin\\ffmpeg.exe")

            voice_clients[msg.guild.id].play(player)
        except Exception as err:
            print(err)

    # command for pauseing a song
    if msg.author != client.user and msg.content.startswith("?pause"):
        try:
            voice_clients[msg.guild.id].pause()
        except Exception as err:
            print(err)

    # command for resuming a song
    if msg.author != client.user and msg.content.startswith("?resume"):
        try:
            voice_clients[msg.guild.id].resume()
        except Exception as err:
            print(err)

    # command for stoping a song
    if msg.author != client.user and msg.content.startswith("?stop"):
        try:
            voice_clients[msg.guild.id].stop()
            # disconnects the bot
            await voice_clients[msg.guild.id].disconnect()
        except Exception as err:
            print(err)

    if msg.author != client.user and msg.author != client.user:
        for text in block_words:
            # instead of 1 You can use any moderator role name
            if "1" not in str(msg.author.roles) and text in str(msg.content.lower()):
                await msg.delete()
                return
        if msg.content.lower().startswith("?hi"):
            await msg.channel.send(f"Hi,{msg.author.display_name}")

client.run(token)
