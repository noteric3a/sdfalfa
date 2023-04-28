import asyncio
import io
from datetime import datetime, timedelta
from random import randint
import aiohttp
import discord
from discord import File
from discord.ext import commands
from flask import jsonify, Flask
import requests

# 4/26/2023

app = Flask(__name__)

gn_target_time = ""
send_message_time = ""
warning_send_message_time = ""
gn_message = ""
gm_message = ""
sending_message = ""
gm_hour = None
gm_minute = None
gm_second = None
message_stopper = True
gm_stop_num = 0
gn_stop_num = 0
warning_time_checker = True
start_date = None
gm_start_date = None
url = "https://discord.com/api/webhooks/1089023578277687386/4Uftkx4wUZyxieQTBIADV0eS5y4JmcFdfzCGZ_qhtVLPACXJNu0FdiMG6WgoPB1qI3sI"


def GoodMorningMessage():
    global gmMessage
    GenericListOfGoodMorning = ['Hi', 'Serena hows life', 'How\'s life', 'How\'s life serena', 'Hiya', 'Oi', 'Boop',
                                'hey', 'Good morning', 'Good morning serena', 'Gm serena', 'whats up serena',
                                'Hi serena', 'hello my favorite NPC', 'wakey wakey', 'aneres iH']
    HigherTierGoodMorning = ['I hate history', 'good morning my favorite NPC', 'lets play chess, pawn to e4',
                             'top of the mornin to ya', 'I hate titration', 'Wakey wakey', 'I didn\'t do my kumon',
                             'ily', 'Why am i up this early', 'I cant sleep', 'bro edward is up playing piano',
                             'Zhao shang hao zhong guo, xian zai wo you bing qi lin', 'Zw sucks', 'how ya doin',
                             'English sucks', 'How J level of kumon', 'dinner > tony', 'You should download minecraft',
                             'I just hate Zw', 'what if drake was a bowl of assorted fruits', 'rhehehehehe',
                             'my brother jeffery arnold lanthrop andrew fruitloop hagleson the fifth got hit with a car going 5 miles an hour',
                             'xueeeeee hua piaooo piaooo']

    listchoice = randint(0, 100)
    if listchoice < 95:  # generic good morning
        listindex = randint(0, len(GenericListOfGoodMorning) - 1)  # random message from list
        gmMessage = GenericListOfGoodMorning[listindex]  # assigns gmMessage as the message

    elif listchoice >= 95:  # higher tier good morning
        listindex2 = randint(0, len(HigherTierGoodMorning) - 1)  # random message from list
        gmMessage = HigherTierGoodMorning[listindex2]  # assigns gmMessage as the message

    return gmMessage


def GoodNightMessage():
    global gnmessage
    gnMessages = ['good night serena', 'gn serena']
    rareGnMessages = ['gn my favorite NPC', 'night night', 'i hope you sleep well']

    chance = randint(0, 101)

    if chance > 90:
        index = randint(0, len(rareGnMessages) - 1)

        gnmessage = rareGnMessages[index]

    elif chance <= 90:
        index = randint(0, len(gnMessages) - 1)

        gnmessage = gnMessages[index]

    print("The message is: " + str(gnmessage))

    return gnmessage


async def target_time_getter(random_hour, random_minute, random_second, bot_type):
    if bot_type == 1:
        if random_hour is None:
            random_hour = randint(4, 7)

        if random_minute is None:
            if random_hour == 7:
                random_minute = randint(00, 15)
                random_second = randint(00, 59)
            else:
                random_minute = randint(00, 59)
                random_second = randint(00, 59)

        if random_second is None:
            random_second = randint(00, 59)

        # formatting

        if random_minute < 10:
            random_minute = "0" + str(random_minute)

        if random_second < 10:
            random_second = "0" + str(random_second)

        if random_hour < 10:
            random_hour = "0" + str(random_hour)

        gm_target_time = str(random_hour) + ":" + str(random_minute) + ":" + str(random_second)

        print("The target time is: " + gm_target_time)

        # gets the target time

        return gm_target_time

    elif bot_type == 2:
        if random_hour is None:
            random_hour = randint(0, 1)
            if random_hour == 1:
                random_hour = "22"
                random_minute = randint(0, 59)
            elif random_hour == 0:
                random_hour = "23"
                random_minute = randint(0, 15)

        if random_second is None:
            random_second = randint(0, 59)

        if random_minute is None:
            if random_hour == "22":
                random_minute = randint(0, 59)
            elif random_hour == "23":
                random_minute = randint(0, 15)
            else:
                random_minute = randint(0, 59)

        if int(random_hour) < 10:
            random_hour = "0" + str(random_hour)

        if int(random_minute) < 10:
            random_minute = "0" + str(random_minute)

        if int(random_second) < 10:
            random_second = "0" + str(random_second)

        gn_target_time = str(random_hour) + ":" + str(random_minute) + ":" + str(random_second)

        print("The target time is: " + gn_target_time)

        return gn_target_time


