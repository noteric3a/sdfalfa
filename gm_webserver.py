import asyncio
import threading
import time
from datetime import datetime
import logging
import pyautogui
import requests
from flask import Flask
from pynput.keyboard import Key, Controller

keyboard = Controller()

logging.basicConfig(filename='gm.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
def WeChatTask(message):
    print(pyautogui.size())
    pyautogui.moveTo(500, 1060, duration=0)
    pyautogui.click(500, 1060)

    # goes to WeChat and clicks it

    pyautogui.moveTo(700, 280, duration=0.5)  # serena is 600, 280. test is 600, 350
    pyautogui.click(700, 280)

    # goes to serena's profile

    pyautogui.typewrite(message)

    # types the message

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    # sends the message

    pyautogui.moveTo(2, 2)
    pyautogui.click(2, 2)

    # clicks off

def logger(event_name, event_details):
    logging.info(f"{event_name}: {event_details}")

app = Flask(__name__)

gm_stopper = True
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


@app.route('/gm', methods=['POST', 'GET'])
def run_script():
    global gm_stopper
    global gm_target_time
    global gm_message
    global run_handle_requests

    # Reset stopper and handle_requests flag to True
    gm_stopper = True
    run_handle_requests = True

    response = requests.get('http://localhost:8080/get_gm_time')
    gm_target_time = response.json().get('variable_name')

    response = requests.get('http://localhost:8080/get_gm_message')
    gm_message = response.json().get('variable_name')

    print("GM message: " + gm_message)

    try:
        logger("Current_time equals Target_time", "Success")
        # does the task
        WeChatTask(gm_message)
        logger("Task done", "Success")
        # sends a success message to turn the embed green
        gm_stopper = False
        run_handle_requests = False
        logger("Returning 200", "Success")
        return "script stopped", 200
    except Exception as e:
        print(e)
        return "Script stopped.", 201


@app.route('/stop_gm', methods=['GET'])
def stop_gm():
    global gm_stopper
    gm_stopper = False
    return "", 200


@app.route('/reroll_gm_message', methods=['GET'])
def reroll_gm_message():
    return "switched", 200


@app.route('/reroll_gm_time', methods=['GET'])
def reroll_gm_time():
    return "switched", 200


@app.route('/set_gm_message', methods=['GET'])
def set_gm_message():
    return "set", 200


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
