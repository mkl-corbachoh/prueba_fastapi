from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.database import Base


class Category(Base):
    __tablename__ = "categories"  # Nombre de la tabla en la base de datos

    id = Column(
        Integer, primary_key=True, index=True
    )  # Crea indice unico en la base de datos
    name = Column(
        String, unique=True, index=True, nullable=False
    )  # Tipo de items unicas no nulas
    products = relationship(
        "Product", back_populates="category"
    )  # Relacion con productos, back_populates para relacion bidireccional