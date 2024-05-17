## file with all the bot commands

import os, sys
import time
import json
import uuid
import socket
import discord
import asyncio
import traceback
import subprocess
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv

# For colorcoding purposes
from colorcode import cc as fxc
from colorcode import p as f
import discord.ext
fxc._init(0)

# Load config file
class Env:
    load_dotenv()
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    DISCORD_GUILD_ID = os.getenv('DISCORD_GUILD_ID')
    DISCORD_VERIFIED_ROLE_ID = os.getenv('DISCORD_VERIFIED_ROLE_ID')

class ZClient(commands.Bot):
    def __init__(self):
        self.system_name = socket.gethostname()
        os.system('cls')
        f.PRINTW(f"Welcome {fxc.FORE('#47eaff')}{self.system_name}{fxc.RESET}. Please wait one moment.")
        super().__init__(command_prefix='?', intents=discord.Intents.all())

    async def setup_hook(self):
        folderssss = os.listdir('./cogs')
        foldersss  = []
        folderss   = ""
        for lmao in folderssss:
            if lmao.endswith('.py'):
                foldersss.append(lmao[:-3])
                folderss = folderss+lmao[:-3]+', '
        f.PRINTV(f"Found {len(foldersss)} cogs.")
        f.PRINTV(f"{folderss[:-2]}.")
        for lmaos in foldersss:
            await self.load_extension("cogs."+lmaos)
        

    async def on_connect(self):
        f.PRINTV(f"{fxc.FORE('##c2c2c2')}discord.client:{fxc.RESET} logging in using static token")
    
    async def on_shard_connect(self, shard_id='None'):
        f.PRINTV(f"{fxc.FORE('##c2c2c2')}discord.gateway:{fxc.RESET} Shard ID {fxc.FORE('#47eaff')}{shard_id}{fxc.RESET} has connected to Gateway.")
    
    async def on_ready(self):
        f.PRINTV(f"{fxc.FORE('#dbfffe')}{self.user}{fxc.RESET} is now running. (ID: {self.user.id})")
        f.PRINTV("Python Version: " + fxc.FORE('#dbfffe') + str(subprocess.check_output('py --version'))[2:-5])
        f.PRINTV("Discord Version: " + fxc.FORE('#dbfffe') + discord.__version__)
        try: 
            lol = await client.tree.sync()
            f.PRINTY(f"Commands synced successfully. {len(lol)} commands loaded.")
        except Exception as e: f.PRINTZ(e)

    
    

## TODO: implement dm verification
## TODO: add ephemerals to most of them
## TODO: make a working error handler


loop = asyncio.get_event_loop()
if loop.is_running() == False:
    client = ZClient()
    client.run(Env.DISCORD_TOKEN, log_handler=None)