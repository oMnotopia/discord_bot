import discord
from discord.ext import commands
from jokes import jokes
import os
import random
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents().all()

bot = commands.Bot(command_prefix="!", intents=intents)
token = os.getenv('TOKEN')


@bot.event
async def on_ready():
    print("Logged in as a bot, {0.user}".format(bot))


@bot.event
async def on_message(message):
    user_message = str(message.content)

    if user_message.lower() == 'turd':
        print()


@bot.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    print(f'Message {user_message} by {username} on {channel}')

    if message.author == bot.user:
        return

    if channel == "general":
        if user_message.lower() == "hello" or user_message.lower() == "hi":
            await message.channel.send(f'Hello {username}')
        elif user_message.lower() == "bye":
            await message.channel.send(f'Bye {username}')
        elif user_message.lower() == "tell me a joke":
            await message.channel.send(random.choice(jokes))

bot.run(token)
