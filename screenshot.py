import tempfile
from flask import Flask, send_file
import pyautogui
import time

app = Flask(__name__)

@app.route('/screenshot', methods=['GET'])
def screenshot():
    pyautogui.moveTo(500, 1060, duration=0)
    pyautogui.click(500, 1060)
    
    time.sleep(1)

    # goes to WeChat and clicks it

    pyautogui.moveTo(700, 280, duration=0.5)  # serena is 670, 280. test is 600, 350
    pyautogui.click(700, 280)

    time.sleep(1)
    
    # get the app window and height
    
    wechat = pyautogui.getWindowsWithTitle('WeChat')[0]
    left, top, width, height = wechat.left, wechat.top, wechat.width, wechat.height
    screenshot = pyautogui.screenshot(region=(left,top,width,height))

    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
        screenshot.save(f.name)
        filename = f.name

    pyautogui.moveTo(2, 2)
    pyautogui.click(2, 2)

    # clicks off

    return send_file(filename, mimetype='image/png'), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=42069)
