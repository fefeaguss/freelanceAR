from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from models.models import Base, SessionLocal, engine
from providers.consultas import UsuariosServiciosConsulta
from fastapi.responses import JSONResponse
from datetime import datetime

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

router = APIRouter(prefix="/usuarios-servicios", tags=["Usuarios-Servicios"])

def format_date(date):
    return date.strftime("%d/%m/%Y")

@router.get("/")
async def listar_usuarios_servicios(id_usuario: Optional[str] = None, id_servicio: Optional[str] = None, db: Session = Depends(get_db)):
    consulta = UsuariosServiciosConsulta(db)
    if not id_usuario and not id_servicio:
        try:
            res = consulta.obtener_todos(db)
        except Exception as error:
            logger.exception("Error inesperado")
            raise HTTPException(status_code=500, detail={"estado": "error durante la consulta"})
        
        lista_res = []
        if not res:
            return JSONResponse(content=[{}], status_code=200)
        
        for item in res:
            lista_res.append({
                "id_usuario": item.usuario.id_usuario,
                "nombre_usuario": item.usuario.nombre,
                "apellido_usuario": item.usuario.apellido,
                "email_usuario": item.usuario.mail,
                "direccion":item.usuario.direccion,
                "descripcion_usuario":item.usuario.descripcion,
                "idioma": item.usuario.idioma,
                "fecha_alta":format_date(item.usuario.fecha_alta_usuario)  ,
                "foto":item.usuario.foto_usuario,
                "rol": item.rol,
                "id_servicio": item.servicio.id_servicio,
                "nombre_servicio": item.servicio.nombre_servicio,
                "descripcion_servicio": item.servicio.descripcion_servicio,
                "precio_servicio": float(item.servicio.precio),
                "categoria_servicio": item.servicio.categoria.nombre_categoria
            })
        
        return JSONResponse(content=lista_res, status_code=200)
    
    if id_usuario:
        try:
            res = consulta.obtener_por_usuario(db, id_usuario)
        except Exception as error:
            logger.exception("Error inesperado")
            raise HTTPException(status_code=500, detail={"estado": "error durante la consulta"})
        
        lista_res = []
        if not res:
            return JSONResponse(content=[{}], status_code=200)
        
        for item in res:
            lista_res.append({
                "id_usuario": item.usuario.id_usuario,
                "nombre_usuario": item.usuario.nombre,
                "apellido_usuario": item.usuario.apellido,
                "email_usuario": item.usuario.mail,
                "descripcion_usuario":item.usuario.descripcion,
                "idioma": item.usuario.idioma,
                "fecha_alta": format_date(item.usuario.fecha_alta_usuario) ,
                "direccion": item.usuario.direccion,
                "foto":item.usuario.foto_usuario,
                "rol": item.rol,
                "id_servicio": item.servicio.id_servicio,
                "nombre_servicio": item.servicio.nombre_servicio,
                "descripcion_servicio": item.servicio.descripcion_servicio,
                "precio_servicio": float(item.servicio.precio),
                "categoria_servicio": item.servicio.categoria.nombre_categoria
            })
        
        return JSONResponse(content=lista_res, status_code=200)
    
    if id_servicio:
        try:
            res = consulta.obtener_por_servicio(db, id_servicio)
        except Exception as error:
            logger.exception("Error inesperado")
            raise HTTPException(status_code=500, detail={"estado": "error durante la consulta"})
        
        lista_res = []
        if not res:
            return JSONResponse(content=[{}], status_code=200)
        
        for item in res:
            lista_res.append({
                "id_usuario": item.usuario.id_usuario,
                "nombre_usuario": item.usuario.nombre,
                "apellido_usuario": item.usuario.apellido,
                "descripcion_usuario":item.usuario.descripcion,
                "email_usuario": item.usuario.mail,
                "idioma": item.usuario.idioma,
                "fecha_alta": item.usuario.fecha_alta_usuario ,
                "direccion": item.usuario.direccion,
                "foto":item.usuario.foto_usuario,
                "rol": item.rol,
                "id_servicio": item.servicio.id_servicio,
                "nombre_servicio": item.servicio.nombre_servicio,
                "descripcion_servicio": item.servicio.descripcion_servicio,
                "precio_servicio": float(item.servicio.precio),
                "categoria_servicio": item.servicio.categoria.nombre_categoria
            })
        
        return JSONResponse(content=lista_res, status_code=200)
    
    return JSONResponse(content=[{}], status_code=400)





@router.post("/", status_code=201)
async def asociar_usuario_servicio(id_usuario: str, id_servicio: str, db: Session = Depends(get_db)):
    try:
        consulta = UsuariosServiciosConsulta(db)
        # Aquí siempre asignamos el rol de "consumidor"
        consulta.asociar_usuario_servicio_nuevo(db, id_usuario, id_servicio, rol='consumidor')
    except Exception as error:
        logger.exception("Error inesperado")
        raise HTTPException(status_code=400, detail={"estado": "error durante la asociación"})
    
    return JSONResponse(content={"estado": "usuario asociado al servicio con rol de consumidor"}, status_code=201)


@router.delete("/{id_usuario}/{id_servicio}", status_code=200)
async def desasociar_usuario_servicio(id_usuario: str, id_servicio: str, db: Session = Depends(get_db)):
    try:
        consulta = UsuariosServiciosConsulta(db)
        consulta.desasociar_usuario_servicio(db, id_usuario, id_servicio)
    except Exception as error:
        logger.exception("Error inesperado")
        raise HTTPException(status_code=500, detail={"estado": "error durante la desasociación"})
    
    return JSONResponse(content={"estado": "usuario desasociado del servicio"}, status_code=200)
