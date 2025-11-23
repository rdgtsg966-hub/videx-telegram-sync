from flask import Flask
from telegram_to_site import client, sincronizar_100

app = Flask(__name__)

@app.route("/")
def home():
    return "Videx Telegram Sync ativo!"

@app.route("/sync100")
def sync100():
    client.loop.create_task(sincronizar_100())
    return "✔ Sincronização iniciada: buscando últimas 100 mensagens..."

if __name__ == "__main__":
    client.start()
    app.run(host="0.0.0.0", port=5000)
