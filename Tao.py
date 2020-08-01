import os
import discord
import random
from discord.ext import commands
TOKEN=os.environ['TOKEN']
GUILD=os.environ['GUILD']
bot=commands.Bot(command_prefix='tao ')


#Opening the datafiles with player data
unfiler=open('unhinged','r')
huntfiler=open('hunt','r')
controlfiler=open('control','r')

#reading player data
unhinged=unfiler.read().splitlines()
hunt=huntfiler.read().splitlines()
control=controlfiler.read().splitlines()
unfiler.close()
huntfiler.close()
controlfiler.close()

#preparing variables to track tardiness
initial=[0]
prepared=[]

#current campaigns
campaigns=['unhinged','hunt','control']

#stores last 1000 message data in acache
acache = []
for x in bot.cached_messages:
    acache.append(x)


#Function that resets lists each time campaign starts
def reset():
    global prepared
    global initial
    prepared[:]=[]
    initial[:]=[0]



@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    channel=bot.get_channel(566459563319099403)
    #await channel.send('Tao has returned from training.')


#when someone types it checks the message
@bot.command(name='start', help='Takes a roll call')
async def start_campaign(ctx):
    global initial
    await ctx.send('Please type anything to indicate your presence')
    initial.insert(0,1)


@bot.command(name='complete', help='Used after start, ends roll call. Ex. (complete campaign)')
async def end_campaign(ctx):
    con = str(ctx.message.content)

    if 'unhinged' in con:
        await ctx.send('Roll call has ended for unhinged')
        for x in unhinged:
            if x not in prepared:
                ids = '<@{}>'.format(x)
                await ctx.send('The following player is not prepared: {} laugh at them.'.format(ids))

    if 'hunt' in con:
        await ctx.send('Roll call has ended for hunt')
        for x in hunt:
            if x not in prepared:
                ids = '<@{}>'.format(x)
                await ctx.send('The following player is not prepared: {} laugh at them.'.format(ids))

    if 'control' in con:
        await ctx.send('Roll call has ended for control')
        for x in control:
            if x not in prepared:
                ids = '<@{}>'.format(x)
                await ctx.send('The following player is not prepared: {} laugh at them.'.format(ids))

    reset()


@bot.command(name='join', help='To join a campaign. Ex. (join campaign)')
async def join(ctx):
    auth=str(ctx.message.author.id)
    con=str(ctx.message.content)

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


@bot.command(name='leave', help='To leave a campaign. Ex.(leave campaign)')
async def leave(ctx):
    auth=str(ctx.message.author.id)
    con=str(ctx.message.content)

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


@bot.command(name='save', help='Saves player data and shuts down')
async def save(ctx):
    unfilew = open('unhinged', 'w')
    huntfilew = open('hunt', 'w')
    controlfilew = open('control', 'w')
    for x in unhinged:
        unfilew.write(x+'\n')
    for x in hunt:
        huntfilew.write(x+'\n')
    for x in control:
        controlfilew.write(x+'\n')
    await ctx.send('Player data has been saved')
    await ctx.send('Tao is leaving to train.')
    await bot.logout()


@bot.command(name='players', help='Check the players in a campaign. Ex.(players campaign)')
async def players(ctx):
    con=str(ctx.message.content)
    await ctx.send('These players are in the campaign: ')

    if 'unhinged' in con:
        for x in unhinged:
            player=int(x)
            print(bot.get_user(int(x)))
            await ctx.send(str(bot.get_user(int(x))))

    if 'hunt' in con:
        for x in hunt:
            player=int(x)
            print(bot.get_user(int(x)))
            await ctx.send(str(bot.get_user(int(x))))

    if 'control' in con:
        for x in control:
            player=int(x)
            print(bot.get_user(int(x)))
            await ctx.send(str(bot.get_user(int(x))))


@bot.command(name='popular', help='Gives the most and least popular person')
async def bestperson(ctx):
    people=bot.users
    await ctx.send('The most popular person is: '+str(random.choice(people)))
    await ctx.send('The least popular person is: ' + str(random.choice(people)))


@bot.event
async def on_message(message):
    global prepared
    auth=str(message.author.id)
    con=message.content

    if (auth in unhinged) and initial[0]==1:
        prepared.append(auth)

    if con.lower()=='thanks tao' or con=='thank you tao' or con=='ty tao' or con=='thanks so much tao':
        await message.channel.send("You are welcome, it's my duty")

    if con=='wisdom':
        ninja = ['No one saves us but ourselves. No one can and no one may. We ourselves must walk the path.',
                 'Three things cannot be long hidden: the sun, the moon, and the truth.',
                 'The mind is everything. What you think you become.']
        response=random.choice(ninja)
        await message.channel.send(response)

    await bot.process_commands(message)



#temporarily disabled, says something everytime someone talks
#@client.event
#async def on_message(message):
#    guild = discord.utils.get(client.guilds, name=GUILD)
#    if message.author == client.user:
#        return
    #if str(message.author) == 'Turaku#5395':
     #   await message.channel.send('You are the chosen one!')

bot.run(TOKEN)
