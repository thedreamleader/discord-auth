## file with all the bot commands

import os
import discord
import json
from discord import app_commands
from dotenv import load_dotenv
from features.tokengen import verif_token

## runs the bot by retrieving the bot's token from the .env file
def run_bot():
    load_dotenv()
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    tree = app_commands.CommandTree(client)

    @client.event
    async def on_ready():
        print(f"{client.user} is now running.")
        try:
            await tree.sync()
            print("Commands synced successfully.")
        except Exception as e:
            print(e)

    ## generates the verification token
    @tree.command(name='token', description='Sends a token for verification. Can only be used with Manage Roles permissions.')
    @app_commands.checks.has_permissions(manage_roles=True)
    async def token(interaction: discord.Interaction):
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("You do not have enough permissions to use this command.")
            return
        
        with open('token.json', 'w') as f:
            json.dump({'verif_token': verif_token}, f, separators=(',', ':'))
        await interaction.response.send_message(verif_token)
        return

    
    ## verifies the user using the generated token
    @tree.command(name='verify', description='Verifies you using the token provided from your inviter. Works in only servers.')
    async def verify(interaction: discord.Interaction, arg: str):
        with open('token.json', 'r') as file:
            token_data = json.load(file)
            
        ## gets the token from the json file & checks if the token is correct    
        verif_token = token_data['verif_token']
        if verif_token == arg:
            guild = client.get_guild(853924006264569886)  # gets server id
            member = guild.get_member(interaction.user.id)
            role_id = 1127415902296612945 # role id of "verified account"
            role = guild.get_role(role_id)

            if role in member.roles:
                return

            await member.add_roles(role)
            if interaction.guild is not None:
                await interaction.response.send_message(f"Successfully verified! Welcome to the server, {interaction.user.mention}!")
            else:
                await interaction.response.send_message(f"Successfully verified! Welcome to the server!")

            ## deleting token after it has been used (for security purposes)
            try:
                os.remove("token.json")
            except OSError:
                pass
            return
    
    client.run(DISCORD_TOKEN)

    ## TODO: implement dm verification
    ## TODO: add ephemerals back on line 41 and 48