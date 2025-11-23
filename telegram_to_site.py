from telethon import TelegramClient, events
import requests
import os

# CONFIGS
api_id = 34508499
api_hash = "0cc400409a89be0c4fdac9bdd68a8ea5"
telefone = "+5519998055114"

grupo_origem = -5089921462
webhook_site = "https://videx.space/receive.php"

client = TelegramClient("sessao_videx", api_id, api_hash)

@client.on(events.NewMessage(chats=grupo_origem))
async def handler(event):
    caption = event.message.message or ""
    if event.message.video:
        caminho = await event.message.download_media()
        with open(caminho, "rb") as f:
            requests.post(webhook_site, data={"caption": caption}, files={"video": f})
        os.remove(caminho)

client.start(phone=telefone)
client.run_until_disconnected()
