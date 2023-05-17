import asyncio
import calendar
import io
import logging
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
gm_embed = None
gn_embed = None
send_message_embed = None
TOKEN = "MTA4OTAyMTQ4NDk1MDkwMDc5OQ.GX1t9O.A7PgLBttKkpaA8MQs0bV3lnavmT7SqAiwOjQyU"
url = "https://discord.com/api/webhooks/1089023578277687386/4Uftkx4wUZyxieQTBIADV0eS5y4JmcFdfzCGZ_qhtVLPACXJNu0FdiMG6WgoPB1qI3sI"

logging.basicConfig(filename='main.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


def logger(event_name, event_details):
    logging.info(f"{event_name}: {event_details}")


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

    datetime_module = datetime.now()

    date_now = datetime_module.strftime("%Y-%m-%d")
    time_now = datetime_module.strftime("%H:%M:%S")

    current_year = int(date_now.split("-")[0])
    current_month = int(date_now.split("-")[1])
    current_day = int(date_now.split("-")[2])
    current_hour = int(targetTime.split(":")[0])
    current_minute = int(targetTime.split(":")[1])
    current_second = int(targetTime.split(":")[2])

    _, days_in_month = calendar.monthrange(current_year,
                                           current_month)  # the underscore is a placeholder because this returns a
    # tuple

    if bot_type2 == 1:
        if int(time_now.split(":")[0]) >= 12:
            current_day += 1

    if current_day > days_in_month:
        current_day = 1
        current_month = int(date_now.split("-")[1]) + 1

    timestamp = datetime(current_year, current_month, current_day, current_hour, current_minute,
                         current_second).timestamp()
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

    if bot_type2 == 1 or bot_type2 == 2:
        embede = discord.Embed(
            title=f"Time for {bot_type}",
            description=f"Time left: <t:{timestamp}:R> \n Target Time: {targetTime} \n Message: {message}",
            color=colors
        )
    elif bot_type2 == 3:
        queue_priority_counter = 0
        messages = ""
        for message in message_queue:
            queue_priority = str(queue_priority_counter)
            messages += f"\n {queue_priority}: {message}"
            queue_priority_counter += 1
        embede = discord.Embed(
            title=f"Time for {bot_type}",
            description=f"Time left: <t:{timestamp}:R> \n Target Time: {targetTime} \n Message Queue: {messages}",
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
        embede.set_footer(text="updated 4/30/2023")

    elif bot_type2 == 3:
        embede.add_field(name="IMPORTANT",
                         value="This message will send at your specified time or in 2 minutes! Use \"stop message\" to stop the bot!",
                         inline=True)

        # Set the author, footer, and thumbnail of the embed
        embede.set_author(name="WeChat Bot")
        embede.set_footer(text="updated 4/30/2023")

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

def makeCurrentDay(bot_type, days, message, mcd_target_time):
    now = datetime.now()
    today_as_string = now.strftime("%d/%m/%Y")
    print(now)
    current_days = days.split("-")[0].strip()
    print(current_days)
    current_day = int(current_days) + 1
    MessageKit = str(
        current_day) + " - " + message + " | " + "Date and Time: " + today_as_string + " " + mcd_target_time
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
    global gm_embed
    global gm_message
    global gn_target_time
    global gn_embed
    global gn_message
    global gm_stop_num
    global gn_stop_num
    global send_message_time
    global warning_time
    global message_stopper
    global interval
    global warning_time_checker

    if message.content.lower() == "stop gm":
        await message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:5000/stop_gm') as resp:
                if resp.status == 200:
                    gm_stop_num = 1

                    logger("stop_gm", "success")
                    embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                                binary=2,
                                                bot_type2=1)
                    await gm_embed.edit(embed=embede)
                    logger("stop_gm, embed changed", "success")
                    pass
                else:
                    logger("stop_gm", "failed")
                    await message.channel.send("Failed to stop GM script.")
    if message.content.lower() == "reroll gm message":  # do not make into elif statements because it won't go to the next one if false
        await message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:5000/reroll_gm_message') as resp:
                if resp.status == 200:

                    gm_message = GoodMorningMessage()

                    logger("rerolling gm message", "success")

                    embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                                binary=2,
                                                bot_type2=1)
                    await gm_embed.edit(embed=embede)
                    await asyncio.sleep(0.3)
                    embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                                binary=1,
                                                bot_type2=1)
                    await gm_embed.edit(embed=embede)

                    logger("rerolling gm message, embed changed", "success")
                else:
                    await message.channel.send("Couldnt reroll GM message.")
    if message.content.lower() == "reroll gm time":
        await message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:5000/reroll_gm_time') as resp:
                if resp.status == 200:
                    new_target_time = await target_time_getter(hour=None, minute=None, second=None, bot_type=1)
                    gm_target_time = new_target_time
                    logger("rerolling gm time", "success")
                    embede = await create_embed(bot_type="GM bot", targetTime=new_target_time, message=gm_message,
                                                binary=2,
                                                bot_type2=1)
                    await gm_embed.edit(embed=embede)
                    await asyncio.sleep(0.3)
                    embede = await create_embed(bot_type="GM bot", targetTime=new_target_time, message=gm_message,
                                                binary=1,
                                                bot_type2=1)
                    await gm_embed.edit(embed=embede)
                    logger("rerolling gm time, embed changed", "success")
                else:
                    await message.channel.send("Couldnt reroll GM time.")
    if message.content.lower().split("&")[0] == "set gm message":
        await message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:5000/set_gm_message') as resp:
                if resp.status == 200:
                    gm_message = message.content.lower().split("&")[1]
                    logger("setting gm message", "success")
                    embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                                binary=2,
                                                bot_type2=1)
                    await gm_embed.edit(embed=embede)
                    await asyncio.sleep(0.3)
                    embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                                binary=1,
                                                bot_type2=1)
                    await gm_embed.edit(embed=embede)
                    logger("setting gm message, embed changed", "success")
                else:
                    await message.channel.send("Couldnt set GM message.")
    if message.content.lower() == "stop gn":
        await message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:5001/stop_gn') as resp:
                if resp.status == 200:
                    gn_stop_num = 1
                    logger("stopping gn", "success")
                    embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                                binary=2,
                                                bot_type2=2)
                    await gn_embed.edit(embed=embede)
                    logger("stopping gn, embed changed", "success")
                    pass
                else:
                    await message.channel.send("Failed to stop GN script.")
    if message.content.lower() == "reroll gn message":  # do not make into elif statements because it won't go to the next one if false
        await message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:5001/reroll_gn_message') as resp:
                if resp.status == 200:
                    gn_message = GoodNightMessage()
                    logger("rerolling gn_message", "success")
                    embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                                binary=2,
                                                bot_type2=2)
                    await gn_embed.edit(embed=embede)
                    await asyncio.sleep(0.3)
                    embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                                binary=1,
                                                bot_type2=2)
                    await gn_embed.edit(embed=embede)
                    logger("rerolling gn_message, embed changed", "success")
                else:
                    await message.channel.send("Couldnt reroll GN message.")
    if message.content.lower() == "reroll gn time":
        await message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:5001/reroll_gn_time') as resp:
                if resp.status == 200:
                    new_target_time = await target_time_getter(hour=None, minute=None, second=None, bot_type=2)
                    gn_target_time = new_target_time
                    logger("rerolling gn_time", "success")
                    embede = await create_embed(bot_type="GN bot", targetTime=new_target_time, message=gn_message,
                                                binary=2,
                                                bot_type2=2)
                    await gn_embed.edit(embed=embede)
                    await asyncio.sleep(0.3)
                    embede = await create_embed(bot_type="GN bot", targetTime=new_target_time, message=gn_message,
                                                binary=1,
                                                bot_type2=2)
                    await gn_embed.edit(embed=embede)
                    logger("rerolling gn_time, embed changed", "success")
                else:
                    await message.channel.send("Couldnt reroll GN time.")
    if message.content.lower().split("&")[0] == "set gn message":
        await message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://localhost:5001/set_gn_message') as resp:
                if resp.status == 200:
                    logger("setting gn_message", "success")
                    gn_message = message.content.lower().split("&")[1]
                    print(gn_message)
                    embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                                binary=2,
                                                bot_type2=2)
                    await gn_embed.edit(embed=embede)
                    await asyncio.sleep(0.3)
                    embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                                binary=1,
                                                bot_type2=2)
                    await gn_embed.edit(embed=embede)
                    logger("setting gn_message, embed changed", "success")
                else:
                    await message.channel.send("Couldnt set GN message.")
    if message.content.lower() == "stop message":
        await message.delete()
        message_stopper = False
        logger("stopping message_send", "success")
        embed = await create_embed(bot_type="Send Message", targetTime=send_message_time,
                                   message=sending_message,
                                   binary=2, bot_type2=3)
        await send_message_embed.edit(embed=embed)
        logger("stopping message_send, embed changed", "success")
    if message.content.lower().split("&")[0] == "set gn time" and message.content.lower() != "set gn time":
        await message.delete()
        gn_time_setter = message.content.lower().split("&")[1]
        gn_time_set = gn_time_setter.split(":")
        gn_hour = int(gn_time_set[0])
        gn_minute = int(gn_time_set[1])
        gn_second = int(gn_time_set[2])
        logger("setting gn_time", "success")
        gn_target_time = await target_time_getter(hour=gn_hour, minute=gn_minute, second=gn_second,
                                                  bot_type=2)
        embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                    binary=2,
                                    bot_type2=2)
        await gn_embed.edit(embed=embede)
        await asyncio.sleep(0.3)
        embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                    binary=1,
                                    bot_type2=2)
        await gn_embed.edit(embed=embede)
        logger("setting gn_time, embed changed", "success")
    if message.content.lower().split("&")[0] == "set gm time" and message.content.lower() != "set gm time":
        await message.delete()
        gm_time_setter = message.content.lower().split("&")[1]
        gm_time_set = gm_time_setter.split(":")
        gm_hour = int(gm_time_set[0])
        gm_minute = int(gm_time_set[1])
        gm_second = int(gm_time_set[2])
        logger("setting gm_time", "success")
        gm_target_time = await target_time_getter(hour=gm_hour, minute=gm_minute, second=gm_second,
                                                  bot_type=2)
        embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                    binary=2,
                                    bot_type2=1)
        await gm_embed.edit(embed=embede)
        await asyncio.sleep(0.3)
        embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                    binary=1,
                                    bot_type2=1)
        await gm_embed.edit(embed=embede)
        logger("setting gm_time, embed changed", "success")

