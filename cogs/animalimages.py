import discord
import requests
import json
import os
from datetime import datetime
from discord.ext import commands

class AnimalImages(commands.Cog):
    def __init__(self, client):
        self.client = client

        self.CATAPI = os.getenv("CATAPI")
        self.DOGAPI = os.getenv("DOGAPI")

    @commands.hybrid_command(description="Get a cat picture :3")
    async def cat(self, ctx):
        try:
            api_key = self.DOGAPI
            url = f"https://api.thecatapi.com/v1/images/search?api_key={api_key}&has_breeds=1"
            headers = {'content-type': 'application/json'}
            response = requests.get(url, headers=headers)

        
            json_data = json.loads(response.text)
            image = json_data[0]['url']
            breed = json_data[0]['breeds'][0]['name']

            embed=discord.Embed(title="Puppy :3", description=f"Breed: {breed}", url=image, color=0x2cfee9)
            embed.set_image(url=image)
            embed.set_footer(text="Image provided by TheDogAPI")
            await ctx.send(embed=embed)
        except requests.HTTPError as err:
            embed = discord.Embed(title=f"requests.HTTPError caught!", description=f"```{err}```", color=0xd34312, timestamp=datetime.now())
            embed.set_footer(text=">->")
            await ctx.send(embed=embed)
        except requests.ConnectionError as err:
            embed = discord.Embed(title=f"requests.ConnectionError caught!", description=f"```{err}```", color=0xd34312, timestamp=datetime.now())
            embed.set_footer(text=">->")
            await ctx.send(embed=embed)
        except requests.Timeout as err:
            embed = discord.Embed(title=f"requests.Timeout caught!", description=f"```{err}```", color=0xd34312, timestamp=datetime.now())
            embed.set_footer(text=">->")
            await ctx.send(embed=embed)

    @commands.hybrid_command(description="Get a dog picture :3")
    async def dog(self, ctx):
        try:
            api_key = self.DOGAPI
            url = f"https://api.thedogapi.com/v1/images/search?api_key={api_key}&has_breeds=1"
            headers = {'content-type': 'application/json'}
            response = requests.get(url, headers=headers)

        
            json_data = json.loads(response.text)
            image = json_data[0]['url']
            breed = json_data[0]['breeds'][0]['name']

            embed=discord.Embed(title="Puppy :3", description=f"Breed: {breed}", url=image, color=0x2cfee9)
            embed.set_image(url=image)
            embed.set_footer(text="Image provided by TheDogAPI")
            await ctx.send(embed=embed)
        except requests.HTTPError as err:
            embed = discord.Embed(title=f"requests.HTTPError caught!", description=f"```{err}```", color=0xd34312, timestamp=datetime.now())
            embed.set_footer(text=">->")
            await ctx.send(embed=embed)
        except requests.ConnectionError as err:
            embed = discord.Embed(title=f"requests.ConnectionError caught!", description=f"```{err}```", color=0xd34312, timestamp=datetime.now())
            embed.set_footer(text=">->")
            await ctx.send(embed=embed)
        except requests.Timeout as err:
            embed = discord.Embed(title=f"requests.Timeout caught!", description=f"```{err}```", color=0xd34312, timestamp=datetime.now())
            embed.set_footer(text=">->")
            await ctx.send(embed=embed)



async def setup(client):
    await client.add_cog(AnimalImages(client))