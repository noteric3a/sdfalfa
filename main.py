import asyncio
import io
from datetime import datetime, timedelta
from random import randint

import aiohttp
import discord
from discord import File
from discord.ext import commands
from flask import jsonify, Flask

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


async def target_time_getter(hour, minute, second, bot_type):
    if bot_type == 1:
        if hour is None:
            hour = randint(4, 7)

        if minute is None:
            if hour == 7:
                minute = randint(00, 15)
                second = randint(00, 59)
            else:
                minute = randint(00, 59)
                second = randint(00, 59)

        if second is None:
            second = randint(00, 59)

        # formatting

        if minute < 10:
            minute = "0" + str(minute)

        if second < 10:
            second = "0" + str(second)

        if hour < 10:
            hour = "0" + str(hour)

        time = str(hour) + ":" + str(minute) + ":" + str(second)

        print("The target time is: " + time)

        # gets the target time

        return time

    elif bot_type == 2:
        if hour is None:
            hour = randint(0, 1)
            if hour == 1:
                hour = "22"
                minute = randint(0, 59)
            elif hour == 0:
                hour = "23"
                minute = randint(0, 15)

        if second is None:
            second = randint(0, 59)

        if minute is None:
            if hour == "22":
                minute = randint(0, 59)
            elif hour == "23":
                minute = randint(0, 15)
            else:
                minute = randint(0, 59)

        if int(hour) < 10:
            hour = "0" + str(hour)

        if int(minute) < 10:
            minute = "0" + str(minute)

        if int(second) < 10:
            second = "0" + str(second)

        time = str(hour) + ":" + str(minute) + ":" + str(second)

        print("The target time is: " + time)

        return time

    elif bot_type == 3:
        timesa = datetime.now()
        time_right_now = timesa.strftime("%H:%M:%S")
        time_split = time_right_now.split(":")

        if hour is None:
            hour = time_split[0]
        elif hour < 10:
            hour = "0" + str(hour)
        else:
            str(hour)

        if minute is None:
            minute = str(int(time_split[1]) + 2)
            if int(minute) < 10:
                minute = "0" + str(minute)
        elif minute < 10:
            minute = "0" + str(minute)
        else:
            str(minute)

        if second is None:
            second = randint(0, 59)
            if second < 10:
                second = "0" + str(second)
        elif second < 10:
            second = "0" + str(second)
        else:
            str(second)

        time = str(hour) + ":" + str(minute) + ":" + str(second)  # target time

        time_format = "%H:%M:%S"
        datetime_object = datetime.strptime(time, time_format)

        time_30_seconds_before = datetime_object - timedelta(seconds=30)
        warning_time = time_30_seconds_before.strftime("%H:%M:%S").lstrip("0").rjust(8, "0")  # warning time

        return time, warning_time  # returns the time and warning time


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
                x = -1
                while True:
                    if lines[x] == "":
                        x -= 1
                    else:
                        gg = lines[x]
                        break
    elif bot_type2 == 2:
        with open("day2.txt", "r") as file:
            lines = file.readlines()
            if lines:  # checks if its empty
                x = -1
                while True:
                    if lines[x] == "":
                        x -= 1
                    else:
                        gg = lines[x]
                        break

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
            x = -1
            while True:
                if lines[x] == "":
                    x -= 1
                else:
                    days = lines[x]
                    break
            # Print the last line
            return days
        else:
            print("File is empty.")
    elif bot_type == 2:
        with open("day2.txt", "r") as file:
            lines = file.readlines()
        if lines:  # checks if its empty
            x = -1
            while True:
                if lines[x] == "":
                    x -= 1
                else:
                    days = lines[x]
                    break
            # Print the last line
            return days
        else:
            print("File is empty.")


# gets the previous day according to the text file

