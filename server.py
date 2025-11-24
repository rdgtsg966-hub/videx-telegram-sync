from flask import Flask
import threading
import asyncio

from telegram_to_site import client

app = Flask(__name__)

@app.route("/")
def home():
    return "Listener ativo — aguardando novas mensagens do Telegram."

async def iniciar_telethon():
    await client.start()
    print("✔ Listener conectado ao Telegram!")
    await client.run_until_disconnected()

def thread_async():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(iniciar_telethon())

threading.Thread(target=thread_async, daemon=True).start()

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
