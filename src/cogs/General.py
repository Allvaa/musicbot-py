from discord.ext import commands
from discord.http import Route
from src.structures.client import MusicBot
from src.structures.interaction import Interaction

class General(commands.Cog):
    def __init__(self, bot: MusicBot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        tag = f"{self.bot.user.name}#{self.bot.user.discriminator}"
        print(f"Logged in as {tag}")

    @commands.Cog.listener()
    async def on_interaction_create(self, data: Interaction):
        print(data.id)

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