#####################

gm_running = False


def get_seconds_until_next_time():
    current_time = datetime.now()
    next_time = current_time.replace(hour=15, minute=0, second=0)  # next time it runs will be at 3:00 PM

    if next_time <= current_time:
        next_time += timedelta(days=1)

    delta = next_time - current_time
    return delta.seconds


@bot.tree.command(name="gm", description="gm bot")
async def gm_bot(interaction: discord.Interaction, hour: int = None, minute: int = None, second: int = None, instant_response: bool = None):
    global gm_start_date

    if gm_start_date is not None and gm_start_date.date() == datetime.now().date():  # so the code doesnt run twice
        logger("starting gm bot...", "already running for today")
        await interaction.response.send_message(content="Already running for today")

    gm_start_date = datetime.now()
    await interaction.response.send_message(content="Running.")
    recursive = 200
    while recursive == 200:
        logger("starting gm bot...", "Running!")
        recursive = await gm(interaction, hour, minute, second)
        logger("starting gm bot...", "Finished!")


async def gm(interaction: discord.Interaction, hour: int = None, minute: int = None,
             second: int = None):
    global gm_embed
    global gm_running
    global gm_target_time
    global gm_message
    global gm_start_date
    channel = interaction.channel

    gm_running = False

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
    logger("gm_target_time generated", f"Success! :{gm_target_time}")

    gm_message = GoodMorningMessage()
    logger("gm_message generated", f"Success! :{gm_message}")
    # Create the initial embed
    embed = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message, binary=1,
                               bot_type2=1)
    gm_embed = await channel.send(embed=embed)
    logger("gm_bot", "Embed Sent!")
    gm_stopper = True

    async with aiohttp.ClientSession() as session:
        async with session.get('http://localhost:42069/instant_response') as resp:
            if resp.status == 200:
                print("instant response triggered")
                gm_stopper = False
                current_days = day(bot_type=1)
                instant_response_time = datetime.now().strftime("%H:%M:%S")
                makeCurrentDay(bot_type=1, days=current_days, message=gm_message, mcd_target_time=instant_response_time)
                logger("gm_bot", "Recorded the current day!")
                embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                            binary=3, bot_type2=1)
                await gm_embed.edit(embed=embede)
            else:
                print("uh oh")

    while gm_stopper:
        current_time = datetime.now().strftime("%H:%M:%S")
        if current_time == gm_target_time:
            try:
                async with aiohttp.ClientSession() as session:
                    logger("gm_bot", "Request sent!")
                    async with session.get('http://localhost:5000/gm') as resp:
                        if resp.status == 200:
                            logger("gm_bot", "Request Code 200!")
                            # Update the embed with a success message
                            current_days = day(bot_type=1)
                            makeCurrentDay(bot_type=1, days=current_days, message=gm_message, mcd_target_time=gm_target_time)
                            logger("gm_bot", "Recorded the current day!")
                            embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                                        binary=3, bot_type2=1)
                            await gm_embed.edit(embed=embede)
                            logger("gm_bot", "Embed is now green")
                            await asyncio.sleep(get_seconds_until_next_time())
                            gm_running = False
                            gm_start_date = None
                            return 200
                        else:
                            logger("gm_bot", f"uh-oh spagettio")
                            embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time,
                                                        message=gm_message, binary=2,
                                                        bot_type2=1)
                            await gm_embed.edit(embed=embede)
            except Exception as e:
                # Update the embed with a failure message
                logger("gm_bot", f"uh-oh spagettio")
                embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message, binary=2,
                                            bot_type2=1)
                await gm_embed.edit(embed=embede)
                print(e)
        await asyncio.sleep(1)
    # Update the embed with the final message and set the flag to indicate that the command has finished running
    gm_running = False

    gm_start_date = None
    logger("gm_bot", "Returned 201")
    return 201


