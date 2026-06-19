import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import fetchServiceImages from "../api/fetchImagenes";

export function SearchBar() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState({ perfiles: [], servicios: [] });
  const [showDropdown, setShowDropdown] = useState(false);
  const navigate = useNavigate();

  const handleSearch = async (e) => {
  const value = e.target.value;
  setQuery(value);

  if (value.length > 0) {
    try {
      const res = await fetch(`http://localhost:8000/v1/buscar?query=${value}`);
      if (!res.ok) throw new Error("Error en la búsqueda");

      const data = await res.json();
      console.log("Resultados de búsqueda:", data);

      // 🔹 Agarramos servicios desde la respuesta
      const servicios = data.servicios || [];

      // 🔹 Traemos imágenes para cada servicio
      const serviciosConImagenes = await Promise.all(
        servicios.map(async (servicio) => {
          const imagenes = await fetchServiceImages(servicio.id_servicio);
          return {
            ...servicio,
            imagenes, // añadimos el array de imágenes
          };
        })
      );

      // 🔹 Guardamos perfiles y servicios
      setResults({
        perfiles: data.perfiles || [],
        servicios: serviciosConImagenes,
      });
      setShowDropdown(true);
    } catch (err) {
      console.error(err);
    }
  } else {
    setResults({ perfiles: [], servicios: [] });
    setShowDropdown(false);
  }
};

  

const handleSelectPerfil = (perfil) => {
 navigate("/perfil-usuario", { state: { usuario: perfil } });

};

  // 🔹 Servicio → pasa id_usuario e id_servicio por query params
  const handleSelectServicio = (servicio) => {
    navigate(`/service?id_usuario=${servicio.id_usuario}&id_servicio=${servicio.id_servicio}`);
    setShowDropdown(false);
    setQuery("");
  };

  return (
    <div className="relative w-1/3 mx-auto">
      {/* Barra de búsqueda */}
      <div className="flex items-center space-x-2 bg-gray-100 text-gray-900 rounded-full p-2 shadow-md">
        <input
          type="text"
          value={query}
          onChange={handleSearch}
          className="flex-grow p-1 rounded-full bg-transparent placeholder-azulOscuro focus:outline-none text-sm text-azulOscuro"
          placeholder="Buscar servicios..."
        />
        <img
          src="src/assets/search_24dp_2C75E0_FILL0_wght400_GRAD0_opsz24.png"
          alt="Buscar"
          className="h-5 w-5 cursor-pointer"
        />
      </div>

      {/* Dropdown flotante */}
      {showDropdown && (results.perfiles.length > 0 || results.servicios.length > 0) && (
        <div className="absolute top-full left-0 mt-2 bg-white rounded-lg shadow-lg border border-gray-200 w-full max-h-64 overflow-y-auto z-50">
          {results.perfiles.length > 0 && (
            <div className="p-2">
              <h3 className="text-xs font-bold text-gray-500 mb-1">Perfiles</h3>
              {results.perfiles.map((perfil) => (
                <div
                  key={perfil.id_usuario}
                  className="flex items-center p-2 hover:bg-gray-100 cursor-pointer rounded"
                  onClick={() => handleSelectPerfil(perfil)}
                >
                  <img
                    src={`http://localhost:8000${perfil.foto_usuario || "/assets/default-avatar.jpg"}`}
                    alt={perfil.nombre}
                    className="w-8 h-8 rounded-full object-cover mr-2"
                  />
                  <span className="font-medium">{perfil.nombre}</span>
                </div>
              ))}
            </div>
          )}
          {results.servicios.length > 0 && (
            <div className="p-2 border-t border-gray-200">
              <h3 className="text-xs font-bold text-gray-500 mb-1">Servicios</h3>
              {results.servicios.map((servicio) => (
                <div
                  key={servicio.id_servicio}
                  className="flex items-center p-2 hover:bg-gray-100 cursor-pointer rounded"
                  onClick={() => handleSelectServicio(servicio)}
                >
                  <img
                    src={
                      servicio.imagenes?.[0]?.url ||
                      "https://via.placeholder.com/40"
                    }
                    alt={servicio.nombre_servicio}
                    className="w-8 h-8 rounded object-cover mr-2"
                  />
                  <div>
                    <span className="font-medium">{servicio.nombre_servicio}</span>
                    <span className="text-sm text-gray-600 ml-2">
                      ${servicio.precio}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
