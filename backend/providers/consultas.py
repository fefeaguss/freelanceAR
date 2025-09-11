import datetime
from typing import Optional, Type, Annotated, TypeVar
from pydantic import BaseModel
from fastapi import HTTPException, Form, UploadFile, File, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload

import os
import uuid
import aiofiles

from models.models import Usuarios, Servicios, Pedidos, Categorias, Transacciones, Mensajes, Valoraciones, Usuarios_Servicios,SessionLocal, Conversaciones
from schemas.shemas import Usuario, servicio, Pedido, PedidoModificacion,categoria, Transaccion, TransaccionModificacion, Mensaje, MensajeModificacion, ValoracionModificacion,Valoracion 

UPLOAD_FOLDER = "photos"  # Carpeta donde se guardarán las imágenes
BASE_URL = "http://localhost:8000"  # Cambia esto si usas un dominio real
PHOTO_URL_PATH = f"{BASE_URL}/static/photos"  # Ruta pública accesible desde el frontend

os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Crea la carpeta si no existe

class UsuariosConsultas():
    def __init__(self, instancia_db):
        self.instancia_db = instancia_db
        
    def oberner_por_mail(self, db: Session, mail: str): 
        return db.query(Usuarios).filter(Usuarios.mail == mail).first() 
    
        
    def oberner_uno(self,db:Session, id_usuario: int):
        return db.query(Usuarios).filter(Usuarios.id_usuario == id_usuario).first()
    
    def obtener_todos(self, db: Session):
        return db.query(Usuarios).all()

    async def crear_usuario(
        self, db: Session, nombre: str, apellido: str, mail: str, username: str,
        direccion: Optional[str], idioma: Optional[str], descripcion: Optional[str], 
        contraseña: str, foto: UploadFile):
        
        try:
 

            # Crear el usuario en la base de datos
            usuario_db = Usuarios(
                id_usuario=str(uuid.uuid4()),
                nombre=nombre,
                apellido=apellido,
                mail=mail,
                username=username,
                direccion=direccion,
                idioma=idioma,
                descripcion=descripcion,
                contraseña=contraseña,  # Guardar la contraseña encriptada
                estado_usuario=1
            )
            
            db.add(usuario_db)
            db.commit()
            db.refresh(usuario_db)

            # Obtener la extensión del archivo
            extension = foto.filename.split(".")[-1]
            filename = f"{usuario_db.id_usuario}.{extension}"
            file_path = os.path.join(UPLOAD_FOLDER, filename)

            # Guardar la imagen de forma asíncrona
            async with aiofiles.open(file_path, "wb") as out_file:
                content = await foto.read()
                await out_file.write(content)

            # Guardar la URL pública en la base de datos
            usuario_db.foto_usuario = f"/static/{usuario_db.id_usuario}.{extension}"

            db.commit()
            db.refresh(usuario_db)

            return usuario_db

        except Exception as e:
            db.rollback()  # Revertir cambios en caso de error
            raise e  # Relanzar el error para que sea manejado externamente




        
    def eliminar_usuario(self, db: Session,id_usuario):
        usuario = self.oberner_uno(db, id_usuario)
        
        if usuario:
            usuario.estado_usuario = 0
            usuario.fecha_baja_usuario = datetime.datetime.now()
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
    
    def modificar(self, db: Session,id_usuario ,usuario: Usuario):
        objeto_actual = self.oberner_uno(db, id_usuario)
        
        if objeto_actual:
            for key, value in usuario.dict(exclude_unset=True).items():
                setattr(objeto_actual, key, value)
            db.commit()
            db.refresh(objeto_actual)
            return objeto_actual
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

class CategoriasConsultas():
    
    def __init__(self, instancia_db):
        self.instancia_db = instancia_db
        
    def oberner_uno(self, db: Session, id_categoria: int):
        return db.query(Categorias).filter(Categorias.id_categoria == id_categoria).first()
    
    def obtener_todos(self, db: Session):
        return db.query(Categorias).all()
    
    def crear_categoria(self, db:Session, catego: categoria):
        nuevo_categoria = Categorias(
            id_categoria = catego.id_categoria,
            nombre_categoria = catego.nombre_categoria,
        )
        db.add(nuevo_categoria)
        db.commit()
        return nuevo_categoria


