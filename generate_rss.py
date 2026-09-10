import requests
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import os

urls = [
    "https://infocatolica.com/?t=autores&a=Mons.+Athanasius+Schneider",
    "https://infocatolica.com/?t=autores&a=Cardenal+Gerhard+M%FCller",
    "https://infocatolica.com/?t=autores&a=Cardenal+Robert+Sarah",
    "https://infocatolica.com/?t=autores&a=Cardenal+Raymond+Leo+Burke",
    "https://www.infocatolica.com/?t=autores&a=Monse%F1or+H%E9ctor+Aguer"
]

fg = FeedGenerator()
fg.title("RSS Infocatolica Cardenales")
fg.link(href="https://www.infocatolica.com")
fg.description("Feed generado automáticamente con GitHub Actions")

print("Iniciando scrap de URLs...")

total_entries = 0

for url in urls:
    print(f"Leyendo {url}")
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"Error al leer {url}: {e}")
        continue

    soup = BeautifulSoup(r.content, "html.parser")
    articles = soup.select("h2 a")[:5]  # primeros 5 titulares
    if not articles:
        print(f"No se encontraron titulares en {url}")
        continue

    for a in articles:
        title = a.get_text(strip=True)
        link = a.get("href")
        if title and link:
            fe = fg.add_entry()
            fe.title(title)
            fe.link(href=link)
            total_entries += 1

rss_file_path = "rss.xml"

# Generar rss.xml aunque no haya entradas
fg.rss_file(rss_file_path)
print(f"RSS generado en {rss_file_path} con {total_entries} entradas")

if os.path.exists(rss_file_path):
    print("rss.xml existe y está listo para commit")
else:
    print("Error: rss.xml no se creó")
