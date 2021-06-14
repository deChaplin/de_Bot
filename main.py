#The bot needs to be restarted for any changes to take action :)

import os
import discord
import random
import json 
import requests
from discord.ext import commands, tasks
from itertools import cycle

from keep_alive import keep_alive #keeps the bot running using Uptimerobot to ping it





#Makes the bot use prefixes.json
def get_prefix(client, message):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]

intents = discord.Intents(messages=True, guilds=True, reactions=True, members=True) #for autorole
client = commands.Bot(command_prefix = get_prefix, intents = intents)     #sets the command_prefix
client.remove_command('help')   #removes default help command

#######################
#   Prefix Commands   #
#######################

#When bot joins the server...
@client.event


async def on_guild_join(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "."

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

#When bot leaves the server...
@client.event
async def on_guild_remove(guild):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    del prefixes[str(guild.id)]

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)


#When bot is pinged...

@client.event
async def on_message(msg):
print("User ID: ", message.author.id)
    try:

        if msg.mentions[0] == client.user:

            with open("prefixes.json", "r") as f:
                prefixes = json.load(f)

            pre = prefixes[str(msg.guild.id)]
            
            await msg.channel.send(f"My current prefix is = '{pre}'")

    except:
        pass

    await client.process_commands(msg)


#Global variables
colours = [0x1abc9c, 0x11806a, 0x2ecc71, 0x1f8b4c, 0x3498db, 0x206694, 0x9b59b6, 0x71368a, 0xe91e63, 0xad1457, 0xf1c40f, 0xc27c0e, 0xe67e22, 0xa84300, 0xe74c3c, 0x992d22, 0x95a5a6, 0x607d8b, 0x979c9f, 0x546e7a, 0x7289da, 0x99aab5]
#status = cycle([".", ".h", ".he", ".hel", ".help", ".help f", ".help fo", ".help for", ".help for c", ".help for co", ".help for com", ".help for comm", ".help for comma", ".help for comman", ".help for command", ".help for commands"]) #,".help for command",".help for comman",".help for comma",".help for comm",".help for com",".help for co",".help for c",".help for",".help fo",".help f",".help",".hel",".he",".h","."])

#status = cycle([".help for commands", ".help", ".help for", ".help for commands"])
status = cycle(["@me for prefix", "Default prefix is '.'"])

#Tic Tac Toe variables
player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

#====================================
#============== Events ==============
#====================================

@client.event
async def on_ready():   #when bot starts do ...
    change_status.start()
    print('Bot is ready.')
#STATUS CYCLE LOOP
@tasks.loop(seconds=2)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))
#ERRORS
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command. Use .help to check the list of commands.")
#AUTO ROLE = NEEDED
@client.event
async def on_member_join(ctx):
    autorole = discord.utils.get(ctx.guild.roles, name = 'Member')
    await ctx.add_roles(autorole)
#COOLDOWN
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown): #checks if the commands is on cooldown.
        message = "You have used that command too often. It is now on cooldown."
        await ctx.send(message)

#======================================
#============== commands ==============
#======================================

#============== help commands ==============
@client.command()
async def help(ctx):
    embed = discord.Embed(colour=random.choice(colours), title="Help!", description="See my current prefix by typing @myname") #Add your name here once you contribute lol

    embed.add_field(name="__General commands__", value="=========================", inline=False)
    embed.add_field(name="ping", value="Sends the bot's ping.", inline=False)
    #Music
    embed.add_field(name="__Music__", value="🎶 .music", inline=False)
    #games
    embed.add_field(name="__Games__", value="🎮 .games", inline=False)
    #Economy
    embed.add_field(name="__Economy__", value="‍💸 .economy", inline=False)
    #Admin
    embed.add_field(name="__Admin__", value="👮‍♂️ .admin", inline=False)

    embed.set_footer(text="Developed by de_Chaplin")
    await ctx.send(embed=embed)

