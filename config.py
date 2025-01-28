import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

PREFIX = "!"
TOKEN = os.getenv("DISCORD_TOKEN")
BOT_OWNER_ID = os.getenv("BOT_OWNER_ID")
DEFAULT_VOLUME = int(os.getenv("DEFAULT_VOLUME", 70))  # Define um valor padrão caso não esteja no .env
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