def makeCurrentDay(bot_type, days, message, target_time):
    now = datetime.now()
    todayasstring = now.strftime("%d/%m/%Y")
    print(now)
    dayss = days.split("-")[0].strip()
    print(dayss)
    currentday = int(dayss) + 1
    MessageKit = str(currentday) + " - " + message + " | " + "Date and Time: " + todayasstring + " " + target_time
    if bot_type == 1:
        with open("day.txt", "a") as file:
            file.write("\n" + MessageKit)
    elif bot_type == 2:
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
    global embed_message
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
                    new_target_time = await target_time_getter(hour=None, minute=None, second=None, bot_type=1)
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
                    new_target_time = await target_time_getter(hour=None, minute=None, second=None, bot_type=2)
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
        await message.delete()
        message_stopper = False
        embede = await create_embed(bot_type="Send Message", targetTime=send_message_time, message=sending_message,
                                    binary=2,
                                    bot_type2=3)
        await embed_message.edit(embed=embede)
    if message.content.lower().split("&")[0] == "set gn time" and message.content.lower() != "set gn time":
        await message.delete()
        gn_time_setter = message.content.lower().split("&")[1]
        gn_time_set = gn_time_setter.split(":")
        gn_hour = int(gn_time_set[0])
        gn_minute = int(gn_time_set[1])
        gn_second = int(gn_time_set[2])
        gn_target_time = await target_time_getter(hour=gn_hour, minute=gn_minute, second=gn_second,
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
    if message.content.lower().split("&")[0] == "set gm time" and message.content.lower() != "set gm time":
        await message.delete()
        gm_time_setter = message.content.lower().split("&")[1]
        gm_time_set = gm_time_setter.split(":")
        gm_hour = int(gm_time_set[0])
        gm_minute = int(gm_time_set[1])
        gm_second = int(gm_time_set[2])
        gm_target_time = await target_time_getter(hour=gm_hour, minute=gm_minute, second=gm_second,
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

    if gm_start_date is not None and gm_start_date.date() == datetime.now().date():  # so the code doesnt run twice
        await interaction.response.send_message(content="Already running for today")

    gm_start_date = datetime.now()
    await interaction.response.send_message(content="Running.")
    recursive = 200
    while recursive == 200:
        recursive = await gm(interaction, hour, minute, second)


async def gm(interaction: discord.Interaction, hour: int = None, minute: int = None,
             second: int = None):
    global embeded
    global gm_running
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

    gm_message = GoodMorningMessage()

    # Create the initial embed
    embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message, binary=1,
                                bot_type2=1)
    embeded = await channel.send(embed=embede)
    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:5000/gm') as resp:
            if resp.status == 200:

                # Update the embed with a success message
                embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                            binary=3, bot_type2=1)
                await embeded.edit(embed=embede)
                current_days = day(bot_type=1)
                makeCurrentDay(bot_type=1, days=current_days, message=gm_message, target_time=gm_target_time)
                await asyncio.sleep(get_seconds_until_next_time())
                gm_running = False
                gm_start_date = None
                return 200
            else:
                # Update the embed with a failure message
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
        recursive = await gn_bot_recursive(interaction, hour, minute, second)


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

    embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message, binary=1, bot_type2=2)
    embeded2 = await channel.send(embed=embede)

    async with aiohttp.ClientSession() as session2:
        async with session2.get('http://localhost:5001/gn') as resp:
            if resp.status == 200:
                embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                            binary=3, bot_type2=2)
                await embeded2.edit(embed=embede)
                current_days = day(bot_type=2)
                makeCurrentDay(bot_type=2, days=current_days, message=gn_message, target_time=gn_target_time)
                await asyncio.sleep(get_seconds_until_next_time())
                gn_running = False
                start_date = None
                return 200  # Recursive call
            else:
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


message_queue = []
queue_start = None

