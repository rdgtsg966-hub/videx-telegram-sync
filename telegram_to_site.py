from telethon import TelegramClient, events
import os
import requests

# CONFIG TELEGRAM
api_id = 34508499
api_hash = "0cc400409a89be0c4fdac9bdd68a8ea5"

# ID do grupo de origem (altere aqui se quiser mudar o grupo)
GRUPO_ORIGEM = -5089921462

# URL do seu site que recebe o vídeo + descrição
WEBHOOK_SITE = "https://videx.space/receive.php"

# Cliente Telethon usando a sessão já autenticada (sessao_videx.session)
client = TelegramClient("sessao_videx", api_id, api_hash)


def enviar_para_site(filepath: str, caption: str) -> None:
    """Envia o vídeo + legenda para o receive.php no seu site."""
    try:
        with open(filepath, "rb") as f:
            requests.post(
                WEBHOOK_SITE,
                data={"caption": caption},
                files={"video": f},
                timeout=60,
            )
        print(f"✔ Enviado para o site: {os.path.basename(filepath)}")
    except Exception as e:
        print(f"❌ Erro ao enviar para o site: {e}")
    finally:
        # apaga o arquivo local depois de enviar
        try:
            os.remove(filepath)
        except Exception:
            pass


async def processar_midia(msg) -> None:
    """Processa UMA mensagem: só envia se for VÍDEO e tiver legenda (caption)."""
    # apenas vídeos
    if not getattr(msg, "video", None):
        return

    # precisa ter legenda
    caption = (msg.message or "").strip()
    if not caption:
        return

    print(f"🎥 Novo vídeo com legenda detectado. ID mensagem: {msg.id}")

    # baixa o vídeo em arquivo temporário
    filepath = await msg.download_media()
    if not filepath:
        print("❌ Não foi possível baixar o vídeo.")
        return

    # envia para o site
    enviar_para_site(filepath, caption)


async def sincronizar_100():
    """Busca as últimas 100 mensagens do grupo e processa como se fossem novas."""
    print("\n⏳ Buscando as últimas 100 mensagens... (apenas vídeos COM legenda serão enviados)")
    count = 0

    async for msg in client.iter_messages(GRUPO_ORIGEM, limit=100):
        try:
            await processar_midia(msg)
            caption = (msg.message or "").strip()
            if getattr(msg, "video", None) and caption:
                count += 1
        except Exception as e:
            print(f"❌ Erro ao processar mensagem {msg.id}: {e}")

    print(f"✔ Finalizado! {count} vídeos com legenda enviados para o site.")


# LISTENER AUTOMÁTICO PARA NOVAS MENSAGENS
@client.on(events.NewMessage(chats=GRUPO_ORIGEM))
async def handler(event):
    try:
        await processar_midia(event.message)
    except Exception as e:
        print(f"❌ Erro no listener de nova mensagem: {e}")
