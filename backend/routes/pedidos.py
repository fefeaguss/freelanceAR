from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from models.models import Base, SessionLocal, engine
from providers.consultas import PedidosConsulta
from schemas.shemas import Pedido, PedidoModificacion

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

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.get("/")
async def listar_pedidos(id: Optional[str] = None, db: Session = Depends(get_db)):
    consulta_pedido = PedidosConsulta(db)
    if not id:
        try:
            res = consulta_pedido.obtener_todos(db)
        except Exception as error:
            logger.exception("Error inesperado")
            raise HTTPException(status_code=500, detail={"estado": "error durante la consulta"})
        lista_res = []
        if not res:
            return JSONResponse(content=[{}], status_code=200)
        for res_pedido in res:
            lista_res.append({
                "id_pedido": res_pedido.id_pedido,
                "id_usuario_comprador": res_pedido.id_usuario_comprador,
                "id_usuario_vendedor": res_pedido.id_usuario_vendedor,
                "id_servicio": res_pedido.id_servicio,
                "estado_pedido": res_pedido.estado_pedido,
                "fecha_alta_pedido": str(res_pedido.fecha_alta_pedido),
                "fecha_entrega": str(res_pedido.fecha_entrega),
                "detalles": res_pedido.detalles,
                "precio_acordado": float(res_pedido.precio_acordado)
            })
        return JSONResponse(content=lista_res, status_code=200)
    res_pedido = consulta_pedido.obtener_uno(db, id)
    return JSONResponse(
        content={
            "id_pedido": res_pedido.id_pedido,
            "id_usuario_comprador": res_pedido.id_usuario_comprador,
            "id_usuario_vendedor": res_pedido.id_usuario_vendedor,
            "id_servicio": res_pedido.id_servicio,
            "estado_pedido": res_pedido.estado_pedido,
            "fecha_alta_pedido": str(res_pedido.fecha_alta_pedido),
            "fecha_entrega": str(res_pedido.fecha_entrega),
            "detalles": res_pedido.detalles,
            "precio_acordado": float(res_pedido.precio_acordado)
        },
        status_code=200
    )

@router.post("/", status_code=201)
async def cargar_pedido(ob_pedido: Pedido, db: Session = Depends(get_db)):
    try:
        consulta_pedido = PedidosConsulta(db)
        consulta_pedido.crear_pedido(db, ob_pedido)
    except Exception as error:
        logger.exception("Error inesperado")
        raise HTTPException(status_code=400, detail={"estado": "error durante la consulta"})
    
    return JSONResponse(content={"estado": "pedido creado"}, status_code=201)


@router.put("/{id_pedido}")
async def modificar_pedido(id_pedido: str, ob_pedido: PedidoModificacion = None, db: Session = Depends(get_db)):
    if not id_pedido:
        raise HTTPException(detail={"estado": "falta parametro id"})
    try:
        consulta_pedido = PedidosConsulta(db)
        res_modificacion = consulta_pedido.modificar_pedido(db, id_pedido, ob_pedido)
    except Exception as error:
        logger.exception("Error inesperado")
        raise HTTPException(status_code=500, detail={"estado": "error durante la consulta"})
    
    return JSONResponse(content={"resultado": {
        "id_pedido": res_modificacion.id_pedido,
        "id_usuario_comprador": res_modificacion.id_usuario_comprador,
        "id_usuario_vendedor": res_modificacion.id_usuario_vendedor,
        "id_servicio": res_modificacion.id_servicio,
        "estado_pedido": res_modificacion.estado_pedido,
        "fecha_alta_pedido": str(res_modificacion.fecha_alta_pedido)
    }})

@router.delete("/{id_pedido}", status_code=200)
async def eliminar_pedido(id_pedido: str, db: Session = Depends(get_db)):
    try:
        consulta_pedido = PedidosConsulta(db)
        consulta_pedido.eliminar_pedido(db, id_pedido)
    except Exception as error:
        logger.exception("Error inesperado")
        raise HTTPException(status_code=500, detail={"estado": "error durante la consulta"})
    
    return JSONResponse(content={"estado": "pedido eliminado"}, status_code=200)