import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
load_dotenv()
intents=discord.Intents.default()
intents.members=True

Bot=commands.Bot(command_prefix='/', intents=intents)

TOKEN=os.getenv("DISCORD_BOT_TOKEN")