import discord
from discord.ext import commands
from jokes import jokes
from list_of_banned_words import curseWords
import os
import random
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents().all()

bot = commands.Bot(command_prefix="!", intents=intents)
token = os.getenv('TOKEN')


@bot.event
async def on_ready():
    # Ensures bot is working on run
    print("Logged in as a bot, {0.user}".format(bot))


@bot.event
async def on_message(message):
    username = str(message.author).split("#")[0]
    channel = str(message.channel.name)
    user_message = str(message.content)

    print(f'Message {user_message} by {username} on {channel}')

    if message.author == bot.user:
        return

    # Bot responses to user inputs
    if channel == "general":
        if user_message.lower() == "hello" or user_message.lower() == "hi":
            await message.channel.send(f'Hello {username}')
        elif user_message.lower() == "bye":
            await message.channel.send(f'Bye {username}')
        elif user_message.lower() == "tell me a joke":
            await message.channel.send(random.choice(jokes))

    # Deletes messages that contain curse words
    if any(word in user_message for word in curseWords):
        await message.delete()

bot.run(token)