#Music
@client.command()
async def music(ctx):
    embed = discord.Embed(colour=random.choice(colours), title="🎶 Music Help!", description="Displays all commands for music.")

    embed.add_field(name="__Music__", value="=========================================================", inline=False)
    embed.add_field(name="play", value="Plays the song (Coming soon)", inline=False)
    embed.add_field(name="stop", value="Stops playing music.", inline=False)

    await ctx.send(embed=embed)

#Games
@client.command()
async def games(ctx):
    embed = discord.Embed(colour=random.choice(colours), title="🎮 Games Help!", description="All game commands.")

    embed.add_field(name="__Games__", value="=========================================================", inline=False)
    embed.add_field(name="tictactoe", value="Starts a game of tic tac toe.", inline=False)
    embed.add_field(name="place", value="Place a mark on the tictactoe board (Between 1 and 9.)", inline=False)
    embed.add_field(name="end", value="Ends the current game of tic tac toe.", inline=False)

    await ctx.send(embed=embed)

#Economy
@client.command()
async def economy(ctx):
    embed = discord.Embed(colour=random.choice(colours), title="🤑 Economy Help!", description="Displays all commands for the economy system.")

    embed.add_field(name="__Economy__", value="=========================================================", inline=False)
    embed.add_field(name="balance/bal", value="Displays your current balance", inline=False)
    embed.add_field(name="deposit/dp", value="Deposits money from your wallet into your bank", inline=False)
    embed.add_field(name="withdraw/wd", value="Withdraws money from your bank into your wallet", inline=False)
    embed.add_field(name="beg", value="Beg for money 🥺", inline=False)
    embed.add_field(name="slots", value="Gamble some moneyyyyy 🤑", inline=False)
    embed.add_field(name="rob", value="Robs whoever you @ 🦹‍♂️", inline=False)
    embed.add_field(name="send", value="Sends money from your wallet to whoever you @ 💸", inline=False)

    await ctx.send(embed=embed)

#Admin
@client.command()
async def admin(ctx):
    embed = discord.Embed(colour=random.choice(colours), title="👮‍♂️ Admin Help!", description="These will only work for admins 😉")

    embed.add_field(name="__Admin__", value="=========================================================", inline=False)
    embed.add_field(name="clear", value="Deletes messages ('clear 10' would clear 10 messages, default is 5)", inline=False)
    embed.add_field(name="changeprefix", value="Changes the prefix for the bot", inline=False)

    await ctx.send(embed=embed)



#============== Music bot =============== **IN WORKING PROGRESS**
@client.command()
async def play(ctx, url : str):
    voiceChannel = discord.utils.get(ctx.guild.voice_channels, name='test')
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await voiceChannel.connect()

@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@client.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()

#================= Economy System ================= **IN WORKING PROGRESS**
#commands
@client.command(aliases=['bal'])
async def balance(ctx, member: discord.Member = None):  #checks users balance
    if not member:
        member = ctx.author
    await open_account(member)  #starts the open account code

    users = await get_bank_data()
    user = member
    wallet_amount = users[str(user.id)]["wallet"]
    bank_amount = users[str(user.id)]["bank"]

    balEmbed = discord.Embed(title = f"{member.name}'s balance", colour = discord.Color.red())
    balEmbed.add_field(name = "Wallet", value = wallet_amount)
    balEmbed.add_field(name = "Bank", value = bank_amount)
    await ctx.send(embed = balEmbed)

@client.command()
@commands.cooldown(1, 30, commands.BucketType.user) #Sets the cooldown
async def beg(ctx):
    await open_account(ctx.author)

    users = await get_bank_data()
    user = ctx.author
    earnings = random.randrange(101)

    await ctx.send(f"Someone gave you {earnings} coins!")

    users[str(user.id)]["wallet"] += earnings

    with open("mainbank.json", "w") as f:
        json.dump(users, f, indent=4)

#Withdrawing money from bank

@client.command(aliases=['wd'])
async def withdraw(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[1]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,amount)
    await update_bank(ctx.author,-1*amount,'bank')
    await ctx.send(f'{ctx.author.mention} You withdrew {amount} coins')

