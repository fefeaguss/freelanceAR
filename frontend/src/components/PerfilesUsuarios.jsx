import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { FaStar, FaMapMarkerAlt, FaGlobe, FaPaperPlane } from "react-icons/fa";
import { ServiceCard } from "./ServiceCard"; // Importa el componente de tarjetas
import useFetchServices from "../api/fetchServicesCard";
import { useUser } from "../context/UserContext";
import { useSelector } from "react-redux";

export function PerfilUsuario() {
  const location = useLocation();
  const navigate = useNavigate();
  const { usuario } = location.state || {}; // Usuario seleccionado
  const user = useSelector((state) => state.user.user); // Usuario logueado
  const { services, loading, error } = useFetchServices(); // Hook personalizado para obtener los servicios
  const [filteredServices, setFilteredServices] = useState([]);

  
  const [promedio, setPromedio] = useState(null);

  useEffect(() => {
    // Limpia los servicios cuando cambia el usuario o los servicios
    setFilteredServices([]);
  
    if (services.length > 0 && usuario?.id_usuario) {
      const serviciosUsuario = services.filter(
        (service) => service.id_usuario === usuario.id_usuario
      );
      setFilteredServices(serviciosUsuario);
    }
  }, [services, usuario?.id_usuario]);
  
  
  const usuarioFinal = {
    nombre_usuario: usuario?.nombre_usuario || user?.nombre,
    apellido_usuario: usuario?.apellido_usuario || user?.apellido,
    descripcion_usuario: usuario?.descripcion_usuario || user?.descripcion,
    foto_final: usuario?.foto || user?.foto,
  };

  useEffect(() => {
    const fetchPromedio = async () => {
      if (!usuario?.id_usuario) return;
      try {
        const response = await fetch(
          `http://localhost:8000/v1/valoraciones/promedio?id_usuario_valorado=${usuario.id_usuario}`
        );
        const data = await response.json();
        setPromedio(data.promedio);
      } catch (error) {
        console.error("Error al obtener el promedio de valoraciones:", error);
      }
    };

    fetchPromedio();
  }, [usuario.id_usuario]);

  const handleComunicarse = async () => {
    if (!user || !usuario?.id_usuario) {
      console.error("Usuario no definido o ID de usuario receptor inválido");
      return;
    }

    console.log("Datos enviados al servidor:", {
      id_usuario_inicia: user.id,
      id_usuario_recibe: usuario.id_usuario,
    });

    try {
      const response = await fetch("http://localhost:8000/v1/mensajes/crear_conversacion", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          id_usuario_inicia: user.id,
          id_usuario_recibe: usuario.id_usuario,
        }),
      });
      const data = await response.json();
      console.log("Respuesta del servidor:", data);

      const idConversacion = data.id_conversacion;

      navigate(`/Chat`, { state: { idConversacion } });
    } catch (error) {
      console.error(
        "Error al crear o unirse a la conversación:",
        error
      );
    }
  };

  if (!usuario) {
    return <div>Error: No se pudo cargar la información del usuario.</div>;
  }

  return (
    <div className="container mx-auto mt-12 p-6 max-w-4xl rounded-lg">
      {/* Contenedor de perfil con dos columnas */}
      <div className="flex items-center justify-between gap-6">
        {/* Imagen + info del usuario */}
        <div className="flex flex-row items-center gap-6">
          {/* Imagen de perfil */}
          <div className="w-28 h-28 flex-shrink-0">
            <img
              src={`http://localhost:8000${usuarioFinal.foto_final || "/assets/default-avatar.jpg"}`}
              alt="Foto de perfil"
              className="w-full h-full rounded-full border border-gray-300 object-cover shadow-md"
            />
          </div>

          {/* Información del usuario */}
          <div className="flex flex-col">
            <h1 className="text-2xl font-bold">{usuarioFinal.nombre_usuario} {usuarioFinal.apellido_usuario}</h1>

            {/* Calificación */}
            {promedio !== null ? (
              <p className="text-yellow-500 flex items-center font-medium text-lg mt-1">
                <FaStar className="mr-1" /> {promedio.toFixed(1)}
                <span className="text-gray-500 ml-2">(valoraciones promedio)</span>
              </p>
            ) : (
              <p className="text-gray-500">Sin valoraciones aún</p>
            )}

            {/* Ubicación e idiomas */}
            <p className="text-sm text-gray-700 flex items-center mt-2">
              <FaMapMarkerAlt className="mr-2" /> {usuario.direccion || "No especificada"}
            </p>
            <p className="text-sm text-gray-700 flex items-center mt-1">
              <FaGlobe className="mr-2" /> {usuario.idioma || "No especificados"}
            </p>
          </div>
        </div>

        {/* Botón de contacto */}
        <button
          onClick={handleComunicarse}
          className="bg-black text-white px-6 py-3 rounded-lg flex items-center gap-2 shadow-md hover:bg-gray-800 transition"
        >
          <FaPaperPlane />
          Contáctame
        </button>
      </div>

      {/* Sección "Sobre mí" */}
      <div className="bg-gray-50 p-6 rounded-lg border border-gray-300 mt-6">
        <h2 className="text-xl font-bold mb-3">Sobre mí</h2>
        <p className="text-gray-700 text-sm leading-relaxed">
          {usuarioFinal.descripcion_usuario || "Este usuario aún no ha proporcionado una descripción personal."}
        </p>
      </div>

      {/* Servicios Ofrecidos */}
      <div className="bg-gray-50 p-6 rounded-lg border border-gray-300 mt-6">
        <h2 className="text-xl font-bold mb-3">Servicios Ofrecidos</h2>
        {loading ? (
          <p className="text-gray-500">Cargando servicios...</p>
        ) : error ? (
          <p className="text-red-500">{error}</p>
        ) : filteredServices.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredServices.map((servicio) => (
              <ServiceCard
                key={servicio.id_servicio}
                id_usuario={servicio.id_usuario}
                id_servicio={servicio.id_servicio}
                username={usuario.nombre_usuario}
                serviceName={servicio.nombre_servicio}
                price={servicio.precio_servicio}
              />
            ))}
          </div>
        ) : (
          <p className="text-gray-600">Este usuario aún no ha registrado servicios.</p>
        )}
      </div>
    </div>
  );
}
