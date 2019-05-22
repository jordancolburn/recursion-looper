from flask import Flask
import OSC
app = Flask(__name__)

@app.route("/")
def flash():
    c = OSC.OSCClient()
    c.connect(('127.0.0.1', 7110))
    c.send( OSC.OSCMessage("/button/realtime_tap", [19] ) )
    return "Flashed LEDs"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
