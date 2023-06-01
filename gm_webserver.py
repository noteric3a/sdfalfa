import asyncio
import logging
import pyautogui
import requests
from flask import Flask, jsonify
from pynput.keyboard import Key, Controller
from PIL import Image, ImageChops
import time
from datetime import datetime
import threading

pyautogui.FAILSAFE = False

instant_response_variable = True
stop_instant_response_variable = True
instant_response_time = ""

keyboard = Controller()

logging.basicConfig(filename='gm.log', level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')
def WeChatTask(message):
    print(pyautogui.size())
    pyautogui.click(510, 1060)

    # goes to WeChat and clicks it

    #    pyautogui.moveTo(700, 280, duration=0.5)  # serena is 600, 280. test is 600, 350
    #    pyautogui.click(700, 280)

    # goes to serena's profile

    pyautogui.typewrite(message)

    # types the message

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    # sends the message

    pyautogui.moveTo(100, 100)
    pyautogui.click(100, 100)

    # clicks off

def logger(event_name, event_details):
    logging.info(f"{event_name}: {event_details}")


def instant_response():
    global thread
    global instant_response_variable
    global instant_response_time
    global stop_instant_response_variable

    stop_instant_response_variable = True

    try:
        pyautogui.click(510, 1060)
        time.sleep(1)
        pyautogui.click(100,100)
        screenshot = pyautogui.screenshot(region=(497, 1040, 40, 40))
        screenshot.save('old.png')
        reference = Image.open('old.png')
    except Exception:
        pyautogui.moveTo(200, 200, duration=1)
        screenshot = pyautogui.screenshot(region=(497, 1040, 40, 40))
        screenshot.save('old.png')
        reference = Image.open('old.png')

    print("Waiting for GN to finish")

    while stop_instant_response_variable:
        current_time = datetime.now().strftime("%H:%M:%S")
        if current_time == "00:00:00":
            break

        time.sleep(1)

    print("Waiting until 4 AM")

    while stop_instant_response_variable:
        current_time = datetime.now().strftime("%H:%M:%S")
        if current_time == "04:00:00":  # instant response starts at 4 AM
            print("Instant response started")
            break

        try:
            screenshot = pyautogui.screenshot(region=(497, 1040, 40, 40))
            screenshot.save('new.png')
            new_reference = Image.open('new.png')
        except Exception:
            pyautogui.moveTo(200,200, duration = 1)
            screenshot = pyautogui.screenshot(region=(497, 1040, 40, 40))
            screenshot.save('new.png')
            new_reference = Image.open('new.png')

        diff = ImageChops.difference(reference, new_reference)

        if diff.getbbox() is None:
            time.sleep(1)
        else:
            try:
                time.sleep(1)

                pyautogui.click(510, 1060)

                # clicks on WeChat

                time.sleep(2)

                pyautogui.click(100,100)

                # Clicks off WeChat
            except Exception:
                pass

    response = requests.get('http://localhost:8080/get_gm_time')
    stop_time = response.json().get('variable_name')

    while stop_instant_response_variable:
        current_time = datetime.now().strftime("%H:%M:%S")

        if current_time == stop_time:  # doesnt auto respond if it is the gm target time
            break

        screenshot = pyautogui.screenshot(region=(497, 1040, 40, 40))
        screenshot.save('new.png')
        new_reference = Image.open('new.png')

        diff = ImageChops.difference(reference, new_reference)

        if diff.getbbox() is None:
            print("images are the same")

        else:
            response = requests.get('http://localhost:8080/get_gm_message')
            instant_gm_message = response.json().get('variable_name')
            print("serena responsed uh oh")
            instant_response_time = datetime.now().strftime("%H:%M:%S")
            instant_response_variable = False
            WeChatTask(instant_gm_message)
            break

        time.sleep(1)

    print("done")
    stop_instant_response_variable = True
    thread = None

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
    global instant_response_variable
    global instant_response_time

    # Reset stopper and handle_requests flag to True
    gm_stopper = True
    run_handle_requests = True

    if instant_response_variable:
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

    return f"{instant_response_time}", 205


@app.route('/stop_gm', methods=['GET'])
def stop_gm():
    global gm_stopper
    gm_stopper = False
    return "", 200

@app.route('/instant_response', methods = ['GET'])
def instant_response_started():
    global thread
    thread = threading.Thread(target=instant_response)
    thread.start()
    return "starting", 200


@app.route('/instant_response_time', methods = ['GET'])
def instant_response_time_get():
    return jsonify(variable_name=instant_response_time)

@app.route('/stop_instant_response', methods = ['GET'])
def stop_instant_response():
    global stop_instant_response_variable
    global thread
    stop_instant_response_variable = False
    thread = None
    return "stopped", 200


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
