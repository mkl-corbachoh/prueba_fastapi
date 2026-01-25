from pydantic_settings import BaseSettings # nos ayuda a crear una clase de confiuracion

class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL: str

    # version de pydantic 2.x, sustituye a la clase Config
    model_config = {
        "env_file": "app/.env", # archivo de entorno
        "env_file_encoding": "utf-8", # codificacion del archivo
    }

settings = Settings() # instancia de la clase Settings
