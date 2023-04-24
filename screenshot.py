import tempfile
from flask import Flask, send_file
import pyautogui

app = Flask(__name__)

@app.route('/screenshot', methods=['GET'])
def screenshot():
    # get the app window and height
    wechat = pyautogui.getWindowsWithTitle('WeChat')[0]
    left, top, width, height = wechat.left, wechat.top, wechat.width, wechat.height
    screenshot = pyautogui.screenshot(region=(left,top,width,height))

    with tempfile.NamedTemporaryFile(delete=False) as f:
        screenshot.save(f.name)
        filename = f.name

    return send_file(filename, mimetype='image/png'), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=42069)
