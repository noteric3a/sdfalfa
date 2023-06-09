import logging
from flask import Flask
import pyautogui
from pynput.keyboard import Key, Controller
import requests
import asyncio

keyboard = Controller()

pyautogui.FAILSAFE = False

logging.basicConfig(filename='gn.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

def logger(event_name, event_details):
    logging.info(f"{event_name}: {event_details}")
def WeChatTask(message):
    print(pyautogui.size())
    pyautogui.click(510, 1060)

    # goes to WeChat and clicks it
    # serena is 600, 280. test is 600, 350
    # pyautogui.click(700, 280)

    # goes to serena's profile

    pyautogui.typewrite(message)

    # types the message

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    # sends the message

    pyautogui.click(100, 100)

    # clicks off


app = Flask(__name__)

gm_stopper = True
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


@app.route('/gn', methods=['POST', 'GET'])
def run_script():
    global gn_stopper
    global gn_target_time
    global gn_message
    global stop_num
    response = requests.get('http://localhost:8080/get_gn_time')
    gn_target_time = response.json().get('variable_name')
    response = requests.get('http://localhost:8080/get_gn_message')
    gn_message = response.json().get('variable_name')
    print("Gn message: " + gn_message)
    try:
        logger("Current_time equals Target_time", "Success")
        # does the task
        WeChatTask(gn_message)
        logger("Task done", "Success")
        # sends a success message to turn the embed green
        logger("Returning 200", "Success")
        return "Script stopped successfully.", 200
    except Exception as e:
        logger("Task failed", "uh oh spagettio: 201")
        print(e)
        return "Script stopped.", 201


@app.route('/stop_gn', methods=['GET'])
def stop_gn():
    global gn_stopper
    gn_stopper = False
    return "", 200


@app.route('/reroll_gn_message', methods=['GET'])
def reroll_gn_message():
    return "switched", 200


@app.route('/reroll_gn_time', methods=['GET'])
def reroll_gn_time():
    return "switched", 200


@app.route('/set_gn_message', methods=['GET'])
def set_gn_message():
    return "set", 200


if __name__ == '__main__':
    app.run(host='localhost', port=5001)
