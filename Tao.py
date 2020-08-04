import os
import random
import discord
from discord.ext import commands
import shelve
from googlesearch import search
import asyncio
import ffmpeg


# Assigning id's and bot object
TOKEN = os.environ['TOKEN']
GUILD = os.environ['GUILD']
bot = commands.Bot(command_prefix='tao ')

# Opening the datafiles with player data
unhinged_file_r = open('unhinged', 'r')
hunt_file_r = open('hunt', 'r')
control_file_r = open('control', 'r')

# Reading player data (stored as one id per line)
unhinged = unhinged_file_r.read().splitlines()
hunt = hunt_file_r.read().splitlines()
control = control_file_r.read().splitlines()

# Closing player data files
unhinged_file_r.close()
hunt_file_r.close()
control_file_r.close()

# Data management for nat20 log
nat20 = shelve.open('nat20.txt', flag='c', writeback=True)

# Data management for quotes
quote_file_r = open('quote','r')
quotes = quote_file_r.read().splitlines()
quote_file_r.close()

# Preparing variables to track tardiness
# (initial is for startup, prepared for storing list of players)
initial = [0]
prepared = []

# Music variables
songs = asyncio.Queue()
play_next_song = asyncio.Event()

# Current campaigns
campaigns = ['unhinged', 'hunt', 'control']

# Stores last 1000 message data in a_cache
a_cache = []
for x in bot.cached_messages:
    a_cache.append(x)


# Function that resets lists each time campaign starts
def reset():
    global prepared
    global initial
    prepared[:] = []
    initial[:] = [0]


# Posts message to log when bot ready
# @bot.event
# async def on_ready():
#     print(f'{bot.user.name} has connected to Discord!')
#     # channel=bot.get_channel(566459563319099403)
#     # await channel.send('Tao has returned from training.')
#
#
# # Start Music
# async def audio_player_task():
#     while True:
#         play_next_song.clear()
#         current = await songs.get()
#         current.start()
#         await play_next_song.wait()
#
#
# def toggle_next():
#     bot.loop.call_soon_threadsafe(play_next_song.set)
#
#
# @bot.command(name='play', help='Play a song')
# async def music_join(ctx,url):
#     audio=discord.AudioSource
#     channel=ctx.author.voice.channel
#     ffmpegAudio(audio)
#     if bot.user not in bot.voice_clients:
#         voice = await channel.connect()
#     player = await voice.play(source=audio.read.(url), after=toggle_next)
#     await songs.put(player)
# End Music


# Bans a user with a reason
@bot.command(name='kill', help='Ban a user')
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.User = None, reason=None):
    if member is None or member == ctx.message.author:
        await ctx.channel.send("I cannot kill you")
        return
    if reason is None:
        reason = "For defiling these lands"
    message = f"You have been banned from {ctx.guild.name} for {reason}"
    await member.send(message)
    await ctx.guild.ban(member, reason=reason)
    await ctx.channel.send(f"I have slain {member}.")


# # Mutes a user with a reason
# @bot.command(name='silence', help='mute a user')
# @commands.has_permissions(administrator=True)
# async def mute(ctx, member: discord.User = None, reason=None):
#     if member is None or member == ctx.message.author:
#         await ctx.channel.send("You cannot be silenced")
#         return
#     if reason is None:
#         reason = "Trash cannot speak"
#     message = f"I have silenced you for {reason}"
#     role = discord.utils.get(member.guild.roles, name="Tina's Punishment")
#     await member.send(message)
#     await bot.add.roles(member, role, reason=reason)
#     await ctx.channel.send(f"{member} is now unable to speak.")


