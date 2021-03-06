import discord
import random
import time
from datetime import datetime
print('Program Start')

print('Discord.py version ' + discord.__version__)

print('Opening token file')
try:
    token = open("token.txt", "r").read()
except:
    print('Error: Token File Not Found!')
    raise SystemExit(0)

print('Waiting for Ready Event')


class MyClient(discord.Client):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))
        print('------------------------------------------------------')

    async def on_member_join(self, member):
        await member.guild.system_channel.send(member.name + " has wandered into town!")

    async def on_message_delete(self, message):
        print('Message Deleted!')

        # ignore if it is the bots message, most likely the admin cleaning up
        if message.author == client.user:
            return

            # ree on delete
        if message.author.permissions_in(message.channel).administrator != True:
            if message.channel.name == 'town-square' or message.channel.name == 'dead-chat':  # only on these two chats
                try:
                    await message.channel.send(
                        message.author.mention + ' deleted a message! It was \n"' + message.content + '"')
                except:
                    print('Error Sending Deleted Message in ' + message.channel.name + '!')

    async def on_message_edit(self, before, after):
        print('Message Edited!')
        if before.author.permissions_in(before.channel).administrator != True:
            if before.content != after.content:
                if before.channel.name == 'town-square' or before.channel.name == 'dead-chat':  # only on these two chats
                    try:
                        await before.channel.send(
                            before.author.mention + ' Edited a message! It was \n"' + before.content + '"')
                    except:
                        print('Error Sending Edit Message!')

    async def on_message(self, message):
        # if message was sent by bot ignore
        if message.author == client.user:
            return

        gmc = discord.utils.get(message.guild.text_channels, name='gm-commands')

        # if message was sent in GM channel by GM
        if message.author.permissions_in(message.channel).administrator == True:
            if message.channel.name == 'gm-commands':

                # Register a list of players to playerlist
                if message.content == '/registerplayers':
                    global playerlist
                    global printplayerlist
                    playerrole = discord.utils.get(message.guild.roles, name='Player')
                    playerlist = playerrole.members
                    printplayerlist = [m.name for m in playerlist]
                    await gmc.send(printplayerlist)
                    return

                # Delete and Create new Houses from playerlist
                if message.content == '/createhouses':
                    housecategory = discord.utils.get(message.guild.categories, name='Houses')
                    housechannels = housecategory.channels
                    for x in housechannels:
                        print('Deleting Channel: ' + x.name)
                        await x.delete()
                    # time.sleep(3)
                    for x in printplayerlist:
                        newchannel = await housecategory.create_text_channel(x + 's-house')
                        await newchannel.set_permissions(discord.utils.get(message.guild.members, name=x), read_messages=True)
                        print('created channel' + newchannel.name)
                        # await newchannel.send('Welcome! This is your house which provides you with a private channel with the Game Masters. This is where you can perform night actions, write wills, ask questions about the game, and receive results and notifications.')
                    return

                # Check the current time from the bot's perspective.
                if message.content == '/checktime':
                    await gmc.send('the current time is' + str(datetime.now()))
                    return

        # if message was sent in pre-post-game-discussion
        if message.channel.name == 'pre-post-game-discussion':
            # message not sent by a gamemaster
            if message.author not in discord.utils.get(message.guild.roles, name='GameMaster').members:
                playerrole = discord.utils.get(message.guild.roles, name='Player')
                spectatorrole = discord.utils.get(message.guild.roles, name='Spectator')
                if message.content == '/join':
                    if message.author in playerrole.members:
                        await message.channel.send(message.author.mention + ' is already a player.')
                        return
                    await message.author.add_roles(playerrole)
                    await message.author.remove_roles(spectatorrole)
                    await message.channel.send(message.author.mention + ' has decided to play!')
                    return
                if message.content == '/leave':
                    if message.author in spectatorrole.members:
                        await message.channel.send(message.author.mention + ' is already a spectator.')
                        return
                    await message.author.add_roles(spectatorrole)
                    await message.author.remove_roles(playerrole)
                    await message.channel.send(message.author.mention + ' has decided to sit out.')
                    return


            # fun little easter egg
        if message.content.find("<@" + str(self.user.id) + ">") != -1:
            if message.content.lower().find("accuse") != -1:
                responses = ["no u",
                             "This is all part of my 'Potato Play' I swear.",
                             "After all I've done for you this is the thanks I get?!",
                             "Where's you will, huh? Wheres your PrOoF?",
                             "do it you wont",
                             "*Actually,* I'm Seer, and you're evil! ",
                             "I claim Wisp",
                             "Noted",
                             "Someone in dead chat is reeing so hard right now",
                             "Oh OK, well I accuse " + message.author.name,
                             "I have not been paying attention at all this game...",
                             "Wait I already made a deal with town!",
                             "**REEEEEEEEEEEEEEEEEEEEEEEE**",
                             "can someone give me a small rundown on what the fuck just happened?",
                             "Hold on, I need to write my will first.",
                             "Wait! I have notes!",
                             "I have a will.. but it doesn't fit in one message, so give me a second..",
                             "Sooner or later we all knew this day was coming",
                             "Hold my beer",
                             "I've been role blocked literally every single night, what do you want from me?",
                             "*muffled screaming*",
                             "*notices ur accusation* uwu what's this?"
                             "oops"
                             ]
                await message.channel.send(responses[random.randint(0, len(responses) - 1)])
                return

        # Help command
        if message.content == '!help':
            await message.channel.send(
                '''!help: Opens Help text           
                
                !purge: Deletes the most recent messages in a channel
                    -Requires User to have Administrator Privileges 
                    -Bot Needs to have manage message privileges
                
                Notes about channels. The bot will only activate on channels named "town-square" or "dead-chat"
                Make sure the names are exactly that or it will not work.
                            ''')
            return

        # Purge command. Has to be exactly that phrase to reduce the change of accidentally activating
        if message.content == ('!purge'):
            print("Purge command sent!")
            # Check if command is sent in town square
            if message.channel.name == 'town-square':
                # checks if user who sent the command is an administrator
                if message.author.permissions_in(message.channel).administrator == True:
                    # grab history of channel and turn it into a list using .flatten()
                    try:
                        # await message.channel.delete_messages(history[0: 99])
                        print("Cloning Town Square")
                        await message.channel.clone()
                        print("Deleting Town Square")
                        await message.channel.delete()
                        print(message.channel.position)
                    except Exception as ex:
                        # bot does not have permissions to execute this command, informs the server it has an issue
                        print(ex)
                        await message.channel.send(
                            'Error: Could not delete messages. Could be a permissions issue or messages are over 14 days old.')
                        return
                    # turns re-enables delete messages when purge is done
                else:
                    # yell at whoever tried to run it without permissions
                    await message.channel.send('Error: You do not have permissions to use this command!')
                return

        if message.channel.name == 'town-square':
            embed = embed = discord.Embed(color=0x000000)
            embed.add_field(name=message.author.display_name, value=message.content, inline=False)
            authorAvitarUrl = message.author.avatar_url
            embed.set_thumbnail(url=authorAvitarUrl)
            spectatorChannel = None
            for x in message.guild.text_channels:
                if x.name == 'spectator-square':
                    spectatorChannel = x
                    break

            await spectatorChannel.send(embed=embed)


client = MyClient(intents = discord.Intents.all())
client.run(token)
client.max_messages = 10000