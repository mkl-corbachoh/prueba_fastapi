from sqlalchemy import Column, Integer, String, Float, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Category(Base):
    __tablename__ = 'categories' # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, index=True) # Crea indice unico en la base de datos
    name = Column(String, unique=True, index=True, nullable=False) # Tipo de items unicas no nulas
    products = relationship("Product", back_populates="category") # Relacion con productos, back_populates para relacion bidireccional

class Product(Base):
    __tablename__ = 'products' # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, index=True) # Crea indice unico en la base de datos
    name = Column(String, index=True, nullable=False) # Tipo de items no nulas
    price = Column(Float, nullable=False) # Tipo de items no nulas
    in_stock = Column(Boolean, default=True) # Tipo de items con valor por defecto
    category_id = Column(Integer, ForeignKey('categories.id')) # Clave foranea a la tabla categorias
    category = relationship("Category", back_populates="products") # Relacion con categorias, back_populates para relacion bidireccional

class User(Base):
    __tablename__ = 'users' # Nombre de la tabla en la base de datos

    id = Column(Integer, primary_key=True, index=True) # Crea indice unico en la base de datos
    username = Column(String, unique=True, index=True, nullable=False) # Tipo de items unicas no nulas
    email = Column(String, unique=True, index=True, nullable=False) # Tipo de items unicas no nulas
    hashed_password = Column(String, nullable=False) # Tipo de items no nulas
    is_admin = Column(Boolean, default=False) # Tipo de items con valor por defecto