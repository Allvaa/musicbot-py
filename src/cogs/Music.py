from discord.ext import commands
from src.structures.client import MusicBot
import wavelink
import os
import re

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

    @commands.command()
    async def play(self, ctx: commands.Context, *, query: str):
        if not await self.check_vc(ctx): return
        tracks = await self.bot.wavelink.get_tracks(query if self.is_valid_url(query) else f"ytsearch: {query}")

        if not tracks:
            return await ctx.send("Could not find any songs with that query.")

        music = self.bot.get_music(ctx.guild.id)
        player = music.player()
        if not player.is_connected:
            await music.join(ctx.author.voice.channel)

        music.queue.append(tracks[0])
        if player.is_playing: await ctx.send(f"Added {str(tracks[0])} to the queue.")
        if not player.is_playing:
            await music.start()
        music.set_text_channel(ctx.channel)

    async def check_vc(self, ctx: commands.Context) -> bool:
        if not ctx.author.voice:
            await ctx.send("You aren't connected to any voice channels")
            return False
        elif ctx.me.voice and ctx.me.voice.channel != ctx.author.voice.channel:
            await ctx.send(f"You need to be in {ctx.me.voice.channel.mention}")
            return False
        else: return True

    async def check_playing(self, ctx: commands.Context) -> bool:
        music = self.bot.get_music(ctx.guild.id)
        if not music.player().is_playing:
            await ctx.send(embed=self.bot.util.embed(description="Sedang tidak memainkan apapun."))
            return False
        return True

    def is_valid_url(self, url: str) -> bool:
        return bool(re.compile(r"^https?:\/\/((([a-z\d]([a-z\d-]*[a-z\d])*)\.)+[a-z]{2,}|((\d{1,3}\.){3}\d{1,3}))(:\d+)?(\/[-a-z\d%_.~+]*)*(\?[;&a-z\d%_.~+=-]*)?(#[-a-z\d_]*)?$", flags=re.I).match(url))

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