@bot.tree.command(name="send", description="sends message at given time or in 2 minutes")
async def send_message_queue(interaction: discord.Interaction, set_message: str, set_hour: int = None,
                             set_minute: int = None, set_second: int = None, interval: int = None):
    global queue_start
    message_queue.append(set_message)  # adds the message to the queue

    if queue_start is None:
        if interval is None or interval < 5:
            interval = 30  # in seconds, will set the delay interval of the queue to 30 as default

        queue_start = "1"
        target_time, warning_time = await target_time_getter(set_hour, set_minute, set_second, 3)
        print(target_time)
        print(warning_time)
        await interaction.response.send_message(content="Send message is starting!")
        await message_queueer(target_time=target_time, warning_time=warning_time, interval=interval,
                              interaction=interaction, set_message=set_message)
    else:
        await interaction.response.send_message(content=f"Send message has already started! If you put a set message, it has been added to the queue! current queue: {message_queue}" , ephemeral=True)
        return


async def message_queueer(target_time, warning_time, interval, interaction, set_message):
    global message_queue
    global queue_start
    global message_stopper
    global embed_message
    channel = interaction.channel
    embede = await create_embed(bot_type="Send Message", targetTime=target_time, message=set_message,
                                binary=1, bot_type2=3)
    embed_message = await channel.send(embed=embede)
    while message_stopper:
        current_time = datetime.now().strftime("%H:%M:%S")
        if current_time == target_time:
            for message in message_queue:  # runs until queue is empty
                print("setting embed to red")
                send_message_embed = await create_embed(bot_type="Send Message", targetTime=target_time,
                                                        message=set_message,
                                                        binary=2, bot_type2=3)
                await embed_message.edit(embed=send_message_embed)
                print("doing the task")
                return_number = await send_message3(message=message)  # sends the message
                send_message_embed = await create_embed(bot_type="Send Message", targetTime=target_time,
                                                        message=set_message,
                                                        binary=1, bot_type2=3)
                print("setting back to blue")
                await embed_message.edit(embed=send_message_embed)
                if return_number == 201:  # fail number
                    send_message_embed = await create_embed(bot_type="Send Message", targetTime=target_time,
                                                            message=set_message,
                                                            binary=2, bot_type2=3)
                    await embed_message.edit(embed=send_message_embed)
                    message_stopper = False
                    break  # completely stops
                await asyncio.sleep(interval)  # sleeps for interval before going back to it
            message_stopper = False
            break  # breaks from the loop

        if current_time == warning_time:  # if it gets to warning time, set the embed to yellow
            send_message_embed = await create_embed(bot_type="Send Message", targetTime=target_time,
                                                    message=set_message,
                                                    binary=6, bot_type2=3)
            await embed_message.edit(embed=send_message_embed)
        await asyncio.sleep(1)

    if message_stopper is True:  # turns it green if it really ended
        send_message_embed = await create_embed(bot_type="Send Message", targetTime=target_time,
                                                message=set_message,
                                                binary=3, bot_type2=3)
        await embed_message.edit(embed=send_message_embed)
    else:
        send_message_embed = await create_embed(bot_type="Send Message", targetTime=target_time,
                                                message=set_message,
                                                binary=2, bot_type2=3)
        await embed_message.edit(embed=send_message_embed)

    message_queue = []  # resets queue
    queue_start = None  # finished queue


async def send_message3(message):
    global sending_message

    sending_message = message  # set message

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:42069/send') as resp:
                if resp.status == 200:
                    return 200
                else:
                    return 201

    except Exception as e:
        print(e)
        return 201


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


@app.route('/get_send_message', methods=['GET'])
def get_send_message():
    return jsonify(variable_name=sending_message)


loop = asyncio.get_event_loop()


def run_flask():
    app.run(host='localhost', port=8080)


async def run_discord():
    await bot.start('MTA5ODc3MTgwMDc2ODM4OTE2MA.GZgk5P.tN0PneF1l4u_IYbJG_1Fz3wxG92Gbtw8lpQrnc', reconnect=True)


# Start the Flask and Discord tasks
flask_task = loop.run_in_executor(None, run_flask)
discord_task = loop.create_task(run_discord())

# Wait for both tasks to complete (this will never happen since both tasks run forever)
loop.run_until_complete(asyncio.gather(discord_task))
loop.run_until_complete(asyncio.gather(discord_task))
