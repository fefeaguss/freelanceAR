from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from models.models import Base, SessionLocal, engine
from providers.consultas import ValoracionesConsulta
from schemas.shemas import Valoracion, ValoracionModificacion

from sqlalchemy.orm import Session

import logging
logger = logging.getLogger(f'{__name__}')

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

router = APIRouter(prefix="/valoraciones", tags=["Valoraciones"])

@router.get("/")
async def listar_valoraciones(id: Optional[str] = None, db: Session = Depends(get_db)):
    consulta_valoracion = ValoracionesConsulta(db)
    if not id:
        try:
            res = consulta_valoracion.obtener_todos(db)
        except Exception as error:
            logger.exception("Error inesperado")
            raise HTTPException(status_code=500, detail={"estado": "error durante la consulta"})
        
        lista_res = []
        if not res:
            return JSONResponse(content=[{}], status_code=200)
        
        for res_valoracion in res:
            promedio = consulta_valoracion.obtener_promedio_valoracion(db, res_valoracion.id_usuario_valorado)
            lista_res.append({
                "id_valoracion": res_valoracion.id_valoracion,
                "id_usuario_valorador": res_valoracion.id_usuario_valorador,
                "id_usuario_valorado": res_valoracion.id_usuario_valorado,
                "puntuacion": res_valoracion.puntuacion,
                "comentario": res_valoracion.comentario,
                "estado_valoracion": res_valoracion.estado_valoracion,
                "fecha_alta_valoracion": str(res_valoracion.fecha_alta_valoracion),
                "promedio_valoracion_usuario": promedio
            })
        return JSONResponse(content=lista_res, status_code=200)

    # Si hay id, devolver solo esa valoración con el promedio del usuario valorado
    res_valoracion = consulta_valoracion.obtener_uno(db, id)
    if not res_valoracion:
        raise HTTPException(status_code=404, detail="Valoración no encontrada")
    
    promedio = consulta_valoracion.obtener_promedio_valoracion(db, res_valoracion.id_usuario_valorado)
    
    return JSONResponse(
        content={
            "id_valoracion": res_valoracion.id_valoracion,
            "id_usuario_valorador": res_valoracion.id_usuario_valorador,
            "id_usuario_valorado": res_valoracion.id_usuario_valorado,
            "puntuacion": res_valoracion.puntuacion,
            "comentario": res_valoracion.comentario,
            "estado_valoracion": res_valoracion.estado_valoracion,
            "fecha_alta_valoracion": str(res_valoracion.fecha_alta_valoracion),
            "promedio_valoracion_usuario": promedio
        },
        status_code=200
    )

@router.post("/", status_code=201)
async def cargar_valoracion(ob_valoracion: Valoracion, db: Session = Depends(get_db)):
    try:
        # Validar que la puntuación esté entre 1 y 5
        if ob_valoracion.puntuacion < 1 or ob_valoracion.puntuacion > 5:
            raise HTTPException(status_code=400, detail="La puntuación debe estar entre 1 y 5")
        
        consulta_valoracion = ValoracionesConsulta(db)
        nueva_valoracion = consulta_valoracion.crear_valoracion(db, ob_valoracion)
    except Exception as error:
        logger.exception("Error inesperado")
        raise HTTPException(status_code=400, detail={"estado": "error durante la consulta"})
    
    return JSONResponse(content={"estado": "valoración creada", "id_valoracion": nueva_valoracion.id_valoracion}, status_code=201)

@router.put("/{id_valoracion}")
async def modificar_valoracion(id_valoracion: str, ob_valoracion: ValoracionModificacion = None, db: Session = Depends(get_db)):
    if not id_valoracion:
        raise HTTPException(status_code=400, detail={"estado": "falta parametro id"})
    
    try:
        consulta_valoracion = ValoracionesConsulta(db)
        # Validar que la puntuación esté entre 1 y 5
        if ob_valoracion.puntuacion is not None and (ob_valoracion.puntuacion < 1 or ob_valoracion.puntuacion > 5):
            raise HTTPException(status_code=400, detail="La puntuación debe estar entre 1 y 5")
        
        # Intentar modificar la valoración
        res_modificacion = consulta_valoracion.modificar_valoracion(db, id_valoracion, ob_valoracion)
    except Exception as error:
        logger.exception("Error inesperado")
        raise HTTPException(status_code=500, detail={"estado": "error durante la consulta"})
    
    return JSONResponse(content={"resultado": {
        "id_valoracion": res_modificacion.id_valoracion,
        "id_usuario_valorador": res_modificacion.id_usuario_valorador,
        "id_usuario_valorado": res_modificacion.id_usuario_valorado,
        "puntuacion": res_modificacion.puntuacion,
        "comentario": res_modificacion.comentario,
        "estado_valoracion": res_modificacion.estado_valoracion,
        "fecha_alta_valoracion": str(res_modificacion.fecha_alta_valoracion)
    }})

@router.delete("/{id_valoracion}", status_code=200)
async def eliminar_valoracion(id_valoracion: str, db: Session = Depends(get_db)):
    try:
        consulta_valoracion = ValoracionesConsulta(db)
        # Eliminar la valoración (baja lógica)
        resultado = consulta_valoracion.eliminar_valoracion(db, id_valoracion)
    except Exception as error:
        logger.exception("Error inesperado")
        raise HTTPException(status_code=500, detail={"estado": "error durante la consulta"})
    
    return JSONResponse(content={"estado": "valoración eliminada"}, status_code=200)

@router.get("/promedio")
async def obtener_promedio(id_usuario_valorado: str, db: Session = Depends(get_db)):
    consulta_valoracion = ValoracionesConsulta(db)
    promedio = consulta_valoracion.obtener_promedio_valoracion(db, id_usuario_valorado)
    
    return JSONResponse(content={"promedio": promedio}, status_code=200)
