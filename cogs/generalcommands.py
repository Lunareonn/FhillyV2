import discord
import platform
import func.fakebrowser as fb
from discord.ext import commands
from datetime import datetime

class GeneralCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(description="Ping!")
    async def ping(self, ctx):
        await ctx.send(f"Ping: {round(self.client.latency * 1000)}ms")

    @commands.hybrid_command(description="Get user information.")
    async def who(self, ctx, member: discord.Member):
        name = member.name
        user_id = member.id
        user_avatar = member.avatar
        user_permissions = member.guild_permissions

        created_at = member.created_at.strftime("%d/%m/%Y, %H:%M:%S")
        joined_at = member.joined_at.strftime("%d/%m/%Y, %H:%M:%S")

        if not user_avatar:
            user_avatar = member.default_avatar

        custom_status = None
        for activity in member.activities:
           if isinstance(activity, discord.CustomActivity):
                custom_status = activity.name
                break

        embed=discord.Embed(description=f"<@{user_id}>", color=0x18cd45)
        embed.set_author(name=f"{name}", icon_url=user_avatar)
        if user_avatar is None:
            embed.set_thumbnail(url=discord.Member.default_avatar)
        else:
            embed.set_thumbnail(url=user_avatar)
        embed.add_field(name="Joined Server", value=joined_at)
        embed.add_field(name="Creation Date", value=created_at)
        embed.add_field(name="Custom Status", value=custom_status, inline=False)
        if ctx.guild.owner_id == user_id:
            embed.add_field(name="Server Owner", value="True")
        if member.bot:
            embed.add_field(name="Bot Account", value="True")
        if user_permissions.ban_members or user_permissions.kick_members or user_permissions.manage_members:
            embed.add_field(name="Staff Member", value="True")

        await ctx.send(embed=embed)

    @commands.hybrid_command(description="Information about the bot")
    async def about(self, ctx):
        client = ctx.bot.user
        author_name = await self.client.fetch_user(237605319159709696)
        commands = [c.name for c in self.client.commands]

        embed = discord.Embed(title="About",
                      description=f"Fhilly V2 is a discord bot created for **{ctx.guild.name}**",
                      colour=0x1cb51f,
                      timestamp=datetime.now())

        embed.set_author(name="Fhilly V2",
                        url="https://github.com/LunaXCBN")

        embed.add_field(name="Author",
                        value=f"{author_name.name}",
                        inline=True)
        embed.add_field(name="Version",
                        value="1.0.0-dev",
                        inline=True)
        embed.add_field(name="# of commands",
                        value=f"{len(commands)}",
                        inline=True)

        embed.set_footer(text=f"discord.py {discord.__version__} | python {platform.python_version()}")
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(GeneralCommands(client))