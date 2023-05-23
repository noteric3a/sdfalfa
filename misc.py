import asyncio
import tempfile
import requests
from flask import Flask, send_file
import pyautogui
from pynput.keyboard import Controller, Key


# 4/26/2023

app = Flask(__name__)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
keyboard = Controller()

@app.route('/screenshot', methods=['GET'])
def screenshot():
    try:
        pyautogui.click(510, 1060)

        # goes to WeChat and clicks it

        pyautogui.click(700, 280)

        # get the app window and height
    except pyautogui.FailSafeException:
        pyautogui.moveTo(500,500)
        pyautogui.click(510, 1060)

        # goes to WeChat and clicks it

        pyautogui.click(700, 280)

        # get the app window and height

    wechat = pyautogui.getWindowsWithTitle('WeChat')[0]
    left, top, width, height = wechat.left, wechat.top, wechat.width, wechat.height
    screenshot = pyautogui.screenshot(region=(left, top, width, height))

    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        screenshot.save(f.name)
        filename = f.name

    pyautogui.click(100, 100)

    # clicks off

    return send_file(filename, mimetype='image/png'), 200



@app.route('/send',methods = ['GET'])
def send_message():
    global set_message_time
    global set_message
    global handler

    response = requests.get('http://localhost:8080/get_send_message')
    set_message = response.json().get('variable_name')

    try:
        pyautogui.click(500, 1060)

        # goes to WeChat and clicks it
        # serena is 670, 280. test is 600, 350
        pyautogui.click(700, 280)

        # goes to serena's profile

        pyautogui.typewrite(set_message)

        # types the message

        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

        # sends the message

        pyautogui.click(100,100)

        # clicks off

        handler = False
        return "success", 200
    except Exception as e:
        print(e)
        return "not success", 201



if __name__ == '__main__':
    app.run(host='localhost', port=42069)
