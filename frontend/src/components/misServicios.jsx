// MisServicios.jsx
import React, { useState, useEffect } from "react";
import { ServiceCard } from "./ServiceCard";
import { useSelector } from "react-redux";
import { useLocation } from "react-router-dom";


export function MisServicios() {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
const location = useLocation();
const usuario = location.state || {};
const user = useSelector((state) => state.user.user);

// Si no viene usuario desde location, usamos el logueado
const idUsuario = usuario.id_usuario || user?.id;

useEffect(() => {
  if (!idUsuario) return; // Evitar fetch si no hay id
  const fetchServices = async () => {
    try {
      const res = await fetch(`http://127.0.0.1:8000/v1/usuarios-servicios/?id_usuario=${idUsuario}`);
      if (!res.ok) throw new Error("Error al traer los servicios");
      const data = await res.json();
      const validData = data.filter((s) => s.id_servicio);
      setServices(validData);
    } catch (error) {
      console.error("Error cargando servicios:", error);
    } finally {
      setLoading(false);
    }
  };
  fetchServices();
}, [idUsuario]);

  const handleDelete = (serviceId) => {
    setServices((prev) => prev.filter((s) => s.id_servicio !== serviceId));
  };

  const handleEdit = (service) => {
    console.log("Editar servicio:", service);
    // acá podrías abrir un modal o redirigir a un formulario
  };

  if (loading) {
    return <p className="text-center mt-10 text-gray-500">Cargando servicios...</p>;
  }

  return (
    <div className="max-w-6xl mx-auto mt-20 p-6">
      {/* Encabezado */}
      <div className="flex justify-between items-center mb-8">
        <h2 className="text-3xl font-bold text-azulOscuro">Mis Trabajos</h2>
        <button
          className="bg-azulBrillante text-white px-5 py-2 rounded-md shadow hover:bg-azulOscuro transition"
        >
          Crear Nuevo Servicio
        </button>
      </div>

      {/* Grid de servicios */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {services.length === 0 ? (
          <p className="col-span-3 text-center text-gray-500">
            No tienes servicios creados todavía.
          </p>
        ) : (
          services.map((service) => (
            <div
              key={service.id_servicio}
              className="bg-white border rounded-lg shadow-lg p-4 flex flex-col items-center"
            >
              {/* Card visual */}
              <ServiceCard
                id_servicio={service.id_servicio}

                //
                image={service.foto || "src/img/default.png"}
                username={`${service.nombre_usuario} ${service.apellido_usuario}`}
                serviceName={service.nombre_servicio}
                price={service.precio_servicio}
              />

              {/* Botones de acción */}
              <div className="flex space-x-3 mt-4">
                <button
                  onClick={() => handleEdit(service)}
                  className="bg-blue-500 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition"
                >
                  Editar
                </button>
                <button
                  onClick={() => handleDelete(service.id_servicio)}
                  className="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-700 transition"
                >
                  Eliminar
                </button>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
}
