import nextcord
import random
from guild_database import get_all_guild_ids

color_codes = [
    0xFF0000,  # Red
    0x00FF00,  # Green
    0x0000FF,  # Blue
    0xFFFF00,  # Yellow
    0xFF00FF,  # Magenta
    0x00FFFF,  # Cyan
    0xFFA500,  # Orange
    0x800080,  # Purple
    0x008000,  # Dark Green
    0x000080,  # Navy Blue
    0x800000,  # Maroon
    0x008080,  # Teal
    0xFFC0CB,  # Pink
    0xFFD700,  # Gold
    0xA52A2A,  # Brown
    0x800000,  # Dark Red
    0x00FF7F,  # Spring Green
    0x808000,  # Olive
    0x008080,  # Teal
    0x008000,  # Green
    0x000080,  # Navy
    0x0000FF,  # Blue
    0xFF00FF,  # Magenta
    0xFF0000,  # Red
    0xFFA500   # Orange
]


def create_embed(title, description, colour, fields):
    embed = nextcord.Embed(
        title=title,
        description=description,
        color=colour
    )
    for field in fields:
        embed.add_field(name=field[0], value=field[1], inline=field[2])

    embed.set_footer(text="Developed by de_Chaplin", icon_url="https://avatars.githubusercontent.com/u/85872356?v=4")
    return embed


def get_random_colour():
    return random.choice(color_codes)


def create_image_embed(title, description, colour, url):
    embed = nextcord.Embed(
        title=title,
        description=description,
        color=colour
    )

    embed.set_image(url=url)

    embed.set_footer(text="Developed by de_Chaplin", icon_url="https://avatars.githubusercontent.com/u/85872356?v=4")
    return embed


guildID = []


def get_guild_id():
    guildID = get_all_guild_ids()
    return guildID


