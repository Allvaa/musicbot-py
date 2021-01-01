from discord.ext import commands
from src.structures import music
from src.util import Util
import discord
import os

class MusicBot(commands.Bot):
    musics = {}

    def __init__(self):
        self.util = Util(self)
        super(MusicBot, self).__init__(
            command_prefix=os.environ.get("PREFIX"),
            intents=discord.Intents(guilds=True, members=True, voice_states=True, messages=True))

    async def is_owner(self, user: discord.User) -> bool:
        owners = [int(x.strip()) for x in os.environ.get("OWNERS").split(",")]
        if user.id in owners: return True
        return await super().is_owner(user)

    def get_music(self, guild_id: int) -> music.MusicHandler:
        if not guild_id in self.musics:
            self.musics[guild_id] = music.MusicHandler(self, self.get_guild(guild_id))
        return self.musics[guild_id]

    def load_cogs(self):
        for ext in [f.split(".")[0] for f in os.listdir("src/cogs") if os.path.isfile(os.path.join("src/cogs", f))]:
            self.load_extension(f"src.cogs.{ext}")
        self.load_extension("jishaku")
