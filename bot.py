#Define import statements
import discord, os, os.path, requests, json, subprocess, praw, sys
from discord.ext import commands
from discord.ext.commands import Bot
from discord import message
from os import path
from sys import platform
from dotenv import load_dotenv

if(platform == 'linux' or platform == 'linux2' or platform == 'darwin'):
    #check if GNU/Mac environmemt
    load_dotenv()
    print(platform)
    #Grabbing the environment variable value which is the token
    TOKEN = os.getenv('DISCORD')
else:
    #Windows platform
    print(platform)
    #Grabbing the environment variable value which is the token
    TOKEN = os.getenv('DISCORD')


#the Bot class inherits from the discord.Client class and as such you can perform the same actions as before
client = commands.Bot(command_prefix='+')

#Display a message upon successful login
@client.event
async def on_ready():
    #Change the activity of the bot
    await client.change_presence(activity=discord.Game('...with your emotions'))
    print(f'Logged in as {client.user}')

#It kind of works but I wnat to be able to
@client.event
async def on_member_join(member):
    #Grab the guild the member joined
    guild = member.guild
    #Grab a collection of text channels in the guild the user joined
    ch = guild.text_channels
    #Declare an empty variable
    welcome = ''
    #loop through the text channels and find the welcome channel
    for txt_channel in ch:
        #If welcome channel is found assign the text channel obj to the welcome variable
        if txt_channel.name == 'welcome' or txt_channel.name == 'Welcome':
            welcome = guild.get_channel(txt_channel.id)        
            #Send the greeting
            await welcome.send(f'''>>> Welcome and well met, {member.mention}. While you're here we ask you observe a few basic rules. No racism, sexism, homophobia, transphobia, etc. of any kind will be tolerated.Please keep the chat free of overly lewd or obscene images or statements. Please be respectful to all members of the Discord. Finally, please listen to mods.\nMake sure to head over to the #role-assign channel next to ensure you're receiving the correct notifications while you're here.\nYou can also head to our #General-ffxiv channel to register your character and make use of Ser Aymeric's FFXIV features. Just type "?iam [World] [Character name]" and remove the brackets. From there, you can check your gear, stats, fflogs, market board pricing/history, gathering node information, and more.\nThanks for joining us and we hope you enjoy your stay!''')


    # # rules = guild.rules_channel

    # print(rules)
    # print(member)
    # print(member.mention)
    # print(guild)
    
    # await ctx.send(f'Welcome {member.mention}')

#Ping a domain/ip address
@client.command(aliases=['p'])
async def ping(ctx,*,ip):
    async with ctx.typing():
        output = subprocess.run(f'ping {ip}',capture_output=True)
        await ctx.send(output.stdout.decode('utf-8'))

#Move the specified user to jail(currently only works on Dress Up Party)
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

#Return information about the specified anime
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

#Give a scenario of would you rather?
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

    guild = ctx.message.author.guild
    # ch = guild.text_channels
    rules = guild.rules_channel

    print(rules)
    # print(member)
    # print(member.mention)
    print(guild)
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

#werewolf - assign a role (werewolf, human)  | Pretty Big Project
#So I was able to add a reaction to the message that the bot sends
#now I need to figure out how to sleep the program for a set amount of time
#Then once time has passed collect the list of users who reacted and assign the role of either human or wolf
@client.command(aliases=['werewolf','werewoof','wwoof','woof'])
async def wwolf(ctx):
    #Send the initial message declaring a game of Werewolf
    await ctx.send('Let\'s play Werewolf/Werewoof!\U0001F43A')
    
    # #message channel
    ch = ctx.message.channel
    #Declare an empty variable
    message = ''
    #loop through the list of messages and grab the most recent one
    async for msg in ch.history(limit=1):
        message = msg
    #Add reaction to the last message that was sent(should be the one that the bot sent earlier in this function)
    await message.add_reaction(':Panic:527715541654306816')
    await message.add_reaction(':monkaS:537560867063988225')

