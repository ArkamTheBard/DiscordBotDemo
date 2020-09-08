#Define import statements
import discord, os, requests, json, subprocess, praw
from discord.ext import commands
from discord.ext.commands import Bot
from discord import message

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
async def ping(ctx,*,ip):
    async with ctx.typing():
        output = subprocess.run(f'ping {ip}',capture_output=True)
        await ctx.send(output.stdout.decode('utf-8'))
@client.command(aliases=['j'])
async def jail(ctx, *, membername):
    for role in ctx.message.author.roles:
        if role.name in ('Mods','Mr Bot Maker Man'):#'Mr Bot Maker Man',
            #Grab the guild that we are trying to work with
            guild = client.get_guild(ctx.message.guild.id)

            # voice_channels = guild.voice_channels

            # for ch in voice_channels:
            #     print(f'{ch.name} | {ch.id}')
            #grab a list of all the users in the guild
            member_list = guild.members

            #This will display all of the emem
            #for member in member_list:
               # print(f'{member.nick} : {member.display_name}')

            #voice channel object that we are moving the user to
            other_voice_channel = guild.get_channel(651994332848717824)#DressUpParty-651994332848717824#Discree-397552560019341329

            #Grab the member we are moving
            member_obj = ''
            roleslist = []
            #obj_list = []

            #Search the list of users and assign user to var if found else 
            for member in member_list:
                if member.nick == membername or member.display_name == membername:
                    member_obj = guild.get_member(member.id)
                    rolelist = member_obj.roles

                    #for role in rolelist:
                    #   obj_list.append(discord.Object(role.id))
                    break
                else:
                    member_obj = None

            if member_obj != None:
                #voice channel to move user to
                await member_obj.move_to(other_voice_channel)
                #await member_obj.remove_roles(guild, member_obj, member_obj.roles[1],reason='Eat my ass')
                # for role in rolelist:
                #     await member_obj.remove_roles(role)
            else:
                await ctx.send('Failed to find member')


    await ctx.send('Finished')
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
# @client.command(aliases=['wyr'])
# async def would_you_rather(ctx):
    return None
#Dice roll simply pass the type of dice (d6, d12)
@client.command(aliases=['dr'])
async def dice_roll(ctx,*,dice):
    # House Fortemps RoombaToday at 12:45 AM
    # !roll 3d6
    # A Dice Bot
    # BOT
    # Today at 12:45 AM
    # @House Fortemps Roomba rolled 9. (5 + 1 + 3 = 9)
    # House Fortemps RoombaToday at 12:46 AM
    # !roll 3d6+5d10
    # A Dice Bot
    # BOT
    # Today at 12:46 AM
    # @House Fortemps Roomba rolled 26. (5 + 1 + 3 = 9,   2 + 8 + 1 + 1 + 5 = 17)
    #url to grab the request from
    url = f'http://roll.diceapi.com/json/{dice.strip()}'
    #Store the response in a variable
    response = requests.get(url)
   
    #Store the dice value in a var for use later
    value = response.json()['dice'][0]['value']

    #Send the data to the chat server
    await ctx.send(f'{ctx.message.author.mention} rolled **{value}**.')
#Coin flip
@client.command(aliases=['cf'])
async def heads_or_tails(ctx):
   #url to grab the request from
    url = f'http://flipacoinapi.com/json'
    #Store the response in a variable
    response = requests.get(url)

    value = response.text.replace('\"','')
    
    await ctx.send(f'{ctx.message.author.mention} flipped **{value}**!')
#Reddit Search
@client.command(aliases=['reddit','r'])
async def reddit_lookup(ctx, *, subreddit):
    
    r = praw.Reddit(user_agent='Deebot-Sama by /u/0xD3adB33f_',client_id = 'VlrewRi3vJa_-Q',client_secret = '5goc9tnVl5hzyx3f7jDWl09Knls')
    
    for submission in r.subreddit(subreddit).hot(limit=1):
        await ctx.send(f'Title: {submission.title}\nText: {submission.selftext}\nURL: {submission.url}\n***************************************************\n')

# @client.command(aliases=['ascii'])
# async def ascii_art(ctx,*,text):
#     text = text.replace(' ','+')
#     url = 'http://artii.herokuapp.com/make?text={text}'

#     response = requests.get(url)

#     string = ''
#     for line in response.text.split('\n'):
#         string = string + line + '\n'
#Doesn't work currently for some reason the text is displayed all messed up but learned that using three ``` before and after the text puts it into some sort of text box

#Run the bot
client.run(TOKEN)

#topic changing - 
#would you rather 
#music //Pretty big project

#roast - @ someone and then create a roast with them
#alert - when someone is going live on twitch [provide the url of the twitch streamer] //Kind of hard
#patch notes 
#werewolf - assign a role (werewolf, human)  | Pretty Big Project