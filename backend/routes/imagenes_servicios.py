from fastapi import APIRouter, File, UploadFile, Depends, HTTPException
from sqlalchemy.orm import Session
import shutil
import os
from models.models import SessionLocal, Servicios, ImagenesServicios, Base, engine
import logging
logger = logging.getLogger(f'{__name__}')

router = APIRouter()

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

UPLOAD_DIR = "uploads/"  # Asegúrate de que este directorio exista

@router.post("/servicios/{id_servicio}/imagenes")
async def subir_imagenes(
    id_servicio: str,
    archivos: list[UploadFile] = File(...),
    db: Session = Depends(get_db)
):
    servicio = db.query(Servicios).filter(Servicios.id_servicio == id_servicio).first()
    if not servicio:
        return {"error": "Servicio no encontrado"}

    urls = []
    for archivo in archivos:
        file_path = os.path.join(UPLOAD_DIR, archivo.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(archivo.file, buffer)

        nueva_imagen = ImagenesServicios(id_servicio=id_servicio, url_imagen=file_path)
        db.add(nueva_imagen)
        urls.append(file_path)

    db.commit()
    return {"message": "Imágenes subidas", "urls": urls}

@router.get("/v1/servicios/{id_servicio}/imagenes")
def obtener_imagenes(id_servicio: str, db: Session = Depends(get_db)):
    if not isinstance(id_servicio, str) or not id_servicio:
        raise HTTPException(status_code=422, detail="El id_servicio no es válido")

    print(f"Recibida solicitud para el servicio: {id_servicio}")
    imagenes = db.query(ImagenesServicios).filter(ImagenesServicios.id_servicio == id_servicio).all()
    print(f"Imágenes encontradas para el servicio {id_servicio}: {imagenes}")

    if not imagenes:
        return {"error": "No se encontraron imágenes para este servicio."}

    return [{"id": img.id_imagen, "url": img.url_imagen} for img in imagenes]

