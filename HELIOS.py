#Helper for teachers In Online Sessions (HELIOS) Discord Bot
#The HELIOS Discord Bot functions as a classroom facilitator and assistant to the professor/teacher

import discord # imports discord module
import random # imports the random function
import json # imports json module
from discord.ext import commands # imports the commands module from the discord extension
from discord.utils import get # imports get function from the discord.utils module

def get_prefix(client, message):
    guildID = str(message.guild.id)
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)
        
    return prefixes[guildID]


TOKEN =  # Unique token for HELIOS bot, functions like an email and password for a Bot
intents = discord.Intents(messages = True, guilds = True, members = True, reactions = True) # Stores additional perms in intents variable
client = commands.Bot(command_prefix = get_prefix, intents = intents) # sets the command prefix and intents perms for the bot 
greetings = ['Hello', 'hello', 'Hi'] # list for the words that HELIOS will respond to.
activity = ['Activity', 'activity']

# variable that stores student permissions 
student_perms = discord.Permissions(change_nickname = True, 
                                    create_instant_invite = True,
                                    add_reactions = True,
                                    read_messages = True,
                                    view_channel = True,
                                    send_messages = True,
                                    read_message_history = True,
                                    external_emojis = True,
                                    connect = True,
                                    speak = True)

################################################################## Start of Events section ###########################################################################




# Start of on_ready event ###########################################################################
@client.event 
async def on_ready(): # Signifies that the bot is ready
    channel = get(client.get_all_channels(), name = 'general') # gets the channel name 'general' of a server where HELIOS will send the message
    print(f"{client.user} is online.")

    # sets the status of the bot as online, and displays how many servers the bot is in
    if len(client.guilds) == 1:
        await client.change_presence(status = discord.Status.online, activity = discord.Activity(name = f"{len(client.guilds)} server", type = discord.ActivityType.watching)) 
    if len(client.guilds) > 1:
        await client.change_presence(status = discord.Status.online, activity = discord.Activity(name = f"{len(client.guilds)} servers", type = discord.ActivityType.watching))
    
# End of on_ready event #############################################################################

# Start of on_guild_join event ######################################################################
@client.event # An event that is triggered when a discord user joins a server managed by HELIOS
async def on_guild_join(guild):
    guildID = str(guild.id)
    
    # creates a role named student with unique permissions
    await guild.create_role(name = "Student",
                            permissions = student_perms,
                            color = discord.Color(0xFFFF00),
                            hoist = True,
                            mentionable = True
                            )
                            
    # creates a role named professor with administrator permissions
    await guild.create_role(name = "Professor/Teacher",
                            permissions = discord.Permissions(administrator = True),
                            color = discord.Color.blue(),
                            hoist = True,
                            mentionable = True
                            )
                            
    with open('prefixes.json', 'r') as file:
        serverPDict = json.load(file)
        
    serverPDict[guildID] = '.'

    with open('prefixes.json', 'w') as file:
        json.dump(serverPDict, file, indent = 4)
    
    with open('raisehand.json', 'r') as rh:
        serverRHDict = json.load(rh)
    
    serverRHDict[guildID] = list()

    with open('raisehand.json', 'w') as rh:
       json.dump(serverRHDict, rh, indent = 4)
    
    with open('questions.json', 'r') as q:
        serverQDict = json.load(q)
    
    serverQDict[guildID] = list()

    with open('questions.json', 'w') as q:
        json.dump(serverQDict, q, indent = 4)
    
    
# End of on_guild_join event #######################################################################################

# Start of on_guild_remove event ###################################################################################
@client.event
async def on_guild_remove(guild):
    guildID = guild.id

    with open('prefixes.json', 'r') as file: # reads the file 'prefixes.json'
        prefixDict = json.load(file)
    
    prefixDict.pop(str(guildID)) # removes the guild ID or server ID associated with the command prefix
    
    with open('prefixes.json', 'w') as file:
        json.dump(prefixDict, file, indent = 4)

    with open('raisehand.json', 'r') as rh:
        rhDict = json.load(rh)
    
    rhDict.pop(str(guildID))

    with open('raisehand.json', 'w') as rh:
        json.dump(rhDict, rh, indent = 4)
    
    with open('questions.json', 'r') as q:
        qDict = json.load(q)
    
    qDict.pop(str(guildID))
    
    with open('questions.json', 'w') as q:
        json.dump(qDict, q, indent = 4)

# End of on_guild_remove event #####################################################################################

