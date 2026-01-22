from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base


class Product(Base):
    __tablename__ = "products"  # Nombre de la tabla en la base de datos

    id = Column(
        Integer, primary_key=True, index=True
    )  # Crea indice unico en la base de datos
    name = Column(String, index=True, nullable=False)  # Tipo de items no nulas
    price = Column(Float, nullable=False)  # Tipo de items no nulas
    in_stock = Column(Boolean, default=True)  # Tipo de items con valor por defecto
    category_id = Column(
        Integer, ForeignKey("categories.id")
    )  # Clave foranea a la tabla categorias
    category = relationship(
        "Category", back_populates="products"
    )  # Relacion con categorias, back_populates para relacion bidireccional
