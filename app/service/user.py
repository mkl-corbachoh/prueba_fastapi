from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.schemas import  UserCreate

# ============ USUARIOS ============

def get_user_by_email(db: Session, email: str):
    """Obtiene un usuario por su email"""
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int):
    """Obtiene un usuario por su ID"""
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    """Crea un nuevo usuario"""
    from app.core.security import hash_password

    existing_user = get_user_by_email(db, user.email)
    if existing_user:
        raise ValueError("Email already registered")

    hashed_password = hash_password(user.password)
    db_user = User(
        username=user.username,
        email=user.email,
        is_admin=user.is_admin,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
