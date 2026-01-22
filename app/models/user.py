from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from app.db.database import Base

class User(Base):
    __tablename__ = "users"  # Nombre de la tabla en la base de datos

    id = Column(
        Integer, primary_key=True, index=True
    )  # Crea indice unico en la base de datos
    username = Column(
        String, unique=True, index=True, nullable=False
    )  # Tipo de items unicas no nulas
    email = Column(
        String, unique=True, index=True, nullable=False
    )  # Tipo de items unicas no nulas
    hashed_password = Column(String, nullable=False)  # Tipo de items no nulas
    is_admin = Column(Boolean, default=False)  # Tipo de items con valor por defecto
