import asyncio
import sys
from datetime import datetime

import logging

import nextcord
from nextcord.ext import commands, tasks
import os
from Checker import vacChecker
import guild_database
import random
from env import get_token, get_steam_key
import functions

# Setting up the client and intents
intents = nextcord.Intents.all()
# Setting up the bots prefix
DEFAULT_PREFIX = '!'

#logging.basicConfig(level=logging.DEBUG)

async def get_prefix(client, message):
    if not message.guild:
        return commands.when_mentioned_or(DEFAULT_PREFIX)(client, message)
    else:
        if guild_database.check_guild(message.guild.id):
            prefix = guild_database.get_prefix(message.guild.id)
            return commands.when_mentioned_or(prefix)(client, message)
        else:
            guild_database.add_guild(message.guild.id, DEFAULT_PREFIX)
            return commands.when_mentioned_or(DEFAULT_PREFIX)(client, message)

client = commands.Bot(command_prefix=get_prefix, intents=intents, help_command=None)

TOKEN = get_token()
KEY = get_steam_key()

# ======================================================================================================================
# Standard Events
# ======================================================================================================================

# On ready
@client.event
async def on_ready():
    vacChecker.start_up()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time} - Bot is ready!")

    if not change_status.is_running():
        change_status.start()

    if not check_vac.is_running():
        check_vac.start()

    guild_database.create_database()

# On bot shutdown
@client.event
async def on_shutdown():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time} - Bot is shutting down. Stopping tasks.")

    if change_status.is_running():
        change_status.stop()
    if check_vac.is_running():
        check_vac.stop()

    await client.close()

# On bot disconnect from discord
@client.event
async def on_disconnect():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time} - Bot is disconnecting. Stopping tasks.")

    if change_status.is_running():
        change_status.stop()
    if check_vac.is_running():
        check_vac.stop()

# On bot connect to discord
@client.event
async def on_connect():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time} - Bot is connecting.")

# On error
@client.event
async def on_error(event, *args, **kwargs):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time} - Error in event {event}: {sys.exc_info()}")

# On guild join
@client.event
async def on_guild_join(guild):
    guild_database.add_guild(guild.id, DEFAULT_PREFIX)
    print(f"Joined {guild.name}")


# On guild remove
@client.event
async def on_guild_remove(guild):
    guild_database.remove_guild(guild.id)
    print(f"Removed {guild.name}")


# On message
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if not guild_database.check_guild(message.guild.id):
        guild_database.add_guild(message.guild.id, DEFAULT_PREFIX)
        functions.get_guild_id()

    mention = f'<@{client.user.id}>'
    if message.content == mention:
        functions.get_guild_id()
        await message.channel.send("I'm using slash commands :)")
        #await message.channel.send("My prefix is " + guild_database.get_prefix(message.guild.id))

    if message.content.startswith(guild_database.get_prefix(message.guild.id)):
        await client.process_commands(message)


# ======================================================================================================================
# Loop Events
# ======================================================================================================================


@tasks.loop(seconds=4)
async def change_status():
    status = [" something", " who gets banned!", " you 👀", " r/Piracy",
           str(get_guilds()) + " servers!"]

    await client.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching,
                                                            name=(random.choice(status))))
        #await asyncio.sleep(4)


# Loop to check for vac bans on all accounts every hour
@tasks.loop(minutes=3)
async def check_vac():
    # Get list of user ids from database
    # iterate through list to check all accounts belonging to user
    # send private message to user

    # Output the current time to the console
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"{current_time} - Checking for VAC bans")

    # Will run for the number of unique discord ids in the database
    discord_ids = vacChecker.get_discord_id()

    if discord_ids:
        for index, id in enumerate(discord_ids):
            user = client.get_user(int(id))

            steam_ids = vacChecker.get_steam_id(int(id))

            for s_index, s_id in enumerate(steam_ids):
                steamID, name, game_banned, game_bans, vac_banned, vac_bans, last_ban = \
                    vacChecker.check_vac(KEY, s_id, int(id))

                if game_banned == "Yes" or vac_banned == "Yes":
                    embed = functions.create_embed("Profile Status", "The current status of " + name,
                                         functions.get_random_colour(), [
                                             ("Name - ", name, False),
                                             ("Steam ID - ", steamID, False),
                                             ("Game Banned - ", game_banned, False),
                                             ("Game Bans - ", game_bans, False),
                                             ("VAC Banned - ", vac_banned, False),
                                             ("VAC Bans - ", vac_bans, False),
                                             ("Last Ban - ", get_days_since_ban(last_ban), False)
                                         ])
                    await user.send(embed=embed)
                    vacChecker.remove_account(steamID, int(id))

        #await asyncio.sleep(60 * 60)


# ======================================================================================================================
# Random functions
# ======================================================================================================================

# Take the days since last ban and return how many days ago it was
def get_days_since_ban(days):
    if days == 0:
        return "Today"
    elif days == 1:
        return "Yesterday"
    else:
        return str(days) + " days ago"


def get_guilds():
    try:
        guilds = guild_database.get_num_guilds()
        if guilds >= 1:
            return guilds
        else:
            return "0"
    except:
        print ("Error getting guilds")
        return "0"


async def main():
    # Loading all cogs
    initial_extensions = []

    for filename in os.listdir('../Cogs'):
        if filename.endswith('.py'):
            initial_extensions.append("Cogs." + filename[:-3])
                # await client.load_extension(f'Cogs.{filename[:-3]}')

    for extension in initial_extensions:
        client.load_extension(extension)

    # Start the loops
    #change_status.start()
    #check_vac.start()

    try:
        await client.start(TOKEN)
    except Exception as e:
        print(f"An error occurred: {e}")


asyncio.run(main())
