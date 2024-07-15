import discord
import datetime
import json
import asyncio
import sqlite3
from discord.ext import commands

class ModCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.hybrid_command(description="Ban someone")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason = 'Not Specified'):
        embed_dm=discord.Embed(title="You have been banned from {}!".format(ctx.guild.name), description="Reason: {}".format(reason), color=0xae000d)
        await member.send(embed=embed_dm)

        embed=discord.Embed(title="Member banned", description="<@{}> ({}#{}) has been banned!".format(member.id, member.name, member.discriminator), color=0xae000d)
        embed.set_thumbnail(url=member.display_avatar)
        embed.add_field(name="Reason:", value=f"{reason}", inline=False)
        embed.add_field(name="Banned by:", value=(f'<@{ctx.author.id}>'), inline=True)
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text="")
        with open('config.json', 'r') as f:
            config = json.load(f)

        channel_id = config['logs_channel_id']
        channel = self.client.get_channel(channel_id)
        await channel.send(embed=embed)

        await member.ban(reason = reason)
    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Incorrect syntax!", description="Example: ``>ban @Trixie Abusing Magic``", color=0xae000d)
            await ctx.send(embed=embed)

    @commands.hybrid_command(description="Unban someone")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id: int):
        member = await self.client.fetch_user(id)
        try:
            await ctx.guild.unban(member)

            embed=discord.Embed(title="Member unbanned", description="<@{}> ({}#{}) has been unbanned!".format(member.id, member.name, member.discriminator), color=0xae000d)
            embed.set_thumbnail(url=member.display_avatar)
            embed.add_field(name="Unbanned by:", value=(f'<@{ctx.author.id}>'), inline=True)
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text="")
            with open('config.json', 'r') as f:
                config = json.load(f)

            channel_id = config['logs_channel_id']
            channel = self.client.get_channel(channel_id)
            await channel.send(embed=embed)
        except discord.NotFound:
            exception_embed=discord.Embed(title="This user isn't banned!")
            await ctx.send(embed=exception_embed)
    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Incorrect syntax!", description="Example: ``>unban 448865446121439233``", color=0xae000d)
            await ctx.send(embed=embed)

    @commands.hybrid_command(description="Kick someone")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, arg = 'Not Specified'):
        reason = arg
        embed_dm=discord.Embed(title="You have been kicked from {}!".format(ctx.guild.name), description="Reason: {}".format(reason), color=0xae000d)
        await member.send(embed=embed_dm)

        embed=discord.Embed(title="Member kicked", description="<@{}> ({}#{}) has been kicked!".format(member.id, member.name, member.discriminator), color=0xae000d)
        embed.set_thumbnail(url=member.display_avatar)
        embed.add_field(name="Reason:", value=f"{reason}", inline=False)
        embed.add_field(name="Kicked by:", value=(f'<@{ctx.author.id}>'), inline=True)
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text="")
        with open('config.json', 'r') as f:
            config = json.load(f)

        channel_id = config['logs_channel_id']
        channel = self.client.get_channel(channel_id)
        await channel.send(embed=embed)

        await member.kick()
    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Incorrect syntax!", description="Example: ``>kick @Trixie Abusing magic``", color=0xae000d)
            await ctx.send(embed=embed)

    @commands.hybrid_command(description="Softban someone")
    @commands.has_permissions(kick_members=True)
    async def softban(self, ctx, member: discord.Member, reason = 'Not Specified', delete_message_seconds=604800):
        embed_dm=discord.Embed(title="You have been softbanned from {}!".format(ctx.guild.name), description="Reason: {}".format(reason), color=0xae000d)
        await member.send(embed=embed_dm)

        embed=discord.Embed(title="Member softbanned", description="<@{}> ({}#{}) has been softbanned!".format(member.id, member.name, member.discriminator), color=0xae000d)
        embed.set_thumbnail(url=member.display_avatar)
        embed.add_field(name="Reason:", value=f"{reason}", inline=False)
        embed.add_field(name="Softbanned by:", value=(f'<@{ctx.author.id}>'), inline=True)
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text="")
        with open('config.json', 'r') as f:
            config = json.load(f)

        channel_id = config['logs_channel_id']
        channel = self.client.get_channel(channel_id)
        await channel.send(embed=embed)

        await member.ban(reason = reason)
        await member.unban()
    @softban.error
    async def softban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Incorrect syntax!", description="Example: ``>softban @Trixie Abusing Magic``", color=0xae000d)
            await ctx.send(embed=embed)

    @commands.hybrid_command(description="Purge some messages")
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount:int):
        amount = amount
        channel = ctx.channel
        deleted = await channel.purge(limit=amount)
        embed=discord.Embed(description=f"Purged {len(deleted)} messages", color=0x04bf33)
        await ctx.send(embed=embed)
    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed=discord.Embed(title="Incorrect syntax!", description="Try: ``>purge 7``", color=0xae000d)
            await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(ModCommands(client))