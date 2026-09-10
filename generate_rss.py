from datetime import datetime, timedelta, timezone
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from feedgen.feed import FeedGenerator
import os
import requests

urls = [
    "https://infocatolica.com/?t=autores&a=Mons.+Athanasius+Schneider",
    "https://infocatolica.com/?t=autores&a=Cardenal+Gerhard+M%FCller",
    "https://infocatolica.com/?t=autores&a=Cardenal+Robert+Sarah",
    "https://infocatolica.com/?t=autores&a=Cardenal+Raymond+Leo+Burke",
    "https://www.infocatolica.com/?t=autores&a=Monse%F1or+H%E9ctor+Aguer",
]

headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

fg = FeedGenerator()
fg.title("RSS Infocatolica - Autores Específicos")
fg.link(href="https://www.infocatolica.com", rel="alternate")
fg.description(
    "Feed personalizado de autores específicos generado con GitHub Actions"
)
fg.language("es")

print("Iniciando scrap de URLs...")
total_entries = 0
# Tomamos la hora actual exacta en UTC asegurando que sea un tiempo pasado válido
base_time = datetime.now(timezone.utc)

for url in urls:
  print(f"Leyendo {url}")
  try:
    r = requests.get(url, headers=headers, timeout=10)
    r.raise_for_status()
  except requests.RequestException as e:
    print(f"Error al leer {url}: {e}")
    continue

  soup = BeautifulSoup(r.content, "html.parser")
  articles = soup.select("h2 a, h3 a")[:5]

  if not articles:
    print(f"No se encontraron titulares en {url}")
    continue

  for a in articles:
    title = a.get_text(strip=True)
    link = a.get("href")
    if title and link:
      absolute_link = urljoin("https://infocatolica.com", link)

      fe = fg.add_entry()
      fe.title(title)
      fe.link(href=absolute_link)
      fe.description(f"Artículo escrito en InfoCatólica: {title}")
      fe.guid(absolute_link, permalink=True)

      # Asignamos una fecha real en el pasado reciente (restando horas/minutos acumulados)
      article_time = base_time - timedelta(hours=1, minutes=total_entries * 10)
      fe.pubDate(article_time)

      total_entries += 1

rss_file_path = "rss.xml"
fg.rss_file(rss_file_path, encoding="UTF-8")
print(f"RSS generado en {rss_file_path} con {total_entries} entradas")

if os.path.exists(rss_file_path):
  print("rss.xml existe y está listo para commit")
else:
  print("Error: rss.xml no se creó")
