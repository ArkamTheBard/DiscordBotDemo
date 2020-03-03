import discord,os,requests,youtube_dl,random
from discord.utils import get
from discord.ext import commands

TOKEN = os.getenv('DISCORD')
COMMANDS = '\n+c - Prints a list of currently available commands\n' + '+g - Greeting\n' + '+k - Kick the specified user from chat\n' + '+sauce - Checks reddit for some sauce and links it in chat\n'

#url for ip information: https://www.ipify.org/
#https://www.youtube.com/watch?v=GgnClrx8N2k
class MyClient(discord.Client):
    #When the program is executed, the bot will sign in and this method will execute
    
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    #Tells bot to join channel where the command originated from
    async def join(ctx):
        channel = ctx.message.author.voice.voice_channel
        await client.join_voice_channel(channel)
    #Tells the bot to leave channel
    async def leave(ctx):
        server = ctx.message.server
        voice_client = client.voice_client_in(server)
        await voice_client.disconnect()        
    #As messages are received in chat, print the author and message contents, Additionally if message begins with $hello bot will respond with Hello!
    async def on_message(self,message):
        #Prints chat messages 
        authorM = message.author.mention
        perm = ''
        print(f'Message from {message.author.name} : {message.content}')
        #This if statement makes sure that the bot doesn't accidentaly enter an endless loop
        if authorM == client.user:
            return
        else:
            if message.content.startswith('+c'):
                await message.channel.send(COMMANDS)
            elif message.content.startswith('+g'):
                GREETINGS = [f'DEE-BOT GREETING RAY ACTIVATE!!! HELLO {authorM}-SAMA!!!!', f'Hello {authorM}, Allonsy!',f'Ey yo what up with it {authorM}',f'Ascend through violence {authorM}! You can do it!',f'Ohaiyo good day to you, {authorM}!',f'Konichi wa madda fakker!', f'You come here often?',f'I sincerely hope you don\'t come into any bodily harm {authorM}!','*ignores you*',f'Your name must be Bepis, cause you looking So-Da-licious:eyes:',f'Are you a keyboard {authorM}? Cause you\'re my type',f'Hey {authorM}! Did you know that blood can be a substitute for eggs! Just letting you know!']
                await message.channel.send(random.choice(GREETINGS))
                # await message.channel.send(f'Hello {authorM}, Welcome to the Rice Fields MF!')
            elif message.content.startswith('+k'):
                for role in message.author.roles:
                    if role.name == 'Mr Bot Maker Man':
                        perm = role.name
                        #await message.channel.send(f'Hold on {authorM}, the feature is almost ready!')
                        break
                if perm == 'Mr Bot Maker Man':
                    await message.channel.send(f'GOT HERE {authorM} :eyes:')
                    perm = ''
                    #do the ting
                else:
                    await message.channel.send(f'Sorry {authorM}, you don\'t have permission to do that!\nTry asking the server admin for permission!')
            elif message.content.startswith('+sauce'):
                await message.channel.send('Nothing yet. Check back soon...')
            else:
                await message.channel.send(f'Invalid command {authorM}! Try using "+c" for a list of commands')
                
client = MyClient()
client.run(TOKEN)
