import asyncio
import io
from datetime import datetime
from random import randint
import aiohttp
import discord
from discord import File
from discord.ext import commands
from flask import jsonify, Flask

app = Flask(__name__)

gn_target_time = ""
gn_message = ""
gm_message = ""
gm_hour = None
gm_minute = None
gm_second = None
gm_stop_num = 0
gn_stop_num = 0
url = "https://discord.com/api/webhooks/1089023578277687386/4Uftkx4wUZyxieQTBIADV0eS5y4JmcFdfzCGZ_qhtVLPACXJNu0FdiMG6WgoPB1qI3sI"  # testing webhook


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
    rareGnMessages = ['gn my favorite NPC']

    chance = randint(0, 101)

    if chance > 99:
        index = randint(0, len(rareGnMessages) - 1)

        gnmessage = rareGnMessages[index]

    elif chance <= 99:
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

    if message.content.lower() == "stop gm":
        await message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://192.168.1.104:5000/stop_gm') as resp:
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
            async with session.get('http://192.168.1.104:5000/reroll_gm_message') as resp:
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
            async with session.get('http://192.168.1.104:5000/reroll_gm_time') as resp:
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
    if message.content.lower().split("&")[0] == "set gm":
        await message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://192.168.1.104:5000/set_gm_message') as resp:
                if resp.status == 200:
                    gm_message = message.content.lower().split("&")[1]
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
            async with session.get('http://192.168.1.104:5001/stop_gn') as resp:
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
            async with session.get('http://192.168.1.104:5001/reroll_gn_message') as resp:
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
            async with session.get('http://192.168.1.104:5001/reroll_gn_time') as resp:
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
    if message.content.lower().split("&")[0] == "set gn":
        await message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get('http://192.168.1.104:5001/set_gn_message') as resp:
                if resp.status == 200:
                    gm_message = message.content.lower().split("&")[1]
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


gm_running = False


@bot.tree.command(name="gm", description="gm bot")
async def gm(interaction: discord.Interaction, hour: int = None, minute: int = None,
             second: int = None):
    global embeded
    global gm_running
    global gm_hour
    global gm_minute
    global gm_second
    global gm_target_time
    global gm_message

    # Check if the command is already running
    if gm_running:
        await interaction.response.send_message("The GM bot is already running.")
        return
    else:
        await interaction.response.send_message("The GM bot has started!")

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
    embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message, binary=1, bot_type2=1)
    embeded = await channel.send(embed=embede)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://192.168.1.104:5000/gm') as resp:
                if resp.status == 200:

                    # Update the embed with a success message
                    makeCurrentDay(bot_type=1, days=current_days)
                    embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                                binary=3, bot_type2=1)
                    await embeded.edit(embed=embede)
                else:
                    # Update the embed with a failure message
                    embede = await create_embed(bot_type="GM bot", targetTime=gm_target_time, message=gm_message,
                                                binary=2, bot_type2=1)
                    await embeded.edit(embed=embede)

    except Exception as e:
        pass

    # Update the embed with the final message and set the flag to indicate that the command has finished running
    await embeded.edit(embed=embede)
    gm_running = False


gn_running = False


@bot.tree.command(name="gn", description="gn bot")
async def gn(interaction: discord.Interaction, hour: int = None, minute: int = None,
             second: int = None):
    global embeded2
    global gn_running
    global gn_hour
    global gn_minute
    global gn_second
    global gn_message
    global gn_target_time

    # Check if the command is already running
    if gn_running:
        await interaction.response.send_message("The GN bot is already running.")
        return
    else:
        await interaction.response.send_message("The GN bot has started!")

    # Set the flag to indicate that the command is running
    gn_running = True

    channel = interaction.channel
    gn_target_time = await target_time_getter(hour, minute, second, bot_type=2)

    time_list = gn_target_time.split(":")
    gn_hour = int(time_list[0])
    gn_minute = int(time_list[1])
    gn_second = int(time_list[2])

    if hour is None:
        gn_hour = None
    if minute is None:
        gn_minute = None
    if second is None:
        gn_second = None

    gn_message = GoodNightMessage()
    current_days = day(bot_type=2)

    # Create the initial embed
    embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message, binary=1, bot_type2=2)
    embeded2 = await channel.send(embed=embede)

    try:
        async with aiohttp.ClientSession() as session2:
            async with session2.get('http://192.168.1.104:5001/gn') as resp:
                if resp.status == 200:

                    # Update the embed with a success message
                    makeCurrentDay(bot_type=2, days=current_days)
                    embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                                binary=3, bot_type2=2)
                    await embeded2.edit(embed=embede)
                else:
                    # Update the embed with a failure message
                    embede = await create_embed(bot_type="GN bot", targetTime=gn_target_time, message=gn_message,
                                                binary=2, bot_type2=2)
                    await embeded2.edit(embed=embede)

    except Exception as e:
        pass

    # Update the embed with the final message and set the flag to indicate that the command has finished running
    await embeded2.edit(embed=embede)
    gn_running = False


@bot.tree.command(name="screenshot", description="takes a screenshot of wechat")
async def screenshot(interaction: discord.Interaction):
    await interaction.response.send_message(content="WeChat Screenshot.")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get('http://192.168.1.104:42069/screenshot') as resp:
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


loop = asyncio.get_event_loop()


def run_flask():
    app.run(host='localhost', port=8080)


async def run_discord():
    await bot.start('MTA5ODc3MTgwMDc2ODM4OTE2MA.GmJTCy.BwmaWa-45FHejlQ34MsMYi6ctcD_KHTHubT-_Q', reconnect=True)


# Start the Flask and Discord tasks
flask_task = loop.run_in_executor(None, run_flask)
discord_task = loop.create_task(run_discord())

# Wait for both tasks to complete (this will never happen since both tasks run forever)
loop.run_until_complete(asyncio.gather(discord_task))
loop.run_until_complete(asyncio.gather(discord_task))
