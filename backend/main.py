from fastapi import FastAPI, Depends,Query, HTTPException, security
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles


from models.models import Base, SessionLocal, engine, Usuarios,Servicios
from sqlalchemy.orm import Session

from routes.Usuarios import router as usuarios_router
from routes.Categorias import router as categoria_router
from routes.servicio import router as servicio_router
from routes.Mensajes import router as mensajes_router 
from routes.usuario_servicio import router as usuario_servicio_router
from routes.pedidos import router as pedidos_router
from routes.transaccion import router as transaccion_router
from routes.valoracion import router as valoracion_router
from routes.imagenes_servicios import router as ImagenesServicios_router


import uvicorn


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


try:
    Base.metadata.create_all(bind=engine)
except Exception as err:
    print(err.args)
    
def get_db():
    
   try:
       db = SessionLocal()
       yield db
   except Exception as error:
       print(error.args)
   finally:
       db.close    

app = FastAPI()

@app.get("/ping")
async def pong():
    return JSONResponse(content={"estado": "pong"}, status_code=201)


titulo = "Freelancear"
descripcion =   ""
tags_metadata = [
    {
        "name": "Usuarios",
        "description": "Endpoints relacionados a Usuarios.",
    },
]



app.include_router(usuarios_router, prefix="/v1")
app.include_router(categoria_router, prefix="/v1")
app.include_router(servicio_router, prefix="/v1")
app.include_router(mensajes_router, prefix="/v1")
app.include_router(usuario_servicio_router, prefix="/v1")
app.include_router(pedidos_router, prefix="/v1")
app.include_router(transaccion_router, prefix="/v1")
app.include_router(valoracion_router, prefix="/v1")
app.include_router(ImagenesServicios_router, prefix="/v1")


origins = [
    "http://localhost:5173",
    "http://localhost:5173/principal",
    "http://localhost:5173/service",
    "http://localhost:5173/Chat",
   
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Cambia esto por dominios específicos en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# Servir imágenes de la carpeta "photos"
app.mount("/static", StaticFiles(directory="photos"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads") 





@app.get("/v1/buscar")
async def buscar(
    query: str = Query(..., description="Texto para buscar"),
    db: Session = Depends(get_db)
):
    try:
        # Buscar perfiles por nombre
        perfiles = db.query(Usuarios).filter(Usuarios.nombre.ilike(f"%{query}%")).all()
        
        # Buscar servicios por nombre
        servicios = db.query(Servicios).filter(Servicios.nombre_servicio.ilike(f"%{query}%")).all()
        
        return {"perfiles": perfiles, "servicios": servicios}
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error durante la búsqueda")