#########################################

gn_running = False


@bot.tree.command(name="gn", description="gn bot")
async def gn_bot(interaction: discord.Interaction, hour: int = None, minute: int = None, second: int = None):
    global start_date
    global gn_embed

    if start_date is not None and start_date.date() == datetime.now().date():
        await interaction.response.send_message(content="Already running for today")
        logger("gn_bot", "stopped due to Already Running Today")

    start_date = datetime.now()
    await interaction.response.send_message(content="Running.")
    logger("gn_bot", "Running!")
    recursive = 200
    while recursive == 200:
        logger("gn_bot", "bot started")
        recursive = await gn_bot_recursive(interaction, hour, minute, second)
        logger("gn_bot", "bot finished")


async def gn_bot_recursive(interaction: discord.Interaction, hour: int = None, minute: int = None, second: int = None):
    global start_date
    global gn_running
    global gn_message
    global gn_target_time
    global gn_embed
    channel = interaction.channel

    if gn_running:
        await channel.send("The GN bot is already running.")
        return
    else:
        await channel.send("The GN bot has started!")

    gn_running = True

    gn_target_time = await target_time_getter(hour, minute, second, bot_type=2)  # gets the gn time
    logger("gn_bot", f"gn_target_time: {gn_target_time}")

    gn_message = GoodNightMessage()  # gets the gn message
    logger("gn_bot", f"gn_message: {gn_message}")

    embed = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message, binary=1, bot_type2=2)
    gn_embed = await channel.send(embed=embed)
    logger("gn_bot", "Embed Sent")  # sends the embed

    gn_stopper = True

    while gn_stopper:
        current_time = datetime.now().strftime("%H:%M:%S")
        if current_time == gn_target_time:
            logger("gn_bot", "started session")
            async with aiohttp.ClientSession() as session2:
                async with session2.get('http://localhost:5001/gn') as resp:
                    if resp.status == 200:
                        logger("gn_bot", "200 recieved from webserver")
                        current_days = day(bot_type=2)
                        makeCurrentDay(bot_type=2, days=current_days, message=gn_message, mcd_target_time=gn_target_time)
                        logger("gn_bot", f"recorded today: {current_days}")
                        embed = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                                   binary=3, bot_type2=2)
                        await gn_embed.edit(embed=embed)
                        logger("gn_bot", "embed is now green")
                        await asyncio.sleep(get_seconds_until_next_time())
                        gn_running = False
                        start_date = None
                        logger("gn_bot", "returning 200")
                        return 200  # Recursive call
                    else:
                        embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                                    binary=2, bot_type2=2)
                        await gn_embed.edit(embed=embede)
                        logger("gn_bot", f"uh-oh spagettio, got a different response code: {resp.status}")
                        gn_stopper = False
        await asyncio.sleep(1)
    gn_running = False

    start_date = None
    logger("gn_bot", "returning 201")
    return 201


