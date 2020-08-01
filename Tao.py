import os
import discord
import random
from discord.ext import commands
TOKEN=os.environ['TOKEN']
GUILD=os.environ['GUILD']
client=discord.Client()
bot=commands.Bot(command_prefix='**')

#Preparing lists to determine who is present
unhinged=('Little Haowie#3217','suCCC#1194','Baecon#6277','Kayo Hinazuki#2531','boo radley#2121')
initial=[0]
prepared=[]

#Function that resets lists each time campaign starts
def reset():
    global prepared
    global initial
    prepared[:]=[]
    initial[:]=[0]


#makes a console message about when bot is ready
@client.event
async def on_ready():
    guild=discord.utils.get(client.guilds, name=GUILD)
    print(f'{client.user} is connected to the following guild: {guild.name}')


@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')


# #sends a message in the channel when a user joins
# bot.event
# async def on_member_join(member):
#     await message.channel.send(
#         f"It's time to begin your training {member.name}, welcome to the den!"
#     )
#

#when someone types it checks the message
@bot.command(name='start unhinged', help='Begins determining who is present')
async def s_unhinged_campaign(ctx):
    global initial

    await ctx.send('Please type anything to indicate your presence')
    initial.insert(0,1)


@bot.command(name='unhinged complete', help='Stops accepting new people')
async def e_unhinged_campaign(ctx):
    await ctx.send('Roll call has ended for Unhinged')
    for x in unhinged:
        if x not in prepared:
            await ctx.send('The following player is not prepared: '+str(x))
    reset()

@bot.event
async def on_message(message):
    auth=str(message.author)
    con=message.content

    if (auth in unhinged) and initial[0]==1:
        prepared.append(auth)

    if con=='wisdom':
        ninja = ['No one saves us but ourselves. No one can and no one may. We ourselves must walk the path.',
                 'Three things cannot be long hidden: the sun, the moon, and the truth.',
                 'The mind is everything. What you think you become.']
        response=random.choice(ninja)
        await message.channel.send(response)



#temporarily disabled, says something everytime someone talks
#@client.event
#async def on_message(message):
#    guild = discord.utils.get(client.guilds, name=GUILD)
#    if message.author == client.user:
#        return
    #if str(message.author) == 'Turaku#5395':
     #   await message.channel.send('You are the chosen one!')

bot.run(TOKEN)
#client.run(TOKEN)
