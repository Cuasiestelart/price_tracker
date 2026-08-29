import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urlunparse

HEADERS = {
    "User-Agent": (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, Like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
}

def clean_price(price_text: str) -> float:
    """Extrae unicamente los digitos y punts decimales de una cadena de texto."""
    #Elimina signos de moneda, comas de miles y espacios
    clean_str = re.sub(r"[^\d.]", "", price_text.replace(",", ""))
    return float(clean_str) if clean_str else 0.0

def fetch_page(url: str) -> BeautifulSoup | None:
    """Descarga el contenido HTML y devuelve el árbol parseado."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")
    except requests.RequestException as e:
        print(f"Error al obtener la URL {url}: {e}")
        return None

def clean_url(url: str) -> str:
    """Limpia URLs largas eliminando parámetros innecesarios."""
    #1. Si es amazon extrae únicamente la estructura
    amazon_match = re.search(r"(https:?://www\.amazon\.[a-z\.]+/)(?:[^/]+/)?dp/([A-Z0-9]{10})", url)
    if amazon_match:
        base_domain, asin = amazon_match.groups()
        return f"{base_domain}dp/{asin}"

    #2. Para otros urls, elimina query params
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))

def scrape_product(url: str, price_selector: str, title_selector: str = None) -> dict | None:
    """Descarga la pagina y extra el producto, titulo y precio."""
    cleaned_url = clean_url(url)

    soup = fetch_page(cleaned_url)
    if not soup:
        return None

    #1. Buscar etiqueta del precio
    price_element = soup.select_one(price_selector)
    if not price_element:
        print(f"No se encontró el precio con el selector: '{price_selector}'")
        return None

    extracted_price = clean_price(price_element.get_text())

    #2. Buscar titulo
    title = None
    if title_selector:
        title_element = soup.select_one(title_selector)
        if title_element:
            title = title_element.get_text().strip()

    return {
        "url": cleaned_url,
        "title": title,
        "price": extracted_price
    }

if __name__ == "__main__":
    # URL real de prueba
    test_url = "https://www.amazon.com.mx/Kingston-Beast-Black-Memoria-Capacidad/dp/B0DCGFCHXF/ref=sr_1_7?crid=36H47BECRN1P&dib=eyJ2IjoiMSJ9.4CJTwmJNjjhJA9-p7ftPpXbEDJR9spZXRUfSKWm5iQrFakT8cpXL--n5OhnJjG4KojY4nX9mUEeaP8TnhxXcQ-a47Ov053HN9AmJ30ytPdCzGjGVlA62uN-MV7htY0u0mS8YySfcMb9CNX3HmPMu_EcTxfGB0Bx1topxtxIVL4BtmbHvbiwpUxA3LEzvjRgteRZIxizOdavfOI5A7iArbDDf7XdVtN4x1dUE8dd_2MfgEtbxR62ye-pJWbKF_CiDzGBnnbV08NIw7iBdQajMlYTar-UQPSIdc32yg686IXM.yALSmz-ShQSAIUMhkbpcSxj1S6EJyV09f2fia1YI-Rs&dib_tag=se&keywords=memoria+ram+ddr5+16gb&qid=1787649110&sprefix=memoria+ram+ddr5+%2Caps%2C159&sr=8-3&ufe=app_do%3Aamzn1.fos.de93fa6a-174c-4df7-be7c-5bc8e9c5a71b"

    #Precio amazon
    resultado =  scrape_product(
        url=test_url,
        price_selector="span.a-offscreen",
        title_selector="#productTitle"
    )

    print("Resultado obtenido:", resultado)