#deposit money to bank

@client.command(aliases=['dp'])
async def deposit(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return


    await update_bank(ctx.author,amount,'bank')
    await update_bank(ctx.author,-1*amount)
    await ctx.send(f'{ctx.author.mention} You deposited {amount} coins')

#send money to someone else

@client.command()
async def send(ctx,member : discord.Member,amount = None):
    await open_account(ctx.author)
    await open_account(member)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)
    if amount == 'all':
        amount = bal[0]

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return

    await update_bank(ctx.author,-1*amount,'bank')
    await update_bank(member,amount,'bank')
    await ctx.send(f'{ctx.author.mention} You gave {member} {amount} coins')

    #steal money from someone else

###########################
# Make it so you can't spam
###########################

@client.command()
@commands.cooldown(1, 60, commands.BucketType.user) #Sets the cooldown
async def rob(ctx,member : discord.Member):
    await open_account(ctx.author)
    await open_account(member)
    bal = await update_bank(member)

    if bal[0]<100:
        await ctx.send('It is useless to rob him :(')
        return

    earning = random.randrange(0,bal[0])

    await update_bank(ctx.author,earning)
    await update_bank(member,-1*earning)
    await ctx.send(f'{ctx.author.mention} You robbed {member} and got {earning} coins')

#Slots
##############################################
# Make it so the slots appear on white squares
##############################################

@client.command()
@commands.cooldown(1, 45, commands.BucketType.user) #Sets the cooldown
async def slots(ctx,amount = None):
    await open_account(ctx.author)
    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = await update_bank(ctx.author)

    amount = int(amount)

    if amount > bal[0]:
        await ctx.send('You do not have sufficient balance')
        return
    if amount < 0:
        await ctx.send('Amount must be positive!')
        return
    final = []
    for i in range(3):
        a = random.choice(['X','O','Q'])

        final.append(a)

    await ctx.send(str(final))

    if final[0] == final[1] or final[1] == final[2] or final[0] == final[2]:
        await update_bank(ctx.author,2*amount)
        await ctx.send(f'You won :) {ctx.author.mention}')
    else:
        await update_bank(ctx.author,-1*amount)
        await ctx.send(f'You lose :( {ctx.author.mention}')

#saving to mainbank.json & openning accounts

async def open_account(user):
    users = await get_bank_data()

    if str(user.id) in users:
        return False
    else:
        users[str(user.id)] = {}
        users[str(user.id)]["wallet"] = 0
        users[str(user.id)]["bank"] = 100

    with open("mainbank.json", "w") as f:
        json.dump(users, f, indent=4)
    return True

async def get_bank_data():
    with open("mainbank.json", "r") as f:
        users = json.load(f)

    return users

async def update_bank(user, change=0, mode="wallet"):
    users = await get_bank_data()

    users[str(user.id)][mode] += change
    with open ("mainbank.json", "w") as f:
        json.dump(users, f, indent=4)

    bal = users[str(user.id)]["wallet"], users[str(user.id)]["bank"]
    return bal

#============== Tic Tac Toe ===============

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@client.command()
async def end(ctx):
  global gameOver
  if not gameOver:
    gameOver = True
    await ctx.send("Stopping current game...")
  else:
    await ctx.send("There is currently no game running!")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a draw!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")

def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@843788923050262569>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")

#============ other commands =============
#PING
@client.command()
async def ping(ctx):    #when 'ping' is used the bot will send the ping back to the server
    await ctx.send(f'The bots ping is = {round(client.latency * 1000)}ms')

#CLEAR
@client.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount)

#PREFIX COMMAND
@client.command()
@commands.has_permissions(administrator = True)
async def changeprefix(ctx, prefix):
    with open("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    await ctx.send(f"The prefix has been changed to {prefix}")

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

#============================== END ==============================

keep_alive()

client.run(os.environ['TOKEN'])    #runs the bot