# Start of on_message event ########################################################################################
@client.listen("on_message") # An event that is triggered when a discord user enters a word that is in the lists above, replies back with the responses below.
async def msg(message):
    prof = get(message.author.guild.roles, name = "Professor/Teacher")
    student = get(message.author.guild.roles, name = "Student")
    for hello in greetings:
        if hello in message.content: 
            responses = ['Hi!', 'Hello!']
            if message.author == client.user:
                return
            await message.channel.send(f"{message.author.mention} {random.choice(responses)}")
            break
    
    for act in activity:
        if act in message.content:
            if message.author == client.user:
                return
            if message.author in prof.members:
                await message.channel.send(f"{student.mention}, your Professor/Teacher has announced a new activity/seatwork!")
                await message.pin()
            break
# End of on_message event ###########################################################################################

# Start of on_member_join event #####################################################################################
@client.event # An event that prints the following text when a member joins a server
async def on_member_join(member):
    print(f"{member} has joined the server {member.guild}.")

    rolestudent = get(member.guild.roles, name = "Student")
    await member.add_roles(rolestudent)
        
    #await get(client.get_all_channels(), name = 'general').send(f"Welcome, {member.mention}! \nRole is set to {rolestudent.mention}.")
# End of on_member_join event ########################################################################################

# Start of on_member_leave event #####################################################################################
@client.event # An event that prints the following text when a member leaves a server
async def on_member_leave(member):
    print(f"{member} has left {member.guild}")
    await discord.utils.get(client.get_all_channels(), name = 'general').send(f"Goodbye, {member.mention}.")
# End of on_member_leave event #######################################################################################


########################################################## Start of Error events ##############################################################################################
@client.event
async def on_command_error(ctx, error):
    guildID = str(ctx.guild.id)
    with open('prefixes.json', 'r') as file:
        pDict = json.load(file)
    
    value = str(pDict[guildID])
    
    if isinstance(error, commands.CommandNotFound):
        embed = discord.Embed(title = "Error",
                          description = f"The command entered was not found. Type {value}help for more information.",
                          color = discord.Color.red()                 
                         )
        await ctx.send(embed = embed)
    
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(title = "Error",
                          description = f"A required argument was missing. Type {value}help for more information.",
                          color = discord.Color.red()                 
                         )
        await ctx.send(embed = embed) 
    
    elif isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(title = "Error",
                          description = f"You do not have permission to use this command. Only administrators can use this command. Type {value}help for more information.",
                          color = discord.Color.red()                 
                         )
        await ctx.send(embed = embed) 
    
    elif isinstance(error, commands.UserInputError):
        embed = discord.Embed(title = "Error",
                          description = f"Input invalid. Type {value}help for more information.",
                          color = discord.Color.red()                 
                         )
        await ctx.send(embed = embed) 
    
    elif isinstance(error, commands.CommandError):
        embed = discord.Embed(title = "Error",
                          description = f"Command failed. Type {value}help for more information.",
                          color = discord.Color.red()                 
                         )
        await ctx.send(embed = embed) 
    
# End of Error events ################################################################################################    


################################################### Start of Commands section ##########################################################################################


# Start of >speak command ############################################################################################
@client.command(aliases = ["speak", "repeat", 'say']) # repeats the message author's original message, then deletes the original message. 
@commands.has_permissions(administrator = True) 
async def announce(ctx, *, message = None): # usage: >say <string, such as announcements, messages, etc.>
    await ctx.send(message)
    await ctx.message.delete()
# End of >speak command ##############################################################################################

# Start of >ban command ##############################################################################################
@client.command(aliases = ['Ban', 'b']) # bans the user mentioned by the administrator role
@commands.has_permissions(administrator = True) 
async def ban(ctx, member: discord.Member, *, reason = None): # usage: >ban @user, >Ban @user, or >b @user

    embed = discord.Embed(title = "Ban",
                          description = f"{member.mention} has been banned.",
                          color = discord.Color.blue()
                         )
    await member.ban(reason = reason)
    await ctx.send(embed = embed)
# End of >ban command #################################################################################################

# Start of >unban command #############################################################################################
@client.command(aliases = ["Unban", 'ub']) # unbans previously banned users (administrator must mention the user with their discord discriminator code e.g. Clint#0764)
@commands.has_permissions(administrator = True) 
async def unban(ctx, *, member): # usage: >unban @user#1234, >Unban @user#1234, or >ub @user#1234 
    

    
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(embed = discord.Embed(title = "Unban",
                          description = f"Unbanned user {user.name}#{user.discriminator}",
                          color = discord.Color.blue()                 
                         ))
    return
