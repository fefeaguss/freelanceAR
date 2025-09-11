import React from "react";
import { ServiceCard } from "./ServiceCard";
import { useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import useFetchServices from "../api/fetchServicesCard";

export function Principal() {
  const user = useSelector((state) => state.user.user);
  const { services, loading, error } = useFetchServices();
 const dispatch = useDispatch();
  if (loading) {
  return (
    <div className="flex justify-center items-center h-screen">
      <div className="animate-spin rounded-full h-12 w-12 border-t-4 border-azulBrillante"></div>
    </div>
  );
}
  if (error)
    return <p className="text-center text-red-500 mt-8">Error: {error}</p>;

  return (
    <main className="flex flex-col items-center w-full min-h-screen bg-azulClaro text-gray-800">
      {/* Sección de Bienvenida */}
      <section className="relative w-full mb-8 text-center">
        <div>
          <img
            src="src/assets/fondo.png"
            className="w-full h-auto object-cover"
            alt="Imagen de fondo"
          />
        </div>

        {/* Contenido superpuesto apenas sobre la parte inferior de la imagen */}
        <div className="absolute bottom-[-100px] left-1/2 transform -translate-x-1/2 bg-white w-3/4 p-6 rounded-lg shadow-lg">
          <h1 className="text-4xl font-extrabold text-yellow-400 mb-4">
            Bienvenido a FreelanceAR, {user ? user.nombre : "Invitado"}!
          </h1>
          <p className="text-xl text-azulOscuro">
            Aquí tienes algunos servicios que ofrecemos para ayudarte a
            encontrar el talento adecuado.
          </p>
        </div>
      </section>

      {/* Servicios en cuadrícula */}
      <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-screen-lg mt-40 ">
        {services.map((service) => (
          <div
            key={service.id_servicio}
            className="bg-white shadow-lg rounded-lg overflow-hidden flex flex-col h-72 items-center mx-4"
          >
            <ServiceCard
              id_usuario={service.id_usuario} // <-- Asegurar que se pasa el id_usuario
              id_servicio={service.id_servicio} // <-- Asegurar que se pasa el id_servicio
              image={service.image}
              username={service.nombre_usuario}
              serviceName={service.nombre_servicio}
              price={service.precio_servicio}
            />
          </div>
        ))}
      </section>
    </main>
  );
}
