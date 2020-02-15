import discord
from discord.ext import commands

import asyncio

class admin(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_guild_permissions(discord.Permissions(manage_roles = True))
    @commands.bot_has_guild_permissions(discord.Permissions(manage_roles = True))
    async def holiday(self, ctx, num_roles: int):
        roles = [await ctx.guild.create_role(name = "holiday " + str(rolenum + 1)) for rolenum in range(num_roles)]
        for index, member in enumerate(ctx.guild.members):
              await member.add_roles(roles[index % num_roles])
              asyncio.sleep(1)



def setup(client):
    client.add_cog(meta(client))