# Records natural 20's
@bot.command(name='log20', help='''Records someone getting a nat20. Ex.(log20 @user). 
May be used for corrections in format (log20 @user correction number''')
@commands.has_role('Dungeoneer')
async def nat20log(ctx, member: discord.User = None):
    auth = str(ctx.message.author)
    member_str = str(member)
    if 'correction' in ctx.message.content:
        for character in ctx.message.content:
            if character.isnumeric():
                if member is None or member == ctx.message.author:
                    nat20[auth] -= int(character)
                    await ctx.send(f"The count for {ctx.message.author} is now {nat20[auth]}.")
                    return
                else:
                    nat20[member_str] -= int(character)
                    await ctx.send(f"The count for {member} is now {nat20[member_str]}.")
                    return
    if member is None or member == ctx.message.author:
        if auth not in nat20:
            nat20[auth] = 0
        nat20[auth] += 1
        return
    else:
        if member_str not in nat20:
            nat20[member_str] = 0
        nat20[member_str] += 1


# Shows current nat20 log
@bot.command(name='show20', help="Shows log of nat20's. Ex.(show20)")
@commands.has_role('Dungeoneer')
async def nat20log(ctx):
    await ctx.send("Here is a list of people and the amount of natural 20's they have got: ")
    temp_log = []
    for key in nat20:
        temp_log.append((key, nat20[key]))
    for pair in temp_log:
        await ctx.send(f"{pair[0]} has rolled {pair[1]} natural 20's.")


# Keeps quotes of people
@bot.command(name='quote', help="Saves a quote")
@commands.has_role('Dungeoneer')
async def save_quotes(ctx, member: discord.User = None):
    auth=str(ctx.message.author)
    content = ctx.message.content
    if member is None:
        await ctx.send('Please mention a user.')
        return
    temp_quote = content.split()
    temp_quote = temp_quote[3:]
    temp_quote = " ".join(temp_quote)
    quotes.append(f"{member} said: '{temp_quote}'")
    await ctx.send('A quote was added for {}'.format(member))


# Shows a random quote from a user
@bot.command(name='show', help="Shows a random quote from a user. Ex.(show @user). if no user, picks from all.")
@commands.has_role('Dungeoneer')
async def quote_log(ctx, member: discord.User = None):
    member_str = str(member)
    if member is None:
        await ctx.send(random.choice(quotes))
        return
    single_user_temp_quotes = [quote for quote in quotes if member_str in quote]
    if not single_user_temp_quotes:
        await ctx.send(f"{member} does not have any quotes")
        return
    await ctx.send(random.choice(single_user_temp_quotes))


# After called, starts tracking who speaks in discord
@bot.command(name='start', help='Takes a roll call')
async def start_campaign(ctx):
    global initial
    await ctx.send('Please type anything to indicate your presence')
    initial.insert(0, 1)


# Stops tracking who speaks in discord
# Compares list of who spoke to given campaign players
# If someone did not speak, posts a message mentioning them
@bot.command(name='complete', help='Used after start, ends roll call. Ex. (complete campaign)')
async def end_campaign(ctx):
    con = str(ctx.message.content)

    if 'unhinged' in con:
        await ctx.send('Roll call has ended for unhinged')
        for person_id in unhinged:
            if person_id not in prepared:
                ids = '<@{}>'.format(person_id)
                await ctx.send('The following player is not prepared: {} laugh at them.'.format(ids))

    if 'hunt' in con:
        await ctx.send('Roll call has ended for hunt')
        for person_id in hunt:
            if person_id not in prepared:
                ids = '<@{}>'.format(person_id)
                await ctx.send('The following player is not prepared: {} laugh at them.'.format(ids))

    if 'control' in con:
        await ctx.send('Roll call has ended for control')
        for person_id in control:
            if person_id not in prepared:
                ids = '<@{}>'.format(person_id)
                await ctx.send('The following player is not prepared: {} laugh at them.'.format(ids))

    reset()


# Allows a user to join a campaign
@bot.command(name='join', help='To join a campaign. Ex. (join campaign)')
async def join(ctx):
    auth = str(ctx.message.author.id)
    con = str(ctx.message.content)

    if 'unhinged' in con and auth not in unhinged:
        unhinged.append(auth)
        await ctx.send('You have joined unhinged')
    elif 'unhinged' in con:
        await ctx.send('You are already in the campaign.')
    if 'hunt' in con and auth not in hunt:
        hunt.append(auth)
        await ctx.send('You have joined hunt')
    elif 'hunt' in con:
        await ctx.send('You are already in the campaign.')
    if 'control' in con and auth not in control:
        control.append(auth)
        await ctx.send('You have joined control')
    elif 'control' in con:
        await ctx.send('You are already in the campaign.')