# End of >unban command ##################################################################################################

# Start of >kick command #################################################################################################
@client.command(aliases = ["Kick", "k"]) # kicks/removes a user from the server that is mentioned by the administrator role
@commands.has_permissions(administrator = True)
async def kick(ctx, member: discord.Member, *, reason = None): # usage: >kick @user, >Kick @user, or >k @user
    
    embed = discord.Embed(title = "Kick",
                          description = f"Kicked user {member.mention}",
                          color = discord.Color.blue()                 
                         )
                         
    await member.kick(reason = reason)
    await ctx.send(embed = embed)
# End of >kick command ###################################################################################################

# Start of >clear command ################################################################################################
@client.command(aliases = ["Clear", "cl"]) # clears/removes messages in the text channel where you are in, default amount of messages removed is 5
@commands.has_permissions(administrator = True)
async def clear(ctx, amount = 5): # usage: >clear, >Clear, or >cl <amount>
    
    await ctx.channel.purge(limit = amount)
    
    embed = discord.Embed(title = "Clear",
                          description = f"Removed {amount} messages.",
                          color = discord.Color.blue()                 
                         )

    await ctx.send(embed = embed)
# End of >clear command ##################################################################################################

# Start of >professor command ############################################################################################
@client.command(aliases = ["Professor"]) # Sets own role to professor
@commands.has_permissions(administrator = True) # Only admin command
async def professor(ctx): # usage: >professor *no arguments*
    user = ctx.author # gets the user which is the author of the command
    roleprof = get(ctx.guild.roles, name = "Professor/Teacher") # gets the professor role from the list of roles of the server
    rolestudent = get(ctx.guild.roles, name = "Student") # gets the student role from the list of roles of the server
    
    if (roleprof not in user.roles) and (rolestudent not in user.roles): # if user is not in both prof and student role
        await user.add_roles(roleprof) # sets the user's role to prof only
        embed = discord.Embed(title = "Role",
                          description = f"Role of user, {user.mention}, is set to {roleprof.mention}",
                          color = discord.Color.blue()                 
                         )
        await ctx.send(embed = embed)
        
    elif (roleprof in user.roles) and (rolestudent in user.roles): # if user is in both prof and student role
        await user.remove_roles(rolestudent) # removes the student role and prof role remains
        embed = discord.Embed(title = "Role",
                          description = f"Role of user, {user.mention}, is set to {roleprof.mention} only",
                          color = discord.Color.blue()                 
                         )
        await ctx.send(embed = embed)  

    elif (roleprof not in user.roles) and (rolestudent in user.roles): # if user is in student role and not in prof role
        await user.remove_roles(rolestudent) # remove the student role of the user
        await user.add_roles(roleprof) # and sets the user's role to professor
        embed = discord.Embed(title = "Role",
                          description = f"Role of user, {user.mention}, is set to {roleprof.mention}",
                          color = discord.Color.blue()                 
                         )
        await ctx.send(embed = embed) 

    elif (roleprof in user.roles) and (rolestudent not in user.roles): # if user is already in prof role and not in student role
        embed = discord.Embed(title = "Role",
                          description = f"Role of user, {user.mention}, is already set to {roleprof.mention}",
                          color = discord.Color.blue()                 
                         )
        await ctx.send(embed = embed) 
# End of >professor command ##############################################################################################

# Start of >student command ##############################################################################################
@client.command(aliases = ["Student"]) # Sets own role to professor
async def student(ctx): # usage: >student *no arguments*
    user = ctx.author
    roleprof = get(ctx.guild.roles, name = "Professor/Teacher")
    rolestudent = get(ctx.guild.roles, name = "Student")
    
    if (roleprof not in user.roles) and (rolestudent not in user.roles): # if user is not in bot prof and student role
        await user.add_roles(rolestudent) # sets the role of the user to student only
        embed = discord.Embed(title = "Role",
                          description = f"Role of user, {user.mention}, is set to {rolestudent.mention}",
                          color = discord.Color.blue()                 
                         )
        await ctx.send(embed = embed)    
        
    elif (roleprof in user.roles) and (rolestudent in user.roles): # if user is in both student and prof role
        await user.remove_roles(roleprof) # removes prof role and student role remains
        embed = discord.Embed(title = "Role",
                          description = f"Role of user, {user.mention}, is set to {rolestudent.mention} only",
                          color = discord.Color.blue()                 
                         )
        await ctx.send(embed = embed)  

    elif (roleprof in user.roles) and (rolestudent not in user.roles): # if user is in prof role and not in student role
        await user.remove_roles(roleprof) # removes the prof role of the user
        await user.add_roles(rolestudent) # sets the user's role to student
        embed = discord.Embed(title = "Role",
                          description = f"Role of user, {user.mention}, is set to {rolestudent.mention}",
                          color = discord.Color.blue()                 
                         )
        await ctx.send(embed = embed) 

    elif (roleprof not in user.roles) and (rolestudent in user.roles): # if user is in student role already and not in prof role
        embed = discord.Embed(title = "Role",
                          description = f"Role of user, {user.mention}, is already set to {rolestudent.mention}",
                          color = discord.Color.blue()                 
                         )
        await ctx.send(embed = embed) 