# gets the time
async def create_embed(bot_type, targetTime, message, binary, bot_type2):
    # getting the timestamp

    datetimemodule = datetime.now()

    date_now = datetimemodule.strftime("%Y-%m-%d")
    time_now = datetimemodule.strftime("%H:%M:%S")

    current_day = int(date_now.split("-")[2])

    if bot_type2 == 1:
        if int(time_now.split(":")[0]) >= 9:
            current_day += 1

    timestamp = datetime(int(date_now.split("-")[0]), int(date_now.split("-")[1]), current_day,
                         int(targetTime.split(":")[0]), int(targetTime.split(":")[1]),
                         int(targetTime.split(":")[2])).timestamp()
    timestamp = str(timestamp).split(".")[0]

    if binary == 1:
        colors = discord.Color.blue()  # working
    elif binary == 2:
        colors = discord.Color.red()  # stopped or changing
    elif binary == 3:
        colors = discord.Color.green()  # success
    elif binary == 4:
        colors = discord.Color.magenta()  # working
    elif binary == 5:
        colors = discord.Color.blurple()  # checks if working
    elif binary == 6:
        colors = discord.Color.dark_gold()  # warning color

    embede = discord.Embed(
        title=f"Time for {bot_type}",
        description=f"Time left: <t:{timestamp}:R> \n Target Time: {targetTime} \n Message: {message}",
        color=colors
    )

    if bot_type2 == 1:
        with open("day.txt", "r") as file:
            lines = file.readlines()
            if lines:  # checks if its empty
                gg = lines[-1]
    elif bot_type2 == 2:
        with open("day2.txt", "r") as file:
            lines = file.readlines()
            if lines:  # checks if its empty
                gg = lines[-1]

    if bot_type2 == 1 or bot_type2 == 2:
        # Add fields to the embed
        embede.add_field(name="Previous day", value=gg.split("-")[0].strip(), inline=False)
        embede.add_field(name="Previous message | Date and Time", value=gg.split("-")[1].strip(), inline=True)

        # Set the author, footer, and thumbnail of the embed
        embede.set_author(name="WeChat Bot")
        embede.set_footer(text="updated 4/17/2023")

    elif bot_type2 == 3:
        embede.add_field(name="IMPORTANT",
                         value="This message will send at your specified time or in 2 minutes! Use \"stop message\" to stop the bot!",
                         inline=True)

        # Set the author, footer, and thumbnail of the embed
        embede.set_author(name="WeChat Bot")
        embede.set_footer(text="updated 4/17/2023")

    return embede


# embed creator

def day(bot_type):
    if bot_type == 1:
        with open("day.txt", "r") as file:
            lines = file.readlines()
        if lines:  # checks if its empty
            days = lines[-1]
            # Print the last line
            return days
        else:
            print("File is empty.")
    elif bot_type == 2:
        with open("day2.txt", "r") as file:
            lines = file.readlines()
        if lines:  # checks if its empty
            days = lines[-1]
            # Print the last line
            return days
        else:
            print("File is empty.")


# gets the previous day according to the text file

def makeCurrentDay(bot_type, days):
    now = datetime.now()
    todayasstring = now.strftime("%d/%m/%Y")
    print(now)
    dayss = days.split("-")[0].strip()
    print(dayss)
    currentday = int(dayss) + 1
    if bot_type == 1:
        MessageKit = str(
            currentday) + " - " + gm_message + " | " + "Date and Time: " + todayasstring + " " + gm_target_time
        with open("day.txt", "a") as file:
            file.write("\n" + MessageKit)
    elif bot_type == 2:
        MessageKit = str(
            currentday) + " - " + gn_message + " | " + "Date and Time: " + todayasstring + " " + gn_target_time
        with open("day2.txt", "a") as file:
            file.write("\n" + MessageKit)


# record the current day that it is sent


