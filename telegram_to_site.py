from telethon import TelegramClient
import os

api_id = 34508499
api_hash = "0cc400409a89be0c4fdac9bdd68a8ea5"

GRUPO_ORIGEM = -2830928638

client = TelegramClient("sessao_videx", api_id, api_hash)

def salvar_no_site(filename, caption):
    outdir = "site_media"
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, filename + ".txt"), "w") as f:
        f.write(caption or "")

async def sincronizar_100():
    print("\n⏳ Buscando as últimas 100 mensagens...")
    count = 0
    async for msg in client.iter_messages(GRUPO_ORIGEM, limit=100):
        if not msg.media:
            continue
        caption = msg.text or ""
        if msg.video:
            filename = f"video_{msg.id}.mp4"
            await msg.download_media(file=os.path.join("site_media", filename))
            salvar_no_site(filename, caption)
            count += 1
        elif msg.photo:
            filename = f"foto_{msg.id}.jpg"
            await msg.download_media(file=os.path.join("site_media", filename))
            salvar_no_site(filename, caption)
            count += 1
    print(f"✔ Finalizado! {count} arquivos capturados.")
