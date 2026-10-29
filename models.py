from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Paralelo(Base):
    __tablename__ = "paralelos"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)  # Ejemplo: 'Paralelo A'

    # Relación 1 a N: Un paralelo contiene muchas materias
    materias = relationship("Materia", back_populates="paralelo_rel")


class Materia(Base):
    __tablename__ = "materias"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)  # Ejemplo: 'Base de Datos I'
    
    # Llave Foránea hacia la tabla 'paralelos'
    paralelo_id = Column(Integer, ForeignKey("paralelos.id"))

    # Relaciones ORM
    paralelo_rel = relationship("Paralelo", back_populates="materias")
    usuarios = relationship("Usuario", back_populates="materia_rel")


class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    cedula = Column(String, unique=True, index=True, nullable=False)
    
    # Llave Foránea hacia la tabla 'materias'
    materia_id = Column(Integer, ForeignKey("materias.id"))

    # Relación ORM hacia Materia
    materia_rel = relationship("Materia", back_populates="usuarios")