class ServiciosConsulta():
    
    def __init__(self, instancia_db):
        self.instancia_db = instancia_db
    
    def obtener_uno(self, db:Session, id_servicio : str):
        return db.query(Servicios).filter(Servicios.id_servicio == id_servicio).first()
    
    def obtener_todos(self, db:Session):
        return db.query(Servicios).all()
    
    async def crear_servicio(self,db:Session,nombre_servicio : str, descripcion_servicio : str, precio:float, id_categoria : int ):
        
        nuevo_servicio = Servicios(
            nombre_servicio = nombre_servicio,
            descripcion_servicio = descripcion_servicio,
            precio =precio,
            id_categoria = id_categoria
        )
        db.add(nuevo_servicio)
        db.commit()
        db.refresh(nuevo_servicio)
        return nuevo_servicio
    
    def modificar_servicio(self, db: Session, id_servicio, servicio: servicio):
        objeto_actual = self.obtener_uno(db, id_servicio)
        
        if objeto_actual:
            for key, value in servicio.dict(exclude_unset=True).items():
                setattr(objeto_actual, key, value)
            db.commit()
            db.refresh(objeto_actual)
            return objeto_actual
        raise HTTPException(status_code=404, detail="Servicio no encontrado")
    
    def eliminar_servicio(self,db: Session, id_servicio):
        servicio = self.obtener_uno(db, id_servicio)
        
        if not servicio:
            raise HTTPException(status_code=404, detail="servicio no encontrado")
        
        db.delete(servicio)
        db.commit()
        return{"messge": "servicio eliminado"}       
        

class MensajesConsulta():
    
    def __init__(self, db:Session):
        self.db = db
    
    def obtener_uno(self, db: Session, id_mensaje: str):
        return db.query(Mensajes).filter(Mensajes.id_mensaje == id_mensaje).first()
    
    def obtener_todos(self, db: Session):
        return db.query(Mensajes).all()
    
    def crear_mensaje(self, db: Session, mensaje: Mensaje):
        nuevo_mensaje = Mensajes(
            id_conversacion=mensaje.id_conversacion, 
            id_usuario_envia=mensaje.id_usuario_envia,
            id_usuario_recibe=mensaje.id_usuario_recibe,
            contenido_mensaje=mensaje.contenido_mensaje,
            estado_mensaje=mensaje.estado_mensaje,
            fecha_alta_mensaje=mensaje.fecha_alta_mensaje
        )
        db.add(nuevo_mensaje)
        db.commit()
        db.refresh(nuevo_mensaje)
        return nuevo_mensaje
    
    def modificar_mensaje(self, db: Session, id_mensaje: str, mensaje: MensajeModificacion):
        objeto_actual = self.obtener_uno(db, id_mensaje)
        
        if objeto_actual:
            for key, value in mensaje.dict(exclude_unset=True).items():
                setattr(objeto_actual, key, value)
            db.commit()
            db.refresh(objeto_actual)
            return objeto_actual
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    
    def eliminar_mensaje(self, db: Session, id_mensaje: str):
        mensaje = self.obtener_uno(db, id_mensaje)
        
        if not mensaje:
            raise HTTPException(status_code=404, detail="Mensaje no encontrado")
        
        db.delete(mensaje)
        db.commit()
        return {"message": "Mensaje eliminado"}
    
    def obtener_conversacion(self, id_usuario_logueado: str, id_usuario_servicio: str):
        return (
            self.db.query(Mensajes)
            .filter(
                ((Mensajes.id_usuario_envia == id_usuario_logueado) & (Mensajes.id_usuario_recibe == id_usuario_servicio)) |
                ((Mensajes.id_usuario_envia == id_usuario_servicio) & (Mensajes.id_usuario_recibe == id_usuario_logueado))
            )
            .order_by(Mensajes.fecha_alta_mensaje)  # Ordena los mensajes por fecha
            .all()
        )
        
    def obtener_mensajes_por_conversacion(self, id_conversacion: str):
        return (
            self.db.query(Mensajes)
            .filter(Mensajes.id_conversacion == id_conversacion)
            .order_by(Mensajes.fecha_alta_mensaje.asc())
            .all()
        )
        
class ConversacionesConsulta():
    
    def __init__(self, db: Session):
        self.db = db

    def crear_o_unirse_conversacion(self, id_usuario_inicia: str, id_usuario_recibe: str):
        conversacion = self.db.query(Conversaciones).filter(
            ((Conversaciones.id_usuario_inicia == id_usuario_inicia) & (Conversaciones.id_usuario_recibe == id_usuario_recibe)) |
            ((Conversaciones.id_usuario_inicia == id_usuario_recibe) & (Conversaciones.id_usuario_recibe == id_usuario_inicia))
        ).first()

        if conversacion:
            return conversacion
        
        nueva_conversacion = Conversaciones(
            id_usuario_inicia=id_usuario_inicia,
            id_usuario_recibe=id_usuario_recibe,
            fecha_alta_conversacion=datetime.datetime.now()
        )

        self.db.add(nueva_conversacion)
        self.db.commit()
        self.db.refresh(nueva_conversacion)  # Refresca la instancia para obtener el ID generado

        return nueva_conversacion



