import React, { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import axios from "axios";

export function ModificarServicio() {
  const location = useLocation();
  const navigate = useNavigate();
  const { servicio } = location.state || {}; // Servicio recibido desde navigate

  // Estados para manejar los datos
  const [nombre, setNombre] = useState(servicio?.nombre_servicio || "");
  const [descripcion, setDescripcion] = useState(servicio?.descripcion_servicio || "");
  const [precio, setPrecio] = useState(servicio?.precio || "");
  const [idCategoria, setIdCategoria] = useState(servicio?.id_categoria || ""); // Añadir estado para categoría
  const [categorias, setCategorias] = useState([]); // Lista de categorías cargadas
  const [error, setError] = useState(null); // Estado para manejar errores

  // Cargar categorías al cargar el componente
  React.useEffect(() => {
    const fetchCategorias = async () => {
      try {
        const response = await axios.get("http://localhost:8000/v1/categorias"); // Ruta para obtener categorías
        setCategorias(response.data); // Guardar las categorías en el estado
      } catch (error) {
        console.error("Error al cargar las categorías:", error);
        setError("No se pudieron cargar las categorías.");
      }
    };
    fetchCategorias();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    const payload = {
      nombre_servicio: nombre,
      descripcion_servicio: descripcion,
      precio: parseFloat(precio), // Convertir precio a número flotante
      id_categoria: parseInt(idCategoria, 10) // Convertir id_categoria a entero
    };
  
    console.log("Datos enviados al servidor:", payload);
  
    try {
      await axios.put(`http://localhost:8000/v1/servicios/${servicio.id_servicio}`, payload);
      alert("Servicio modificado con éxito.");
      navigate("/mis-servicios");
    } catch (error) {
      console.error("Error al modificar el servicio:", error.response?.data || error.message);
      alert("Ocurrió un error al intentar modificar el servicio.");
    }
  };
  

  return (
    <div className="container mx-auto mt-8 p-6 max-w-4xl bg-white rounded-lg shadow-md">
      <h2 className="text-3xl font-bold text-azulOscuro mb-6">Modificar Servicio</h2>

      {error && <p className="text-red-500 mb-4">{error}</p>} {/* Mostrar errores */}

      <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
        <label>
          Nombre del Servicio:
          <input
            type="text"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            className="w-full border rounded-lg p-2"
          />
        </label>

        <label>
          Descripción:
          <textarea
            value={descripcion}
            onChange={(e) => setDescripcion(e.target.value)}
            className="w-full border rounded-lg p-2"
          />
        </label>

        <label>
          Precio:
          <input
            type="number"
            value={precio}
            onChange={(e) => setPrecio(e.target.value)}
            className="w-full border rounded-lg p-2"
          />
        </label>

        <label>
          Categoría:
          <select
            value={idCategoria}
            onChange={(e) => setIdCategoria(e.target.value)}
            className="w-full border rounded-lg p-2"
          >
            <option value="">Selecciona una categoría</option>
            {categorias.map((categoria) => (
              <option key={categoria.id_categoria} value={categoria.id_categoria}>
                {categoria.nombre_categoria}
              </option>
            ))}
          </select>
        </label>

        <button type="submit" className="bg-azulBrillante text-white py-2 px-4 rounded-lg hover:bg-azulOscuro transition">
          Guardar Cambios
        </button>
      </form>
    </div>
  );
}