# End of >student command ##############################################################################################

# Start of >setrole command ############################################################################################
@client.command(aliases = ["Setrole"]) # sets role of other people
@commands.has_permissions(administrator = True) # Only admin command
async def setrole(ctx, member:discord.Member, role:discord.Role): # usage: >setrole <@name> <@role>
    roleprof = get(ctx.guild.roles, name = "Professor/Teacher")
    rolestudent = get(ctx.guild.roles, name = "Student")
    
    if role == roleprof: # If the role of the mentioned member is needed to be set to professor (similar to the >professor command block of code)
        if (roleprof not in member.roles) and (rolestudent not in member.roles): 
            await member.add_roles(roleprof) 
            embed = discord.Embed(title = "Role",
                          description = f"Role of user, {member.mention}, is set to {roleprof.mention}",
                          color = discord.Color.blue()                 
                         )
            await ctx.send(embed = embed)    
        
        elif (roleprof in member.roles) and (rolestudent in member.roles): 
            await member.remove_roles(rolestudent)
            embed = discord.Embed(title = "Role",
                          description = f"Role of user, {member.mention}, is set to {roleprof.mention} only",
                          color = discord.Color.blue()                 
                         )
            await ctx.send(embed = embed)  

        elif (roleprof not in member.roles) and (rolestudent in member.roles): 
            await member.remove_roles(rolestudent)
            await member.add_roles(roleprof)
            embed = discord.Embed(title = "Role",
                          description = f"Role of user, {member.mention}, is set to {roleprof.mention}",
                          color = discord.Color.blue()                 
                         )
            await ctx.send(embed = embed) 

        elif (roleprof in member.roles) and (rolestudent not in member.roles): 
            embed = discord.Embed(title = "Role",
                          description = f"Role of user, {member.mention}, is already set to {roleprof.mention}",
                          color = discord.Color.blue()                 
                         )
            await ctx.send(embed = embed) 
    
    elif role == rolestudent: # If the role of the mentioned member is needed to be set to student (similar to the >student command block of code)
        if (roleprof not in member.roles) and (rolestudent not in member.roles):
            await member.add_roles(rolestudent)
            embed = discord.Embed(title = "Role",
                          description = f"Role of user, {member.mention}, is set to {rolestudent.mention}",
                          color = discord.Color.blue()                 
                         )
            await ctx.send(embed = embed)    
        
        elif (roleprof in member.roles) and (rolestudent in member.roles):
            await member.remove_roles(roleprof)
            embed = discord.Embed(title = "Role",
                          description = f"Role of user, {member.mention}, is set to {rolestudent.mention} only",
                          color = discord.Color.blue()                 
                         )
            await ctx.send(embed = embed)  

        elif (roleprof in member.roles) and (rolestudent not in member.roles): 
            await member.remove_roles(roleprof)
            await member.add_roles(rolestudent)
            embed = discord.Embed(title = "Role",
                          description = f"Role of user, {member.mention}, is set to {rolestudent.mention}",
                          color = discord.Color.blue()                 
                         )
            await ctx.send(embed = embed) 

        elif (roleprof not in member.roles) and (rolestudent in member.roles): 
            embed = discord.Embed(title = "Role",
                          description = f"Role of user, {member.mention}, is already set to {rolestudent.mention}",
                          color = discord.Color.blue()                 
                         )
            await ctx.send(embed = embed) 

    else: # Sets the role of the mentioned member to roles other than student and professor
        await member.add_roles(role)
        embed = discord.Embed(title = "Role",
                          description = f"Role of user, {member.mention}, is set to {role.mention}",
                          color = discord.Color.blue()                 
                         )
        await ctx.send(embed = embed)
# End of >setrole command ##############################################################################################