#################


@bot.tree.command(name="screenshot", description="takes a screenshot of wechat")
async def screenshot(interaction: discord.Interaction):
    await interaction.response.send_message(content="WeChat Screenshot.")
    logger("Screenshot", "sent the message")
    try:
        async with aiohttp.ClientSession() as session:
            logger("Screenshot", "started session, awaiting screenshot")
            async with session.get('http://localhost:42069/screenshot') as resp:
                if resp.status == 200:
                    logger("Screenshot", "200")
                    file_data = io.BytesIO(await resp.read())
                    logger("Screenshot", "reading file")
                    file = File(file_data, filename='screenshot.png')
                    await interaction.channel.send(file=file)
                    logger("Screenshot", "sent the screenshot")
                else:
                    await interaction.channel.send(f'failed: {resp.status}')
                    logger("Screenshot", "failed after sending request")

    except Exception as e:
        print(f"Screenshot Failed: {e}")
        logger("Screenshot", f"failed by starting session: {e}")
        pass

processed_interactions = set()

@bot.tree.command(name="list_all_days", description="history of the messages")
async def list_all_days(interaction: discord.Interaction, bot_type: int, page: int = None):
    if interaction.id in processed_interactions:
        return
    processed_interactions.add(interaction.id)
    dchannel = interaction.channel
    embeds = []
    message_string = ""
    if bot_type == 1:
        with open("day.txt", "r") as f:  # opens gm file
            lines = f.readlines()
    elif bot_type == 2:
        with open("day2.txt", "r") as f:  # opens gn file
            lines = f.readlines()

    for i, message in enumerate(lines, start=1):
        message_string += f"{message.strip()}\n"

        if i % 20 == 0 or i == len(lines):
            message_embed = discord.Embed(
                title="History of all messages sent",
                description=message_string,
                color=discord.Color.blurple()
            )
            embeds.append(message_embed)
            message_string = ""

    try:
        if page is None:
            message_index = 0  # indexing the list of the embeds, this is the first embed
            await interaction.response.send_message(content="Page 1")
        else:
            if 0 <= page - 1 <= len(embeds):
                message_index = page - 1  # if page is specified, will go to that page
                await interaction.response.send_message(content=f"Page {page}")
            else:
                message_index = 0  # sets page to 0 if page is not valid
                await interaction.response.send_message(content=f"Page {message_index}")
    except Exception:
        message_index = 0

    message = await dchannel.send(embed=embeds[message_index])  # sends the first embed
    await message.add_reaction("⏮️")  # adds this ⏮️ emoji, which will indicate to go to the first embed
    await message.add_reaction("⬅️")  # adds this ⬅️ emoji, which will indicate the previous embed
    await message.add_reaction("➡️")  # adds this ➡️ emoji, which will indicate the next embed
    await message.add_reaction("⏭️")  # adds this ⏭️ emoji, which will indicate the last embed

    def check(reaction, user):
        return user == interaction.user and str(reaction.emoji) in ["⏮️", "⬅️", "➡️",
                                                                    "⏭️"] and reaction.message == message

    while True:
        try:
            reaction, user = await bot.wait_for("reaction_add", timeout=60, check=check)
            """
            keeps running until a reaction is sent within 60 seconds.
            the reaction is the emoji sent by the user which is user
            it then puts that into the check function respectively
            """
        except asyncio.TimeoutError:
            break  # breaks from while loop

        if str(reaction.emoji) == "⏭️":
            message_index = len(embeds) - 1  # goes to the very end of the messages
            await message.edit(embed=embeds[message_index])
        elif str(reaction.emoji) == "➡️" and message_index < len(embeds) - 1:  # if the reaction emoji is equal to the emoji, and if the message index is less than the length of the list
            message_index += 1
            await message.edit(embed=embeds[message_index])
        elif str(reaction.emoji) == "⬅️" and message_index > 0:
            message_index -= 1
            await message.edit(embed=embeds[message_index])
        elif str(reaction.emoji) == "⏮️":
            message_index = 0
            await message.edit(embed=embeds[message_index])
        await message.remove_reaction(reaction, user)


