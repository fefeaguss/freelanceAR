from typing import List
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from models.models import Base, SessionLocal, engine, Conversaciones
from providers.consultas import MensajesConsulta, ConversacionesConsulta
from schemas.shemas import Mensaje, MensajeModificacion, MensajeResponse, ConversacionResponse, ConversacionRequest
from sqlalchemy.orm import Session
import logging
import datetime

logger = logging.getLogger(f'{__name__}')

try:
    Base.metadata.create_all(bind=engine)
except Exception as err:
    logger.error(err)

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as error:
        logger.error(error)
    finally:
        db.close()

router = APIRouter(prefix="/mensajes", tags=["Mensajes"])

@router.get("/", response_model=List[MensajeResponse])
async def obtener_mensajes(id_usuario_envia: str, id_usuario_recibe: str, db: Session = Depends(get_db)):
    consulta_mensaje = MensajesConsulta(db)
    try:
        mensajes = consulta_mensaje.obtener_conversacion(id_usuario_envia, id_usuario_recibe)
    except Exception as error:
        logger.exception("Error inesperado al obtener la conversación")
        raise HTTPException(status_code=500, detail={"estado": "error inesperado"})

    if not mensajes:
        return JSONResponse(content=[], status_code=200)

    lista_res = [
        {
            "id": mensaje.id_mensaje,
            "id_usuario_envia": mensaje.id_usuario_envia,
            "nombre_usuario_envia": mensaje.usuario_envia.nombre if mensaje.usuario_envia else "Desconocido",
            "foto_usuario_envia": mensaje.usuario_envia.foto_usuario if mensaje.usuario_envia else "default-avatar.jpg",
            "id_usuario_recibe": mensaje.id_usuario_recibe,
            "nombre_usuario_recibe": mensaje.usuario_recibe.nombre if mensaje.usuario_recibe else "Desconocido",
            "foto_usuario_recibe": mensaje.usuario_recibe.foto_usuario if mensaje.usuario_recibe else "default-avatar.jpg",
            "contenido_mensaje": mensaje.contenido_mensaje,
            "estado_mensaje": mensaje.estado_mensaje,
            "fecha_alta_mensaje": str(mensaje.fecha_alta_mensaje),
        }
        for mensaje in mensajes
    ]

    return JSONResponse(content=lista_res, status_code=200)

@router.post("/", status_code=201)
async def cargar_mensaje(ob_mensaje: Mensaje, db: Session = Depends(get_db)):
    try:
        consulta_mensaje = MensajesConsulta(db)
        nuevo_mensaje = consulta_mensaje.crear_mensaje(db, ob_mensaje)

        # Convierte el objeto a un diccionario y serializa fecha_alta_mensaje
        mensaje_dict = {
            "id_conversacion": nuevo_mensaje.id_conversacion,
            "id_usuario_envia": nuevo_mensaje.id_usuario_envia,
            "id_usuario_recibe": nuevo_mensaje.id_usuario_recibe,
            "contenido_mensaje": nuevo_mensaje.contenido_mensaje,
            "estado_mensaje": nuevo_mensaje.estado_mensaje,
            "fecha_alta_mensaje": nuevo_mensaje.fecha_alta_mensaje.isoformat(),  # Serializamos a ISO 8601
        }

        return JSONResponse(content={"estado": "mensaje creado", "mensaje": mensaje_dict}, status_code=201)
    except Exception as error:
        logger.exception("Error inesperado al crear mensaje")
        raise HTTPException(status_code=400, detail={"estado": "error durante consulta"})


@router.put("/{id_mensaje}")
async def modificar_mensaje(id_mensaje: str, ob_mensaje: MensajeModificacion, db: Session = Depends(get_db)):
    if not id_mensaje:
        raise HTTPException(status_code=400, detail={"estado": "falta parámetro id"})

    try:
        consulta_mensaje = MensajesConsulta(db)
        res_modificacion = consulta_mensaje.modificar_mensaje(db, id_mensaje, ob_mensaje)
        return JSONResponse(content={
            "resultado": {
                "id_mensaje": res_modificacion.id_mensaje,
                "id_usuario_envia": res_modificacion.id_usuario_envia,
                "id_usuario_recibe": res_modificacion.id_usuario_recibe,
                "contenido_mensaje": res_modificacion.contenido_mensaje,
                "estado_mensaje": res_modificacion.estado_mensaje,
                "fecha_alta_mensaje": str(res_modificacion.fecha_alta_mensaje)
            }
        })
    except Exception as error:
        logger.exception("Error inesperado al modificar mensaje")
        raise HTTPException(status_code=500, detail={"estado": "error durante consulta"})

