import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}

def buscar_preco(url):
    try:
        resposta = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(resposta.text, "html.parser")

        # Seletor para o site books.toscrape.com
        preco_elemento = soup.select_one("p.price_color")

        if preco_elemento:
            preco_texto = preco_elemento.text.strip()
            # Remove símbolo £ e converte para float
            preco_texto = preco_texto.replace("£", "").replace("Â", "").strip()
            return float(preco_texto)
        else:
            return None

    except Exception as e:
        print(f"Erro ao buscar preço: {e}")
        return None