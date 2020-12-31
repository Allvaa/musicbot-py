from discord.ext import commands
from src.structures.client import MusicBot
import wavelink
import os

class Music(commands.Cog, wavelink.WavelinkMixin):
    def __init__(self, bot: MusicBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.wavelink = wavelink.Client(bot=self.bot)
        rest_uri = "http://{host}:{port}".format(host=os.environ.get("LAVA_HOST"), port=os.environ.get("LAVA_PORT"))

        await self.bot.wavelink.initiate_node(host=os.environ.get("LAVA_HOST"),
                                              port=os.environ.get("LAVA_PORT"),
                                              rest_uri=rest_uri,
                                              password=os.environ.get("LAVA_PASS"),
                                              identifier="main",
                                              region=os.environ.get("LAVA_REGION"))

def setup(bot: MusicBot):
    bot.add_cog(Music(bot))