class UsuariosServiciosConsulta():
    
    def __init__(self, instancia_db):
        self.instancia_db = instancia_db
    
    def obtener_uno(self, db: Session, id_usuario: str, id_servicio: str):
        return db.query(Usuarios_Servicios).filter(
            Usuarios_Servicios.id_usuario == id_usuario,
            Usuarios_Servicios.id_servicio == id_servicio
        ).first()
        
    def obtener_por_usuario(self, db: Session, id_usuario: str): return db.query(Usuarios_Servicios).options( joinedload(Usuarios_Servicios.usuario), joinedload(Usuarios_Servicios.servicio) ).filter(Usuarios_Servicios.id_usuario == id_usuario).all()

    
    def obtener_por_servicio(self, db: Session, id_servicio: str): return db.query(Usuarios_Servicios).options( joinedload(Usuarios_Servicios.usuario), joinedload(Usuarios_Servicios.servicio) ).filter(Usuarios_Servicios.id_servicio == id_servicio).all()
    

    def obtener_todos(self, db: Session):
        return db.query(Usuarios_Servicios).options(
            joinedload(Usuarios_Servicios.usuario),
            joinedload(Usuarios_Servicios.servicio)
        ).all()
    
    def asociar_usuario_servicio(self, db: Session, id_usuario: str, id_servicio: str): 
        # Verificar si el servicio ya tiene un creador 
        servicio_existente = db.query(Usuarios_Servicios).filter_by(id_servicio=id_servicio, rol='vendedor').first() 
        if servicio_existente: 
            rol = 'consumidor' 
        else: 
            rol = 'vendedor' 
            
            nuevo_usuarios_servicios = Usuarios_Servicios( 
                id_usuario=id_usuario, 
                id_servicio=id_servicio, 
                rol=rol ) 
            
            db.add(nuevo_usuarios_servicios) 
            db.commit() 
            return nuevo_usuarios_servicios
        
    def asociar_usuario_servicio_nuevo(self, db: Session, id_usuario: str, id_servicio: str, rol: str = 'consumidor'): 
   
            nuevo_usuarios_servicios = Usuarios_Servicios( id_usuario=id_usuario, id_servicio=id_servicio, rol=rol ) 
            db.add(nuevo_usuarios_servicios) 
            db.commit() 
            return nuevo_usuarios_servicios 
       
    
    def desasociar_usuario_servicio(self, db: Session, id_usuario: str, id_servicio: str):
        relacion = self.obtener_uno(db, id_usuario, id_servicio)
        
        if not relacion:
            raise HTTPException(status_code=404, detail="Relación no encontrada")
        
        db.delete(relacion)
        db.commit()
        return {"message": "Relación desasociada"}
    
class PedidosConsulta():
    
    def __init__(self, instancia_db):
        self.instancia_db = instancia_db
    
    def obtener_uno(self, db: Session, id_pedido: str):
        return db.query(Pedidos).filter(Pedidos.id_pedido == id_pedido).first()
    
    def obtener_todos(self, db: Session):
        return db.query(Pedidos).all()
    
    def crear_pedido(self, db: Session, pedido: Pedido):
        nuevo_pedido = Pedidos(
            id_usuario_comprador=pedido.id_usuario_comprador,
            id_usuario_vendedor=pedido.id_usuario_vendedor,
            id_servicio=pedido.id_servicio,
            estado_pedido=pedido.estado_pedido,
            detalles=pedido.detalles,            # Si se define en Pedido
            precio_acordado=pedido.precio_acordado  # Si se define en Pedido
        )
        db.add(nuevo_pedido)
        db.commit()
        return nuevo_pedido
 
    def modificar_pedido(self, db: Session, id_pedido: str, pedido: PedidoModificacion):
        objeto_actual = self.obtener_uno(db, id_pedido)
        
        if objeto_actual:
            for key, value in pedido.dict(exclude_unset=True).items():
                setattr(objeto_actual, key, value)
            db.commit()
            db.refresh(objeto_actual)
            return objeto_actual
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    def eliminar_pedido(self, db: Session, id_pedido: str):
        pedido = self.obtener_uno(db, id_pedido)
        
        if pedido:
            pedido.estado_pedido = 0  # Asignar el estado de baja lógica
            pedido.fecha_entrega = datetime.now()  # Registrar la fecha de baja
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
        
        return {"message": "Pedido marcado como eliminado"}


