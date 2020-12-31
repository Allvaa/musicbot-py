from src.structures import client
import discord
import wavelink

class MusicHandler:
    loop = False
    current = None
    previous = None
    queue = []
    text_channel = None

    def __init__(self, bot: "client.MusicBot", guild: discord.Guild):
        self.bot = bot
        self.guild = guild

    def player(self) -> wavelink.Player:
        return self.bot.wavelink.get_player(self.guild.id)

    def set_text_channel(self, text_ch: discord.TextChannel):
        self.text_channel = text_ch

    async def join(self, vc: discord.VoiceChannel):
        if not self.player().is_connected: await self.player().connect(vc.id)
    
    async def start(self):
        if self.player().is_connected: await self.player().play(self.queue[0])
    
    async def pause(self):
        if self.player().is_connected and self.player().is_playing and not self.player().paused:
            await self.player().set_pause(True)

    async def resume(self):
        if self.player().is_connected and self.player().is_playing and self.player().paused:
            await self.player().set_pause(False)

    async def skip(self):
        if self.player().is_connected and self.player().is_playing:
            await self.player().stop()

    async def stop(self):
        if self.player().is_connected and self.player().is_playing:
            self.queue = []
            self.loop = False
            await self.skip()

    async def set_volume(self, vol: int):
        if self.player().is_connected and self.player().is_playing:
            await self.player().set_volume(vol)

    async def destroy(self):
        if self.player().is_connected: await self.player().destroy()
        del self.bot.musics[self.guild.id]
