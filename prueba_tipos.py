from typing import Optional, Dict, Any

def clean_price_string(raw_price: str) -> Optional[float]:
    """
    Recive un sting sucio como '$1,123.50 MXN' y devuelve un float 1123.50.
    Si el formato es invalido o está vació, devuelve None.
    """
    if not raw_price or not isinstance(raw_price, str):
        return None

    #Limpieza básica
    cleaned = raw_price.replace("$", "").replace(",", "").replace("MXN", "").strip()

    if cleaned == "":
        return None

    try:
        return float(cleaned)
    except ValueError:
        return None


def build_product_record(name: str, price: Optional[float], in_stock: bool) ->Dict[str, Any]:
    return {
        "product_name": name,
        "price": price,
        "is_available": in_stock
    }

if __name__ == "__main__":
    # Prueba1: Formato estándar
    precio_1 = clean_price_string("$2,899.99 MXN")
    producto_1 = build_product_record("RAM DDR 32GB", precio_1, True)

    # Prueba 2: Producto sin stock / texto no numérico
    precio_2 = clean_price_string("Agotado")
    producto_2 = build_product_record("SSD NVMe 1TB", precio_2, False)
    print("Producto 2:", producto_2)