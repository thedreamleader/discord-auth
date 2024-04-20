## file with all the bot commands

import os
import discord
import json
import secrets
from discord import app_commands
from dotenv import load_dotenv

# For colorcoding purposes
from mutefxc import cc as fxc
from mutefxc import p as f

## runs the bot by retrieving the bot's token from the .env file
def keygenr():
    return str(secrets.token_hex(16))


def run_bot():
    load_dotenv()
    DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
    client = discord.Client(intents=discord.Intents.default())
    tree = app_commands.CommandTree(client)

    @client.event
    async def on_ready():
        print(f"{client.user} is now running.")
        try:
            await tree.sync()
            print("Commands synced successfully.")
        except Exception as e:
            print(e)

    ## generates the verification key
    @tree.command(name='keygen', description='Sends a key for verification. Can only be used with Manage Roles permissions.')
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.cooldown(rate=1, per=5, key=lambda lol: (lol.guild.id, lol.user.id))
    async def keygen(interaction: discord.Interaction):
        if not interaction.user.guild_permissions.manage_roles:
            return await interaction.response.send_message("You do not have permission to use this command.")
        
        else:
            verif_key = keygenr()

            # Default json template
            # Write into json from this dict
            lmaos = {
                "available": [],
                "used": []
            }

            # Read old json
            lolx = open('key.json', 'r')
            try:
                lmaox = json.load(lolx)
                # Test if the dict works, if not rewrite file
                with lmaox as ppp:
                    lolpp = ppp['available']
                    lolkk = ppp['used']
                lolx.close()
            except:
                lolx.close()
                with open('key.json', 'w') as qqq:
                    json.dump(
                        lmaos, 
                        qqq, 
                        indent=4, 
                        separators=(',', ':')
                    )
                lolx = open('key.json', 'r')
                lmaox = json.load(lolx)
                lolx.close()
            
            # Dict for individual keys
            keysss = {
                "key": verif_key,
                "expiry_date": 0, # Gonna use epoch here
                "creator": interaction.user.id
            }

            lmaox['available'].append(keysss) # Insert new key into 'available' section
            with open('key.json', 'w') as f:
                json.dump(lmaox, f, indent=4) # Save the json
            # Make embed
            lolff = discord.Embed(description="New Key Created", colour=0xb8c8ff)
            lolff.set_author(name="Keygen",icon_url="https://cdn.discordapp.com/avatars/678544159102992385/eba0a0c10e56d2c6a894c9ac0015f4d5.jpg")
            lolff.add_field(name="Key",value=f"||`{verif_key}`||",inline=False)
            lolff.add_field(name="Created by?",value=f"{interaction.user.display_name} (`{interaction.user.name}`)",inline=True)
            lolff.add_field(name="Expire date?",value="1/1/1945",inline=True)
            lolff.set_footer(text="Sent from Python")
            return await interaction.response.send_message(embeds=[lolff])

    
    ## verifies the user using the generated key
    @tree.command(name='verify', description='Verifies you using the key provided from your inviter. Works in only servers.')
    @app_commands.checks.cooldown(rate=1, per=30, key=lambda lol: (lol.guild.id, lol.user.id))
    @app_commands.describe(key="Enter your 32 character key.")
    async def verify(
        interaction: discord.Interaction, 
        key: app_commands.Range[str, 32, 32]
    ):
        with open('key.json', 'r') as file:
            key_data = json.load(file)
            
        ## gets the key from the json file & checks if the key is correct    
        verif_key = key_data['verif_key']
        if verif_key == key:
            guild = client.get_guild(853924006264569886)  # gets server id
            member = interaction.user
            role_id = 1127415902296612945 # role id of "verified account"
            role = guild.get_role(role_id)

            if role in member.roles:
                return await interaction.response.send_message("Error: You are already verified!")

            else:
                await member.add_roles(role)
                if interaction.guild is not None:
                    await interaction.response.send_message(f"Successfully verified! Welcome to the server, {interaction.user.mention}!")
                else:
                    await interaction.response.send_message(f"Successfully verified! Welcome to the server!")

            # - No longer deletes, edits the json
            try:
                os.remove("key.json")
            except OSError:
                pass
            return
        
        else:
            return await interaction.response.send_message("Error: Invalid key entered!", ephemeral=False)
    
    client.run(DISCORD_TOKEN)

    ## TODO: implement dm verification
    ## TODO: add ephemerals to most of them

if (__name__ == "__main__"):
    run_bot() 