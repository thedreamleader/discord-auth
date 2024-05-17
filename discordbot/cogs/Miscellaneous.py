import discord
from bot import Env
from discord import app_commands
from discord.ext import commands
from colorcode import cc as fxc
from colorcode import p as f

class Slash(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        f.PRINTX("Ping cog loaded")

    @commands.command()
    async def sync(self, ctx) -> None:
        fmt = await ctx.client.tree.sync(guild=ctx.guild)
        await ctx.send(f"Synced {len(fmt)} commands.")

    @app_commands.command(name="slash", description="test slash command")
    async def ping(self, interaction: discord.Interaction):
        bot_latency = round(self.client.latency * 1000)
        await interaction.response.send_message(f"Latency: {bot_latency} ms.")


async def setup(client:commands.Bot) -> None:
    await client.add_cog(Slash(client))