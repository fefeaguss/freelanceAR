from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from models.models import Base, SessionLocal, engine
from providers.consultas import CategoriasConsultas
from schemas.shemas import categoria

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
        
router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.post("/")
async def cargar_categoria(categoria: categoria, db: Session = Depends(get_db)):
    try:
        consulta_categoria = CategoriasConsultas(db)
        rta = consulta_categoria.crear_categoria(db, categoria)
    except Exception as error:
        logger.exception("Error inesperado")
        raise HTTPException(status_code=500, detail={"estado":"error durante la consulta"})
    return rta

@router.get("/")
async def listar_categoria(id: Optional[int] = None, db: Session = Depends(get_db)):
    consulta_categoria = CategoriasConsultas(db)
    if not id:
        try:
            res = consulta_categoria.obtener_todos(db)
        except Exception as error:
            logger.exception("error inesperado")
            raise HTTPException(status_code=500, detail={"estado":"error durante la consulta"})
        lista_res = []
        if not res:
            return JSONResponse(content=[{}], status_code=200)
        for res_categoria in res:
            lista_res.append({
                "id_categoria": res_categoria.id_categoria,
                "nombre_categoria": res_categoria.nombre_categoria
            })
        return JSONResponse(
            content=lista_res,
            status_code=200
        )    
    res_categoria = consulta_categoria.oberner_uno(db, id)
    return JSONResponse(
        content={
            "id_categoria": res_categoria.id_categoria,
            "nombre_categoria": res_categoria.nombre_categoria
        },
        status_code=200
    )
            