intents = discord.Intents.default()
intents.message_content = True
bot = commands.AutoShardedBot(command_prefix='!', intents=intents, auto_reconnect=True, heartbeat_interval=60)


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@bot.event
async def on_message(message):
    global gm_target_time
    global embeded
    global gm_message
    global gn_target_time
    global embeded2
    global gn_message
    global gm_stop_num
    global gn_stop_num
    global message_stopper
    global embeded3
    global warning_time_checker

    if message.content.lower() == "stop gm":
        await message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:5000/stop_gm') as resp:
                if resp.status == 200:
                    gm_stop_num = 1
                    embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                                binary=2,
                                                bot_type2=1)
                    await embeded.edit(embed=embede)
                    pass
                else:
                    await message.channel.send("Failed to stop GM script.")
    if message.content.lower() == "reroll gm message":  # do not make into elif statements because it won't go to the next one if false
        await message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:5000/reroll_gm_message') as resp:
                if resp.status == 200:
                    gm_message = GoodMorningMessage()
                    embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                                binary=2,
                                                bot_type2=1)
                    await embeded.edit(embed=embede)
                    await asyncio.sleep(0.3)
                    embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                                binary=1,
                                                bot_type2=1)
                    await embeded.edit(embed=embede)
                else:
                    await message.channel.send("Couldnt reroll GM message.")
    if message.content.lower() == "reroll gm time":
        await message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:5000/reroll_gm_time') as resp:
                if resp.status == 200:
                    new_target_time = await target_time_getter(gm_hour, gm_minute, gm_second, bot_type=1)
                    gm_target_time = new_target_time
                    embede = await create_embed(bot_type="GM bot", targetTime=new_target_time, message=gm_message,
                                                binary=2,
                                                bot_type2=1)
                    await embeded.edit(embed=embede)
                    await asyncio.sleep(0.3)
                    embede = await create_embed(bot_type="GM bot", targetTime=new_target_time, message=gm_message,
                                                binary=1,
                                                bot_type2=1)
                    await embeded.edit(embed=embede)
                else:
                    await message.channel.send("Couldnt reroll GM time.")
    if message.content.lower().split("&")[0] == "set gm message":
        await message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:5000/set_gm_message') as resp:
                if resp.status == 200:
                    gm_message = message.content.lower().split("&")[1]
                    print(gm_message)
                    embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                                binary=2,
                                                bot_type2=1)
                    await embeded.edit(embed=embede)
                    await asyncio.sleep(0.3)
                    embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                                binary=1,
                                                bot_type2=1)
                    await embeded.edit(embed=embede)
                else:
                    await message.channel.send("Couldnt set GM message.")
    if message.content.lower() == "stop gn":
        await message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:5001/stop_gn') as resp:
                if resp.status == 200:
                    gn_stop_num = 1
                    embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                                binary=2,
                                                bot_type2=2)
                    await embeded2.edit(embed=embede)
                    pass
                else:
                    await message.channel.send("Failed to stop GN script.")
    if message.content.lower() == "reroll gn message":  # do not make into elif statements because it won't go to the next one if false
        await message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:5001/reroll_gn_message') as resp:
                if resp.status == 200:
                    gn_message = GoodNightMessage()
                    embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                                binary=2,
                                                bot_type2=2)
                    await embeded2.edit(embed=embede)
                    await asyncio.sleep(0.3)
                    embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                                binary=1,
                                                bot_type2=2)
                    await embeded2.edit(embed=embede)
                else:
                    await message.channel.send("Couldnt reroll GN message.")
    if message.content.lower() == "reroll gn time":
        await message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:5001/reroll_gn_time') as resp:
                if resp.status == 200:
                    new_target_time = await target_time_getter(gn_hour, gn_minute, gn_second, bot_type=2)
                    gn_target_time = new_target_time
                    embede = await create_embed(bot_type="GN bot", targetTime=new_target_time, message=gn_message,
                                                binary=2,
                                                bot_type2=2)
                    await embeded2.edit(embed=embede)
                    await asyncio.sleep(0.3)
                    embede = await create_embed(bot_type="GN bot", targetTime=new_target_time, message=gn_message,
                                                binary=1,
                                                bot_type2=2)
                    await embeded2.edit(embed=embede)
                else:
                    await message.channel.send("Couldnt reroll GN time.")
    if message.content.lower().split("&")[0] == "set gn message":
        await message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:5001/set_gn_message') as resp:
                if resp.status == 200:
                    gn_message = message.content.lower().split("&")[1]
                    print(gn_message)
                    embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                                binary=2,
                                                bot_type2=2)
                    await embeded2.edit(embed=embede)
                    await asyncio.sleep(0.3)
                    embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                                binary=1,
                                                bot_type2=2)
                    await embeded2.edit(embed=embede)
                else:
                    await message.channel.send("Couldnt set GN message.")
    if message.content.lower() == "stop message":
        warning_time_checker = False
        await message.delete()
        message_stopper = False
        embede = await create_embed(bot_type="Send Message", targetTime=send_message_time, message=sending_message,
                                    binary=2,
                                    bot_type2=3)
        await embeded3.edit(embed=embede)
    if message.content.lower().split("&")[0] == "set gn time":
        await message.delete()
        gn_time_setter = message.content.lower().split("&")[1]
        gn_time_set = gn_time_setter.split(":")
        gn_hour = int(gn_time_set[0])
        gn_minute = int(gn_time_set[1])
        gn_second = int(gn_time_set[2])
        gn_target_time = await target_time_getter(random_hour=gn_hour, random_minute=gn_minute, random_second=gn_second,
                                                  bot_type=2)
        embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                    binary=2,
                                    bot_type2=2)
        await embeded2.edit(embed=embede)
        await asyncio.sleep(0.3)
        embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                    binary=1,
                                    bot_type2=2)
        await embeded2.edit(embed=embede)
    if message.content.lower().split("&")[0] == "set gm time":
        await message.delete()
        gm_time_setter = message.content.lower().split("&")[1]
        gm_time_set = gm_time_setter.split(":")
        gm_hour = int(gm_time_set[0])
        gm_minute = int(gm_time_set[1])
        gm_second = int(gm_time_set[2])
        gm_target_time = await target_time_getter(random_hour=gm_hour, random_minute=gm_minute, random_second=gm_second,
                                                  bot_type=2)
        embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                    binary=2,
                                    bot_type2=1)
        await embeded.edit(embed=embede)
        await asyncio.sleep(0.3)
        embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                    binary=1,
                                    bot_type2=1)
        await embeded.edit(embed=embede)


