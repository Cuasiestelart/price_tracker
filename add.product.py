from database import insert_product
from src.scraper import scrape_product, clean_url

DEFAULT_PRICE_SELECTOR = "span.a-offscreen"
DEFALUT_TITLE_SELECTOR = "#productTitle"

def register_new_product():
    print("=== REGISTRAR NUEVO PRODUCTO ===")
    raw_url = input("Ingresa la URL del producto de Amazon: ").strip()

    if not raw_url:
        print("URL no valida.")
        return

    #1. Limpiar la URL para evitar basura de rastreo
    clean_product_url = clean_url(raw_url)

    #2. Obtener el título y precio actual automáticamente con el scraper
    print("Obteniendo información del producto...")
    scraped_data = scrape_product(
        url=clean_product_url,
        price_selector=DEFAULT_PRICE_SELECTOR,
        title_selector=DEFALUT_TITLE_SELECTOR
    )

    if not scraped_data or not scraped_data.get("title"):
        print("No se puedo obtener la información automáticamente. Escribe un nombre manual")
        title = input("Nombre del producto: ").strip()
        current_price = 0.0
    else:
        title = scraped_data["title"]
        current_price = scraped_data["price"]
        print(f"\nProducto no encontrado {title}")
        print(f"Precio actal en tienda: ${current_price:,.2f}")

    #3. Pedir el precio meta
    target_input = input("\n¿Cuál es tu precio deseado / meta (MXN)?: ").strip()
    try:
        target_price = float(target_input.replace(",", ""))
    except ValueError:
        print("Precio inválido, asignado 0.0 por defecto.")

    #4. Guardar en la tabla 'products' de Supabase
    nuevo_registro = insert_product(
        name=title,
        url=clean_product_url,
        target_price=target_price
    )

    print(f"\n ¡Producto registrado con éxito en la base de datos! (ID:{nuevo_registro[0]['id']})")

if __name__ == "__main__":
    register_new_product()