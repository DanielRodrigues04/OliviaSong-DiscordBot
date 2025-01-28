import discord
from discord.ext import commands
import os
import config  # Importando o arquivo config.py

# Configuração do bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=config.PREFIX, intents=intents)

# Carrega cogs automaticamente
@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            try:
                await bot.load_extension(f'cogs.{filename[:-3]}')
                print(f'Cog {filename} carregado com sucesso!')
            except Exception as e:
                print(f'Erro ao carregar o cog {filename}: {e}')

bot.run(config.TOKEN)
