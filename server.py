from flask import Flask
import asyncio
import threading

from telegram_to_site import client, sincronizar_100

app = Flask(__name__)

# fila de tarefas para rodar no loop principal
task_queue = asyncio.Queue()


@app.route("/")
def home():
    return "Videx Telegram Sync ativo! Use /sync100 para puxar as últimas 100 mensagens."


@app.route("/sync100")
def sync100():
    # adiciona tarefa à fila (será executada no loop async do Telethon)
    task_queue.put_nowait(("sync100",))
    return "✔ Sincronização iniciada: buscando últimas 100 mensagens (apenas vídeos com legenda)."


async def task_worker():
    """Worker que consome a fila e executa as tarefas no loop principal."""
    while True:
        task = await task_queue.get()
        try:
            if task[0] == "sync100":
                print("➡ Executando sincronização /sync100...")
                await sincronizar_100()
                print("✔ Sincronização /sync100 concluída!")
        except Exception as e:
            print(f"❌ Erro no worker: {e}")
        finally:
            task_queue.task_done()


async def async_setup():
    """Configura o cliente Telethon e inicia o worker + listener."""
    # conecta usando a sessão existente
    await client.connect()

    if not await client.is_user_authorized():
        print("❌ Sessão inválida. Verifique o arquivo sessao_videx.session.")
    else:
        print("✔ Sessão Telethon conectada com sucesso!")

    # inicia worker de tarefas
    asyncio.create_task(task_worker())


def start_async_loop():
    """Cria e mantém o loop async em uma thread separada."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(async_setup())
    loop.run_forever()


# inicia o loop assíncrono (Telethon + worker) em background
threading.Thread(target=start_async_loop, daemon=True).start()


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