@router.delete("/{id_mensaje}", status_code=200)
async def eliminar_mensaje(id_mensaje: str, db: Session = Depends(get_db)):
    try:
        consulta_mensaje = MensajesConsulta(db)
        consulta_mensaje.eliminar_mensaje(db, id_mensaje)
        return JSONResponse(content={"estado": "mensaje eliminado"}, status_code=200)
    except Exception as error:
        logger.exception("Error inesperado al eliminar mensaje")
        raise HTTPException(status_code=500, detail={"estado": "error durante consulta"})

@router.post("/crear_conversacion", response_model=ConversacionResponse, status_code=201)
async def crear_conversacion(payload: ConversacionRequest, db: Session = Depends(get_db)):
    consulta_conversacion = ConversacionesConsulta(db)
    try:
        conversacion = consulta_conversacion.crear_o_unirse_conversacion(
            payload.id_usuario_inicia, 
            payload.id_usuario_recibe
        )
        conversacion_response = ConversacionResponse.from_orm(conversacion)
        return conversacion_response
    except Exception as error:
        logger.exception("Error inesperado al crear o unirse a la conversación")
        raise HTTPException(status_code=500, detail={"estado": "error inesperado"})

@router.get("/conversaciones/{id_usuario}", response_model=List[ConversacionResponse])
async def obtener_conversaciones_usuario(id_usuario: str, db: Session = Depends(get_db)):
    try:
        conversaciones = db.query(Conversaciones).filter(
            (Conversaciones.id_usuario_inicia == id_usuario) | 
            (Conversaciones.id_usuario_recibe == id_usuario)
        ).all()

        if not conversaciones:
            return JSONResponse(content=[], status_code=200)

        lista_res = [
            {
                "id_conversacion": conv.id_conversacion,
                "id_usuario_inicia": conv.id_usuario_inicia,
                "nombre_usuario_inicia": conv.usuario_inicia.nombre if conv.usuario_inicia else "Desconocido",
                "foto_usuario_inicia": conv.usuario_inicia.foto_usuario if conv.usuario_inicia else "default-avatar.jpg",
                "id_usuario_recibe": conv.id_usuario_recibe,
                "nombre_usuario_recibe": conv.usuario_recibe.nombre if conv.usuario_recibe else "Desconocido",
                "foto_usuario_recibe": conv.usuario_recibe.foto_usuario if conv.usuario_recibe else "default-avatar.jpg",
                "fecha_alta_conversacion": str(conv.fecha_alta_conversacion),
            }
            for conv in conversaciones
        ]

        return JSONResponse(content=lista_res, status_code=200)

    except Exception as error:
        logger.exception("Error inesperado al obtener conversaciones del usuario")
        raise HTTPException(status_code=500, detail={"estado": "error inesperado"})

@router.get("/conversacion/{id_conversacion}", response_model=List[MensajeResponse])
async def obtener_mensajes_por_conversacion(id_conversacion: str, db: Session = Depends(get_db)):
    """Obtiene todos los mensajes de una conversación específica."""
    consulta_mensaje = MensajesConsulta(db)
    try:
        mensajes = consulta_mensaje.obtener_mensajes_por_conversacion(id_conversacion)
    except Exception as error:
        logger.exception("Error inesperado al obtener mensajes de la conversación")
        raise HTTPException(status_code=500, detail={"estado": "error inesperado"})

    if not mensajes:
        return JSONResponse(content=[], status_code=200)

    lista_res = [
        {
            "id": mensaje.id_mensaje,
            "id_usuario_envia": mensaje.id_usuario_envia,
            "nombre_usuario_envia": mensaje.usuario_envia.nombre if mensaje.usuario_envia else "Desconocido",
            "foto_usuario_envia": mensaje.usuario_envia.foto_usuario if mensaje.usuario_envia else "default-avatar.jpg",
            "id_usuario_recibe": mensaje.id_usuario_recibe,
            "nombre_usuario_recibe": mensaje.usuario_recibe.nombre if mensaje.usuario_recibe else "Desconocido",
            "foto_usuario_recibe": mensaje.usuario_recibe.foto_usuario if mensaje.usuario_recibe else "default-avatar.jpg",
            "contenido_mensaje": mensaje.contenido_mensaje,
            "estado_mensaje": mensaje.estado_mensaje,
            "fecha_alta_mensaje": str(mensaje.fecha_alta_mensaje),
        }
        for mensaje in mensajes
    ]

    return JSONResponse(content=lista_res, status_code=200)
