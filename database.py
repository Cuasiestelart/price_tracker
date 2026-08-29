from supabase_client import supabase

def get_all_products():
    """Obriene todos los productos activos a monitorear."""
    response = supabase.table("products").select("*").execute()
    return response.data
def insert_product(name: str, url: str, target_price: float):
    """"Inserta un nuevo producto a la lista del seguimiento."""
    data = {
        "name": name,
        "url": url,
        "target_price": target_price
    }
    response = supabase.table("products").insert(data).execute()
    return response.data

def log_price(product_id: int, price: float):
    """Guarda un nuevo registro en el historial de precios."""
    data = {
        "product_id": product_id,
        "price": price
    }
    response = supabase.table("price_history").insert(data).execute()
    return response.data
