import discord
from discord.ext import commands
from discord import app_commands
from colorcode import cc as fxc
from colorcode import p as f

class testcog(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        f.PRINTX("AuthExtra cog loaded")

    @app_commands.command(name='cog1', description='Test')
    async def cog1(self, ctx: discord.Interaction):
        await ctx.response.send_message("Test success")

async def setup(client:commands.Bot) -> None:
    await client.add_cog(testcog(client))