class TransaccionesConsulta():
    
    def __init__(self, instancia_db):
        self.instancia_db = instancia_db
    
    def obtener_uno(self, db: Session, id_transaccion: str):
        return db.query(Transacciones).filter(Transacciones.id_transaccion == id_transaccion).first()
    
    def obtener_todos(self, db: Session):
        return db.query(Transacciones).all()
    
    def crear_transaccion(self, db: Session, transaccion: Transaccion):
        nueva_transaccion = Transacciones(
            id_usuario_comprador=transaccion.id_usuario_comprador,
            id_usuario_vendedor=transaccion.id_usuario_vendedor,
            monto=transaccion.monto,
            fecha_pago=transaccion.fecha_pago,
            metodo_pago=transaccion.metodo_pago,
        )
        db.add(nueva_transaccion)
        db.commit()
        return nueva_transaccion
    
    def modificar_transaccion(self, db: Session, id_transaccion: str, transaccion: TransaccionModificacion):
        objeto_actual = self.obtener_uno(db, id_transaccion)
        
        if objeto_actual:
            for key, value in transaccion.dict(exclude_unset=True).items():
                setattr(objeto_actual, key, value)
            db.commit()
            db.refresh(objeto_actual)
            return objeto_actual
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    
    def eliminar_transaccion(self, db: Session, id_transaccion: str):
        transaccion = self.obtener_uno(db, id_transaccion)
        
        if transaccion:
            transaccion.estado_transaccion = 0  # Asignar el estado de baja lógica
            transaccion.fecha_pago_realizado = datetime.now()  # Registrar la fecha de baja
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="Transacción no encontrada")
        
        return {"message": "Transacción marcada como eliminada"}


class ValoracionesConsulta():
    
    def __init__(self, instancia_db):
        self.instancia_db = instancia_db
    
    def obtener_uno(self, db: Session, id_valoracion: str):
        return db.query(Valoraciones).filter(Valoraciones.id_valoracion == id_valoracion).first()
    
    def obtener_todos(self, db: Session):
        return db.query(Valoraciones).all()
    
    def crear_valoracion(self, db: Session, valoracion: Valoracion):
        # Validar que la puntuación esté entre 1 y 5
        if valoracion.puntuacion < 1 or valoracion.puntuacion > 5:
            raise HTTPException(status_code=400, detail="La puntuación debe estar entre 1 y 5")
        
        nueva_valoracion = Valoraciones(
            id_usuario_valorador=valoracion.id_usuario_valorador,
            id_usuario_valorado=valoracion.id_usuario_valorado,
            puntuacion=valoracion.puntuacion,
            comentario=valoracion.comentario,
            estado_valoracion=valoracion.estado_valoracion
        )
        db.add(nueva_valoracion)
        db.commit()
        return nueva_valoracion
    
    def modificar_valoracion(self, db: Session, id_valoracion: str, valoracion: ValoracionModificacion):
        objeto_actual = self.obtener_uno(db, id_valoracion)
        
        if objeto_actual:
            # Validar que la puntuación esté entre 1 y 5
            if valoracion.puntuacion is not None and (valoracion.puntuacion < 1 or valoracion.puntuacion > 5):
                raise HTTPException(status_code=400, detail="La puntuación debe estar entre 1 y 5")
            
            # Verificar que el estado de la valoración es activo antes de modificarla
            if objeto_actual.estado_valoracion == 0:  # Si está eliminada, no se puede modificar
                raise HTTPException(status_code=400, detail="No se puede modificar una valoración eliminada")
            
            for key, value in valoracion.dict(exclude_unset=True).items():
                setattr(objeto_actual, key, value)
            db.commit()
            db.refresh(objeto_actual)
            return objeto_actual
        raise HTTPException(status_code=404, detail="Valoración no encontrada")
    
    def eliminar_valoracion(self, db: Session, id_valoracion: str):
        valoracion = self.obtener_uno(db, id_valoracion)
        
        if valoracion:
            valoracion.estado_valoracion = 0  # Asignar el estado de baja lógica (valoración eliminada)
            valoracion.fecha_baja_valoracion = datetime.now()  # Registrar la fecha de baja
            db.commit()
        else:
            raise HTTPException(status_code=404, detail="Valoración no encontrada")
        
        return {"message": "Valoración marcada como eliminada"}
    
    
    def obtener_promedio_valoracion(self, db: Session, id_usuario_valorado: str):
        """
        Obtiene el promedio de puntuaciones de un usuario.
        """
        result = db.query(func.avg(Valoraciones.puntuacion)) \
            .filter(Valoraciones.id_usuario_valorado == id_usuario_valorado, 
                    Valoraciones.estado_valoracion == 1).first()  # Solo valoraciones activas (estado = 1)
        
        if result[0]:
            return round(result[0], 2)  # Redondeamos a dos decimales
        return 0  # Si no hay valoraciones, devolver 0