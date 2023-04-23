from flask import Flask
from datetime import datetime
import pyautogui
import time
from pynput.keyboard import Key, Controller
import requests
import asyncio
import threading

keyboard = Controller()


def WeChatTask(message):
    print(pyautogui.size())
    pyautogui.moveTo(420, 1060, duration=0)
    pyautogui.click(420, 1060)

    time.sleep(1)

    # goes to WeChat and clicks it

    pyautogui.moveTo(600, 280, duration=0.5)  # serena is 600, 280. test is 600, 350
    pyautogui.click(600, 280)

    time.sleep(1)

    # goes to serena's profile

    pyautogui.typewrite(message)

    # types the message

    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    # sends the message

    pyautogui.moveTo(2, 2)
    pyautogui.click(2, 2)

    # clicks off


app = Flask(__name__)

gm_stopper = True
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

run_handle_requests = True
def handle_requests():
    global gn_target_time
    global gn_message
    global gn_stopper
    global stop_num
    global run_handle_requests
    while run_handle_requests:
        response_time = requests.get('http://localhost:8080/get_gn_time')
        gn_target_time = response_time.json().get('variable_name')
        response_message = requests.get('http://localhost:8080/get_gn_message')
        gn_message = response_message.json().get('variable_name')
        response_stop = requests.get('http://localhost:8080/stop_gn')
        stop_num = response_stop.json().get('variable_name')
        if stop_num == 1:
            gn_stopper = False
            run_handle_requests = False
            break
        time.sleep(10)


@app.route('/gn', methods=['POST', 'GET'])
def run_script():
    global gn_stopper
    global gn_target_time
    global gn_message
    global stop_num
    global run_handle_requests
    gn_stopper = True
    response = requests.get('http://localhost:8080/get_gn_time')
    gn_target_time = response.json().get('variable_name')
    response = requests.get('http://localhost:8080/get_gn_message')
    gn_message = response.json().get('variable_name')
    thread = threading.Thread(target=handle_requests)
    thread.start()
    while gn_stopper:
        current_time = datetime.now().strftime("%H:%M:%S")
        try:
            if current_time == gn_target_time:
                # does the task
                WeChatTask(gn_message)
                # sends a success message to turn the embed green
                gn_stopper = False
                return "Script started successfully.", 200
            time.sleep(1)
        except Exception as e:
            return f"Error: {e}", 500

    # Set handle_requests flag to False
    run_handle_requests = False

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
    app.run(host='0.0.0.0', port=5001)
