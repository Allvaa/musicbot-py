from src.structures.client import MusicBot
import os

def start():
    bot = MusicBot()
    bot.load_cogs()
    bot.run(os.environ.get("TOKEN"))