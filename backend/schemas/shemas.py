from typing import Optional
from pydantic import BaseModel, UUID4, Field
from fastapi import File, UploadFile, Form
from uuid import uuid4
from enum import Enum
import datetime

class UsuarioGetOne(BaseModel):
    id_usuario: str = Form(...)
    nombre: str
    apellido: str
    mail: str
    direccion: str
    idioma: str
    descripcion: str
    contrasena: str
    estado_usuario: int
    foto: Optional[str]  # URL o ruta del archivo subido

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_usuario": "123e4567-e89b-12d3-a456-426614174000",
                "nombre": "Agustin",
                "apellido": "Bressan",
                "mail": "agus@gamil.com",
                "direccion": "Argentina",
                "idioma": "Español",
                "descripcion": "soy feminista",
                "contrasena": "123",
                "estado_usuario": 1,
                "foto": "photos/agus@gmail.com_imagen.jpg"
            }
        }



class Usuario(BaseModel):
    nombre: str
    apellido: str
    mail: str
    direccion: str
    idioma: str
    descripcion: str
    contraseña: str
    foto: str
    
    class config:
        json_schema_extra={
            "example":{
                "nombre": "Agustin",
                "apellido": "Bressan",
                "mail": "agus@gamil.com",
                "direccion": "Argentina",
                "idioma": "Español",
                "descripcion": "soy feminista",
                "contraseña": "123",

            }
        }

class UsuarioModificacion(BaseModel):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    mail: Optional[str] = None
    direccion: Optional[str] = None
    idioma: Optional[str] = None
    descripcion: Optional[str] = None
    contraseña: Optional[str] = None
    estado_usuario: Optional[int] = Field(default=1)
    foto: Optional[UploadFile] = File()
    
    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Juan",
                "apellido": "Perez",
                "mail": "juan.perez@example.com",
                "direccion": "Calle Falsa 123, Ciudad, País",
                "idioma": "ingles",  # Ejemplo: 1 para DNI, 2 para Pasaporte, etc.
                "descripcion": "soy programador",
                "contraseña": "fefe",
                "estado": 1
            }
        }
        
class EstadoMensaje(int, Enum):
    ENVIADO = 1
    LEIDO = 2
    ENTREGADO = 3
        
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Mensaje(BaseModel):
    id_conversacion: str
    id_usuario_envia: str
    id_usuario_recibe: str
    contenido_mensaje: str
    estado_mensaje: int
    fecha_alta_mensaje: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


        
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional

class MensajeResponse(BaseModel):
    id: str
    id_usuario_envia: str
    nombre_usuario_envia: Optional[str]
    foto_usuario_envia: Optional[str]
    id_usuario_recibe: str
    nombre_usuario_recibe: Optional[str]
    foto_usuario_recibe: Optional[str]
    contenido_mensaje: str
    estado_mensaje: int
    fecha_alta_mensaje: datetime

    class Config:
        model_config = ConfigDict(arbitrary_types_allowed=True)  # Añadir esta línea



class MensajeModificacion(BaseModel):
    id_usuario_envia: Optional[str] = None
    id_usuario_recibe: Optional[str] = None
    contenido_mensaje: Optional[str] = None
    estado_mensaje: Optional[int] = None
   

    class Config:
        json_schema_extra = {
            "example": {
                "id_usuario_envia": "123",
                "id_usuario_recibe": "456",
                "contenido_mensaje": "Mensaje actualizado",
                "estado_mensaje": 1,
            }
        }
        
class Transaccion(BaseModel):
    id_usuario_comprador: str
    id_usuario_vendedor: str
    monto: float
    metodo_pago: str

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id_usuario_comprador": "123",
                "id_usuario_vendedor": "456",
                "monto": 150.00,
                "metodo_pago": "Tarjeta de Crédito"
            }
        }
        
