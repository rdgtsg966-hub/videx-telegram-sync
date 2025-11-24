from flask import Flask
import asyncio, threading
from telegram_to_site import client, sincronizar_100

app = Flask(__name__)
task_queue = asyncio.Queue()

@app.route("/")
def home():
    return "Videx Telegram Sync ativo!"

@app.route("/sync100")
def sync100():
    task_queue.put_nowait(("sync100",))
    return "➡ Sync100 iniciado"

async def task_worker():
    while True:
        t = await task_queue.get()
        if t[0]=="sync100":
            await sincronizar_100()
        task_queue.task_done()

async def async_setup():
    print("🔌 Iniciando sessão Telethon...")
    await client.start()
    print("✔ Telethon conectado!")
    asyncio.create_task(task_worker())

def start_loop():
    loop=asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_setup())
    loop.run_forever()

threading.Thread(target=start_loop, daemon=True).start()

if __name__ == "__main__":
    import os
    port=int(os.environ.get("PORT",5000))
    app.run(host="0.0.0.0", port=port)
