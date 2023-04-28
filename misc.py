import asyncio
import tempfile
import threading
from datetime import datetime
import requests
from flask import Flask, send_file
import pyautogui
import time
from pynput.keyboard import Controller, Key

# 4/26/2023

app = Flask(__name__)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
keyboard = Controller()

@app.route('/screenshot', methods=['GET'])
def screenshot():
    pyautogui.moveTo(500, 1060, duration=0)
    pyautogui.click(500, 1060)

    time.sleep(1)

    # goes to WeChat and clicks it

    pyautogui.moveTo(700, 280, duration=0.5)  # serena is 700, 280. test is 600, 350
    pyautogui.click(700, 280)

    time.sleep(1)

    # get the app window and height

    wechat = pyautogui.getWindowsWithTitle('WeChat')[0]
    left, top, width, height = wechat.left, wechat.top, wechat.width, wechat.height
    screenshot = pyautogui.screenshot(region=(left, top, width, height))

    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        screenshot.save(f.name)
        filename = f.name

    pyautogui.moveTo(2, 2)
    pyautogui.click(2, 2)

    # clicks off

    return send_file(filename, mimetype='image/png'), 200

def handle_requests(stop_event):
    while not stop_event.is_set():
        response = requests.get('http://localhost:8080/stop_send_message')
        stop_checker = response.json().get('variable_name')
        if not stop_checker:
            stop_event.set()
        time.sleep(1)


@app.route('/send',methods = ['GET'])
def send_message():
    global set_message_time
    global set_message
    global handler

    response = requests.get('http://localhost:8080/get_send_message_time')
    set_message_time = response.json().get('variable_name')
    response = requests.get('http://localhost:8080/get_send_message')
    set_message = response.json().get('variable_name')

    handler = True
    stop_event = threading.Event()

    thread = threading.Thread(target=handle_requests, args=(stop_event,))
    thread.start()

    while handler:
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")

        if current_time == set_message_time:
            # send message code here
            handler = False
            stop_event.set()

    thread.join()
    return "success", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=42069)