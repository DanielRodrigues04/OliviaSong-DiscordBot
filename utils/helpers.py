# utils/helpers.py

def format_duration(seconds):
    """Formata a duração de segundos para o formato mm:ss."""
    minutes, seconds = divmod(seconds, 60)
    return f"{minutes}:{seconds:02}"

def shorten_text(text, length=50):
    """Encurta um texto se ele for maior que 'length' caracteres."""
    return text if len(text) <= length else text[:length] + "..."

def is_url(string):
    """Verifica se uma string é uma URL válida."""
    return string.startswith(("http://", "https://"))

def escape_markdown(text):
    """Escapa caracteres especiais do Discord Markdown."""
    special_chars = ["*", "_", "~", "`", "|"]
    for char in special_chars:
        text = text.replace(char, f"\\{char}")
    return text