# Start of >mute command ###############################################################################################
@client.command(aliases = ["Mute"])
@commands.has_permissions(administrator = True)
async def mute(ctx, member:str): 
    user = ctx.author
    try:
        if member == "all": # if professor wants to mute all except himself/herself
            embed = discord.Embed(title = "Mute",
                          description = f"All users are muted in channel {user.voice.channel.mention}",
                          color = discord.Color.blue()                 
                         )
            for mem in user.voice.channel.members: # mutes members in the voice channel of the professor
                if mem == user:
                    pass
                else:
                    await mem.edit(mute = True)
            
            await ctx.send(embed = embed)
            
        else:
            member = member.replace("@","") 
            member = member.replace("!","")
            member = member.replace("<","")
            member = member.replace(">","")
            member = ctx.guild.get_member(int(member))
            await member.edit(mute = True)

            embed = discord.Embed(title = "Mute",
                                description = f"Muted user {member.mention}",
                                color = discord.Color.blue()                 
                                )
            await ctx.send(embed = embed)
    
    except:
        embed = discord.Embed(title = "Mute",
                              description = f"User {member.mention} is not in a voice channel",
                              color = discord.Color.red()                 
                             )
        await ctx.send(embed = embed)
# End of >mute command ###################################################################################################

# Start of >unmute command ###############################################################################################
@client.command(aliases = ["Unmute"])
@commands.has_permissions(administrator = True)
async def unmute(ctx, member:str): 
    user = ctx.author
    try:
        if member == "all": # if professor wants to unmute all except himself/herself
            embed = discord.Embed(title = "Unmute",
                          description = f"All users are unmuted in channel {user.voice.channel.mention}",
                          color = discord.Color.blue()                 
                         )
            for mem in user.voice.channel.members: # unmutes members in the voice channel of the professor
                if mem == user:
                    pass
                else:
                    await mem.edit(mute = False)
            
            await ctx.send(embed = embed)
            
        else:
            member = member.replace("@","")
            member = member.replace("!","")
            member = member.replace("<","")
            member = member.replace(">","")
            member = ctx.guild.get_member(int(member))
            await member.edit(mute = False)

            embed = discord.Embed(title = "Unmute",
                                description = f"Unmuted user {member.mention}",
                                color = discord.Color.blue()                 
                                )
            await ctx.send(embed = embed)
    
    except:
        embed = discord.Embed(title = "Mute",
                          description = f"User {member.mention} is not in a voice channel",
                          color = discord.Color.red()                 
                         )
        await ctx.send(embed = embed)
# End of >unmute command #################################################################################################

# Start of >move command ###############################################################################################
@client.command(aliases = ["Move"])
@commands.has_permissions(administrator = True)
async def move(ctx, member: str, *, channel: discord.VoiceChannel):
    user = ctx.author
    try:
        if member == "all":
            embed = discord.Embed(title = "Move",
                                  description = f"All users in {user.voice.channel.mention} was moved to {channel.mention}",
                                  color = discord.Color.blue()                 
                                 )
            for mem in user.voice.channel.members:
                await mem.move_to(channel)

            await ctx.send(embed = embed)
        
        else:
            member = member.replace("@","")
            member = member.replace("!","")
            member = member.replace("<","")
            member = member.replace(">","")
            member = ctx.guild.get_member(int(member))
            await member.move_to(channel)

            embed = discord.Embed(title = "Move",
                                  description = f"Moved user {member.mention} to {channel.mention}",
                                  color = discord.Color.blue()                 
                                 )
            await ctx.send(embed = embed)

    except:
        embed = discord.Embed(title = "Move",
                              description = f"User {member.mention} is not in a voice channel",
                              color = discord.Color.red()                 
                             )
        await ctx.send(embed = embed)
# End of >move command ########################################################################################################

