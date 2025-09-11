from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Form, UploadFile,File
from fastapi.responses import JSONResponse

from models.models import Base, SessionLocal, engine
from providers.consultas import UsuariosConsultas, UsuariosServiciosConsulta
from schemas.shemas import Usuario, UsuarioModificacion, UsuarioGetOne

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
        

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/")
async def listar_usuarios(id: Optional[str] = None, db: Session = Depends(get_db)):
    consulta_usuario = UsuariosConsultas(db)
    if not id:
        try:
            res = consulta_usuario.obtener_todos(db)
        except Exception as error:
            logger.exception("Error inesperado")
            raise HTTPException(status_code=500, detail={"estado": "error durante consulta"})
        lista_res = []
        if not res:
            return JSONResponse(content=[{}], status_code=200)
        for res_usuario in res:
            lista_res.append({
                "id": res_usuario.id_usuario,
                "nombre": res_usuario.nombre,
                "apellido": res_usuario.apellido,
                "mail": res_usuario.mail,
                "direccion": res_usuario.direccion,
                "idioma": res_usuario.idioma,
                "descripcion": res_usuario.descripcion,
                "foto": res_usuario.foto_usuario

            })
        return JSONResponse(
            content=lista_res,
            status_code=200
        )        
    res_usuario = consulta_usuario.oberner_uno(db, id)
    return JSONResponse(
        content={
                "id": res_usuario.id_usuario,
                "nombre": res_usuario.nombre,
                "apellido": res_usuario.apellido,
                "mail": res_usuario.mail,
                "direccion": res_usuario.direccion,
                "idioma": res_usuario.idioma,
                "descripcion": res_usuario.descripcion,
                 "foto": res_usuario.foto_usuario

        },
        status_code=200
    )

@router.get("/buscar_por_mail")
async def listar_usuario_por_mail(mail: str, db: Session = Depends(get_db)):
    consulta_usuario = UsuariosConsultas(db)
    try:
        res_usuario = consulta_usuario.oberner_por_mail(db, mail)
        if not res_usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        return JSONResponse(
            content={
                "id": res_usuario.id_usuario,
                "nombre": res_usuario.nombre,
                "apellido": res_usuario.apellido,
                "mail": res_usuario.mail,
                "contraseña": res_usuario.contraseña,
                "foto": res_usuario.foto_usuario,
                "idioma": res_usuario.idioma,
                "descripcion": res_usuario.descripcion,
                "direccion": res_usuario.direccion,
                
            },
            status_code=200
        )
    except Exception as error:
        logger.exception("Error inesperado")
        raise HTTPException(status_code=400, detail={"estado": "contraseña o mail incorrecto"})

    
@router.post("/", status_code=201)
async def cargar_usuario(
        nombre: str = Form(...),
        apellido: str = Form(...),
        mail: str = Form(...),
        username: str = Form(...),
        direccion: Optional[str] = Form(...),
        idioma: str = Form(...),
        descripcion: str = Form(...),
        contraseña: str = Form(...),
        foto: UploadFile = File(...),
        db: Session = Depends(get_db)):
    try:
        consulta_usuario = UsuariosConsultas(db)
        await consulta_usuario.crear_usuario(db, nombre, apellido, mail, username, direccion, idioma, descripcion, contraseña, foto)
    except Exception as error:
        logger.exception("Error inesperado")
        raise HTTPException(status_code=400, detail={"estado": "error durante consulta"})
    
    return JSONResponse(content={"estado": "usuario creado"}, status_code=201)

    
@router.put('/{id_usuario}')
async def modifica_usuario(id_usuario: str, ob_usuario: UsuarioModificacion = None, db: Session = Depends(get_db)):
    if not id_usuario:
        raise HTTPException(detail={"estado": "falta parametro id"}, status_code=400)
    try:
        consulta_usuario = UsuariosConsultas(db)
        res_modificacion = consulta_usuario.modificar(db, id_usuario, ob_usuario)
    except Exception as error:
        logger.exception("Error inesperado")
        raise HTTPException(status_code=500, detail={"estado":"error durante consulta"})
    
    return JSONResponse(content={"resultado":{
                "id": res_modificacion.id_usuario,
                "nombre": res_modificacion.nombre,
                "apellido": res_modificacion.apellido,
                "mail": res_modificacion.mail,
                "direccion": res_modificacion.direccion,
                "idioma": res_modificacion.idioma,
                "descripcion": res_modificacion.descripcion,
                "servicio": res_modificacion.servicio.nombre_servicio,
                "estado": res_modificacion.estado_usuario}}, status_code=200)
    
@router.delete("/")
async def baja_usuario(id_usuario: str, db:Session = Depends(get_db)):
    if not id_usuario:
        raise HTTPException(detail={"estado": "falta parametro id"}, status_code=400)
    try:
        consulta_usuario = UsuariosConsultas(db)
        consulta_usuario.eliminar_usuario(db, id_usuario)
    except Exception as error:
        logger.exception("error inesperado")
        raise HTTPException(status_code=500, detail={"estado":"error durante consulta"})
    
    return JSONResponse(
        content={
            "detalle":"usuario eliminado"
        },
        status_code=200
    )
    
    # Manejo de relación muchos a muchos
@router.post("/{id_usuario}/servicios/{id_servicio}", status_code=201)
async def asociar_servicio_usuario(id_usuario: str, id_servicio: str, db: Session = Depends(get_db)):
    try:
        consulta_usuarios_servicios = UsuariosServiciosConsulta(db)
        consulta_usuarios_servicios.asociar_usuario_servicio(db, id_usuario, id_servicio)
    except Exception as error:
        logger.exception("Error inesperado")
        raise HTTPException(status_code=400, detail={"estado": "error durante la asociación"})
    
    return JSONResponse(content={"estado": "servicio asociado al usuario"}, status_code=201)