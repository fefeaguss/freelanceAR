// ServicePage.jsx
import React, { useState } from "react";
import { CreateServiceCard } from "./CreateServiceCard";
import { ServiceCard } from "./ServiceCard";

export function MisServicios() {
  const [showCreateServiceCard, setShowCreateServiceCard] = useState(false);
  const [services, setServices] = useState([
    {
      id: 1,
      image: "src/img/freelancear-high-resolution-logo-transparent.png",
      username: "Usuario1",
      serviceName: "Servicio 1",
      price: 100,
    },
    {
      id: 2,
      image: "src/img/freelancear-high-resolution-logo.png",
      username: "Usuario2",
      serviceName: "Servicio 2",
      price: 200,
    },
  ]);
  const [editingService, setEditingService] = useState(null);

  const handleCreateServiceCard = () => {
    setShowCreateServiceCard(true);
  };

  const closeCreateServiceCard = () => {
    setShowCreateServiceCard(false);
    setEditingService(null);
  };

  const handleCreate = (newService) => {
    setServices((prev) => [...prev, newService]);
  };

  const handleEdit = (service) => {
    setEditingService(service);
    setShowCreateServiceCard(true);
  };

  const handleUpdate = (updatedService) => {
    setServices((prev) =>
      prev.map((s) => (s.id === updatedService.id ? updatedService : s))
    );
  };

  const handleDelete = (serviceId) => {
    setServices((prev) => prev.filter((s) => s.id !== serviceId));
  };

  return (
    <div className="max-w-6xl mx-auto mt-20 p-6">
      {/* Encabezado */}
      <div className="flex justify-between items-center mb-8">
        <h2 className="text-3xl font-bold text-azulOscuro">Mis Trabajos</h2>
        <button
          onClick={handleCreateServiceCard}
          className="bg-azulBrillante text-white px-5 py-2 rounded-md shadow hover:bg-azulOscuro transition"
        >
          Crear Nuevo Servicio
        </button>
      </div>

      {/* Grid de servicios */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {services.map((service) => (
          <div
            key={service.id}
            className="bg-white border rounded-lg shadow-lg p-4 flex flex-col items-center"
          >
            {/* Card visual */}
            <ServiceCard
              image={service.image}
              username={service.username}
              serviceName={service.serviceName}
              price={service.price}
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
                onClick={() => handleDelete(service.id)}
                className="bg-red-500 text-white px-4 py-2 rounded-md hover:bg-red-700 transition"
              >
                Eliminar
              </button>
            </div>
          </div>
        ))}
      </div>

      {/* Modal Crear/Editar */}
      {showCreateServiceCard && (
        <div className="fixed inset-0 bg-black bg-opacity-40 flex justify-center items-center z-50">
          <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-lg">
            <CreateServiceCard
              onClose={closeCreateServiceCard}
              onCreate={editingService ? handleUpdate : handleCreate}
              editingService={editingService}
            />
          </div>
        </div>
      )}
    </div>
  );
}
