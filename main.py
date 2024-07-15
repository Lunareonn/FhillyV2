# Imports
import discord
import os
import json
from dotenv import load_dotenv
from discord.ext import commands
# End of Imports

# Intialize client
load_dotenv() # Load env for token
intents = discord.Intents.all()
client = commands.Bot(command_prefix=">", intents=intents, help_command=None)

# Check config.json
with open('config.json', 'r') as f:
    config = json.load(f)


@client.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context):
    synced = await client.tree.sync()
    await ctx.send(f"{len(synced)} commands synced")

@client.hybrid_group()
async def config(ctx):
    if ctx.invoked_subcommand is None:
        embed=discord.Embed(title="Incorrect syntax!", description="Examples:\n``>config set_logs #logs``\n``>config set_autorole @Member``", color=0xae000d)
        await ctx.send(embed=embed)

@config.command(description="Set channel for Action Logs")
async def set_logs(ctx, channel: discord.TextChannel):
    with open('config.json', 'r') as f:
        config = json.load(f)
        logs = config.get('logs', [])

        if channel.id == logs[0]['logs_channel_id']:
            embed=discord.Embed(title="Error!", description="The selected channel is the same as the previous channel.", color=0xff171d)
            await ctx.send(embed=embed)
        else:
            if logs:
                logs[0]['logs_channel_id'] = channel.id
                logs[0]['logs_channel_name'] = channel.name
            else:
                logs.append({
                    'logs_channel_id': channel.id,
                    'logs_channel_name': channel.name
                })

            with open('config.json', 'w') as f:
                json.dump(config, f, indent=2)
            embed=discord.Embed(title="New action log destination set!", description=f"Logs channel is now: <#{channel.id}> ({channel.id})", color=0x3aff17)
            await ctx.send(embed=embed)
@set_logs.error
async def set_logs_error(ctx, error):
    if isinstance(error, commands.ChannelNotFound):
        channel = error.argument
        embed=discord.Embed(title="Invalid Channel", description=f"Could not find channel ``{channel}``", color=0xae000d)
        await ctx.send(embed=embed)

@config.command(description="Set role for Auto Role")
async def set_autorole(ctx, role: discord.Role):
    with open('config.json', 'r') as f:
        config = json.load(f)
        logs = config.get('autorole', [])

        if role.id == logs[0]['role_id']:
            embed=discord.Embed(title="Error!", description="The selected role is the same as the previous role.", color=0xff171d)
            await ctx.send(embed=embed)
        else:
            if logs:
                logs[0]['role_id'] = role.id
                logs[0]['role_name'] = role.name
            else:
                logs.append({
                    'role_id': role.id,
                    'role_name': role.name
                })

            with open('config.json', 'w') as f:
                json.dump(config, f, indent=2)
            embed=discord.Embed(title="New autorole set!", description=f"New members will now be assigned: <@&{role.id}>", color=0x3aff17)
            await ctx.send(embed=embed)
@set_autorole.error
async def set_autorole_error(ctx, error):
    if isinstance(error, commands.RoleNotFound):
        role = error.argument
        embed=discord.Embed(title="Invalid Role", description=f"Could not find role ``{role}``", color=0xae000d)
        await ctx.send(embed=embed)

@config.command(description="Reload Extension")
async def reload_ext(ctx, extension):
    await client.reload_extension(f'cogs.{extension}')

@config.command(description="Unload Extension")
async def unload_ext(ctx, extension):
    await client.unload_extension(f'cogs.{extension}')

@config.error
async def config_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        embed=discord.Embed(title="You do not own this bot!", color=0xae000d)
        await ctx.send(embed=embed)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} ({client.user.id})')

@client.event
async def setup_hook():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded Cog: {filename[:-3]}')

TOKEN = os.getenv("TOKEN")
client.run(TOKEN)