import discord
from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandInvokeError):
            original = error.original
            if isinstance(original, discord.HTTPException):
                status = original.status
                code = original.code
                text = original.text
                embed = discord.Embed(title="Something went wrong!", description="It's not your fault, don't worry.", color=0xae000d)
                embed.add_field(name="Status Code", value=status, inline=False)
                embed.add_field(name="Code", value=code, inline=False)
                embed.add_field(name="Error Text", value=text, inline=False)
                await ctx.send(embed=embed)
            elif isinstance(original, discord.DiscordException):
                embed = discord.Embed(title="Something went wrong!", description="Blame Luna for this.", color=0xae000d)
                embed.add_field(name="Exception thrown:", value="discord.DiscordException", inline=False)
                await ctx.send(embed=embed)
            elif isinstance(original, discord.ClientException):
                embed = discord.Embed(title="Something went wrong!", description="This one's your fault.", color=0xae000d)
                embed.add_field(name="Exception thrown:", value="discord.ClientException", inline=False)
                await ctx.send(embed=embed)
            elif isinstance(original, discord.RateLimited):
                embed = discord.Embed(title="Something went wrong!", description="Rate limited.")
                embed.add_field(name="Exception thrown:", value="discord.RateLimited", inline=False)
                await ctx.send(embed=embed)
            elif isinstance(original, discord.Forbidden):
                status = original.status
                code = original.code
                text = original.text
                embed = discord.Embed(title="Something went wrong!", description="I can't do that.")
                embed.add_field(name="Status Code", value=status, inline=False)
                embed.add_field(name="Code", value=code, inline=False)
                embed.add_field(name="Error Text", value=text, inline=False)
                await ctx.send(embed=embed)
            elif isinstance(original, discord.NotFound):
                status = original.status
                code = original.code
                text = original.text
                embed = discord.Embed(title="Something went wrong!", description="Couldn't find that.")
                embed.add_field(name="Status Code", value=status, inline=False)
                embed.add_field(name="Code", value=code, inline=False)
                embed.add_field(name="Error Text", value=text, inline=False)
                await ctx.send(embed=embed)
            elif isinstance(original, discord.DiscordServerError):
                status = original.status
                code = original.code
                text = original.text
                embed = discord.Embed(title="Something went wrong!", description="Tell discord to fix their shit.")
                embed.add_field(name="Status Code", value=status, inline=False)
                embed.add_field(name="Code", value=code, inline=False)
                embed.add_field(name="Error Text", value=text, inline=False)
                await ctx.send(embed=embed)
            elif isinstance(original, discord.InvalidData):
                embed = discord.Embed(title="Something went wrong!", description="Discord gave me invalid data.")
                embed.add_field(name="Exception thrown:", value="discord.InvalidData")
                await ctx.send(embed=embed)
            else:
                raise error

async def setup(client):
    await client.add_cog(ErrorHandler(client))