from flask import Flask
import threading, time, requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Videx Telegram Bot RUNNING!"

def keepalive():
    url = "https://SEU-SERVICO-RENDER.onrender.com"
    while True:
        try:
            requests.get(url)
        except:
            pass
        time.sleep(60)

if __name__ == "__main__":
    threading.Thread(target=keepalive).start()
    app.run(host="0.0.0.0", port=10000)
