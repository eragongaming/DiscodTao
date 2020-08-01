import os
import discord
import random
from discord.ext import commands
TOKEN=os.environ['TOKEN']
GUILD=os.environ['GUILD']
bot=commands.Bot(command_prefix='tao ')

#Preparing lists to determine who is present
unfilew=open('unhinged','w')
huntfilew=open('hunt','w')
controlfilew=open('control','w')
unfiler=open('unhinged','r')
huntfiler=open('hunt','r')
controlfiler=open('control','r')
unhinged=unfiler.readlines()
hunt=huntfiler.readlines()
control=controlfiler.readlines()
initial=[0]
prepared=[]
campaigns=['unhinged','hunt','control']

#Function that resets lists each time campaign starts
def reset():
    global prepared
    global initial
    prepared[:]=[]
    preparedid[:]=[]
    initial[:]=[0]



@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


#when someone types it checks the message
@bot.command(name='start_unhinged', help='Begins determining who is present')
async def s_unhinged_campaign(ctx):
    global initial
    await ctx.send('Please type anything to indicate your presence')
    initial.insert(0,1)


@bot.command(name='unhinged_complete', help='Stops accepting new people')
async def e_unhinged_campaign(ctx):
    await ctx.send('Roll call has ended for Unhinged')
    for x in unhinged:
        if x not in prepared:
            id='<@{}>'.format(x)
            await ctx.send('The following player is not prepared: {} laugh at them.'.format(id))
    reset()


@bot.command(name='join', help='Allows a user to join a campaign, put the name of the campaign after')
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

@bot.command(name='leave', help='Allows a user to leave a campaign, put the name of the campaign after')
async def leave(ctx):
    auth=str(ctx.message.author.id)
    con=str(ctx.message.content)

    if 'unhinged' in con and auth in unhinged:
        unhinged.remove(auth)
    elif 'unhinged' in con:
        await ctx.send('You are not in the campaign.')
    if 'hunt' in con and auth in hunt:
        hunt.remove(auth)
    elif 'hunt' in con:
        await ctx.send('You are not in the campaign.')
    if 'control' in con and auth in control:
        control.remove(auth)
    elif 'control' in con:
        await ctx.send('You are not in the campaign.')


@bot.command(name='save', help='Saves an updated list of players before closing tao')
async def save(ctx):
    unfilew.writelines(unhinged)
    huntfilew.writelines(hunt)
    controlfilew.writelines(control)
    ctx.send('Player data has been saved')


@bot.event
async def on_message(message):
    global preparedu
    auth=str(message.author.id)
    con=message.content
    print(unhinged)

    if (auth in unhinged) and initial[0]==1:
        prepared.append(auth)


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
