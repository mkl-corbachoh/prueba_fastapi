from app.models import user
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import JWTError
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.core.security import verify_access_token
from app.service.user import get_user_by_email
from app.models.user import User

# =========== DATABASE DEPENDENCIES ============
# Crea una nueva sesion para ejcutar operaciones en la base de datos que se cierra automaticamente despues de usarla
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ===== Dependencias de la aplicacion =====
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/auth/login"
)  # Crea el esquema OAuth2 con password (y flujo de "bearer")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    cred_exeptions = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},  # Indica que se usa el esquema Bearer
    )
    try:
        payload = verify_access_token(token)
        email: str = payload.get(
            "sub"
        )  # Extrae el email del token, el sub es el identificador del usuario
        if email is None:
            raise cred_exeptions
    except JWTError:
        raise cred_exeptions

    user = get_user_by_email(db, email=email)
    if user is None:
        raise cred_exeptions
    return user


def reqires_admin(current_user: User = Depends(get_current_user)):
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have enough permissions",
        )
    return current_user