class TransaccionModificacion(BaseModel):
    id_usuario_comprador: Optional[str] = None
    id_usuario_vendedor: Optional[str] = None
    monto: Optional[float] = None
    metodo_pago: Optional[str] = None
    estado_transaccion: Optional[int] = Field(default=1)  # Campo para la baja lógica

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id_usuario_comprador": "123",
                "id_usuario_vendedor": "456",
                "monto": 200.00,
                "metodo_pago": "Transferencia Bancaria",
                "estado_transaccion": 0,
            }
        }

        
class Valoracion(BaseModel):
    id_usuario_valorador: str
    id_usuario_valorado: str
    puntuacion: int
    comentario: str
    estado_valoracion: int = Field(default=1)  # Campo para la baja lógica

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id_usuario_valorador": "123",
                "id_usuario_valorado": "456",
                "puntuacion": 5,
                "comentario": "Excelente trabajo",
                "estado_valoracion": 1
            }
        }
        
class ValoracionModificacion(BaseModel):
    id_usuario_valorador: Optional[str] = None
    id_usuario_valorado: Optional[str] = None
    puntuacion: Optional[int] = None
    comentario: Optional[str] = None
    estado_valoracion: Optional[int] = Field(default=1)  # Campo para la baja lógica
    fecha_baja_valoracion: Optional[datetime] = None  # Fecha de baja lógica

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id_usuario_valorador": "123",
                "id_usuario_valorado": "456",
                "puntuacion": 4,
                "comentario": "Buen trabajo, aunque podría mejorar en algunos aspectos",
                "estado_valoracion": 0,
                "fecha_baja_valoracion": "2024-02-01T00:00:00"
            }
        }

        
class categoria(BaseModel):
    id_categoria: int
    nombre_categoria: str
    
    class config:
        json_schema_extra ={
            "example":{
                "id_categoria": "1",
                "nombre_categoia": "desarrollador web",
                
            }
        }    

class servicio(BaseModel):  
    nombre_servicio: str
    descripcion_servi: str
    precio: float
    id_categoria:int
    
    class config:
        json_schema_extra ={
            "example":{
                "nombre_servicio": "desarrollo web",
                "desripcion": "hago todo lo relacionado",
                "precio": 599,
                "id_categoria":"1"
            }
        }

class servicioModificacion(BaseModel):
    nombre_servicio: Optional[str] = None
    descripcion_servicio: Optional[str] = None
    precio: Optional[float] = None
    id_categoria: Optional[int] = None
    foto: Optional[UploadFile] = None

    
    class Config:
        json_schema_extra ={
            "example":{
                "nombre_servicio": "desarrollo web",
                "desripcion": "hago todo lo relacionado",
                "precio": 599,
                "id_categoria":1
            }
        }
        
        
class Pedido(BaseModel):
    id_usuario_comprador: str
    id_usuario_vendedor: str
    id_servicio: str
    estado_pedido: int
    detalles: Optional[str] = None
    precio_acordado: Optional[float] = None

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id_usuario_comprador": "123",
                "id_usuario_vendedor": "456",
                "id_servicio": "789",
                "estado_pedido": 1,
                "detalles": "Detalles adicionales del pedido",
                "precio_acordado": 150.00
            }
        }

class PedidoModificacion(BaseModel):
    id_usuario_comprador: Optional[str] = None
    id_usuario_vendedor: Optional[str] = None
    id_servicio: Optional[str] = None
    estado_pedido: Optional[int] = None
    detalles: Optional[str] = None
    precio_acordado: Optional[float] = None

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "id_usuario_comprador": "123",
                "id_usuario_vendedor": "456",
                "id_servicio": "789",
                "estado_pedido": 2,  # Por ejemplo, 2 podría indicar un estado diferente
                "detalles": "Detalles actualizados del pedido",
                "precio_acordado": 200.00
            }
        }
class archivo_adjunto(BaseModel):
    ud:str

class ConversacionResponse(BaseModel):
    id_conversacion: str
    id_usuario_inicia: str
    id_usuario_recibe: str
    fecha_alta_conversacion: datetime

    class Config:
       from_attributes = True
       
class ConversacionRequest(BaseModel):
    id_usuario_inicia: str
    id_usuario_recibe: str