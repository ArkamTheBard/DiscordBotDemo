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
    #Don't ask how this works haha
    headers = {"Accept":"application/vnd.api+json","Content-Type":"text/html"}
    anime_original = anime
    #change the spaces to %20 which is how the api denotes spaces in text
    anime = anime.replace(' ', '%20')
    #Send get request and return a Response object
    response = requests.get(f'https://kitsu.io/api/edge/anime?filter[text]={anime}', headers=headers)

    final_string = ''
    final_string = final_string + 'Titles\n'
    for line in response.json()['data'][0]['attributes']['titles'].items():
        final_string = final_string + f'\t{line[0]} : {line[1]}\n'
    
    final_string = final_string + '\nSynopsis : '+ response.json()['data'][0]['attributes']['synopsis']
    
    final_string = final_string + '\nAverage Rating : ' + response.json()['data'][0]['attributes']['averageRating']
    
    final_string = final_string + '\nStart Date : '+ response.json()['data'][0]['attributes']['startDate']
    if response.json()['data'][0]['attributes']['endDate'] == None:
        final_string = final_string + '\nEnd Date : ' + 'Ongoing'
    else:
        final_string = final_string + '\nEnd Date : ' + response.json()['data'][0]['attributes']['endDate']
    
    final_string = final_string + '\nStatus : ' + response.json()['data'][0]['attributes']['status']
    
    final_string = final_string + '\nEpisode Count : ' + str(response.json()['data'][0]['attributes']['episodeCount'])

    await ctx.send(f'Anime : {anime_original}\n{final_string}')
#Run the bot
client.run(TOKEN)