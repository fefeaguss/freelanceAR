from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from models.models import Base, SessionLocal, engine
from providers.consultas import TransaccionesConsulta
from schemas.shemas import Transaccion, TransaccionModificacion

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

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

@router.get("/")
async def listar_transacciones(id: Optional[str] = None, db: Session = Depends(get_db)):
    consulta_transaccion = TransaccionesConsulta(db)
    if not id:
        try:
            res = consulta_transaccion.obtener_todos(db)
        except Exception as error:
            logger.exception("Error inesperado")
            raise HTTPException(status_code=500, detail={"estado": "error durante la consulta"})
        lista_res = []
        if not res:
            return JSONResponse(content=[{}], status_code=200)
        for res_transaccion in res:
            lista_res.append({
                "id": res_transaccion.id_transaccion,
                "id_usuario_comprador": res_transaccion.id_usuario_comprador,
                "id_usuario_vendedor": res_transaccion.id_usuario_vendedor,
                "monto": float(res_transaccion.monto),
                "fecha_pago": str(res_transaccion.fecha_pago),
                "metodo_pago": res_transaccion.metodo_pago,
                "estado_transaccion": res_transaccion.estado_transaccion
            })
        return JSONResponse(content=lista_res, status_code=200)
    res_transaccion = consulta_transaccion.obtener_uno(db, id)
    return JSONResponse(
        content={
            "id": res_transaccion.id_transaccion,
            "id_usuario_comprador": res_transaccion.id_usuario_comprador,
            "id_usuario_vendedor": res_transaccion.id_usuario_vendedor,
            "monto": float(res_transaccion.monto),
            "fecha_pago": str(res_transaccion.fecha_pago),
            "metodo_pago": res_transaccion.metodo_pago,
            "estado_transaccion": res_transaccion.estado_transaccion
        },
        status_code=200
    )

@router.post("/", status_code=201)
async def cargar_transaccion(ob_transaccion: Transaccion, db: Session = Depends(get_db)):
    try:
        consulta_transaccion = TransaccionesConsulta(db)
        consulta_transaccion.crear_transaccion(db, ob_transaccion)
    except Exception as error:
        logger.exception("Error inesperado")
        raise HTTPException(status_code=400, detail={"estado": "error durante la consulta"})
    
    return JSONResponse(content={"estado": "transacción creada"}, status_code=201)

@router.put("/{id_transaccion}")
async def modificar_transaccion(id_transaccion: str, ob_transaccion: TransaccionModificacion = None, db: Session = Depends(get_db)):
    if not id_transaccion:
        raise HTTPException(detail={"estado": "falta parametro id"})
    try:
        consulta_transaccion = TransaccionesConsulta(db)
        res_modificacion = consulta_transaccion.modificar_transaccion(db, id_transaccion, ob_transaccion)
    except Exception as error:
        logger.exception("Error inesperado")
        raise HTTPException(status_code=500, detail={"estado": "error durante la consulta"})
    
    return JSONResponse(content={"resultado": {
        "id_transaccion": res_modificacion.id_transaccion,
        "id_usuario_comprador": res_modificacion.id_usuario_comprador,
        "id_usuario_vendedor": res_modificacion.id_usuario_vendedor,
        "monto": float(res_modificacion.monto),
        "fecha_pago": str(res_modificacion.fecha_pago),
        "metodo_pago": res_modificacion.metodo_pago,
        "estado_transaccion": res_modificacion.estado_transaccion
    }})

@router.delete("/{id_transaccion}", status_code=200)
async def eliminar_transaccion(id_transaccion: str, db: Session = Depends(get_db)):
    try:
        consulta_transaccion = TransaccionesConsulta(db)
        consulta_transaccion.eliminar_transaccion(db, id_transaccion)
    except Exception as error:
        logger.exception("Error inesperado")
        raise HTTPException(status_code=500, detail={"estado": "error durante la consulta"})
    
    return JSONResponse(content={"estado": "transacción eliminada"}, status_code=200)