gm_running = False

def get_seconds_until_next_time():
    current_time = datetime.now()
    next_time = current_time.replace(hour=15, minute=0, second=0)  # next time it runs will be at 3:00 PM

    if next_time <= current_time:
        next_time += timedelta(days=1)

    delta = next_time - current_time
    return delta.seconds


@bot.tree.command(name="gm", description="gm bot")
async def gm_bot(interaction: discord.Interaction, hour: int = None, minute: int = None, second: int = None):
    global gm_start_date

    if gm_start_date is not None and gm_start_date.date() == datetime.now().date(): # so the code doesnt run twice
        await interaction.response.send_message(content="Already running for today")

    gm_start_date = datetime.now()
    await interaction.response.send_message(content="Running.")
    recursive = 200
    while recursive == 200:
        try:
            recursive = await gm(interaction, hour, minute, second)
        except Exception as e:
            print(e)


async def gm(interaction: discord.Interaction, hour: int = None, minute: int = None,
             second: int = None):
    global embeded
    global gm_running
    global gm_hour
    global gm_minute
    global gm_second
    global gm_target_time
    global gm_message
    global gm_start_date
    channel = interaction.channel

    # Check if the command is already running
    if gm_running:
        await channel.send("The GM bot is already running.")
        return
    else:
        await channel.send("The GM bot has started!")

    # Set the flag to indicate that the command is running
    gm_running = True

    channel = interaction.channel
    gm_target_time = await target_time_getter(hour, minute, second, 1)

    time_list = gm_target_time.split(":")
    gm_hour = int(time_list[0])
    gm_minute = int(time_list[1])
    gm_second = int(time_list[2])

    if hour is None:
        gm_hour = None
    if minute is None:
        gm_minute = None
    if second is None:
        gm_second = None

    gm_message = GoodMorningMessage()
    current_days = day(bot_type=1)

    # Create the initial embed
    embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message, binary=1,
                                bot_type2=1)
    embeded = await channel.send(embed=embede)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:5000/gm') as resp:
                if resp.status == 200:

                    # Update the embed with a success message
                    makeCurrentDay(bot_type=1, days=current_days)
                    embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                                binary=3, bot_type2=1)
                    await embeded.edit(embed=embede)
                    await asyncio.sleep(get_seconds_until_next_time())
                    gm_running = False
                    gm_start_date = None
                    return 200
                else:
                    # Update the embed with a failure message
                    embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                                binary=2, bot_type2=1)
                    await embeded.edit(embed=embede)

    except Exception as e:
        print(e)
        embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                    binary=2, bot_type2=1)
        await embeded.edit(embed=embede)

    # Update the embed with the final message and set the flag to indicate that the command has finished running
    gm_running = False

    gm_start_date = None

    return 201


