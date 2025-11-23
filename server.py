from flask import Flask
import asyncio
import threading

from telegram_to_site import client, sincronizar_100

app = Flask(__name__)

# FILA DE TAREFAS
task_queue = asyncio.Queue()

@app.route("/")
def home():
    return "Videx Telegram Sync ativo!"

@app.route("/sync100")
def sync100():
    # adiciona tarefa à fila
    task_queue.put_nowait(("sync100",))
    return "✔ Sincronização iniciada: buscando últimas 100 mensagens..."

async def task_worker():
    while True:
        task = await task_queue.get()
        if task[0] == "sync100":
            await sincronizar_100()
        task_queue.task_done()

def start_async_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # inicia o cliente Telethon
    loop.run_until_complete(client.start())

    # inicia o worker
    loop.create_task(task_worker())

    # roda eternamente
    loop.run_forever()

# inicia o loop async em thread separada
threading.Thread(target=start_async_loop, daemon=True).start()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
