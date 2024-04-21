import sys
import time
import json
import uuid
import discord
import traceback
from bot import Env
from discord import app_commands
from discord.ext import commands

# For colorcoding purposes
from colorcode import cc as fxc
from colorcode import p as f

class Auth(commands.Cog):
    def __init__(self, client:commands.Bot):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        f.PRINTX("Auth cog loaded")
    
    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        # Handle the errors here
        if isinstance(error, commands.MemberNotFound):
            await interaction.response.send_message(f"I could not find member '{error.argument}'. Please try again")

        elif isinstance(error, commands.CommandOnCooldown):
            # (cooldown, retry_after, type)
            await interaction.response.send_message(f"Command on cooldown! Try again in {error.retry_after} seconds.")

        elif isinstance(error, commands.MissingRequiredArgument):
            await interaction.response.send_message(f"`{error.param.name}` is a required argument.")
            
        else: # All unhandled errors will print their original traceback
            print(f'Ignoring exception in command {interaction.command}:', file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def keygenr(self):
        return str(uuid.uuid4()) # Generate Keys using UUID v4
        'return str(secrets.token_hex(16))' # Old way of making keys, using secrets module

    # - AUTH METHOD
    ## generates the verification key
    @app_commands.command(name='keygen', description='Sends a key for verification. Can only be used with Manage Roles permissions.')
    @app_commands.checks.has_permissions(manage_roles=True)
    @app_commands.checks.cooldown(rate=1, per=5, key=lambda lol: (lol.guild.id, lol.user.id))
    async def keygen(self, interaction: discord.Interaction):
        if not interaction.user.guild_permissions.manage_roles:
            return await interaction.response.send_message("You do not have permission to use this command.")
        
        else:
            verif_key = self.keygenr()
            current_epoch = int(time.time())

            # structure of the json looks something like this:
            _p = {
                "available": [
                    {
                        "key": "a key",
                        "expiry_date": 0, 
                        "date_created": "current epoch time", 
                        "creator": "id of the creator" 
                    },
                    {
                        "key": "a different key",
                        "expiry_date": 0, 
                        "date_created": "current epoch time", 
                        "creator": "id of the creator"
                    }
                ],
                "invalid": [
                    {
                        "key": "a key",
                        "expiry_date": 0, 
                        "date_created": "current epoch time", 
                        "creator": "id of the creator",
                        "reason": "Expired"
                    },
                    {
                        "key": "a different key",
                        "expiry_date": 0, 
                        "date_created": "current epoch time", 
                        "creator": "id of the creator",
                        "reason": "Used",
                        "used_by": 764133642716708894,
                        "date_used": "epoch unix time"
                    }
                ]
            }
            # Basically, im just making a larger sized json that instead of deleting the file itself, it just keeps updating the file
            # It will keep rewriting over itself every time a new key is made
            # So in theory, it just becomes a database for keys. I might have to migrate to something else in the future lmao


            # Default json template
            # Write into json from this dict
            lmaos = {
                "available": [],
                "invalid": []
            }

            # Read old json
            try:
                lolx = open('key.json', 'r')
                lmaox = json.load(lolx)
                # Test if the dict works, if not rewrite file
                lmaox['available']
                lolx.close()
            except:
                try: lolx.close()
                except: pass
                # Completely rewrite file as the checking previously failed
                with open('key.json', 'w') as qqq:
                    json.dump(
                        lmaos, 
                        qqq, 
                        indent=4
                    )
                lolx = open('key.json', 'r')
                lmaox = json.load(lolx)
                lolx.close()
            
            # Dict for individual keys
            # This will be the json data for individual keys that will be put in "available" list in the json.
            keysss = {
                "key": verif_key,
                "expiry_date": 0, # Gonna use epoch here
                "date_created": current_epoch, # Current time in epoch unix
                "creator": interaction.user.id # ID of author
            }

            lolx = open('key.json', 'r')
            lmaox = json.load(lolx)
            lmaox['available'].append(keysss) # Insert new key into 'available' section

            lolx.close()
            with open('key.json', 'w') as fppp:
                json.dump(lmaox, fppp, indent=4) # Save the json

            # Make embed
            lolff = discord.Embed(description="New Key Created", colour=0xb8c8ff)
            lolff.set_author(name="Keygen",icon_url="https://cdn.discordapp.com/attachments/798029919661064225/1231273495564910682/key-512.png?ex=66365bcd&is=6623e6cd&hm=ece1706643ad6603a3419e629ebb226c994322ad71f3ebfa4c3c8567ce177639&")
            lolff.add_field(name="Key",value=f"```{verif_key}```",inline=False)
            lolff.add_field(name="Created by?",value=f"{interaction.user.display_name} (`{interaction.user.name}`)",inline=True)
            lolff.add_field(name="Expire date?",value="1/1/1945",inline=True)
            lolff.set_footer(text="Sent from Python")
            f.PRINTX(f"Key generated by {interaction.user.display_name} ({interaction.user.name}) ID: {interaction.user.id}")
            return await interaction.response.send_message(embeds=[lolff])


    ## verifies the user using the generated key
    # REMIND ME TO WRITE COMMENTS FOR THIS, Im sleeping tonight
    @app_commands.command(name='verify', description='Verifies you using the key provided from your inviter.')
    @app_commands.checks.cooldown(rate=1, per=30, key=lambda lol: (lol.guild.id, lol.user.id))
    @app_commands.describe(key="Enter your 36 character key.")
    async def verify(
        self,
        interaction: discord.Interaction, 
        key: app_commands.Range[str, 36, 36]
    ):
        with open('key.json', 'r') as file:
            key_data = json.load(file)
            
        ## gets the key from the json file & checks if the key is correct    
        verif_key = key_data['available']
        verif_key_invalid = key_data['invalid']
        for pos, keylmao in enumerate(verif_key):   # Loops through the "available" list
            if key != keylmao['key']:               # Checks for all wrong keys.
                pass                                # If a matching key is found, it breaks the loop and verifies the user.
            else:
                guild = self.client.get_guild(int(Env.DISCORD_GUILD_ID))  # gets server id
                member = interaction.user
                role_id = int(Env.DISCORD_VERIFIED_ROLE_ID) # role id of "verified account"
                role = guild.get_role(role_id)

                if role in member.roles:
                    await interaction.response.send_message("Error: You are already verified!")
                    return

                else:
                    await member.add_roles(role)
                    if interaction.guild is not None:
                        await interaction.response.send_message(f"Successfully verified! Welcome to the server, {interaction.user.mention}!")
                    else:
                        await interaction.response.send_message(f"Successfully verified! Welcome to the server!")

                # - No longer deletes, edits the json
                fread = open('key.json', 'r')
                jsonfile = json.load(fread)
                jsonfile['available'][pos]
                fread.close()

                epoch_now = int(time.time())

                keylmao['reason'] = "Used"
                keylmao['used_by'] = interaction.user.id
                keylmao['date_used'] = epoch_now


                invalid_list = jsonfile['invalid']
                invalid_list.append(keylmao)

                fileqqq = open('key.json', 'w')
                json.dump(jsonfile, fileqqq, indent=4)
                fileqqq.close()
                f.PRINTX(f"Verified the user {interaction.user.display_name} ({interaction.user.name}) ID: {interaction.user.id}")
                return
            
        for pos, keylmaos in enumerate(verif_key_invalid):
            if key != keylmaos['key']:      # Checks for all wrong keys.
                pass                        # If a matching key is found, it breaks the loop and verifies the user.
            else:
                # - A little list of invalid key reasons
                lolpp = keylmaos['reason']
                if lolpp == "Used":
                    return await interaction.response.send_message("Error: That key has already been used!", ephemeral=False)
                if lolpp == "Expired":
                    return await interaction.response.send_message("Error: That key is expired!", ephemeral=False)
                else:
                    return await interaction.response.send_message("Error: That key is invalid!", ephemeral=False)
                
        return await interaction.response.send_message("Error: No such key is available!", ephemeral=False)
    
async def setup(client:commands.Bot) -> None:
    await client.add_cog(Auth(client))