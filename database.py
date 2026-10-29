from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Nombre del archivo de base de datos SQLite que se creará automáticamente
SQLALCHEMY_DATABASE_URL = "sqlite:///./sistema_academico.db"

# Crear el motor (Engine) para SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Crear la fábrica de sesiones de base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base de la cual heredarán todos los modelos ORM
Base = declarative_base()

# Función generadora para inyectar la sesión en los endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()