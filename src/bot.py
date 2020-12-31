from src.structures.client import MusicBot
import os

def start():
    bot = MusicBot()
    bot.run(os.environ.get("TOKEN"))