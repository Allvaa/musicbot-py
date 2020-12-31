from discord.ext import commands
from src.structures.client import MusicBot

class General(commands.Cog):
    def __init__(self, bot: MusicBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        tag = f"{self.bot.user.name}#{self.bot.user.discriminator}"
        print(f"Logged in as {tag}")

    @commands.command()
    async def ping(self, ctx: commands.Context):
        ctx.send("Pong!")

def setup(bot: MusicBot):
    bot.add_cog(General(bot))