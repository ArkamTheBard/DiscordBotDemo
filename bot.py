#Define import statements
import discord, os, os.path, requests, json, subprocess, praw, sys, discord.utils, asyncio, random, youtube_dl, shutil
from discord.ext import commands
from discord.ext.commands import Bot
from discord import message
from os import path
from sys import platform
from dotenv import load_dotenv
from discord.utils import get


#Test to determine the OS the code is working with.
if(platform == 'linux' or platform == 'linux2' or platform == 'darwin'):
    #check if GNU/Mac environment
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

# @client.command(aliases=['help','h'])
# async def help_command(ctx):
#     with ctx.typing():
#         await ctx.send('something temporary')

#Join the voice channel that the user who ran the command is currently in
@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()

#Leave the voice channel that the user who ran the command is currently in
@client.command()
async def leave(ctx):
    server = ctx.message.guild
    voice_client = client.voice_clients[0]
    await voice_client.disconnect()

#Play a song in the voice channel the user is currently in
@client.command(aliases=['pp','pplay'])
async def play(ctx,*,url):

    def check_queue():
        queue_infile = os.path.isdir('./Queue')
        if queue_infile is True:
            DIR = os.path.abspath(os.path.realpath('Queue'))
            length = len(os.listdir(DIR))

            still_q = length - 1
            try:
                first_file = os.listdir(DIR)[0]
            except:
                queues.clear()
                return
            
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath('Queue') + '\\' + first_file)
            if length != 0:
                song_there = os.path.isfile(main_location+ '\\' + 'song.mp3')
                if song_there:
                    os.remove(main_location+ '\\' + 'song.mp3')
                    queues.clear()
                
                shutil.move(song_path,main_location)

                for file in os.listdir(main_location):
                    if file.endswith('.mp3'):
                        os.rename(main_location+ '\\' + file, main_location+ '\\' + 'song.mp3')

                voice.play(discord.FFmpegPCMAudio(main_location+ '\\' + 'song.mp3'), after=lambda e: check_queue())#, after=lambda e: print(f'{name} has finished playing'))
                voice.source = discord.PCMVolumeTransformer(voice.source)
                #Set the volume of the bot
                voice.source.volume = 0.02
            else:
                queues.clear()
                return
            
        else:
            queues.clear()

    async with ctx.typing():
        #Need to add a test to see if the bot is already in channel. If so then skip this step and instead just play the song
        # await join(ctx)
        main_location = os.path.dirname(os.path.realpath(__file__))
        #Boolean test to see if song file already exists
        song_there = os.path.isfile(main_location+ '\\' + 'song.mp3')
        try:        
            #if song is there delete it
            if song_there:
                os.remove(main_location+ '\\' + 'song.mp3')
                queues.clear()
                # print('Removed old song file')
        except PermissionError:
            #If user tries to play another song before one is done playing throw an error
            print('Cannot delete song due to song being played')
            await ctx.send('Error... Music is currently playing')

        queue_infile = os.path.isdir('./Queue')
        try:
            queue_folder = './Queue'
            if queue_infile is True:
                shutil.rmtree(queue_folder)
        except:
            print('No old queue folder')

        voice = client.voice_clients[0]

        ydl_opts = {
            'format':'bestaudio/best',
            'quiet':True,
            'postprocessors':[{
                'key': 'FFmpegExtractAudio',
                'preferredcodec':'mp3',
                'preferredquality':'192',
            }]
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            # print('Downloading audio now\n')
            #download the file
            ydl.download([url])


        for file in os.listdir('./'):
            if file.endswith('.mp3'):
                name = file
                # print(f'Renamed File: {file}\n')
                os.rename(file,main_location + '\\' +'song.mp3')


        voice.play(discord.FFmpegPCMAudio(main_location+ '\\' +'song.mp3'), after=lambda e: check_queue())#, after=lambda e: print(f'{name} has finished playing'))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        #Set the volume of the bot
        voice.source.volume = 0.02
        

    # server = ctx.message.guild
    # voice_client = client.voice_clients[0]
    # player = await.voice_client.create()

#Pause a song that is currently playing in a voice channel
@client.command(aliases=['pa','pau'])
async def pause(ctx):
    voice_client = client.voice_clients[0]

    voice_client.pause()

    await ctx.send('Music Paused')

#Resume a song that is paused
@client.command(aliases=['re','res'])
async def resume(ctx):
    voice_client = client.voice_clients[0]

    voice_client.resume()

    await ctx.send('Music resumed!')

#Stop a song that is currently playing on a server
@client.command(aliases=['st','sto'])
async def stop(ctx):

    voice_client = client.voice_clients[0]

    queues.clear()

    queue_infile= os.path.isdir('./Queue')
    if queue_infile is True:
        shutil.rmtree('./Queue')

    voice_client.stop()

    await ctx.send('Music stopped!')

@client.command(aliases=['skip','next'])
async def next_song(ctx):

    voice_client = client.voice_clients[0]

    voice_client.stop()

    await ctx.send('Skipped song!')
queues = {}

@client.command(aliases=['qu','q'])
async def queue(ctx,*, url):
    queue_infile = os.path.isdir('./Queue')
    if queue_infile is False:
        os.mkdir('Queue')
    DIR = os.path.abspath(os.path.realpath('Queue'))
    q_num  = len(os.listdir(DIR))
    q_num += 1

    add_queue = True

    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath('Queue') + f'\song{q_num}.%(ext)s')



    ydl_opts = {
            'format':'bestaudio/best',
            'quiet':True,
            'outtmpl':queue_path,
            'postprocessors':[{
                'key': 'FFmpegExtractAudio',
                'preferredcodec':'mp3',
                'preferredquality':'192',
            }]
        }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #download the file
        ydl.download([url])