#########################################

gn_running = False

@bot.tree.command(name="gn", description="gn bot")
async def gn_bot(interaction: discord.Interaction, hour: int = None, minute: int = None, second: int = None):
    global start_date

    if start_date is not None and start_date.date() == datetime.now().date():
        await interaction.response.send_message(content="Already running for today")

    start_date = datetime.now()
    await interaction.response.send_message(content="Running.")
    recursive = 200
    while recursive == 200:
        try:
            recursive = await gn_bot_recursive(interaction, hour, minute, second)
        except Exception as e:
            print(e)


async def gn_bot_recursive(interaction: discord.Interaction, hour: int = None, minute: int = None, second: int = None):
    global start_date
    global gn_running
    global gn_message
    global gn_target_time
    global embeded2
    channel = interaction.channel

    if gn_running:
        await chanel.send("The GN bot is already running.")
        return
    else:
        await channel.send("The GN bot has started!")

    gn_running = True

    gn_target_time = await target_time_getter(hour, minute, second, bot_type=2)

    gn_message = GoodNightMessage()
    current_days = day(bot_type=2)

    embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message, binary=1, bot_type2=2)
    embeded2 = await channel.send(embed=embede)

    try:
        async with aiohttp.ClientSession() as session2:
            async with session2.get('http://localhost:5001/gn') as resp:
                if resp.status == 200:
                    makeCurrentDay(bot_type=2, days=current_days)
                    embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                                binary=3, bot_type2=2)
                    await embeded2.edit(embed=embede)
                    await asyncio.sleep(get_seconds_until_next_time())
                    gn_running = False
                    start_date = None
                    return 200 # Recursive call
                else:
                    embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                                binary=2, bot_type2=2)
                    await embeded2.edit(embed=embede)
    except Exception as e:
        gn_running = False
        print(e)
        embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                    binary=2, bot_type2=2)
        await embeded2.edit(embed=embede)

    gn_running = False

    start_date = None

    return 201

#################


@bot.tree.command(name="screenshot", description="takes a screenshot of wechat")
async def screenshot(interaction: discord.Interaction):
    await interaction.response.send_message(content="WeChat Screenshot.")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:42069/screenshot') as resp:
                if resp.status == 200:
                    file_data = io.BytesIO(await resp.read())
                    file = File(file_data, filename='screenshot.png')
                    await interaction.channel.send(file=file)
                else:
                    await interaction.channel.send('failed')

    except Exception as e:
        pass


@bot.tree.command(name="list_all_days", description="history of the messages")
async def list_all_days(interaction: discord.Interaction, bot_type: int):
    await interaction.response.send_message(content="Messages:")
    dchannel = interaction.channel
    if bot_type == 1:
        message_string = ""
        with open("day.txt", "r") as f:
            lines = f.readlines()
        for i, messages in enumerate(lines, start=1):
            message_string += f"{messages.strip()}\n"
        message_embed = discord.Embed(
            title="History of all messages sent",
            description=message_string,
            color=discord.Color.blurple()
        )
        await dchannel.send(embed=message_embed)
    elif bot_type == 2:
        message_string = ""
        with open("day2.txt", "r") as f:
            lines = f.readlines()
        for i, messages in enumerate(lines, start=1):
            message_string += f"{messages.strip()}\n"
        message_embed = discord.Embed(
            title="History of all messages sent",
            description=message_string,
            color=discord.Color.blurple()
        )
        await dchannel.send(embed=message_embed)


async def check_warning_time(message, send_message_time, set_message, warning_send_message_time):
    global warning_time_checker
    warning_time_checker = True
    while warning_time_checker:
        current_time = datetime.now().strftime("%H:%M:%S")
        if current_time == warning_send_message_time:
            send_message_embed = await create_embed(bot_type="Send Message", targetTime=send_message_time,
                                                    message=set_message,
                                                    binary=6, bot_type2=3)
            await message.edit(embed=send_message_embed)
            warning_time_checker = False
        await asyncio.sleep(1)


