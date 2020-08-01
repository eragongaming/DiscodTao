import os
import discord
import random
TOKEN='NzM4OTAwMjc1MTU4NTgxMzA5.XySogQ.BxMjvjk-Hdtux5iuTCos8fsq_lk'
GUILD="Feeder's Den"
client=discord.Client()

unhinged=('Little Haowie#3217','suCCC#1194','Baecon#6277','Kayo Hinazuki#2531','boo radley#2121')
initial=[]
prepared=[]


def reset():
    global prepared
    global initial
    prepared[:]=[]
    initial[:]=[]


@client.event
async def on_ready():
    guild=discord.utils.get(client.guilds, name=GUILD)
    print(f'{client.user} is connected to the following guild: {guild.name}')


#client.event
#async def on_member_join(member):
#    await message.channel.send(
#        f"It's time to begin your training {member.name}, welcome to the den!"
#    )


@client.event
async def on_message(message):
    if message.author==client.user:
        return
    ninja=['No one saves us but ourselves. No one can and no one may. We ourselves must walk the path.','Three things cannot be long hidden: the sun, the moon, and the truth.','The mind is everything. What you think you become.']
    if message.content=='wisdom':
        response=random.choice(ninja)
        await message.channel.send(response)


@client.event
async def on_message(message):
    guild = discord.utils.get(client.guilds, name=GUILD)
    if message.author == client.user:
        return
    #if str(message.author) == 'Turaku#5395':
     #   await message.channel.send('You are the chosen one!')


@client.event
async def on_message(message):
    if message.author==client.user:
        return
    global initial
    if str(message.content)=='unhinged starting':
        await message.channel.send('Please type anything to indicate your presence')
        initial.append(1)

@client.event
async def on_message(message):
    if message.author==client.user:
        return
    global prepared
    for x in unhinged:
        if str(message.author)==x and initial[0]==1:
            prepared.append(x)


@client.event
async def on_message(message):
    if message.author==client.user:
        return
    if str(message.content)=='unhinged complete':
        await message.channel.send('Roll call has ended for Unhinged')
        for x in unhinged:
            if x not in prepared:
                await message.channel.send('The following player is not prepared: '+str(x))

        reset()
client.run(TOKEN)
