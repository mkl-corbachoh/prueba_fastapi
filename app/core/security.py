# Autentificacion con jwt
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta, UTC
from app.core.config import settings

# Configuraciones
SECRET_KEY = settings.SECRET_KEY  # varible secreta debe venir del entorno
ALGORITHM = settings.ALGORITHM  # Algoritmo de encriptacion
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES  # Tiempo de expiracion del token

# Configuracion de Passlib para hashear contraseñas
pwd_context = CryptContext(
    schemes=["bcrypt"], deprecated="auto"
)  # deprecated="auto" para manejar esquemas obsoletos

# Funcion para crear token de acceso
def create_access_token(sub: str, is_admin: bool):
    expire = datetime.now(UTC) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )  # Tiempo de expiracion
    data = {"sub": sub, "is_admin": is_admin, "exp": expire}
    encoded_jwt = jwt.encode(
        data, SECRET_KEY, algorithm=ALGORITHM
    )  # Codificar el token
    return encoded_jwt


# Funcion para verificar el token de acceso
def verify_access_token(token: str):
    try:
        payload = jwt.decode(
            token, SECRET_KEY, algorithms=[ALGORITHM]
        )  # Decodificar el token
        return payload  # Retornar el payload si es valido
    except JWTError:
        return None  # Retornar None si el token no es valido

# Funciones para hashear y verificar contraseñas
def hash_password(password: str) -> str:  # entra un str y sale un str
    """Hashea una contraseña"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash"""
    return pwd_context.verify(plain_password, hashed_password)