import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

from config import *
from commands import *
load_dotenv()

@Bot.event
async def on_ready():
    try:
     # await add_commands()
      synced=await Bot.tree.sync()
      print(f"Synced {len(synced)} command(s)")
      print(f"Bot is ready: {Bot.user}")
    except Exception as e:
       print(f"Error: {e}")

Bot.run(TOKEN)