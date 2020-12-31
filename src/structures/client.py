from discord.ext import commands
import discord
import os

class MusicBot(commands.Bot):
    def __init__(self):
        super(MusicBot, self).__init__(
            command_prefix=os.environ.get("PREFIX"),
            intents=discord.Intents(guilds=True, members=True, voice_states=True, messages=True))

    async def is_owner(self, user: discord.User) -> bool:
        owners = [int(x.strip()) for x in os.environ.get("OWNERS").split(",")]
        if user.id in owners: return True
        return await super().is_owner(user)

    def load_cogs(self):
        for ext in [f.split(".")[0] for f in os.listdir("src/cogs") if os.path.isfile(os.path.join("src/cogs", f))]:
            self.load_extension(f"src.cogs.{ext}")
        self.load_extension("jishaku")
