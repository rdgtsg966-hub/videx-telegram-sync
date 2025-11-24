from telethon import TelegramClient, events
import os
import requests

api_id = 34508499
api_hash = "0cc400409a89be0c4fdac9bdd68a8ea5"
GRUPO_ORIGEM = -5089921462
WEBHOOK_SITE = "https://videx.space/receive.php"

client = TelegramClient("sessao_videx", api_id, api_hash)

def enviar_para_site(filepath, caption):
    try:
        with open(filepath, "rb") as f:
            requests.post(
                WEBHOOK_SITE,
                data={"caption": caption},
                files={"video": f},
                timeout=60
            )
        print("✔ Enviado para o site:", filepath)
    except Exception as e:
        print("❌ Falha ao enviar:", e)
    finally:
        try: os.remove(filepath)
        except: pass

async def processar(msg):
    if not msg.video: return
    caption = (msg.message or "").strip()
    if not caption: return
    print("🎥 Nova mídia detectada:", msg.id)
    filepath = await msg.download_media()
    if not filepath:
        print("❌ Erro ao baixar vídeo.")
        return
    enviar_para_site(filepath, caption)

@client.on(events.NewMessage(chats=GRUPO_ORIGEM))
async def handler(event):
    try:
        await processar(event.message)
    except Exception as e:
        print("❌ Erro no handler:", e)
