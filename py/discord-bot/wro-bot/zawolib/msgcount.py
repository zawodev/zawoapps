"""  Liczenie wiadomosci poszczegolnych uzytkownikow serwera i sortowanie eleganckie tego rankingu  """
import os
import discord
from zawolib import progressbar
from datetime import datetime
clear = lambda: os.system('cls')

messagesCount = {}
avatars = {}
guild = None
async def downloadUserMessagesCount(bot, guildid, ctx = None, adminOutput = False, adminLimit = None, adminBeforeTime = ""): #on a whole server | 11/02/22 16:06:35 = 11 luty 2022 16:06:35
    global messagesCount
    global guild

    guild = bot.get_guild(int(guildid))

    msgCount = 0
    maxCount = 0

    messagesCount = {}

    messagesChannelsList = []
    channelList = []
    #for server in bot.guilds:
    for channel in guild.channels:
        if str(channel.type) == 'text':
            channelList.append(channel)

    channelMax = len(channelList)

    if(ctx != None):
        percentMsg = await ctx.channel.send(f"`ładowanie wiadomości na serwerze: {guild.name}\nproszę czekać...`")
    else:
        print(1)

    channelCount = 0
    for channel in channelList:
        channelCount += 1
        if adminBeforeTime != "now": messagesList = await channel.history(limit=None, before=datetime.strptime(adminBeforeTime,"%d/%m/%y %H:%M:%S")).flatten()
        else: messagesList = await channel.history(limit=None).flatten()
        maxCount += len(messagesList)
        messagesChannelsList.append(messagesList)
        print(f"maxCount: {maxCount}, {channelCount}/{channelMax}, {channel}")
        #if(ctx != None): await ctx.channel.send(f"maxCount: {maxCount}, {channelCount}/{channelMax}, {channel}")

    channelCount = 0
    for messagesList in messagesChannelsList:
        messagesList.reverse()
        channelCount += 1
        for msg in messagesList:
            clear()
            print(messagesCount)
            print(f"wiadomosc: {msgCount}/{maxCount}, kanał: {channelCount}/{channelMax} {channelList[channelCount-1]}\n{msgCount*100.0/(maxCount)}%\n")
            if adminLimit == None:
                msgCount += 1
                await countNewMessage(bot, msg, percentMsg, msgCount, maxCount, channelCount, channelMax, channelList[channelCount-1])
            else:
                msgCount += 1
                if adminLimit > msgCount:
                    await countNewMessage(bot, msg, percentMsg, msgCount, maxCount, channelCount, channelMax, channelList[channelCount-1])
                else:
                    await writeOutMessagesCount(ctx, adminOutput, messagesCount, msgCount)
                    return


    await writeOutMessagesCount(ctx, adminOutput, messagesCount, msgCount)

async def writeOutMessagesCount(ctx, adminOutput, messagesCount, msgCount):
    global avatars

    sortedMessagesByBest = sorted(messagesCount.items(), key=lambda x: x[1], reverse=True)
    sortedMessagesByDate = messagesCount.items()

    returnmsg = "```\n"
    returnnames = "```\n"
    returnnames_bar = ""
    returnavatars = ""
    #with open(filename, "w", encoding="utf-8") as file:
    if adminOutput:
        for user in sortedMessagesByDate:
            returnmsg += f"{user[1]}\n"
            returnnames += f"{user[0]}\n"
            returnavatars += f"{avatars[user[0]]}\n"
        for user in sortedMessagesByBest:
            returnnames_bar += f"{progressbar.progress_bar(user[1], minvalue=0, maxvalue=msgCount, length=20)}{round(user[1]*100.0/msgCount, 2)}% ({user[1]}/{msgCount}) {user[0]}\n"
    else:
        for user in sortedMessagesByBest:
            returnmsg += f"{user[0]} | {user[1]} | {user[1]*100.0/msgCount}%\n"

    returnmsg += "```"
    returnnames += "```"
    #returnnames_bar += "```"
    #returnavatars += "```"

    if(ctx != None):
        await ctx.send(returnmsg)
        if adminOutput: 
            await ctx.send(returnnames)
            
            with open("avatars.txt", "w") as file1:
                #file.write('arg1 = {0}, arg2 = {1}'.format(arg1, arg2))
                file1.write(returnavatars)
            with open("avatars.txt", "rb") as file1:
                await ctx.send("Avatary:", file=discord.File(file1, "avatars.txt"))

            with open("result_bar.txt", "w", encoding="utf-8") as file2:
                #file.write('arg1 = {0}, arg2 = {1}'.format(arg1, arg2))
                file2.write(returnnames_bar)
            with open("result_bar.txt", "rb") as file2:
                await ctx.send("Tabelka:", file=discord.File(file2, "result_bar.txt"))

    else:
        #error pv
        print(1)

    #await percentMsg.edit(content=f"`wiadomosc: {msgCount}/{maxCount}, kanał: {channelCount}/{channelMax} {channel}\n{msgCount*100.0/(maxCount)}%\n`")

#display_name or name or nick in member
#only name in user
async def countNewMessage(bot, msg, percentMsg, msgCount, maxCount, channelCount, channelMax, channel):
    global messagesCount
    global guild
    global avatars
    #await bot.get_guild(870021183737823262).get_channel(1002292758582669392).send(msg.content)
    try: 
        member = guild.get_member(msg.author.id)

        if(percentMsg != None and msgCount % 69 == 0 or msgCount == maxCount):
            await percentMsg.edit(content=f"`wiadomosc: {msgCount}/{maxCount}, kanał: {channelCount}/{channelMax} {str(channel)}\n{msgCount*100.0/(maxCount)}%\n`")
        if(member.display_name not in messagesCount): 
            messagesCount[str(member.display_name)] = 1
            avatars[str(member.display_name)] = msg.author.avatar_url
        else: messagesCount[str(member.display_name)] += 1
    except:
        print("no such member lol")


async def downloadChannelHistory(channel):
    filename = f"{channel.name}.txt"
    maxcount = 99221
    currencount = 0
    with open(filename, "w", encoding="utf-8") as file:
        async for msg in channel.history(limit=None):
            currencount += 1
            clear()
            file.write(f"{msg.author.name}#{msg.clean_content}\n") 
            print(f"{currencount}/{maxcount}\n{currencount*100.0/maxcount}%\n")
