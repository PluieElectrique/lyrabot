import discord
from discord.ext import commands
import requests

import re

class embedfix(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.Cog.listener()
    async def on_message(self, message):
        for embed in message.embeds:
            if embed.thumbnail == discord.Embed.Empty:
                continue

            fix_msg = self.check_and_fix(embed.thumbnail.url)
            if fix_msg:
                await message.channel.send(fix_msg)



    def check_and_fix(self, url):
        sources = {
            "derpicdn.net": self.derpi_fixer
        }
        for source, fixfunc in sources.items():
            if source in url:
                return fixfunc(url)
        return None


    def derpi_fixer(self, url):
        # regex the url: address  id  filename
        regex = re.compile("^.*/(\d*)/[^/]*$")
        match = regex.match(url)
        if match:
            image_id = int(match.group(1))
            image_url = f"https://derpibooru.org/api/v1/json/images/{image_id}"
            data = requests.get(image_url).json()["image"]
            print(data)
            while "duplicate_of" in data and data["duplicate_of"]:
                data = requests.get(f"https://derpibooru.org/api/v1/json/images/{data['duplicate_of']}")["image"]
                print(data)
            return data["representations"]["full"]
        return None

def setup(client):
    client.add_cog(embedfix(client))
