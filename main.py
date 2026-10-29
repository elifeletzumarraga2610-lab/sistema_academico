from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import models
import schemas
from database import engine, get_db

# Crear las tablas en la base de datos SQLite al iniciar
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Sistema Académico - API CRUD FastAPI",
    description="Deber de Base de Datos: CRUD con 3 tablas relacionadas y 20 registros iniciales.",
)

# ----------------------------------------------------
# CARGA AUTOMÁTICA DE 20 REGISTROS AL INICIAR LA API
# ----------------------------------------------------
@app.on_event("startup")
def cargar_datos_iniciales():
    db = next(get_db())
    if db.query(models.Usuario).count() == 0:
        # 1. Creación de Paralelos
        p1 = models.Paralelo(nombre="Paralelo A")
        p2 = models.Paralelo(nombre="Paralelo B")
        db.add_all([p1, p2])
        db.commit()

        # 2. Creación de Materias relacionadas con Paralelos
        m1 = models.Materia(nombre="Base de Datos I", paralelo_id=p1.id)
        m2 = models.Materia(nombre="Análisis Matemático II", paralelo_id=p2.id)
        db.add_all([m1, m2])
        db.commit()

        # 3. Lista de 20 Usuarios/Estudiantes
        usuarios_iniciales = [
            ("Carlos", "Pérez", "1720000001", m1.id),
            ("María", "Gómez", "1720000002", m1.id),
            ("Juan", "López", "1720000003", m2.id),
            ("Ana", "Torres", "1720000004", m2.id),
            ("Luis", "Ramírez", "1720000005", m1.id),
            ("Sofia", "Mendoza", "1720000006", m2.id),
            ("Diego", "Castillo", "1720000007", m1.id),
            ("Elena", "Flores", "1720000008", m2.id),
            ("Javier", "Morales", "1720000009", m1.id),
            ("Lucía", "Herrera", "1720000010", m2.id),
            ("Mateo", "Sánchez", "1720000011", m1.id),
            ("Camila", "Romero", "1720000012", m2.id),
            ("Gabriel", "Álvarez", "1720000013", m1.id),
            ("Valeria", "Díaz", "1720000014", m2.id),
            ("Daniel", "Espinoza", "1720000015", m1.id),
            ("Paula", "Benítez", "1720000016", m2.id),
            ("Andrés", "Cárdenas", "1720000017", m1.id),
            ("Sara", "Aguilar", "1720000018", m2.id),
            ("Fernando", "Paredes", "1720000019", m1.id),
            ("Andrea", "Molina", "1720000020", m2.id),
        ]

        for nombre, apellido, cedula, materia_id in usuarios_iniciales:
            db.add(
                models.Usuario(
                    nombre=nombre,
                    apellido=apellido,
                    cedula=cedula,
                    materia_id=materia_id,
                )
            )

        db.commit()


# ----------------------------------------------------
# RUTAS DEL CRUD COMPLETO (GET, POST, PUT, DELETE)
# ----------------------------------------------------

# READ ALL (GET) - Lista los 20 usuarios con su materia y paralelo
@app.get("/usuarios/", response_model=List[schemas.UsuarioResponse])
def listar_todos_los_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()


# READ ONE (GET) - Buscar un usuario específico por su ID
@app.get("/usuarios/{usuario_id}", response_model=schemas.UsuarioResponse)
def obtener_usuario_por_id(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


# CREATE (POST) - Crear un nuevo usuario
@app.post(
    "/usuarios/",
    response_model=schemas.UsuarioResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_nuevo_usuario(usuario: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    existe_cedula = (
        db.query(models.Usuario)
        .filter(models.Usuario.cedula == usuario.cedula)
        .first()
    )
    if existe_cedula:
        raise HTTPException(
            status_code=400, detail="La cédula ya se encuentra registrada."
        )

    nuevo_usuario = models.Usuario(**usuario.model_dump())
    db.add(nuevo_usuario)
    db.commit()
    db.refresh(nuevo_usuario)
    return nuevo_usuario


# UPDATE (PUT) - Actualizar información de un usuario
@app.put("/usuarios/{usuario_id}", response_model=schemas.UsuarioResponse)
def actualizar_usuario(
    usuario_id: int,
    datos: schemas.UsuarioCreate,
    db: Session = Depends(get_db),
):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    usuario.nombre = datos.nombre
    usuario.apellido = datos.apellido
    usuario.cedula = datos.cedula
    usuario.materia_id = datos.materia_id

    db.commit()
    db.refresh(usuario)
    return usuario


# DELETE (DELETE) - Eliminar un usuario
@app.delete("/usuarios/{usuario_id}")
def eliminar_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.query(models.Usuario).filter(models.Usuario.id == usuario_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    db.delete(usuario)
    db.commit()
    return {"mensaje": f"El usuario con ID {usuario_id} ha sido eliminado con éxito."}