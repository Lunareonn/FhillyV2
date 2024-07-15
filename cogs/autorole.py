import discord
import discord.utils
import json
import sqlite3
from discord.ext import commands

class AutoRole(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        with open('config.json', 'r') as f:
            config = json.load(f)

        autorole_enabled = config['autorole_enabled']
        if autorole_enabled is False:
            pass

        autorole_id = config['autorole_id']
        role = member.get_role(autorole_id)
        await member.add_roles(role)


async def setup(client):
    await client.add_cog(AutoRole(client))