########################################################

message_queue = []
queue_start = None

interactions_for_send = set()

@bot.tree.command(name="send", description="sends message at given time or in 2 minutes")
async def send_message_queue(interaction: discord.Interaction, set_message: str, set_hour: int = None,
                             set_minute: int = None, set_second: int = None, interval: int = None):
    global queue_start, send_message_time, warning_time

    if interaction.id in interactions_for_send:
        return

    processed_interactions.add(interaction.id)
    message_queue.append(set_message)  # adds the message to the queue
    if queue_start is None:
        if interval is None or interval < 5:
            interval = 30  # in seconds, will set the delay interval of the queue to 30 as default

        queue_start = "1"
        send_message_time, warning_time = await target_time_getter(set_hour, set_minute, set_second, 3)
        print(send_message_time)
        print(warning_time)
        await interaction.response.send_message(content="Send message is starting!")
        await message_queue_function(target_time=send_message_time, warning_time=warning_time, interval=interval,
                                     interaction=interaction, set_message=set_message, queue_type=1)
    else:
        await interaction.response.send_message(
            content=f"Send message has already started! If you put a set message, it has been added to the queue! current queue: {message_queue}",
            ephemeral=True)
        # Edit the existing embed message to include the new message in the queue
        await message_queue_function(target_time=send_message_time, warning_time=warning_time, interval=interval,
                                     interaction=interaction, set_message=set_message, queue_type=2)
        return


