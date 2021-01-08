import json
from typing import List
import discord
from discord.embeds import Embed
from discord.http import Route
from discord.mentions import AllowedMentions
from src.structures import client

class ExtHttpClient:
    def __init__(self, bot: "client.MusicBot") -> None:
        self.bot = bot
        
    async def respond_interaction(self, interaction_id: str, interaction_token: str, content: str, *, tts=False, embeds: List[Embed] = [], allowed_mentions: AllowedMentions = None, type: int = 4):
        r = Route("POST", f"/interactions/{interaction_id}/{interaction_token}/callback")
        payload = {
            "type": type,
            "data": {}
        }

        if content:
            payload["data"]["content"] = content

        if tts:
            payload["data"]["tts"] = True

        if embeds:
            payload["data"]["embeds"] = embeds

        if allowed_mentions:
            payload["data"]["allowed_mentions"] = allowed_mentions

        return self.bot.http.request(r, json=payload)
