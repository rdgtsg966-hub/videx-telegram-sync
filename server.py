from flask import Flask
import asyncio
import threading

from telegram_to_site import client, sincronizar_100

app = Flask(__name__)

task_queue = asyncio.Queue()

@app.route("/")
def home():
    return "Videx Telegram Sync ativo!"

@app.route("/sync100")
def sync100():
    task_queue.put_nowait(("sync100",))
    return "✔ Sincronização iniciada: buscando últimas 100 mensagens..."

async def task_worker():
    while True:
        task = await task_queue.get()
        if task[0] == "sync100":
            print("➡ Executando sincronização...")
            await sincronizar_100()
            print("✔ Sincronização concluída!")
        task_queue.task_done()

async def async_setup():
    # Conecta o cliente Telethon corretamente
    await client.connect()
    
    if not await client.is_user_authorized():
        print("❌ ERRO: sessão inválida. O arquivo .session não é aceito.")
    else:
        print("✔ Sessão Telethon conectada com sucesso!")

    # Inicia worker
    asyncio.create_task(task_worker())

def start_async_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_setup())
    loop.run_forever()

threading.Thread(target=start_async_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
