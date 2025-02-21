import discord
import meilisearch
import json
import dotenv
import os
dotenv.load_dotenv()
client = meilisearch.Client(os.getenv("SEARCH-URL"), os.getenv("SEARCH-TOKEN"))
loaders = ["Forge", "NeoForge", "Fabric", "Quilt"]
index = client.index("addons")

async def addonsearch(ctx, query, limit=1):
    request = index.search(query, {"limit": limit})
    data = request.get("hits", [])  # Safely get 'hits' (default to empty list if not found)
    return data

async def send_embeds(message, data):
    for mod_data in data:  # `data` is a list of addon dictionaries
        embed = await gen_embed(mod_data)
        await message.reply(embed=embed)

def format_loaders(loaders):
    if not loaders:
        return "No loaders available"
    return " ".join([f"{loader}" for loader in loaders])

async def gen_embed(data):
    loaders_field = format_loaders(data.get("loaders", []))  # Use `.get()` for safety
    embed = discord.Embed(title=data["name"], description=data["description"], color=0x689AEE)
    embed.set_author(name=data["author"])
    embed.set_thumbnail(url=data["icon"])
    embed.add_field(name="Loaders", value=loaders_field, inline=False)
    embed.add_field(name="Download", value=f"https://nottelling.youthe.domain/addons/{data['slug']}", inline=False)
    embed.set_footer(text=f"Downloads: {data['downloads']}")
    return embed
