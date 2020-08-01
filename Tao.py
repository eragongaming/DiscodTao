import os
import discord
import random
from discord.ext import commands
TOKEN=os.environ['TOKEN']
GUILD=os.environ['GUILD']
bot=commands.Bot(command_prefix='TAO!')

#Preparing lists to determine who is present
unhinged=('Little Haowie#3217','suCCC#1194','Baecon#6277','Kayo Hinazuki#2531','boo radley#2121')
initial=[0]
prepared=[]
preparedid=[]

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
            await ctx.send('The following player is not prepared: '+str(x)+' laugh at them.')
    reset()


@bot.command(name='join', help='Allows a user to join a campaign, put the name of the campaign after')
async def join(ctx):
    print(ctx.message.content)
    if ctx.message.content=='TAO! join unhinged' and ctx.message.author not in unhinged:
        unhinged.append(str(ctx.message.author))
        print(unhinged)
    elif ctx.message.content=='TAO! join unhinged':
        await ctx.send('You are already in the campaign.')


@bot.command(name='leave', help='Allows a user to leave a campaign, put the name of the campaign after')
async def leave(ctx):
    if ctx.message.content=='unhinged' and ctx.message.author in unhinged:
        unhinged.append(str(ctx.message.author))


@bot.event
async def on_message(message):
    global preparedu
    auth=str(message.author)
    con=message.content

    if (auth in unhinged) and initial[0]==1:
        prepared.append(auth)
        preparedid.append(message.author.id)


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
