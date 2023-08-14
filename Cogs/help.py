import nextcord
from nextcord.ext import commands
from nextcord import Interaction

from Bot.functions import *


class Help(commands.Cog):
    def __init__(self, client):
        self.client = client

        guild_ids = get_guild_id()

    # Help command
    @nextcord.slash_command(name="help", guild_ids=get_guild_id())
    async def main(self, interaction: Interaction):
        pass

    @main.subcommand(name="main", description="Shows the main help commands")
    async def help(self, interaction: Interaction):
        embed = create_embed("Bot Help", "Commands for de_Bot", get_random_colour(), [
            ("help vac", "Displays command for the VAC Checking", True),
            ("help search", "Displays commands for the search tools", True),
            #("help fun", "SoonTM", True),

            #("help music", "SoonTM", True),
            #("setPrefix", "Change the prefix for the server", True),
            #("checkPrefix", "Shows current prefix for the server", True),
        ])

        await interaction.response.send_message(embed=embed)

    # VAC Checker Help command
    @main.subcommand(name="vac", description="Shows the available commands for VAC checker")
    async def vac(self, interaction: Interaction):
        embed = create_embed("VAC Checker Help", "Commands for the VAC Checker Bot", get_random_colour(), [
            ("vac status <steamID>", "Check the status of a specific account", True),
            ("vac add <steamID>", "Add a steam account to the database", True),
            ("vac remove <steamID>", "Remove a steam account from the database", True),
        ])

        await interaction.response.send_message(embed=embed)

    # Search Help command
    @main.subcommand(name="search", description="Shows the available commands for searching")
    async def search(self, interaction: Interaction):
        embed = create_embed("de_Search help", "Commands for the search Bot", get_random_colour(), [
            ("generate <prompt>", "SoonTM", True),  # TODO
            ("image <prompt>", "Gets an image", True),  # TODO
            #("search <prompt>", "Searches using <> search engine", True),  # TODO

            ("wiki <prompt>", "Searches using the Wikipedia search engine", True),  # TODO
            ("define <prompt>", "Searches using the Dictionary search engine", True),  # TODO
            ("arrr <prompt>", "Searches using the Rezi.one search engine", True),  # TODO
        ])

        await interaction.response.send_message(embed=embed)


async def setup(client):
    client.add_cog(Help(client))
