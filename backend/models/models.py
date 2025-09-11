from sqlalchemy import Column, ForeignKey, Integer, String, DECIMAL, DateTime, func
from sqlalchemy.orm import relationship
from sqlalchemy.schema import CheckConstraint
import uuid

from providers.database import iniciar_conexion

engine, SessionLocal, Base = iniciar_conexion()


class Usuarios(Base):
    __tablename__ = "usuarios"
    
    id_usuario = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    mail = Column(String(250), unique=True, index=True)
    contraseña = Column(String(250))
    nombre = Column(String(250), nullable=True)
    apellido = Column(String(250), nullable=True)
    direccion = Column(String(250), nullable=True)
    idioma = Column(String(250), nullable=True) 
    descripcion = Column(String(500), nullable=True)
    username = Column(String(250), nullable=True)
    fecha_alta_usuario = Column(DateTime, server_default=func.now())
    fecha_baja_usuario = Column(DateTime, default=None)
    estado_usuario = Column(Integer, default=1)
    foto_usuario = Column(String(), nullable=True)
    
    servicios = relationship("Usuarios_Servicios", back_populates="usuario")
    mensajes_enviados = relationship("Mensajes", foreign_keys="[Mensajes.id_usuario_envia]", back_populates="usuario_envia")
    mensajes_recibidos = relationship("Mensajes", foreign_keys="[Mensajes.id_usuario_recibe]", back_populates="usuario_recibe")
    transacciones_comprador = relationship("Transacciones", foreign_keys="[Transacciones.id_usuario_comprador]", back_populates="usuario_comprador")
    transacciones_vendedor = relationship("Transacciones", foreign_keys="[Transacciones.id_usuario_vendedor]", back_populates="usuario_vendedor")
    valoraciones_hechas = relationship("Valoraciones", foreign_keys="[Valoraciones.id_usuario_valorador]", back_populates="usuario_valorador")
    valoraciones_recibidas = relationship("Valoraciones", foreign_keys="[Valoraciones.id_usuario_valorado]", back_populates="usuario_valorado")
    pedidos_comprador = relationship("Pedidos", foreign_keys="[Pedidos.id_usuario_comprador]", back_populates="usuario_comprador")
    pedidos_vendedor = relationship("Pedidos", foreign_keys="[Pedidos.id_usuario_vendedor]", back_populates="usuario_vendedor")
    archivos_adjuntos = relationship("Archivos_adjuntos", back_populates="usuario")

    # Relaciones con Conversaciones
    conversaciones_inicia = relationship("Conversaciones", foreign_keys="[Conversaciones.id_usuario_inicia]", back_populates="usuario_inicia")
    conversaciones_recibe = relationship("Conversaciones", foreign_keys="[Conversaciones.id_usuario_recibe]", back_populates="usuario_recibe")


class Categorias(Base):
    __tablename__ = "categorias"
    
    id_categoria = Column(Integer, primary_key=True)
    nombre_categoria = Column(String(200))
    
    servicios = relationship("Servicios", back_populates="categoria")


class Servicios(Base):
    __tablename__ = "servicios"
    
    id_servicio = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre_servicio = Column(String(250))
    descripcion_servicio = Column(String(500))
    precio = Column(DECIMAL(18, 2))
    id_categoria = Column(Integer, ForeignKey('categorias.id_categoria'))
    fecha_alta_servicio = Column(DateTime, server_default=func.now())
    fecha_baja_servicio = Column(DateTime, default=None)
    foto_servicio = Column(String, nullable=True)
    
    imagenes = relationship("ImagenesServicios", back_populates="servicio", cascade="all, delete-orphan")
    categoria = relationship("Categorias", back_populates="servicios")
    usuarios = relationship("Usuarios_Servicios", back_populates="servicio")
    pedidos = relationship("Pedidos", back_populates="servicio")
    archivos_adjuntos = relationship("Archivos_adjuntos", back_populates="servicio")
    
class Usuarios_Servicios(Base):
    __tablename__ = "usuarios_servicios"
    
    id_usuario = Column(String(36), ForeignKey('usuarios.id_usuario'), primary_key=True)
    id_servicio = Column(String(36), ForeignKey('servicios.id_servicio'), primary_key=True)
    rol = Column(String(50), nullable=False, default="vendedor")  # Ejemplo: 'owner', 'consumer'
    fecha_alta = Column(DateTime, server_default=func.now())
    estado = Column(Integer, default=1)
    
    usuario = relationship("Usuarios",foreign_keys=[id_usuario] ,back_populates="servicios")
    servicio = relationship("Servicios",foreign_keys=[id_servicio], back_populates="usuarios")



class Mensajes(Base):
    __tablename__ = "mensajes"
    
    id_mensaje = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_conversacion = Column(String(36), ForeignKey('conversaciones.id_conversacion'), nullable=False)  # 🔹 Nuevo campo
    id_usuario_envia = Column(String(36), ForeignKey('usuarios.id_usuario'))
    id_usuario_recibe = Column(String(36), ForeignKey('usuarios.id_usuario'))
    contenido_mensaje = Column(String(500))
    fecha_alta_mensaje = Column(DateTime, server_default=func.now())
    fecha_baja_mensaje = Column(DateTime, default=None)
    estado_mensaje = Column(Integer, default=1)
    
    usuario_envia = relationship("Usuarios", foreign_keys=[id_usuario_envia], back_populates="mensajes_enviados")
    usuario_recibe = relationship("Usuarios", foreign_keys=[id_usuario_recibe], back_populates="mensajes_recibidos")
    conversacion = relationship("Conversaciones", foreign_keys=[id_conversacion], back_populates="mensajes")  # 🔹 Relación



