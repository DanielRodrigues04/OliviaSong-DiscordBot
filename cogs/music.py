import discord
from discord.ext import commands
import yt_dlp as youtube_dl
from asyncio import Queue
import os
import subprocess
import asyncio
import shutil

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_clients = {}
        self.queue = Queue()

    async def play_next(self, ctx):
        if not self.queue.empty():
            song = await self.queue.get()
            await self.play_song(ctx, song)
        else:
            await ctx.send("Não há mais músicas na fila.")
            await ctx.voice_client.disconnect()

    async def convert_audio(self, video_file, mp3_file):
        """Converte o arquivo de vídeo MP4 para MP3 de maneira assíncrona."""
        process = await asyncio.create_subprocess_exec(
            r"C:\ffmpeg\ffmpeg.exe", '-i', video_file, '-vn', '-acodec', 'libmp3lame', '-ar', '44100', '-ac', '2', mp3_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            raise Exception(f"Erro ao converter o arquivo para MP3: {stderr.decode()}")
        return mp3_file

    async def play_song(self, ctx, song):
        voice_client = ctx.voice_client
        if voice_client.is_playing():
            voice_client.stop()

        # Caminho do ffmpeg
        ffmpeg_path = r"C:\ffmpeg\ffmpeg.exe"
        
        # Usar yt-dlp para baixar o áudio temporariamente
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',
            'noplaylist': True,  # Não fazer download de playlists
            'quiet': True,  # Para não mostrar logs excessivos
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(song['url'], download=True)  # Download do áudio
                video_file = f"downloads/{info['id']}.mp4"  # Ajuste para o formato de vídeo baixado

            print(f"Arquivo de vídeo baixado: {video_file}")  # Log para verificar se o arquivo foi baixado corretamente

            if not os.path.exists(video_file):
                await ctx.send(f"Erro ao baixar o vídeo: {video_file}")
                return

            # Converter o arquivo MP4 para MP3
            mp3_file = f"downloads/{info['id']}.mp3"
            mp3_file = await self.convert_audio(video_file, mp3_file)

            # Verificar se o arquivo MP3 foi gerado corretamente
            if not os.path.exists(mp3_file):
                await ctx.send(f"Erro ao converter o arquivo para MP3: {mp3_file}")
                return

            # Usar ffmpeg para tocar o áudio convertido
            voice_client.play(
                discord.FFmpegPCMAudio(mp3_file, executable=ffmpeg_path),
                after=lambda e: self.bot.loop.create_task(self.play_next(ctx))
            )
            await ctx.send(f"Tocando: {song['title']}")

            # Agendar a exclusão do arquivo após a reprodução da música
            await self.wait_for_audio_to_finish(voice_client, mp3_file, video_file)

        except Exception as e:
            await ctx.send(f"Erro ao tentar baixar a música: {str(e)}")
            print(f"Erro completo: {e}")  # Log completo do erro para depuração

    async def wait_for_audio_to_finish(self, voice_client, mp3_file, video_file):
        """Aguarda a reprodução da música e limpa os arquivos temporários após a reprodução."""
        while voice_client.is_playing():
            await asyncio.sleep(1)  # Aguarda a música terminar

        # Remover os arquivos temporários após a reprodução
        os.remove(mp3_file)
        os.remove(video_file)

        # Limpar todos os arquivos temporários na pasta 'downloads'
        self.clear_temp_files()

    def clear_temp_files(self):
        """Limpa a pasta 'downloads' removendo todos os arquivos temporários."""
        folder = 'downloads'
        try:
            for filename in os.listdir(folder):
                file_path = os.path.join(folder, filename)
                if os.path.isfile(file_path):
                    os.remove(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove diretórios e seu conteúdo
            print("Pasta 'downloads' limpa com sucesso.")
        except Exception as e:
            print(f"Erro ao tentar limpar a pasta de arquivos temporários: {e}")

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
        else:
            await ctx.send("Você precisa estar em um canal de voz!")

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client:
            await ctx.voice_client.disconnect()
        else:
            await ctx.send("Não estou em um canal de voz!")

    @commands.command()
    async def play(self, ctx, url: str):
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'downloads/%(id)s.%(ext)s',  # Define onde o áudio será salvo
        }

        try:
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                # Verificar o formato de áudio
                formats = info.get('formats', [])
                song = None
                for f in formats:
                    if f.get('acodec') != 'none':
                        song = {
                            'title': info['title'],
                            'url': f['url']  # URL do áudio
                        }
                        break

            if not song:
                await ctx.send("Não foi possível encontrar o áudio.")
                return

            if ctx.voice_client is None:
                if ctx.author.voice:
                    channel = ctx.author.voice.channel
                    await channel.connect()
                else:
                    await ctx.send("Você precisa estar em um canal de voz!")
                    return

            if ctx.voice_client.is_playing():
                await self.queue.put(song)
                await ctx.send(f"Adicionado à fila: {song['title']}")
            else:
                await self.play_song(ctx, song)

        except Exception as e:
            await ctx.send(f"Erro ao tentar processar a música: {str(e)}")
            print(f"Erro completo: {e}")

    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("Música pausada.")
        else:
            await ctx.send("Nenhuma música está tocando.")

    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("Música retomada.")
        else:
            await ctx.send("Nenhuma música está pausada.")

    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client:
             # Para a música
            ctx.voice_client.stop()
            await ctx.send("Música parada.")
        
            # Limpar arquivos temporários após parar a música
            await self.clear_temp_files()
        else:
            await ctx.send("Não estou tocando música.")

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client and ctx.voice_client.is_playing():
            # Para a música
            ctx.voice_client.stop()
            await ctx.send("Música pulada.")

            # Limpar arquivos temporários após pular a música
            await self.clear_temp_files()

            # Reproduzir a próxima música na fila
            await self.play_next(ctx)
        else:
            await ctx.send("Não estou tocando música.")


    @commands.command()
    async def queue(self, ctx):
        if self.queue.empty():
            await ctx.send("A fila está vazia.")
        else:
            song_list = "\n".join([song['title'] for song in list(self.queue._queue)])
            await ctx.send(f"Músicas na fila:\n{song_list}")

    @commands.command()
    async def clear_queue(self, ctx):
        self.queue = Queue()  # Limpar a fila
        await ctx.send("Fila limpa.")

async def setup(bot):
    await bot.add_cog(Music(bot))
