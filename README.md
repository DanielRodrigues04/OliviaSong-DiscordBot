
# Bot de Música para Discord

Este é um bot de música para Discord que permite tocar músicas a partir de links do YouTube, com comandos para controlar a reprodução como pausar, pular, adicionar músicas à fila e muito mais.

## Requisitos

1. Python 3.8 ou superior.
2. Dependências do Python: `discord.py`, `yt-dlp` e `ffmpeg`.
3. Conta no Discord e criação de um bot no [Discord Developer Portal](https://discord.com/developers/applications).
4. `ffmpeg` instalado e configurado no PATH.

## Instalação

### 1. Clone o repositório ou baixe o código:
   ```bash
   git clone https://github.com/seu-usuario/bot-musica-discord.git
   ```

### 2. Crie um ambiente virtual e ative-o:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Para Linux/macOS
   venv\Scripts\activate     # Para Windows
   ```

### 3. Instale as dependências necessárias:
   ```bash
   pip install -r requirements.txt
   ```

### 4. Instale o `ffmpeg` e adicione ao PATH (se ainda não tiver feito isso). Você pode baixar o `ffmpeg` [aqui](https://ffmpeg.org/download.html).

### 5. Crie um bot no [Discord Developer Portal](https://discord.com/developers/applications) e copie o token de autenticação.

### 6. Adicione o token do bot ao seu arquivo de configuração (por exemplo, `config.json` ou diretamente no código).

### 7. Inicie o bot:
   ```bash
   python bot.py
   ```

## Comandos

Aqui estão os principais comandos que o bot oferece:

### `!join`
O bot se conecta ao canal de voz onde o usuário está.

### `!leave`
O bot sai do canal de voz.

### `!play <url>`
Reproduz a música do link fornecido (do YouTube). O bot vai baixar o áudio e tocar no canal de voz.

### `!pause`
Pausa a música que está sendo tocada.

### `!resume`
Retoma a música que foi pausada.

### `!stop`
Para a música e desconecta o bot do canal de voz.

### `!skip`
Pula a música atual e começa a tocar a próxima na fila.

### `!queue`
Exibe as músicas que estão na fila para reprodução.

### `!clear_queue`
Limpa a fila de músicas.

## Limpeza de Arquivos Temporários

Após cada música, o bot remove os arquivos temporários MP3 e MP4 baixados do YouTube, garantindo que a pasta `downloads` não acumule arquivos desnecessários.

## Contribuição

Sinta-se à vontade para fazer melhorias ou adicionar novos recursos. Se você encontrar algum bug ou tiver sugestões de melhorias, abra uma issue ou envie um pull request.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## Agradecimentos

- `discord.py`: Biblioteca principal para interação com a API do Discord.
- `yt-dlp`: Biblioteca para baixar vídeos do YouTube.
- `ffmpeg`: Ferramenta de código aberto para processamento de áudio e vídeo.



## Desenvolvedor Responsavel
- Daniel Rodrigues