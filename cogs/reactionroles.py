import discord
import sqlite3
from discord.ext import commands

class ReactionRoles(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.conn = sqlite3.connect('database.db')
        self.conn.execute("CREATE TABLE IF NOT EXISTS \"reaction_role_messages\" (id INTEGER PRIMARY KEY AUTOINCREMENT, guild_id INTEGER, channel_id INTEGER, message_id INTEGER, emoji TEXT, role_id INTEGER, existing BOOLEAN);")

    @commands.hybrid_group()
    async def reaction_roles(self, ctx):
        if ctx.invoked_subcommand is None:
            embed=discord.Embed(title="Incorrect syntax!", description="Examples:\n``>reaction_roles add``\n``>reaction_roles remove``", color=0xae000d)
            await ctx.send(embed=embed)

    @reaction_roles.command(description="Add Reaction Roles to a message.")
    async def add(self, ctx, channel_id: discord.TextChannel, message_id: int, role: discord.Role, emoji: str):
        guild_id = ctx.guild.id
        channel_id = channel_id.id
        role_id = role.id
        emoji = str(emoji)
        existing = True

        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO reaction_role_messages (guild_id, channel_id, message_id, emoji, role_id, existing) VALUES(?, ?, ?, ?, ?, ?);", (guild_id, channel_id, message_id, emoji, role_id, existing,))
        self.conn.commit()
        await ctx.send("ye")

    @reaction_roles.command(description="Remove Reaction Roles from a message.")
    async def remove(self, ctx, message_id: int):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM reaction_role_messages WHERE message_id = ?;", (message_id,))
        self.conn.commit()
        await ctx.send("ye")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM reaction_role_messages WHERE guild_id=? AND channel_id=? AND message_id=?", (payload.guild_id, payload.channel_id, payload.message_id))
        rows = cursor.fetchall()

        if len(rows) == 0:
            return

        for row in rows:
            if str(payload.emoji) != str(row[4]):
                continue

            guild = self.client.get_guild(payload.guild_id)
            role = discord.utils.get(guild.roles, id=row[5])
            await payload.member.add_roles(role, atomic=True)

async def setup(client):
    await client.add_cog(ReactionRoles(client))