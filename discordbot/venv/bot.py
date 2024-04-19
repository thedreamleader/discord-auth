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

    @tree.command(name="test")
    async def hello(interaction: discord.Interaction):
        await interaction.response.send_message(f"hey {interaction.user.mention}! if you see this message, your slash commands work now ;-;")

    @tree.command(name="speak")
    @app_commands.describe(thing_to_say = "What should I say?")
    async def speak(interaction, thing_to_say: str):
        await interaction.response.send_message(f"{interaction.user.name} said: {thing_to_say}")

    ## generates the verification token
    @tree.command(name='token', description='Sends a token for verification. Can only be used with Manage Roles permissions.')
    @app_commands.checks.has_permissions(manage_roles=True)
    async def token(interaction: discord.Interaction):
        if not interaction.user.guild_permissions.manage_roles:
            await interaction.response.send_message("You do not have permission to use this command.") # put ephemerals back when know code work
            return
        
        ## saves the token in a json file
        with open('token.json', 'w') as f:
            json.dump({'verif_token': verif_token}, f, indent=2)
        
        await interaction.response.send_message(f"Verify using: {verif_token}") # same instruction, refer to line 37 command
        return

    
    ## verifies the user using the generated token
    @tree.command(name='verify', description='Verifies you using the token provided from your inviter.')
    async def verify(interaction: discord.Interaction, arg: str):
        with open('token.json', 'r') as file:
            token_data = json.load(file)
            
        ## gets the token from the json file & checks if the token is correct    
        verif_token = token_data['verif_token'] 
        if verif_token == arg:
            user = interaction.user
            role = discord.utils.get(interaction.guild.roles, name="Verified Account")

            await interaction.user.add_roles(role)
            await interaction.response.send_message(f"Successfully verified! {user.mention}, welcome to the server!")

            ## deleting token after it has been used (for security purposes)
            try:
                os.remove("token.json")
            except OSError:
                pass


    client.run(DISCORD_TOKEN)