@bot.tree.command(name="send", description="sends message at given time or in 2 minutes")
async def send_message3(interaction: discord.Interaction, set_message: str, set_hour: int = None,
                        set_minute: int = None, set_second: int = None):
    global send_message_time
    global sending_message
    global warning_send_message_time
    global embeded3
    global message_checker
    channel = interaction.channel
    await interaction.response.send_message(content="Send message has started!")

    timesa = datetime.now()
    time_right_now = timesa.strftime("%H:%M:%S")
    time_split = time_right_now.split(":")

    if set_hour is None:
        set_hour = time_split[0]
    elif set_hour < 10:
        set_hour = "0" + str(set_hour)
    else:
        str(set_hour)

    if set_minute is None:
        set_minute = str(int(time_split[1]) + 2)
        if int(set_minute) < 10:
            set_minute = "0" + str(set_minute)
    elif set_minute < 10:
        set_minute = "0" + str(set_minute)
    else:
        str(set_minute)

    if set_second is None:
        set_second = randint(0, 59)
        if set_second < 10:
            set_second = "0" + str(set_second)
    elif set_second < 10:
        set_second = "0" + str(set_second)
    else:
        str(set_second)

    send_message_time = str(set_hour) + ":" + str(set_minute) + ":" + str(set_second)  # target time
    sending_message = set_message  # set message

    time_format = "%H:%M:%S"
    datetime_object = datetime.strptime(send_message_time, time_format)

    time_30_seconds_before = datetime_object - timedelta(seconds=30)
    warning_send_message_time = time_30_seconds_before.strftime("%H:%M:%S").lstrip("0").rjust(8, "0")  # warning time

    send_message_embed = await create_embed(bot_type="Send Message", targetTime=send_message_time, message=set_message,
                                            binary=1, bot_type2=3)
    embeded3 = await channel.send(embed=send_message_embed)

    message_checker = True

    try:
        asyncio.create_task(check_warning_time(embeded3, send_message_time, set_message, warning_send_message_time))
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:42069/send') as resp:
                if resp.status == 200:
                    send_message_embed = await create_embed(bot_type="Send Message", targetTime=send_message_time,
                                                            message=set_message,
                                                            binary=3, bot_type2=3)
                    await embeded3.edit(embed=send_message_embed)
                    message_checker = False
                else:
                    send_message_embed = await create_embed(bot_type="Send Message", targetTime=send_message_time,
                                                            message=set_message,
                                                            binary=2, bot_type2=3)
                    await embeded3.edit(embed=send_message_embed)

    except Exception as e:
        send_message_embed = await create_embed(bot_type="Send Message", targetTime=send_message_time,
                                                message=set_message,
                                                binary=2, bot_type2=3)
        await embeded3.edit(embed=send_message_embed)
        print(e)


# get requests from webserver to get the variables
@app.route('/get_gm_time', methods=['GET'])
def get_gm_time():
    data = {"variable_name": f"{gm_target_time}"}
    return jsonify(data)


@app.route('/get_gm_message', methods=['GET'])
def get_gm_message():
    data = {"variable_name": f"{gm_message}"}
    return jsonify(data)


@app.route('/stop_gm', methods=['GET'])
def stop_gm():
    global gm_stop_num
    response = jsonify(variable_name=gm_stop_num)
    gm_stop_num = 0
    return response


@app.route('/stop_gn', methods=['GET'])
def stop_gn():
    global gn_stop_num
    response = jsonify(variable_name=gn_stop_num)
    gn_stop_num = 0
    return response


@app.route('/get_gn_time', methods=['GET'])
def get_gn_time():
    return jsonify(variable_name=gn_target_time)


@app.route('/get_gn_message', methods=['GET'])
def get_gn_message():
    data = {"variable_name": f"{gn_message}"}
    return jsonify(data)


@app.route('/get_send_message_time', methods=['GET'])
def get_send_message_time():
    return jsonify(variable_name=send_message_time)


@app.route('/get_send_message', methods=['GET'])
def get_send_message():
    return jsonify(variable_name=sending_message)


@app.route('/stop_send_message', methods=['GET'])
def get_stop_send():
    return jsonify(variable_name=message_stopper)


loop = asyncio.get_event_loop()


def run_flask():
    app.run(host='localhost', port=8080)


async def run_discord():
    await bot.start('MTA4OTAyMTQ4NDk1MDkwMDc5OQ.GjKL5O.BaqdAAoJCfRKbrpLdn6E1fKWylt4lHudTdLNzI', reconnect=True)


# Start the Flask and Discord tasks
flask_task = loop.run_in_executor(None, run_flask)
discord_task = loop.create_task(run_discord())

# Wait for both tasks to complete (this will never happen since both tasks run forever)
loop.run_until_complete(asyncio.gather(discord_task))
loop.run_until_complete(asyncio.gather(discord_task))
