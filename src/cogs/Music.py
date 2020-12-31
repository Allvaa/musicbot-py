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

    @wavelink.WavelinkMixin.listener()
    async def on_track_start(self, node: wavelink.Node, payload: wavelink.TrackStart):
        music = self.bot.get_music(payload.player.guild_id)
        music.current = music.queue.pop(0)

        if music.text_channel: await music.text_channel.send(f"Now playing {music.current.title}")

    @wavelink.WavelinkMixin.listener()
    async def on_track_end(self, node: wavelink.Node, payload: wavelink.TrackEnd):
        if payload.reason == "REPLACED": return

        music = self.bot.get_music(payload.player.guild_id)

        music.previous = music.current
        music.current = None

        if music.loop: music.queue.append(music.previous)

        if not music.queue:
            if music.text_channel: await music.text_channel.send("Queue is empty")
            return await music.destroy()

        await music.start()

    @wavelink.WavelinkMixin.listener()
    async def on_track_exception(self, node: wavelink.Node, payload: wavelink.TrackException):
        music = self.bot.get_music(payload.player.guild_id)
        if music.text_channel: await music.text_channel.send(f"An error occured: {payload.error}")

def setup(bot: MusicBot):
    bot.add_cog(Music(bot))