#Reddit Search
@client.command(aliases=['reddit','r'])
async def reddit_lookup(ctx, *, subreddit):
    
    r = praw.Reddit(user_agent='Deebot-Sama by /u/0xD3adB33f_',client_id = 'VlrewRi3vJa_-Q',client_secret = '5goc9tnVl5hzyx3f7jDWl09Knls')
    
    for submission in r.subreddit(subreddit).hot(limit=5):
        await ctx.send(f'Title: {submission.title}\nText: {submission.selftext}\nURL: {submission.url}\n***************************************************\n')


#add subreddit to storage
@client.command(aliases=['ar']) #addreddit
async def reddit_save(ctx, *, subreddit):

    guild = client.get_guild(ctx.message.guild.id)
    guild_str = str(guild)
    file = (guild_str + '.fuk')

    if path.exists(guild_str + '.fuk') and os.stat(file).st_size >= 0:
        with open(file) as f:
            if subreddit in f.read():
                await ctx.send('Already in file!')
                f.close()
            else:
                f.close()
                f = open(file, 'a')
                f.write('\n' + subreddit)
                f.close()
                await ctx.send('Stored subreddit!')
    else:
        guild = client.get_guild(ctx.message.guild.id)
        guild_str = str(guild)
        file = (guild_str + '.fuk')
        f = open(file, 'x')
        f.close()
        f = open(file, 'a')
        f.write(subreddit + '\n')
        f.close()
        await ctx.send('Stored subreddit!')
        

#list subreddits
@client.command(aliases=['lr'])
async def reddit_list(ctx):
    guild = client.get_guild(ctx.message.guild.id)
    guild_str = str(guild)
    file = (guild_str + '.fuk')

    if path.exists(guild_str + '.fuk') and os.stat(file).st_size > 0:
        async with ctx.typing():
            with open(file) as f:
                lines = (line.rstrip() for line in f) #all lines including the blank ones
                lines = list(line for line in lines if line) #nonblank lines
                await ctx.send(f'subreddits stored: `{lines}`')
                f.close()

    else:
        await ctx.send('No subreddits stored')

#delete subreddit from storage #TODO - add a check if subreddit is stored
@client.command(aliases=['delr'])
async def reddit_del(ctx, *, subreddit):

    guild = client.get_guild(ctx.message.guild.id)
    guild_str = str(guild)
    file = (guild_str + '.fuk')

    if path.exists(guild_str + '.fuk') and os.stat(file).st_size > 0:
        f = open(file, 'r')
        if subreddit not in f.read():
            f.close()
            await ctx.send('Subreddit has to be stored before deleting :b:')
        else:
            new_file_content = ''
            for line in f:
                stripped_line = line.strip()
                new_line = stripped_line.replace(subreddit, '')
                new_file_content += new_line
            f.close()
            writing_file = open(file, 'w')
            writing_file.write(new_file_content)
            writing_file.close()
            await ctx.send("Removed subreddit!")

    elif (os.path.isfile(file) == False or os.stat(file).st_size == 0):
        await ctx.send('You need to add a subreddit before attempting to delete')

#Psuedo-Reddit homepage
@client.command(aliases=['rh']) #Reddit Here (rh)
async def reddit_here(ctx):
    guild = client.get_guild(ctx.message.guild.id)
    guild_str = str(guild)

    r = praw.Reddit(user_agent='Deebot-Sama by /u/0xD3adB33f_',client_id = 'VlrewRi3vJa_-Q',client_secret = '5goc9tnVl5hzyx3f7jDWl09Knls') 
    if path.exists(guild_str + '.fuk'):
        file = (guild_str + '.fuk')
        with open(file) as f:
            lines = (line.rstrip() for line in f) #all lines including the blank ones
            lines = list(line for line in lines if line) #nonblank lines
            for line in lines:
                for submission in r.subreddit(line).hot(limit=5):
                    if submission.stickied: #skip pinned posts
                        continue
                    else:
                        await ctx.send(f'Title: {submission.title}\nText: {submission.selftext}\nURL: {submission.url}\n***************************************************\n')
        f.close()

    else:
        await ctx.send('Add subreddit via add_reddit command first')


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