async def message_queue_function(target_time, warning_time, interval, interaction, set_message, queue_type):
    global message_queue
    global send_message_embed
    global queue_start
    global message_stopper
    channel = interaction.channel
    if queue_type == 1:
        embed = await create_embed(bot_type="Send Message", targetTime=target_time, message=set_message,
                                   binary=1, bot_type2=3)
        send_message_embed = await channel.send(embed=embed)
        message_stopper = True
        while message_stopper:
            current_time = datetime.now().strftime("%H:%M:%S")
            if current_time == target_time:
                interval_stopper = 0
                for message in message_queue:  # runs until queue is empty
                    interval_stopper += 1
                    embed = await create_embed(bot_type="Send Message", targetTime=target_time,
                                                            message=set_message,
                                                            binary=2, bot_type2=3)
                    await send_message_embed.edit(embed=embed)
                    return_number = await send_message3(message=message)  # sends the message
                    embed = await create_embed(bot_type="Send Message", targetTime=target_time,
                                                            message=set_message,
                                                            binary=1, bot_type2=3)
                    await send_message_embed.edit(embed=embed)
                    if return_number == 201:  # fail number
                        embed = await create_embed(bot_type="Send Message", targetTime=target_time,
                                                                message=set_message,
                                                                binary=2, bot_type2=3)
                        await send_message_embed.edit(embed=embed)
                        message_stopper = False
                        break  # completely stops
                    await channel.send(content=f"\"{message}\" has been sent")
                    if interval_stopper < len(message_queue):  # if there's more than 1 message in the queue
                        await asyncio.sleep(interval)  # sleeps for interval before going back to it
                break  # breaks from the loop

            if current_time == warning_time:  # if it gets to warning time, set the embed to yellow
                message_embed = await create_embed(bot_type="Send Message", targetTime=target_time,
                                                   message=set_message,
                                                   binary=6, bot_type2=3)
                await send_message_embed.edit(embed=message_embed)
            await asyncio.sleep(1)

        if message_stopper is True:  # turns it green if it really ended
            message_embed = await create_embed(bot_type="Send Message", targetTime=target_time,
                                               message=set_message,
                                               binary=3, bot_type2=3)
            await send_message_embed.edit(embed=message_embed)
        else:
            message_embed = await create_embed(bot_type="Send Message", targetTime=target_time,
                                               message=set_message,
                                               binary=2, bot_type2=3)
            await send_message_embed.edit(embed=message_embed)

        message_queue = []  # resets queue
        queue_start = None  # finished queue
    elif queue_type == 2:
        message_embed = await create_embed(bot_type="Send Message", targetTime=target_time,
                                           message=set_message,
                                           binary=2, bot_type2=3)
        await send_message_embed.edit(embed=message_embed)
        await asyncio.sleep(0.1)
        embed = await create_embed(bot_type="Send Message", targetTime=target_time, message=set_message,
                                    binary=1, bot_type2=3)
        await send_message_embed.edit(embed=embed)


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
    await bot.start(TOKEN, reconnect=True)


# Start the Flask and Discord tasks
flask_task = loop.run_in_executor(None, run_flask)
discord_task = loop.create_task(run_discord())

# Wait for both tasks to complete (this will never happen since both tasks run forever)
loop.run_until_complete(asyncio.gather(discord_task))
loop.run_until_complete(asyncio.gather(discord_task))