# Start of >raisehand command #################################################################################################
@client.command(aliases = ["Raisehand", "rh", "Rh", "RH"])
async def raisehand(ctx, *, arg = None):
    user = str(ctx.message.author.mention)
    roleprof = get(ctx.guild.roles, name = "Professor/Teacher")
    with open("raisehand.json", "r") as f:
        filerh = json.load(f)
        
    values = filerh[str(ctx.guild.id)]
    
    if arg == None:
        if user in values:
            values.remove(user)
            with open("raisehand.json", "w") as f:
                json.dump(filerh, f, indent = 4)
            await ctx.send(f"{user} hand removed.") 
            
        else:
            values.append(str(user))

            with open("raisehand.json", "w") as f:
                json.dump(filerh, f, indent = 4)
        
        if not values:
            embed = discord.Embed(title = "Raisehand",
                            description = "None",
                            color = discord.Color.blue()
                            )
        else:                 
            values = str(filerh[str(ctx.guild.id)])[1:-1]
            values = values.replace("'", "")
            values = values.replace(",", "")
            values = values.replace(" ", "\n")
           
            await ctx.send(f"Hand/s raised {roleprof.mention}") 
        
            embed = discord.Embed(title = "Raisehand",
                                description = values,
                                color = discord.Color.blue()
                                )
                                
        await ctx.send(embed = embed)

    elif arg == "list":
        if not values:
            embed = discord.Embed(title = "Raisehand",
                            description = "None",
                            color = discord.Color.blue()
                            )
        else:
            values = str(filerh[str(ctx.guild.id)])[1:-1]
            values = values.replace("'", "")
            values = values.replace(",", "")
            values = values.replace(" ", "\n")
           
            await ctx.send(f"Hand/s raised {roleprof.mention}") 
        
            embed = discord.Embed(title = "Raisehand",
                                    description = values,
                                    color = discord.Color.blue()
                                    )
                                
        await ctx.send(embed = embed)
    
    elif arg == "remove":
        values.remove(str(user))
        
        with open("raisehand.json", "w") as f:
            json.dump(filerh, f, indent = 4)
            
        if not values:
            embed = discord.Embed(title = "Raisehand",
                            description = "None",
                            color = discord.Color.blue()
                            )
        else:
            values = str(filerh[str(ctx.guild.id)])[1:-1]
            values = values.replace("'", "")
            values = values.replace(",", "")
            values = values.replace(" ", "\n")
           
            await ctx.send(f"{user} hand removed. Hand/s raised {roleprof.mention}") 
        
            embed = discord.Embed(title = "Raisehand",
                                    description = values,
                                    color = discord.Color.blue()
                                    )
                                
        await ctx.send(embed = embed)

    elif arg == "remove all":
        if ctx.message.author.guild_permissions.administrator:
            
            if not values:
                embed = discord.Embed(title = "Raisehand",
                                description = "None",
                                color = discord.Color.blue()
                                )
                embed.set_footer(text = "Raised hand list was already empty.")
            else:
                values.clear()
                with open("raisehand.json", "w") as f:
                    json.dump(filerh, f, indent = 4)

                embed = discord.Embed(title = "Raisehand",
                                description = "None",
                                color = discord.Color.blue()
                                )

            await ctx.send(embed = embed)
        
        else:
            raise commands.MissingPermissions
    else:
        raise commands.CommandError
# End of >raisehand command ###################################################################################################

# Start of >question command ##################################################################################################
@client.command(aliases = ["Question", "Q", "q"])
async def question(ctx, arg = None, *, arg2 = None):
    user = ctx.message.author
    roleprof = get(ctx.guild.roles, name = "Professor/Teacher")
    upresent = False
    with open("questions.json", "r") as f:
        fileq = json.load(f)

    values = fileq[str(ctx.guild.id)]
    if arg == "ask":
        for v in values:
            if v.startswith(f"{user.name}"):
                upresent = True
            break

        if upresent == True:
            await ctx.send('```Question/s```' + f'```{"".join(values)}```')
            await ctx.send(f"{user.name} already asked a question. Question/s raised {roleprof.mention}")
        else: 
            values.append(f"{user.name}: {arg2}\n")
            with open("questions.json", "w") as f:
                    json.dump(fileq, f, indent = 4)

            await ctx.send('```Question/s```' + f'```{"".join(values)}```')
            await ctx.send(f"Question/s raised {roleprof.mention}")
            
    elif arg == "list" and arg2 == None:
        if not values:
            await ctx.send("```Question/s```" + "```None```")
        else:
            await ctx.send('```Question/s```' + f'```{"".join(values)}```')
            await ctx.send(f"Question/s raised {roleprof.mention}")
    elif arg == "remove" and arg2 == None:
        for v in values:
            if v.startswith(str(user.name)):
                values.remove(v)
                break

        with open("questions.json", "w") as f:
            json.dump(fileq, f, indent = 4)
        
        if not values:
            await ctx.send("```Question/s```" + "```None```")
        else:
            await ctx.send('```Question/s```' + f'```{"".join(values)}```')
            await ctx.send(f"Question/s raised {roleprof.mention}")
    elif arg == "remove" and arg2 == "all":
        if ctx.message.author.guild_permissions.administrator:
            if not values:
                await ctx.send("```Question/s```" + "```None```" + "```The question list was already empty```")
            else:
                values.clear()

                with open("questions.json", "w") as f:
                    json.dump(fileq, f, indent = 4)

                await ctx.send("```Question/s```" + "```None```")
        else:
            raise commands.MissingPermissions
        
    else:
        raise commands.CommandError
