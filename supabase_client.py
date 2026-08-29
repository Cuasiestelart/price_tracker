from supabase import create_client, Client
from config.settings import settings

def get_supabase_client() -> Client:
    """ Crea y devuelve la instancia del cliente del clirente de Supabase usando settings."""
    return create_client(settings.supabase_url, settings.supabase_key)

#Instancia global exportable para operaciones en la base de datos
supabase: Client = get_supabase_client()

if __name__ == "__main__":
    print("Conexión inicializada con éxito", supabase)