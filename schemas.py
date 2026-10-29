from pydantic import BaseModel
from typing import Optional


# --- ESQUEMAS PARA PARALELO ---
class ParaleloBase(BaseModel):
    nombre: str


class ParaleloCreate(ParaleloBase):
    pass


class ParaleloResponse(ParaleloBase):
    id: int

    class Config:
        from_attributes = True


# --- ESQUEMAS PARA MATERIA ---
class MateriaBase(BaseModel):
    nombre: str
    paralelo_id: int


class MateriaCreate(MateriaBase):
    pass


class MateriaResponse(MateriaBase):
    id: int
    paralelo_rel: Optional[ParaleloResponse] = None

    class Config:
        from_attributes = True


# --- ESQUEMAS PARA USUARIO ---
class UsuarioBase(BaseModel):
    nombre: str
    apellido: str
    cedula: str
    materia_id: int


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioResponse(UsuarioBase):
    id: int
    # Muestra automáticamente la Materia y el Paralelo asociados (JOIN)
    materia_rel: Optional[MateriaResponse] = None

    class Config:
        from_attributes = True