from database import Base, engine
from db_imports import *

Base.metadata.create_all(bind=engine) # Crear las tablas en la base de datos
print("Tablas creadas correctamente.")