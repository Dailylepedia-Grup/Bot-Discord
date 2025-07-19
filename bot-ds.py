import discord
from dotenv import load_dotenv
load_dotenv()
from discord.ext import commands
from yt_dlp import YoutubeDL
import asyncio
import os
import requests

# === CONFIG ===
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

queues = {}
loop_status = {}
audio_effects = {}

# === Load YouTube cookies from browser ===
def get_browser_cookies():
    try:
        return cookies.load_cookies("chrome")  # Ganti ke "firefox" jika pakai Firefox
    except Exception as e:
        print(f"Gagal ambil cookie dari browser: {e}")
        return None

# === Custom FFMPEG options per guild ===
def get_ffmpeg_options(guild_id):
    base = "-vn"
    effects = audio_effects.get(guild_id, "")
    return {
        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
        "options": f"{base} {effects}".strip()
    }

# === YouTubeDL Config ===
YTDL_OPTIONS = {
    "format": "bestaudio/best",
    "noplaylist": True,
    "quiet": True,
    "extractaudio": True,
    "audioformat": "mp3",
}

ytdl = YoutubeDL(YTDL_OPTIONS)

# === Helper ===
def play_next(ctx, guild_id):
    if guild_id in loop_status and loop_status[guild_id]:
        ctx.voice_client.play(ctx.voice_client.source, after=lambda e: play_next(ctx, guild_id))
    elif guild_id in queues and queues[guild_id]:
        source, title = queues[guild_id].pop(0)
        ctx.voice_client.play(source, after=lambda e: play_next(ctx, guild_id))

async def join_channel(ctx):
    if ctx.author.voice:
        await ctx.author.voice.channel.connect()

# === Commands ===
@bot.command()
async def join(ctx):
    await join_channel(ctx)

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()

@bot.command()
async def play(ctx, *, query: str):
    if not ctx.voice_client:
        await join_channel(ctx)

    try:
        if "youtube.com" in query or "youtu.be" in query:
            info = ytdl.extract_info(query, download=False)
        else:
            info = ytdl.extract_info(f"ytsearch:{query}", download=False)

        video = info['entries'][0] if 'entries' in info else info
        url = video["url"]
        title = video["title"]

        source = discord.FFmpegPCMAudio(url, **get_ffmpeg_options(ctx.guild.id))

        guild_id = ctx.guild.id
        if ctx.voice_client.is_playing():
            if guild_id not in queues:
                queues[guild_id] = []
            queues[guild_id].append((source, title))
            await ctx.send(f"✅ **{title}** ditambahkan ke antrian.")
        else:
            ctx.voice_client.play(source, after=lambda e: play_next(ctx, guild_id))
            await ctx.send(f"🎶 Sekarang memutar: **{title}**")

    except Exception as e:
        await ctx.send(f"⚠️ Gagal memutar lagu: {str(e)}")

@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("⏸️ Lagu dijeda.")

@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("▶️ Lagu dilanjutkan.")

@bot.command()
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏭️ Lagu di-skip.")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        queues[ctx.guild.id] = []
        ctx.voice_client.stop()
        await ctx.send("🛑 Playback dihentikan & antrian dikosongkan.")

@bot.command()
async def bassboost(ctx, intensity: int = 10):
    audio_effects[ctx.guild.id] = f"-af equalizer=f=40:width_type=o:width=2:g={intensity}"
    await ctx.send(f"🔊 Bassboost diaktifkan dengan intensitas {intensity}.")

@bot.command()
async def nightcore(ctx):
    audio_effects[ctx.guild.id] = "-af asetrate=44100*1.25,aresample=44100"
    await ctx.send("✨ Nightcore effect diaktifkan.")

@bot.command()
async def queue(ctx):
    guild_id = ctx.guild.id
    if guild_id in queues and queues[guild_id]:
        await ctx.send("📜 **Antrian lagu:**\n" + "\n".join([f"{i+1}. {title}" for i, (_, title) in enumerate(queues[guild_id])]))
    else:
        await ctx.send("❌ Tidak ada lagu dalam antrian.")

@bot.command()
async def remove(ctx, index: int):
    guild_id = ctx.guild.id
    if guild_id in queues and 0 <= index-1 < len(queues[guild_id]):
        _, title = queues[guild_id].pop(index-1)
        await ctx.send(f"🗑️ Lagu **{title}** dihapus dari antrian.")
    else:
        await ctx.send("⚠️ Indeks tidak valid atau antrian kosong.")

@bot.command()
async def loop(ctx):
    guild_id = ctx.guild.id
    loop_status[guild_id] = not loop_status.get(guild_id, False)
    status = "✅ aktif" if loop_status[guild_id] else "❌ non-aktif"
    await ctx.send(f"🔁 Loop sekarang {status}.")

@bot.command()
async def volume(ctx, level: int):
    if ctx.voice_client and 0 <= level <= 200:
        ctx.voice_client.source = discord.PCMVolumeTransformer(ctx.voice_client.source)
        ctx.voice_client.source.volume = level / 100
        await ctx.send(f"🔊 Volume diatur ke {level}%.")
    else:
        await ctx.send("⚠️ Volume harus di antara 0 dan 200.")

@bot.command()
async def lyrics(ctx, *, title: str):
    try:
        response = requests.get(f"https://api.lyrics.ovh/v1/{title}")
        data = response.json()
        lyrics = data.get("lyrics", "Lyrics not found.")
        await ctx.send(lyrics[:2000])
    except Exception as e:
        await ctx.send(f"⚠️ Gagal mengambil lirik: {str(e)}")

# === Auto cleanup if bot is disconnected ===
@bot.event
async def on_voice_state_update(member, before, after):
    if member == bot.user and after.channel is None:
        guild_id = before.channel.guild.id
        queues.pop(guild_id, None)
        loop_status.pop(guild_id, None)
        audio_effects.pop(guild_id, None)

# === Run Bot ===
bot.run(os.getenv("DISCORD_TOKEN"))  # Token dari environment variable