# Lets a user leave a campaign
@bot.command(name='leave', help='To leave a campaign. Ex.(leave campaign)')
async def leave(ctx):
    auth = str(ctx.message.author.id)
    con = str(ctx.message.content)

    if 'unhinged' in con and auth in unhinged:
        unhinged.remove(auth)
        await ctx.send('You have been removed from unhinged')
    elif 'unhinged' in con:
        await ctx.send('You are not in the campaign.')
    if 'hunt' in con and auth in hunt:
        hunt.remove(auth)
        await ctx.send('You have been removed from hunt')
    elif 'hunt' in con:
        await ctx.send('You are not in the campaign.')
    if 'control' in con and auth in control:
        control.remove(auth)
        await ctx.send('You have been removed from control')
    elif 'control' in con:
        await ctx.send('You are not in the campaign.')


# Saves the player data and shuts down the bot
@bot.command(name='save', help='Saves player data and shuts down')
async def save(ctx):
    unhinged_file_w = open('unhinged', 'w')
    hunt_file_w = open('hunt', 'w')
    control_file_w = open('control', 'w')
    quote_file_w = open('quote', 'w')
    for person_id in unhinged:
        unhinged_file_w.write(person_id+'\n')
    for person_id in hunt:
        hunt_file_w.write(person_id+'\n')
    for person_id in control:
        control_file_w.write(person_id+'\n')
    for single_quote in quotes:
        quote_file_w.write(single_quote+'\n')
    unhinged_file_w.close()
    hunt_file_w.close()
    control_file_w.close()
    quote_file_w.close()
    nat20.sync()
    nat20.close()
    await ctx.send('Player data has been saved')
    await ctx.send('Tao is leaving to train.')
    await bot.logout()


# Allows users to see which players are in the campaigns
@bot.command(name='players', help='Check the players in a campaign. Ex.(players campaign)')
async def players(ctx):
    con = str(ctx.message.content)
    await ctx.send('These players are in the campaign: ')

    if 'unhinged' in con:
        for person_id in unhinged:
            await ctx.send(str(bot.get_user(int(person_id))))

    if 'hunt' in con:
        for person_id in hunt:
            await ctx.send(str(bot.get_user(int(person_id))))

    if 'control' in con:
        for person_id in control:
            await ctx.send(str(bot.get_user(int(person_id))))


# Randomly chooses users as the most or least popular person
@bot.command(name='popular', help='Gives the most and least popular person')
async def best_person(ctx):
    people = bot.users
    await ctx.send('The most popular person is: '+str(random.choice(people)))
    await ctx.send('The least popular person is: ' + str(random.choice(people)))


# Examines all messages
@bot.event
async def on_message(message):
    global prepared
    auth = str(message.author.id)
    con = message.content

    # Used in conjunction with start to track who speaks
    if (auth in unhinged) and initial[0] == 1:
        prepared.append(auth)

    # Responds to people thanking the bot
    if con.lower() == 'thanks tao' or con == 'thank you tao' or con == 'ty tao' or con == 'thanks so much tao':
        await message.channel.send("You are welcome, it's my duty")

    # Gives wisdom when people say wisdom
    if con == 'wisdom':
        ninja = ['No one saves us but ourselves. No one can and no one may. We ourselves must walk the path.',
                 'Three things cannot be long hidden: the sun, the moon, and the truth.',
                 'The mind is everything. What you think you become.']
        response = random.choice(ninja)
        await message.channel.send(response)

    # Allows messages to eventually reach commands
    await bot.process_commands(message)


# Initializes the bot object
bot.run(TOKEN)
