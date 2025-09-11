import { useState, useEffect } from "react";
import { useUser } from "../context/UserContext";
import { crearServicio, obtenerCategorias } from "../api/fetchCrearServicio";

export function CreateServicePage() {
  const { user } = useUser();
  const [nombre, setNombre] = useState("");
  const [descripcion, setDescripcion] = useState("");
  const [precio, setPrecio] = useState("");
  const [imagenes, setImagenes] = useState([]);
  const [categorias, setCategorias] = useState([]);
  const [idCategoria, setIdCategoria] = useState("");

  useEffect(() => {
    async function cargarCategorias() {
      const response = await obtenerCategorias();
      if (response.success) {
        setCategorias(response.data);
      } else {
        alert("Error al cargar categorías");
      }
    }
    cargarCategorias();
  }, []);

  const handleImageChange = (e) => {
    const files = Array.from(e.target.files);
    const newImages = files.map((file) => ({
      file,
      preview: URL.createObjectURL(file),
    }));

    setImagenes((prevImages) => [...prevImages, ...newImages]);
  };

  const handleRemoveImage = (index) => {
    setImagenes((prevImages) => prevImages.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!user || !user.id) {
      alert("Error: No se ha encontrado el usuario. Inicia sesión nuevamente.");
      return;
    }

    if (!idCategoria) {
      alert("Por favor, selecciona una categoría");
      return;
    }

    const response = await crearServicio({
      nombre,
      descripcion,
      precio,
      id_usuario: user.id,
      id_categoria: idCategoria, // Enviar el id de la categoría
      imagenes,
    });

    if (response.success) {
      alert("Servicio creado con éxito");
      setNombre("");
      setDescripcion("");
      setPrecio("");
      setImagenes([]);
      setIdCategoria("");
    } else {
      alert(`Error: ${response.message}`);
    }
  };

  return (
    <div className="flex flex-row max-w-5xl mx-auto mt-20 space-x-6">
      <div className="flex-1 w-2/3 p-6 bg-white border border-gray-300 rounded-lg shadow-md">
        <h2 className="text-3xl font-bold mb-6">Crear Servicio</h2>
        <form onSubmit={handleSubmit} className="flex flex-col space-y-4">
          <label className="block">
            <span className="text-gray-700 font-semibold">Nombre del servicio:</span>
            <input
              type="text"
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              required
              className="w-full mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-azulOscuro"
            />
          </label>

          <label className="block">
            <span className="text-gray-700 font-semibold">Descripción:</span>
            <textarea
              value={descripcion}
              onChange={(e) => setDescripcion(e.target.value)}
              required
              className="w-full mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-azulOscuro"
            ></textarea>
          </label>

          <label className="block">
            <span className="text-gray-700 font-semibold">Precio (US$):</span>
            <input
              type="number"
              value={precio}
              onChange={(e) => setPrecio(e.target.value)}
              required
              className="w-full mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-azulOscuro"
            />
          </label>

          <label className="block">
            <span className="text-gray-700 font-semibold">Categoría:</span>
            <select
              value={idCategoria}
              onChange={(e) => setIdCategoria(e.target.value)}
              required
              className="w-full mt-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-azulOscuro"
            >
              <option value="">Selecciona una categoría</option>
              {categorias.map((categoria) => (
                <option key={categoria.id_categoria} value={categoria.id_categoria}>
                  {categoria.nombre_categoria}
                </option>
              ))}
            </select>
          </label>

          <label className="block">
            <span className="text-gray-700 font-semibold">Imágenes:</span>
            <input type="file" multiple onChange={handleImageChange} className="mt-1" />
          </label>

          <button
            type="submit"
            className="bg-azulOscuro text-white py-2 px-4 rounded-md hover:bg-azulBrillante transition duration-200"
          >
            Crear Servicio
          </button>
        </form>
      </div>

      <div className="w-1/3 bg-white p-4 border border-gray-300 rounded-lg shadow-md">
        <h3 className="text-xl font-bold mb-4">Vista Previa</h3>
        <div className="grid grid-cols-2 gap-2">
          {imagenes.length > 0 ? (
            imagenes.map((img, index) => (
              <div key={index} className="relative flex flex-col items-center">
                <img
                  src={img.preview}
                  alt={`Preview ${index}`}
                  className="w-full h-auto object-cover rounded-md "
                />
                <button
                  onClick={() => handleRemoveImage(index)}
                  className="mt-2 bg-red-500 text-white text-sm py-1 px-2 rounded-md hover:bg-red-600 transition duration-200"
                >
                  Eliminar
                </button>
              </div>
            ))
          ) : (
            <p className="text-gray-500 text-center col-span-2">No hay imágenes seleccionadas</p>
          )}
        </div>
      </div>
    </div>
  );
}
