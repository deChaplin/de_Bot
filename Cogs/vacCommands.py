import nextcord
from nextcord.ext import commands
from nextcord import Interaction
from Bot.functions import *
from Checker import vacChecker
from Bot.env import get_steam_key


class VacCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.KEY = get_steam_key()

    # Main command for the vac checker
    @nextcord.slash_command(name="vac", guild_ids=get_guild_id())
    async def main(self, interaction: Interaction):
        pass

    # Command to check the status of a steam account
    @main.subcommand(name="status", description="Get the status of a steam account using it's steamID")
    async def status(self, interaction: Interaction, arg: str):
        try:
            steamID, name, game_banned, game_bans, vac_banned, vac_bans, last_ban = \
                vacChecker.check_vac(self.KEY, arg, interaction.user.id)

            if game_banned == "Yes" or vac_banned == "Yes":
                color = 0xFF0000
            else:
                color = 0x44ff00

            embed = create_embed("Profile Status", "The current status of " + name, color, [
                ("Name - ", name, False),
                ("Steam ID - ", steamID, False),
                ("Game Banned - ", game_banned, False),
                ("Game Bans - ", game_bans, False),
                ("VAC Banned - ", vac_banned, False),
                ("VAC Bans - ", vac_bans, False),
                ("Last Ban - ", get_days_since_ban(last_ban), False)
            ])

            await interaction.response.send_message(embed=embed)
        except:
            await interaction.response.send_message("Error checking account!")

    # Command to add a steam account to the database
    @main.subcommand(name="add", description="Add a steam account to be watched")
    async def add(self, interaction: Interaction, arg: str):
        try:
            name = vacChecker.add_account(self.KEY, arg, interaction.user.id)
            await interaction.response.send_message(f"{name} added to database!")
        except:
            await interaction.response.send_message("Error adding account to database!")

    # Command to remove a steam account from the database
    @main.subcommand(name="remove", description="Remove a steam account from the watch list")
    async def remove(self, interaction: Interaction, arg: str):
        if vacChecker.remove_account(arg, interaction.user.id):
            await interaction.response.send_message("Account removed from database!")
        else:
            await interaction.response.send_message("Only the person who added the account can remove it!")


async def setup(client):
    client.add_cog(VacCommands(client))


# Take the days since last ban and return how many days ago it was
def get_days_since_ban(days):
    if days == 0:
        return "Today"
    elif days == 1:
        return "Yesterday"
    else:
        return str(days) + " days ago"