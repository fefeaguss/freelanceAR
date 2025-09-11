import React, { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { FaStar, FaMapMarkerAlt, FaGlobe, FaPaperPlane } from "react-icons/fa";
import { ServiceCard } from "./ServiceCard";
import useFetchServices from "../api/fetchServicesCard";
//import { useUser } from "../context/UserContext";
import { useSelector } from "react-redux";

export function UserProfile() {
  const location = useLocation();
  const navigate = useNavigate();

  const  user  = useSelector((state) => state.user); // Usuario logueado
  const { services, loading, error } = useFetchServices(); // Hook actualizado para obtener servicios
  const [filteredServices, setFilteredServices] = useState([]);
  const [promedio, setPromedio] = useState(null);

  // Usuario actual (viene del estado o del contexto)
  const usuario = location.state?.usuario || user; // Usa el usuario del estado o del contexto
  const userId = usuario?.id; // Obtén el ID del usuario

  useEffect(() => {
    if (services.length > 0 && userId) {
      // Filtra los servicios por el ID del usuario
      const serviciosUsuario = services.filter((service) => service.id_usuario === userId);
      setFilteredServices(serviciosUsuario);
    }
  }, [services, userId]);

  useEffect(() => {
    const fetchPromedio = async () => {
      if (!userId) return;
      try {
        const response = await fetch(
          `http://localhost:8000/v1/valoraciones/promedio?id_usuario_valorado=${userId}`
        );
        if (!response.ok) {
          throw new Error("Error al obtener el promedio");
        }
        const data = await response.json();
        setPromedio(data.promedio);
      } catch (error) {
        console.error("Error al obtener el promedio de valoraciones:", error);
      }
    };
    fetchPromedio();
  }, [userId]);

  const handleComunicarse = async () => {
    if (!user || !userId) {
      console.error("Usuario no definido o ID de usuario receptor inválido");
      return;
    }
    try {
      const response = await fetch("http://localhost:8000/v1/mensajes/crear_conversacion", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          id_usuario_inicia: user.id,
          id_usuario_recibe: userId,
        }),
      });
      const data = await response.json();
      navigate(`/Chat`, { state: { idConversacion: data.id_conversacion } });
    } catch (error) {
      console.error("Error al crear o unirse a la conversación:", error);
    }
  };

  if (loading) {
    return <p>Cargando perfil y servicios...</p>;
  }

  if (error) {
    return <p className="text-red-500">Error: {error}</p>;
  }

  return (
    <div className="container mx-auto mt-12 p-6 max-w-4xl rounded-lg">
      <div className="flex items-center justify-between gap-6">
        <div className="flex flex-row items-center gap-6">
          <div className="w-28 h-28 flex-shrink-0">
            <img
              src={`http://localhost:8000${usuario?.foto || "/assets/default-avatar.jpg"}`}
              alt="Foto de perfil"
              className="w-full h-full rounded-full border border-gray-300 object-cover shadow-md"
            />
          </div>
          <div className="flex flex-col">
            <h1 className="text-2xl font-bold">{usuario?.nombre} {usuario?.apellido}</h1>
            {promedio !== null ? (
              <p className="text-yellow-500 flex items-center font-medium text-lg mt-1">
                <FaStar className="mr-1" /> {promedio.toFixed(1)}
                <span className="text-gray-500 ml-2">(valoraciones promedio)</span>
              </p>
            ) : (
              <p className="text-gray-500">Sin valoraciones aún</p>
            )}
            <p className="text-sm text-gray-700 flex items-center mt-2">
              <FaMapMarkerAlt className="mr-2" /> {usuario?.direccion || "No especificada"}
            </p>
            <p className="text-sm text-gray-700 flex items-center mt-1">
              <FaGlobe className="mr-2" /> {usuario?.idioma || "No especificado"}
            </p>
          </div>
        </div>
        
      </div>
      <div className="bg-gray-50 p-6 rounded-lg border border-gray-300 mt-6">
        <h2 className="text-xl font-bold mb-3">Sobre mí</h2>
        <p className="text-gray-700 text-sm leading-relaxed">
          {usuario?.descripcion || "Este usuario aún no ha proporcionado una descripción personal."}
        </p>
      </div>
      <div className="bg-gray-50 p-6 rounded-lg border border-gray-300 mt-6">
        <h2 className="text-xl font-bold mb-3">Servicios Ofrecidos</h2>
        {filteredServices.length > 0 ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {filteredServices.map((servicio) => (
              <ServiceCard
                key={servicio.id_servicio}
                id_usuario={servicio.id_usuario}
                id_servicio={servicio.id_servicio}
                username={usuario?.nombre}
                serviceName={servicio.nombre_servicio}
                price={servicio.precio}
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
