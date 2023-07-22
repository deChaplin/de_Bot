import nextcord
from nextcord.ext import commands
from Bot.functions import *
from Bot.env import get_rezi, get_cse, get_google
from nextcord import Interaction
import wikipedia
from API import handle
from googleapiclient.discovery import build


class SearchCommands(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.REZI_KEY = get_rezi()
        self.SEARCH_ENGINE_ID = get_cse()
        self.GOOGLE_KEY = get_google()

        guild_ids = get_guild_id()

    @nextcord.slash_command(name="arrr", description="Search for a game", guild_ids=get_guild_id())
    async def arrr(self, interaction: Interaction, game: str):
        try:
            titles, links = handle.search_rezi(game, self.REZI_KEY)

            results = ""

            for i in titles:
                results += i + "\n" + links[titles.index(i)] + "\n\n"

            emb = create_embed(f"Downloads for - {game}", "", get_random_colour(),
                               [("", results, False)])

            await interaction.response.send_message(embed=emb, ephemeral=False)
        except:
            emb = create_embed(f"Unable to find game", "Please check manually ️", get_random_colour(),
                               [("", "https://rezi.one/", False)])
            await interaction.response.send_message(embed=emb, ephemeral=False)

    @nextcord.slash_command(name="wiki", description="Search wikipedia", guild_ids=get_guild_id())
    async def wiki(self, interaction: Interaction, arg: str):
        try:
            page = wikipedia.page(arg)
            title = page.title

            try:
                summary = wikipedia.summary(arg, sentences=3)
            except:
                summary = "Summary not available :("
            url = page.url

            emb = create_embed("Wikipedia", "", get_random_colour(),
                               [(title, "", False), ("Summary", summary, False), ("Link", url, False)])

            await interaction.response.send_message(embed=emb, ephemeral=False)
        except:
            emb = create_embed("Wikipedia", "Error getting information :(", get_random_colour(),
                               [("Link", f"https://en.wikipedia.org/wiki/{arg}", False)])
            await interaction.response.send_message(embed=emb, ephemeral=False)

    @nextcord.slash_command(name="image", description="Search for an image", guild_ids=get_guild_id())
    async def image(self, interaction: Interaction, arg: str):
        ran = random.randint(0, 9)
        resource = build("customsearch", "v1", developerKey=self.GOOGLE_KEY).cse()
        result = resource.list(q=f"{arg}", cx=self.SEARCH_ENGINE_ID, searchType="image").execute()
        url = result['items'][ran]['link']

        emb = create_image_embed(f"Your image - {arg}", "", get_random_colour(), url)

        await interaction.response.send_message(embed=emb, ephemeral=False)

    @nextcord.slash_command(name="define", description="Gets the definition of a word", guild_ids=get_guild_id())
    async def define(self, interaction: Interaction, arg: str):
        try:
            noun_def, verb_def = handle.search_dict(arg)

            nouns = ""
            verbs = ""

            for i in noun_def:
                nouns += i + "\n\n"

            for i in verb_def:
                verbs += i + "\n\n"

            emb = create_embed(f"Definition for - {arg}", "", get_random_colour(),
                               [("Noun", nouns, False),
                                ("Verb", verbs, False)])

            await interaction.response.send_message(embed=emb, ephemeral=False)
        except:
            emb = create_embed("Dictionary", "Error getting information :(", get_random_colour(),
                               [("", f"Sorry I couldn't get the definition for - {arg}", False)])
            await interaction.response.send_message(embed=emb, ephemeral=False)


async def setup(client):
    client.add_cog(SearchCommands(client))
