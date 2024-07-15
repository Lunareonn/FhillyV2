import discord
import sqlite3
from discord.ext import commands

class Macros(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.conn = sqlite3.connect('database.db')
        self.conn.execute("CREATE TABLE IF NOT EXISTS \"macros\" (name TEXT, alias TEXT, content TEXT);")

    @commands.hybrid_command()
    @commands.has_permissions(moderate_members=True)
    async def macroadd(self, ctx, name, content):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM macros")
        rows = cursor.fetchall()
        for r in rows:
            if r == name:
                await ctx.send("That macro already exists.")
                return

        cursor.execute("INSERT INTO macros (name, content) VALUES(?, ?);", (name, content,))
        self.conn.commit()
        await ctx.send(f"Added macro {name}")

    @commands.hybrid_command()
    @commands.has_permissions(moderate_members=True)
    async def macroremove(self, ctx, name):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM macros WHERE name = ?", (name,))
        await ctx.send(f"Removed macro {name}")


    @commands.hybrid_command()
    async def m(self, ctx, name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name, content FROM macros")
        macro = cursor.fetchall()

        for m in macro:
            if m[0] == name:
                content = str(m[1])
                pass

        await ctx.send(f"{content}") 

    @commands.hybrid_command()
    async def macros(self, ctx):
        cursor = self.conn.cursor()
        cursor.execute("SELECT name FROM macros")
        macro = cursor.fetchall()

        macros = "**Available macros:**\n"

        for m in macro:
            macros += "- " + m[0] + "\n"

        await ctx.send(macros)

async def setup(client):
    await client.add_cog(Macros(client))