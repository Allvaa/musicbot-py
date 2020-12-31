from src.structures.client import MusicBot
import os

def start():
    bot = MusicBot()
    bot.load_extension("jishaku")
    bot.run(os.environ.get("TOKEN"))