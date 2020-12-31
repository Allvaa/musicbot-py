from discord.ext import commands
import discord
import os

class MusicBot(commands.Bot):
    def __init__(self):
        super(MusicBot, self).__init__(
            command_prefix=os.environ.get("PREFIX"),
            intents=discord.Intents(guilds=True, members=True, voice_states=True, messages=True))
