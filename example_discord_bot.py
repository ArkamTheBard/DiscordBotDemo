import discord,os,requests,youtube_dl

TOKEN = os.getenv('DISCORD')
COMMANDS = '\n+c - Prints a list of currently available commands\n' + '+g - Greeting\n' + '+k - Kick the specified user from chat\n' + '+sauce - Checks reddit for some sauce and links it in chat\n'

#url for ip information: https://www.ipify.org/
#https://www.youtube.com/watch?v=GgnClrx8N2k
class MyClient(discord.Client):
    #When the program is executed, the bot will sign in and this method will execute
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
    #As messages are received in chat, print the author and message contents, Additionally if message begins with $hello bot will respond with Hello!
    async def on_message(self,message):
        print(message.author.roles)
        #Prints chat messages 
        print(f'Message from {message.author} : {message.content}')
        #This if statement makes sure that the bot doesn't accidentaly enter an endless loop
        if message.author == client.user:
            return 
        else:
            if message.content.startswith('+c'):
                await message.channel.send(COMMANDS)
            elif message.content.startswith('+g'):
                await message.channel.send(f'Hello {message.author.name}, Welcome to the Rice Fields MF!')
            elif message.content.startswith('+k'):
                await message.channel.send('Nothing yet. Check back soon...')
                # message.channel.send('Kicking...')
                # message.channel.send('Done!')
                for role in message.author.roles:
                    if role.name == 'Mr Bot Maker Man':
                            #do something
                            await message.channel.send(f'Hold on {message.author.name}, the feature is almost ready!')
                else:
                    await message.channel.send(f'Sorry {message.author.name}, you don\'t have permission to do that!\nTry asking the server admin for permission!')
            elif message.content.startswith('+sauce'):
                await message.channel.send('Nothing yet. Check back soon...')
            else:
                await message.channel.send(f'Invalid command {message.author.name}! Try using "+c" for a list of commands')
                
client = MyClient()
client.run(TOKEN)