# End of >question command ##############################################################################################################

# Start of >remove command ##############################################################################################################
@client.command(aliases = ["Remove"])
@commands.has_permissions(administrator = True)
async def remove(ctx, member:discord.Member, arg = None):
    roleprof = get(ctx.guild.roles, name = "Professor/Teacher")
    if arg == "raise":
        with open("raisehand.json", "r") as f:
            filerh = json.load(f)

        values = filerh[str(ctx.guild.id)]

        values.remove(str(member.mention))
        
        with open("raisehand.json", "w") as f:
            json.dump(filerh, f, indent = 4)
            
        if not values:
            embed = discord.Embed(title = "Raisehand",
                            description = "None",
                            color = discord.Color.blue()
                            )
        else:
            values = str(filerh[str(ctx.guild.id)])[1:-1]
            values = values.replace("'", "")
            values = values.replace(",", "")
            values = values.replace(" ", "\n")
           
            await ctx.send(f"{member.mention} hand removed. Hand/s raised {roleprof.mention}") 
        
            embed = discord.Embed(title = "Raisehand",
                                    description = values,
                                    color = discord.Color.blue()
                                    )
                                
        await ctx.send(embed = embed)
    
    elif arg == "question":
        with open("questions.json", "r") as f:
            fileq = json.load(f)

        values = fileq[str(ctx.guild.id)]
        for v in values:
            if v.startswith(str(member.name)):
                values.remove(v)
                break
        
        with open("questions.json", "w") as f:
                    json.dump(fileq, f, indent = 4)
        
        if not values:
            await ctx.send("```Question/s```" + "```None```")
        else:
            await ctx.send('```Question/s```' + f'```{"".join(values)}```')
            await ctx.send(f"Question/s raised {roleprof.mention}")
    else:
        raise commands.CommandError

# End of >remove command ##############################################################################################################


# Start of >changeprefix command ########################################################################################################
@client.command(aliases = ["cp", "Changeprefix", "Cp"])
async def changeprefix(ctx, *, newPrefix: str = None):
    key = str(ctx.guild.id)
    with open('prefixes.json', 'r') as file:
        prefixes = json.load(file)

    value = str(prefixes[key])

    if newPrefix == value:
        prefixes[key] = newPrefix
        embed = discord.Embed(title = "Change Prefix - Error",
                            description = f"The command prefix for this server is already set to {newPrefix}. Please enter another command prefix.",
                            color = discord.Color.red()
                            )
    elif newPrefix != value:
        prefixes[key] = newPrefix
        with open('prefixes.json', 'w') as file:
            json.dump(prefixes, file, indent = 4)
            
        embed = discord.Embed(title = "Change Prefix",
                            description = f'The command prefix for this server has been changed to "{newPrefix}".',
                            color = ctx.author.color
                            )
    
    await ctx.send(embed = embed)
# End of >changeprefix command ##########################################################################################################