class Transacciones(Base):
    __tablename__="transacciones"
    
    id_transaccion = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_usuario_comprador = Column(String(36), ForeignKey('usuarios.id_usuario'))
    id_usuario_vendedor = Column(String(36), ForeignKey('usuarios.id_usuario'))
    monto = Column(DECIMAL(18, 2))
    estado_transaccion = Column(Integer, default=1 )
    fecha_pago = Column(DateTime, server_default=func.now())
    fecha_pago_realizado = Column(DateTime, default=None)
    metodo_pago = Column(String(60))

    usuario_comprador = relationship("Usuarios", foreign_keys=[id_usuario_comprador], back_populates="transacciones_comprador")
    usuario_vendedor = relationship("Usuarios", foreign_keys=[id_usuario_vendedor], back_populates="transacciones_vendedor")

    
class Valoraciones(Base):
    __tablename__ = "valoraciones"
    
    id_valoracion = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario_valorador = Column(String(36), ForeignKey('usuarios.id_usuario'))
    id_usuario_valorado = Column(String(36), ForeignKey('usuarios.id_usuario'))
    
    # Se modifica la columna 'puntuacion' para permitir valores entre 1 y 5
    puntuacion = Column(Integer, nullable=False)
    
    comentario = Column(String(300))
    fecha_alta_valoracion = Column(DateTime, server_default=func.now())
    fecha_baja_valoracion = Column(DateTime, default=None)
    estado_valoracion = Column(Integer, default=1)
    
    # Añadimos una restricción para que la puntuación esté entre 1 y 5
    __table_args__ = (
        CheckConstraint('puntuacion >= 1 AND puntuacion <= 5', name='check_puntuacion'),
    )

    usuario_valorador = relationship("Usuarios", foreign_keys=[id_usuario_valorador], back_populates="valoraciones_hechas")
    usuario_valorado = relationship("Usuarios", foreign_keys=[id_usuario_valorado], back_populates="valoraciones_recibidas")

class Pedidos(Base):
    __tablename__ = "pedidos"
    
    id_pedido = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_usuario_comprador = Column(String(36), ForeignKey('usuarios.id_usuario'))
    id_usuario_vendedor = Column(String(36), ForeignKey('usuarios.id_usuario'))
    id_servicio = Column(String(36), ForeignKey('servicios.id_servicio'))
    estado_pedido = Column(Integer, default=1)  # Podría usarse un ENUM para estados definidos
    fecha_alta_pedido = Column(DateTime, server_default=func.now())
    fecha_entrega = Column(DateTime, nullable=True)  # Fecha límite de entrega
    detalles = Column(String(500), nullable=True)  # Descripción adicional del pedido
    precio_acordado = Column(DECIMAL(18, 2), nullable=True)  # Precio final acordado para el pedido
    
    usuario_comprador = relationship("Usuarios", foreign_keys=[id_usuario_comprador], back_populates="pedidos_comprador")
    usuario_vendedor = relationship("Usuarios", foreign_keys=[id_usuario_vendedor], back_populates="pedidos_vendedor")
    servicio = relationship("Servicios", back_populates="pedidos")


class Archivos_adjuntos(Base):
    __tablename__ = "archivos_adjuntos"
    
    id_archivo = Column(Integer, primary_key=True, autoincrement=True)
    id_usuario = Column(String(36), ForeignKey('usuarios.id_usuario'))
    id_servicio = Column(String(36), ForeignKey('servicios.id_servicio'))
    nombre_archivos = Column(String(100))
    extension = Column(String(5))
    formato = Column(String(200))
    fecha_alta_archivo = Column(DateTime, server_default=func.now())
    fecha_baja_archivo = Column(DateTime, default=None)
    
    usuario = relationship("Usuarios", back_populates="archivos_adjuntos")
    servicio = relationship("Servicios", back_populates="archivos_adjuntos")
    
class ImagenesServicios(Base):
    __tablename__ = "imagenes_servicios"
    
    id_imagen = Column(Integer, primary_key=True, autoincrement=True)
    id_servicio = Column(String(36), ForeignKey('servicios.id_servicio'))
    url_imagen = Column(String(300), nullable=False)  # URL donde se guarda la imagen
    fecha_alta = Column(DateTime, server_default=func.now())

    servicio = relationship("Servicios", back_populates="imagenes")


class Conversaciones(Base):
    __tablename__ = "conversaciones"

    id_conversacion = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id_usuario_inicia = Column(String(36), ForeignKey('usuarios.id_usuario'), nullable=False)
    id_usuario_recibe = Column(String(36), ForeignKey('usuarios.id_usuario'), nullable=False)
    fecha_alta_conversacion = Column(DateTime, nullable=False, server_default=func.now())

    usuario_inicia = relationship("Usuarios", foreign_keys=[id_usuario_inicia], back_populates="conversaciones_inicia")
    usuario_recibe = relationship("Usuarios", foreign_keys=[id_usuario_recibe], back_populates="conversaciones_recibe")
    mensajes = relationship("Mensajes", back_populates="conversacion", cascade="all, delete-orphan")


