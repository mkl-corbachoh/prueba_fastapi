from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# conexion a la base de datos
DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/fastapi_db"

# crear el motor de la base de datos
engine = create_engine(DATABASE_URL)

# crear sesion local, 
# autocomit: no se guarden los cambios automaticamente
# autoflush: no se guarden los cambios antes de hacer commit
# bind: enlazar el motor de la base de datos 
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# crear la clase base para los modelos
Base = declarative_base()