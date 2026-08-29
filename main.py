import time
from database import get_all_products, log_price
from src.scraper import scrape_product

#selectores por defecto (de momento solo amazon)
DEFAULT_PRICE_SELECTOR = "span.a_offscreen"
DEFAULT_TITLE_SELECTOR = "#producTitle"

def track_all_products():
    """Recorre la lista de productos, raspa el precio actual y lo guarda en Supabase"""
    print("Iniciando ciclo de rastreo...")
    productos = get_all_products()

    if not productos:
        print("No hay productos registrados para rastrear")
        return

    for item in productos:
        prod_id = item["id"]
        prod_name = item.get("name")
        prod_url = item.get("url")
        target_price = float(item.get("target_price", 0.0))

        print(f"\nProcesando [{prod_id}]: {prod_name}")

        #1. Scraping en vivo
        scraped_data = scrape_product(
            url=prod_url,
            price_selector=DEFAULT_PRICE_SELECTOR,
            title_selector=DEFAULT_TITLE_SELECTOR
        )

        if not scraped_data or scraped_data.get("price") is None:
            print(f"No se pudo obtener el precio para el producto ID {prod_id}")
            continue

        current_price = scraped_data["price"]
        print(f"Precio actual: ${current_price:,.2f} | Meta: ${target_price:,.2f}")

        #2. REgistrar en historial de base de datos
        registro = log_price(product_id=prod_id, price=current_price)
        print(f"Historial actualizado con éxito (ID registro: {registro[0]['id']})")

        #3. Verificación de alerta
        if current_price <= target_price:
            print(f"  !OFERTA ALCANZADA¡ {prod_name} está a ${current_price:,.2f} (Meta: ${target_price:,.2f})")
        else:
            diferencia = current_price - target_price
            print(f"Aún falta bajar ${diferencia:,.2f} para alcanzar la meta.")

            time.sleep(2)

if __name__ == "__main__":
    track_all_products()