# Start of >help command ######################################################################################################
@client.remove_command('help') # Removes built-in discord help command
@client.command()
async def help(ctx, *, arg = None):
    key = str(ctx.guild.id)
    with open ('prefixes.json', 'r') as file: 
        guildsDict = json.load(file)
        
    keyList = str(guildsDict.keys())
    value = str(guildsDict[key])

    if arg == None:

        embed = discord.Embed(title = 'HELIOS - Help', 
                              description = 'Here is what I can do.', 
                              color = ctx.author.color)
        embed.add_field(name = 'Help', value = f"Returns main help menu or menu of a specific command.\n\n{value}help, {value}help <command name>\n\ne.g. {value}help question", inline = False)  
        embed.add_field(name = 'Mute (Admin Only)', value = f"Mutes a member or multiple members.\n\nType {value}help mute for information on this command's usage.", inline = True) 
        embed.add_field(name = 'Unmute (Admin Only)', value = f"Unmutes a member or multiple members.\n\nType {value}help unmute for information on this command's usage.", inline = True)
        embed.add_field(name = 'Kick (Admin Only)', value = f"Kicks a member or multiple members from the server.\n\nType {value}help kick for information on this command's usage.", inline = True)
        embed.add_field(name = 'Ban (Admin Only)', value = f"Bans a member or multiple members from the server.\n\nType {value}help ban for information on this command's usage.", inline = True)
        embed.add_field(name = 'Unban (Admin Only)', value = f"Unbans a member or multiple members from the server.\n\nType {value}help unban for information on this command's usage.", inline = True)
        embed.add_field(name = 'Move (Admin Only)', value = f"Moves a member or multiple members to specified channels.\n\nType {value}help move for information on this command's usage.", inline = True)
        embed.add_field(name = 'Clear (Admin Only)', value = f"Clears messages in the voice channel where the command is called.\n\nType {value}help clear for information on this command's usage.", inline = True)
        embed.add_field(name = 'Raise Hand', value = f"Raises hand of a member or multiple members.\n\nNote: Only the Professor/Teacher role and an administrator can remove all the raised hands.\n\nType {value}help raisehand for information on this command's usage.", inline = True)
        embed.add_field(name = 'Announce', value = f"Repeats what the message author says.\n\nType {value}help announce for information on this command's usage.", inline = True)
        embed.add_field(name = 'Question', value = f"Stores the user's question, then displays it when {value}Question, {value}question list is called.\n\nNote: Only the Professor/Teacher and an administrator can remove all questions.\n\nType {value}help question for information on this command's usage.", inline = True)
        embed.add_field(name = 'Activity', value = f"Notifies students and pins activities from the professor.\n\n If <message> contains the word 'activity' or 'Activity', automatically pins the message as a task.", inline = True)
        
    if arg == 'mute':
        embed = discord.Embed(title = 'Help - Mute (Admin Only)',
                             description = f'usage: {value}Mute, {value}mute <@user> or {value}Mute, {value}mute <all>\n\n e.g. {value}mute @bot or {value}mute all',
                             color = ctx.author.color)
    
    if arg == 'unmute':
        embed = discord.Embed(title = 'Help - Unmute (Admin Only)',
                             description = f'usage: {value}Unmute, {value}unmute <@user> or {value}Unmute, {value}unmute <all>\n\n e.g. {value}unmute @bot, or {value}unmute all',
                             color = ctx.author.color)
    
    if arg == 'kick':
        embed = discord.Embed(title = 'Help - Kick (Admin Only)',
                             description = f'usage: {value}Kick, {value}kick <@user\n\n e.g. {value}kick @bot',
                             color = ctx.author.color)
    
    if arg == 'ban':
        embed = discord.Embed(title = 'Help - Ban (Admin Only)',
                              description = f'usage: {value}Ban, {value}ban <@user>\n\n e.g. {value}ban @bot',
                              color = ctx.author.color)
    
    if arg == 'unban':
        embed = discord.Embed(title = 'Help - Unban (Admin Only)',
                             description = f'usage: {value}Unban, {value}unban, {value}ub <user#1234>\n\n e.g. {value}unban bot#1234',
                             color = ctx.author.color)
    if arg == 'move':
        embed = discord.Embed(title = 'Help - Move (Admin Only)',
                             description = f'usage: {value}Move, {value}move <@user>, {value}move all\n\n e.g. {value}move @bot voice or {value}move all voice',
                             color = ctx.author.color)
    if arg == 'clear':
        embed = discord.Embed(title = 'Help - Clear (Admin Only)',
                             description = f'usage: {value}Clear, {value}cl <insert amount of messages>\n\n e.g. {value}clear 20',
                             color = ctx.author.color)

    if arg == 'raisehand':
        embed = discord.Embed(title = 'Help - Raise Hand',
                             description = f'usage: {value}Raisehand, {value}Rh, {value}rh, {value}RH (list/remove/remove all)\n\n e.g. {value}raisehand (to raise hand), {value}raisehand list, {value}raisehand remove or {value}raisehand remove all',
                             color = ctx.author.color)
        
    if arg == 'announce':
        embed = discord.Embed(title = 'Help - Announce',
                             description = f'usage: {value}announce, {value}say, {value}repeat <message>\n\n e.g. {value}announce Hello',
                             color = ctx.author.color)
    
    if arg == 'question':
        embed = discord.Embed(title = 'Help - Question',
                             description = f'usage: {value}Question, {value}question (ask/list/next/clear)\n\n e.g. {value}question ask hello?, {value}question list, {value}question next, {value}question clear',
                             color = ctx.author.color)
                             
    if arg == 'changeprefix':
        embed = discord.Embed(title = 'Help - Change Prefix',
                             description = f'usage: {value}Changeprefix, {value}Cp, {value}cp <new command prefix>\n\n e.g. {value}changeprefix >',
                             color = ctx.author.color)
 
                             
    await ctx.send(embed = embed)
# End of >help command ################################################################################################

################################################## End of Commands section #####################################################################


client.run(TOKEN) # Runs the bot 
