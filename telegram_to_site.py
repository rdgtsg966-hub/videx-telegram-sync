from telethon import TelegramClient, events
import os, requests

api_id = 34508499
api_hash = "0cc400409a89be0c4fdac9bdd68a8ea5"
GRUPO_ORIGEM = -5089921462
WEBHOOK_SITE = "https://videx.space/receive.php"

client = TelegramClient("sessao_videx", api_id, api_hash)

def enviar_para_site(filepath, caption):
    try:
        with open(filepath, "rb") as f:
            requests.post(WEBHOOK_SITE, data={"caption": caption}, files={"video": f}, timeout=60)
        print("✔ Enviado:", filepath)
    except Exception as e:
        print("❌ Erro:", e)
    finally:
        try: os.remove(filepath)
        except: pass

async def processar_midia(msg):
    if not getattr(msg, "video", None):
        return
    caption = (msg.message or "").strip()
    if not caption:
        return
    print(f"🎥 Vídeo com legenda: {msg.id}")
    filepath = await msg.download_media()
    if filepath:
        enviar_para_site(filepath, caption)

async def sincronizar_100():
    print("⏳ Sync 100...")
    count=0
    async for msg in client.iter_messages(GRUPO_ORIGEM, limit=100):
        if getattr(msg,"video",None) and (msg.message or "").strip():
            await processar_midia(msg)
            count+=1
    print("✔ Finalizado:", count)

@client.on(events.NewMessage(chats=GRUPO_ORIGEM))
async def handler(event):
    try:
        await processar_midia(event.message)
    except Exception as e:
        print("❌ Listener:", e)
