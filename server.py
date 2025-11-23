from flask import Flask
import asyncio
import threading

from telegram_to_site import client, sincronizar_100

app = Flask(__name__)

# fila de tarefas
task_queue = asyncio.Queue()


@app.route("/")
def home():
    return "Videx Telegram Sync ativo!"


@app.route("/sync100")
def sync100():
    task_queue.put_nowait(("sync100",))
    return "✔ Iniciando sincronização das últimas 100 mensagens..."


async def task_worker():
    """Executa tarefas da fila dentro do loop principal."""
    while True:
        task = await task_queue.get()
        try:
            if task[0] == "sync100":
                print("➡ Executando /sync100...")
                await sincronizar_100()
                print("✔ /sync100 concluído!")
        except Exception as e:
            print(f"❌ Erro no worker: {e}")
        finally:
            task_queue.task_done()


async def async_setup():
    """Inicia Telethon + worker + listener."""
    print("🔌 Iniciando sessão Telethon...")

    # client.start() = conecta + autentica + habilita listeners
    await client.start()

    print("✔ Telethon iniciado!")

    # worker
    asyncio.create_task(task_worker())

    # MUITO IMPORTANTE: mantém o cliente vivo
    asyncio.create_task(client.run_until_disconnected())


def start_async_loop():
    """Loop async do Telethon rodando em thread separada."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_setup())
    loop.run_forever()


# inicia a thread do Telegram
threading.Thread(target=start_async_loop, daemon=True).start()


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
