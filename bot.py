#Define import statements
import discord, os, requests, json
from discord.ext import commands

#Grabbing the environment variable value which is the token
TOKEN = os.getenv('DISCORD')
#the Bot class inherits from the discord.Client class and as such you can perform the same actions as before
client = commands.Bot(command_prefix='+')

#Display a message upon successful login
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

#Defining bot commands and the aliases used for them
@client.command(aliases=['g'])
async def greet(ctx):
    await ctx.send('Wait you cheeky bastard!')
@client.command(aliases=['p'])
async def ping(ctx):
    await ctx.send('Pong!')
@client.command(aliases=['a'])
async def anime(ctx,*,anime):
    await ctx.send(f'Anime : {anime}\n')


#Run the bot
client.run(TOKEN)