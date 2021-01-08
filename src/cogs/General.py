from discord.ext import commands
from discord.http import Route
from src.structures.client import MusicBot
import zlib

inflator = zlib.decompressobj()

class General(commands.Cog):
    _buffer = bytearray()
    def __init__(self, bot: MusicBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        tag = f"{self.bot.user.name}#{self.bot.user.discriminator}"
        print(f"Logged in as {tag}")

    @commands.Cog.listener()
    async def on_socket_response(self, msg):
        if msg["t"] != "INTERACTION_CREATE": return
        interaction_id = msg["d"]["id"]
        interaction_token = msg["d"]["token"]
        await self.bot.http.request(Route("POST", f"/interactions/{interaction_id}/{interaction_token}/callback"), json={
            "type": 4,
            "data": {
                "content": "a"
            }
        })
        print(msg["d"])

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        if hasattr(ctx.command, 'on_error'):
            return

        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = (commands.CommandNotFound, )
        error = getattr(error, 'original', error)

        if isinstance(error, ignored):
            return

        else:
            await ctx.send(error.args)

    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send("Pong!")

def setup(bot: MusicBot):
    bot.add_cog(General(bot))
