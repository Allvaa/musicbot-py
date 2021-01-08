import discord
from src.structures import client

class Interaction:
    def __init__(self, bot: "client.MusicBot", raw) -> None:
        self.bot = bot
        self.raw = raw
        self.raw["member_id"] = raw["member"]["user"]["id"]
        self.id = raw["id"]
        self.type = raw["type"]
        self.data = raw["data"]
        self.token = raw["token"]

    @property
    def guild(self) -> discord.Guild :
        return self.bot.get_guild(int(self.raw["guild_id"]))

    @property
    def channel(self) -> discord.abc.GuildChannel:
        return self.bot.get_channel(int(self.raw["channel_id"]))
    
    @property
    def member(self) -> discord.Member:
        return self.guild.get_member(int(self.raw["member_id"]))
