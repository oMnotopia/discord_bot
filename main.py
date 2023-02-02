import discord
from discord.ext import commands, tasks
from jokes import jokes
from list_of_banned_words import curseWords
import os
import random
from dotenv import load_dotenv
from dataclasses import dataclass

load_dotenv()

STUDYING_CHANNEL_ID = 1070770440525598751
MAX_SESSION_TIME = 45


@dataclass
class Session:
    is_active: bool = False
    start_time: int = 0
    stop_time: int = 0


intents = discord.Intents().all()

bot = commands.Bot(command_prefix='!', intents=intents)
token = os.getenv('TOKEN')

session = Session()


@bot.event
async def on_ready():
    # Ensures bot is working on run
    print("Logged in as a bot, {0.user}".format(bot))


@bot.command()
async def joke(ctx):
    channel = str(ctx.channel.name)
    if (channel == 'studying'):
        return

    await ctx.send(random.choice(jokes))


@bot.command()
async def start(ctx):
    channel = str(ctx.channel.name)
    if (channel != 'studying'):
        return

    if session.is_active:
        await ctx.send("A session is already started!")
        return

    # Starts break reminder execution
    break_reminder.start()

    session.is_active = True
    session.start_time = ctx.message.created_at.timestamp()
    human_readable_start_time = ctx.message.created_at.strftime("%H:%M:%S")
    await ctx.send(f'Sessions started at {human_readable_start_time}')


@bot.command()
async def stop(ctx):
    channel = str(ctx.channel.name)
    if (channel != 'studying'):
        return

    if not session.is_active:
        await ctx.send("A session is not started!")
        return

    # Stops break reminder execution
    break_reminder.stop()

    session.is_active = False
    session.stop_time = ctx.message.created_at.timestamp()
    human_readable_stop_time = ctx.message.created_at.strftime("%H:%M:%S")
    await ctx.send(f'Sessions stopped at {human_readable_stop_time}')


@tasks.loop(seconds=MAX_SESSION_TIME, count=17)
async def break_reminder():
    # Ignore the first execution because it happens instantly
    if break_reminder.current_loop == 0:
        return

    channel = bot.get_channel(STUDYING_CHANNEL_ID)
    await channel.send(f"**Take a break!** You have been studying for {MAX_SESSION_TIME*break_reminder.current_loop} minutes")


@bot.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    print(f'Message {user_message} by {username} on {channel}')

    if message.author == bot.user:
        return

    # Deletes messages that contain curse words
    if any(word in user_message.lower() for word in curseWords):
        await message.delete()

    await bot.process_commands(message)

bot.run(token)
