from src.structures import client
from discord.colour import Colour
import discord

class Util:
    def __init__(self, bot: "client.MusicBot") -> None:
        self.bot = bot

    def embed(self) -> discord.Embed:
        return discord.Embed(colour=Colour.blurple())
