import os
from dotenv import load_dotenv
# Cargar las variables desde el archivo .env
load_dotenv()

class Settings:
    def __init__(self) -> None:
        self.environment: str = os.getenv("ENVIRONMENT", "development")
        self.supabase_url: str = self._get_required_env("SUPABASE_URL")
        self.supabase_key: str = self._get_required_env("SUPABASE_KEY")
        self.check_interval: int = int(os.getenv("CHECK_INTERVAL_HOURS", "6"))

    def _get_required_env(self, key: str) -> str:
        value = os.getenv(key)
        if not value:
            raise ValueError(f"CRITICAL ERROR: Missing required environment variable '{key}' in .env file.")
        return value

    #Instancia global, lista pra usar en todo el proyecto
settings = Settings()

if __name__ == "__main__":
    print(f"Loaded environment: {settings.environment}")
    print(f"Supabase URL: {settings.supabase_url}")
    print(f"Check interval: {settings.check_interval} hours")

    
