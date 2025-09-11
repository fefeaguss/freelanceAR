from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile, File
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import os
import shutil
import logging
import uuid

from routes.usuario_servicio import desasociar_usuario_servicio

from models.models import Base, SessionLocal, engine, ImagenesServicios, Servicios, Usuarios_Servicios
from providers.consultas import ServiciosConsulta, UsuariosServiciosConsulta
from schemas.shemas import servicio, servicioModificacion

logger = logging.getLogger(f'{__name__}')

UPLOAD_DIR = "uploads/"  # Directorio donde se guardan las imágenes
os.makedirs(UPLOAD_DIR, exist_ok=True)  # Crea la carpeta si no existe

try:
    Base.metadata.create_all(bind=engine)
except Exception as err:
    logger.error(err)
    
def get_db():
    try:
        db = SessionLocal()
        yield db
    except Exception as error:
        logger.error(error)
    finally:
        db.close()


router = APIRouter(prefix="/servicios", tags=["Servicios"])


@router.get("/")
async def listar_servicio(id: Optional[str] = None, db: Session = Depends(get_db)):
    consulta_servicio = ServiciosConsulta(db)
    if not id:
        try:
            res = consulta_servicio.obtener_todos(db)
        except Exception as error:
            logger.exception("Error inesperado")
            raise HTTPException(status_code=500, detail={"estado": "error durante la consulta"})

        lista_res = []
        if not res:
            return JSONResponse(content=[{}], status_code=200)

        for res_servicio in res:
            imagenes = db.query(ImagenesServicios).filter(ImagenesServicios.id_servicio == res_servicio.id_servicio).all()
            lista_res.append({
                "id": res_servicio.id_servicio,
                "nombre": res_servicio.nombre_servicio,
                "descripcion": res_servicio.descripcion_servicio,
                "precio": float(res_servicio.precio),
                "categoria": res_servicio.categoria.nombre_categoria,
                "imagenes": [{"id": img.id_imagen, "url": img.url_imagen} for img in imagenes]
            })
        return JSONResponse(content=lista_res, status_code=200)

    res_servicio = consulta_servicio.obtener_uno(db, id)
    imagenes = db.query(ImagenesServicios).filter(ImagenesServicios.id_servicio == res_servicio.id_servicio).all()
    return JSONResponse(
        content={
            "id": res_servicio.id_servicio,
            "nombre": res_servicio.nombre_servicio,
            "descripcion": res_servicio.descripcion_servicio,
            "precio": float(res_servicio.precio),
            "categoria": res_servicio.id_categoria.nombre_categoria,
            "imagenes": [{"id": img.id_imagen, "url": img.url_imagen} for img in imagenes]
        },
        status_code=200
    )


@router.post("/", status_code=201)
async def cargar_servicio(
    nombre_servicio: str = Form(...),
    descripcion_servicio: str = Form(...),
    precio: float = Form(...),
    id_usuario: str = Form(...),
    id_categoria: int = Form(...),
    imagenes: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    try:
        consulta_servicio = ServiciosConsulta(db)
        nuevo_servicio = await consulta_servicio.crear_servicio(  # 🔹 Se añade 'await' aquí
            db, nombre_servicio, descripcion_servicio, precio, id_categoria
        )

        consulta_usuarios_servicios = UsuariosServiciosConsulta(db)
        consulta_usuarios_servicios.asociar_usuario_servicio(db, id_usuario, nuevo_servicio.id_servicio)

        urls = []
        for imagen in imagenes:
            filename = f"{uuid.uuid4()}_{imagen.filename.replace(' ', '_')}"
            file_path = os.path.join(UPLOAD_DIR, filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(imagen.file, buffer)

            nueva_imagen = ImagenesServicios(id_servicio=nuevo_servicio.id_servicio, url_imagen=file_path)
            db.add(nueva_imagen)
            urls.append(file_path)

        db.commit()

    except Exception as error:
        logger.exception("Error inesperado")
        raise HTTPException(status_code=400, detail={"estado": "error durante consulta"})

    return JSONResponse(content={"estado": "servicio creado y usuario asociado con imágenes", "imagenes": urls}, status_code=201)



@router.put("/{id_servicio}")
async def modificar_servicio(id_servicio: str, ob_servicio: servicioModificacion = None, db: Session = Depends(get_db)):
    if not id_servicio:
        raise HTTPException(detail={"estado": "falta parametro id"})
    try:
        consulta_servicio = ServiciosConsulta(db)
        res_modificacion = consulta_servicio.modificar_servicio(db, id_servicio, ob_servicio)
    except Exception as error:
        logger.exception("Error inesperado")
        raise HTTPException(status_code=500, detail={"estado": "error durante consulta"})
    
    return JSONResponse(content={"resultado": {
        "id_servicio": res_modificacion.id_servicio,
        "servicio": res_modificacion.nombre_servicio,
        "descripcion": res_modificacion.descripcion_servicio,
        "precio": float(res_modificacion.precio),
        "categoria": res_modificacion.categoria.nombre_categoria
    }})


@router.delete("/{id_servicio}", status_code=200)
async def eliminar_servicio(id_servicio: str, db: Session = Depends(get_db)):
    try:
        consulta_servicio = ServiciosConsulta(db)
        consulta_usuarios_servicios = UsuariosServiciosConsulta(db)

        # Verifica si el servicio existe
        servicio = consulta_servicio.obtener_uno(db, id_servicio)
        if not servicio:
            raise HTTPException(status_code=404, detail="Servicio no encontrado")

        # Desasociar a todos los usuarios relacionados con el servicio
        usuarios_relacionados = db.query(Usuarios_Servicios).filter(Usuarios_Servicios.id_servicio == id_servicio).all()
        for usuario_rel in usuarios_relacionados:
            consulta_usuarios_servicios.desasociar_usuario_servicio(db, usuario_rel.id_usuario, id_servicio)

        # Procede a eliminar el servicio
        consulta_servicio.eliminar_servicio(db, id_servicio)
        db.commit()

        return {"estado": "Servicio eliminado con éxito"}

    except Exception as e:
        logger.exception("Error durante la eliminación del servicio")
        raise HTTPException(status_code=500, detail=f"Error durante la eliminación del servicio: {str(e)}")



# Manejo de relación muchos a muchos
@router.post("/{id_servicio}/usuarios/{id_usuario}", status_code=201)
async def asociar_usuario_servicio(id_servicio: str, id_usuario: str, db: Session = Depends(get_db)):
    try:
        consulta_usuarios_servicios = UsuariosServiciosConsulta(db)
        consulta_usuarios_servicios.asociar_usuario_servicio(db, id_servicio, id_usuario)
    except Exception as error:
        logger.exception("Error inesperado")
        raise HTTPException(status_code=400, detail={"estado": "error durante la asociación"})
    
    return JSONResponse(content={"estado": "usuario asociado al servicio"}, status_code=201)