#Ping a domain/ip address
@client.command(aliases=['p'])
async def ping(ctx,*,ip):
    async with ctx.typing():
        output = subprocess.run(f'ping {ip}',capture_output=True)
        await ctx.send(output.stdout.decode('utf-8'))

#Move the specified user to jail(currently only works on Dress Up Party)
@client.command(aliases=['j'])
async def jail(ctx, *, membername):
    with ctx.typing():
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
    with ctx.typing():
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
    # return None

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
    with ctx.typing():
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
    with ctx.typing():
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
@client.command(aliases=['wwhelp','whelp','wh'])
async def werewolf_help(ctx):
    rulebook = 'https://pegasusshop.de/media/pdf/d8/9a/93/4250231704208_gb.pdf'
    rulebook2 = 'https://www.playwerewolf.co/rules'
    youtube = 'https://www.youtube.com/watch?v=GaBZgOuuH5o&ab_channel=CleverMove'
    await ctx.send(f'Alright so here are the rules for Werewolf \U0001F913\U0001F913\U0001F913:\nRulebook \U0001F4DA: {rulebook}\nEasy Explanation \U0001F3EB: {rulebook2}\nYoutube Video Explanation\U0001F4FA: {youtube}')
@client.command(aliases=['werewolf','werewoof','wwoof','woof'])
async def wwolf(ctx,*,wait_time=1):
    #Setup : 1 Seer, 1 Doctor, and 2 werewolves and the rest of the players should be villagers. If you have 16 or more players you can replace a villager for 1 additional werewolf
   
    roles = {
        'Apprentice Seer' : 'Become the Seer if the Seer is killed.',
        'Aura Seer' : 'At night, find the team of one player. (variation: At night, find out if someone has a no-ordinary role and what it is)',
        'Beholder' : 'Opens his eyes the first night to see who the seer is',
        'Big Bad Wolf' : 'If the werewolves target is beside you, you can kill any combination of your adjacent players. However, if the leprechaun redirects the initial attack, none of your adjacent players die. (variation: you can attack one person beside the intial werewolf target.',
        'Bogeyman' : 'If the wolves can\'t decide who to kil, you\'ll do it for them. You win if all the night-active players are dead.',
        'Body Guard' : 'Choose a different player each night to protet. That player cannot be killed that night.',
        'Cupid' : 'Choose two players to be lovers. If one of those players dies, the other dies from a broken heart.',
        'The Count' : 'The first night, you are told how many werewolves there are in each half of the village.',
        'Diseased' : 'If you are attacked by werewolves, the werewolves do not get fed the following night.',
        'Fruit Brute': 'If you are the last wolf left alive, you lose your appetite and cannot feed, but you are trying to root out all the villagers',
        'Ghost': 'Die the first night, then each day, write one letter clues as a message from the beyond (no names or initials).',
        'Hunter':'If you are killed, take someone down with you.',
        'Village Idiot':'Always vote for players to die',
        'Insomniac':'Each knight, learn at least one of your neightbors has woken up during the night.',
        'Lycan':'You are a villager, but you appear falsely to be a werewolf to the Seers and PI.',
        'Wolf man' : 'The exact opposite of a lycan.'
    }
    async with ctx.typing():
    #Send the initial message declaring a game of Werewolf
        await ctx.send('Let\'s play Werewolf/Werewoof! \U0001F43A')
    
    # #message channel
    ch = ctx.message.channel    
    #Declare an empty variable
    message = ''
    #loop through the list of messages and grab the most recent one
    async for msg in ch.history(limit=1):
        message = msg
    #store the message id in a var for usage later
    message_id = message.id

    await message.add_reaction(':Panic:527715541654306816')
    # await message.add_reaction(':monkaS:537560867063988225')

    #sleep the program for 1 minute to allow ppl to make a decision if they will participate in werewolf or not
    await asyncio.sleep(int(wait_time) * 60)
    #should remove the bot's reaction
    await message.remove_reaction(':Panic:527715541654306816',client.user)
    #refresh and grab the updated message
    message = await ch.fetch_message(message_id)

    roles = ['Werewolf','Werewolf','Seer','Doctor','Villager']
    #Loop through the collection object and get the count of a type of reaction
    for reaction in message.reactions:
        #If there are at least 6 reactions we can begin the game of werewolf, else the user needs to run the command again
        if reaction.count >= 1:
            await ctx.send(f'Starting soon...')
            #flatten the async iterator into a list of users
            users = await reaction.users().flatten()
            
            #1 werewolf if ppl 6 - 8, 2 werewolf if ppl 9 - 11, 3 for 12 - 15
            #loop through the user list and print out who reacted
            for user in users:
                print(f'{user.name} reacted!')
                role = random.choice(roles)
                roles.remove(role)
                await user.send(f'{user.mention} you are a {role}!')
                
                

        else:
            await ctx.send('Sorry there weren\'t enough players to start.\U0001F631\U0001F631\U0001F631\n You need at least 5 players to play! \U0001F64C\U0001F64C\U0001F64C')


#Reddit Search
@client.command(aliases=['reddit','r'])
async def reddit_lookup(ctx, *, subreddit):
    with ctx.typing():
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


@client.command(aliases=['ascii'])
async def ascii_art(ctx,*,text):
    # text = text.replace(' ','%20')
    text = text.replace(' ','+')
    url = 'http://artii.herokuapp.com/make?text='+text

    response = requests.get(url)

    string = ''
    for line in response.text.split('\n'):
        string = string + line + '\n'
    await ctx.send(f'```\n{string}\n```')
    
#Run the bot
client.run(TOKEN)

#topic changing - 
#would you rather 
#roast - @ someone and then create a roast with them
#alert - when someone is going live on twitch [provide the url of the twitch streamer] //Kind of hard
#patch notes