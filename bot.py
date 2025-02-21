import discord
from discord.ext import commands
from colorama import Back, Style
from addonsearch import addonsearch
import dotenv
import os
dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True  # Required for reading user messages
bot = commands.Bot(command_prefix="??", intents=intents)

bot.remove_command("help")

@bot.event
async def on_ready():
    print(f"{Back.GREEN}Logged in as {bot.user}{Style.RESET_ALL}")

@bot.command()
async def help(ctx):
    embed = discord.Embed(
        title="Commands available",
        description="Addons & Schematics commands",
        color=discord.Color.blurple()
    )
    embed.add_field(
        name="Addon Commands",
        value="??addon search <query> [how many default=1] - Search for addons on Blueprint.",
        inline=False
    )
    embed.add_field(
        name="Schematic Commands",
        value="Such emptyness",
        inline=False
    )
    embed.add_field(
        name="Data types",
        value="""
        <> - needed
        [] - optional
""",
        inline=False
    )
    await ctx.reply(embed=embed)

# Create "addon" group command
@bot.group(invoke_without_command=True)
async def addon(ctx):
    await ctx.send("Use `??addon search <query>` to find addons.")

# Subcommand for "addon"
@addon.command()
async def search(ctx, *, query: str):
    # Extract the number of results from the end of the query (if available)
    parts = query.split()
    if parts[-1].isdigit():
        limit = int(parts[-1])
        query = " ".join(parts[:-1])  # Remove the number from the query
    else:
        limit = 1  # Default to 1 result if no number is specified
    
    # Ensure the limit is between 1 and 5
    limit = max(1, min(limit, 5))
    
    await ctx.send(f"Searching for {limit} addon(s) related to: `{query}`")
    await addonsearch(ctx=ctx, query=query, limit=limit)
bot.run(os.getenv("TOKEN"))