from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from app.core.config import settings

# conexion a la base de datos
DATABASE_URL = settings.DATABASE_URL

# crear el motor de la base de datos
engine = create_engine(DATABASE_URL)

# crear sesion local, 
# autocomit: no se guarden los cambios automaticamente
# autoflush: no se guarden los cambios antes de hacer commit
# bind: enlazar el motor de la base de datos 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# crear la clase base para los modelos
Base = declarative_base()