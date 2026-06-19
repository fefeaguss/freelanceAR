import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useSelector, useDispatch } from "react-redux";
import { logout } from "../Context/userSlice";
import MessagesMenu from "./MessagesMenu";
import { SearchBar } from "./SearchBar";

export function Headers() {
  const user = useSelector((state) => state.user.user);
  const dispatch = useDispatch();
  const [isDropDownOpen, setIsDropdownOpen] = useState(false);
  const [isMessagesOpen, setIsMessagesOpen] = useState(false);
  const navigate = useNavigate();
  const [query, setQuery] = useState("");
  const [results, setResults] = useState({perfiles: [], servicios: []}); // 🔹 para almacenar resultados de búsqueda


  const toggledDropdown = () => setIsDropdownOpen(!isDropDownOpen);
  const toggleMessages = () => setIsMessagesOpen(!isMessagesOpen);

  const handleGetStarted = () => navigate("/login-register");
  const handleClickMisTrabajos = () => navigate("/Mis-servicios");

  const cerrarSesion = () => {
    dispatch(logout());
    navigate("/");
  };

  const handleGetPrincipal = () => {
    if (user) navigate("/principal");
  };

  const handleProfileClick = () => {
    navigate("/user-profile", { state: { usuario: user } });
  };

  const handleSearch = async () => {
    if (!query.trim()) return;

    try {
      const response = await fetch(`http://localhost:8000/v1/buscar?query=${query}`);
      if (!response.ok) throw new Error("Error en la búsqueda");
      const data = await response.json();
      setResults(data); // 🔹 guarda perfiles y servicios
    } catch (error) {
      console.error("Error buscando:", error);
    }
  };

  const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

  return (
    <header className="flex justify-between bg-azulClaro fixed top-0 left-0 h-18 w-full p-4 z-50 text-white items-center">
      {/* LOGO */}
      <div className="flex-none flex items-center text-blue-900 w-44 p-2 h-16">
        <img
          onClick={handleGetPrincipal}
          src="/src/assets/ChatGPT Image 16 sept 2025, 19_06_10.png"
          alt="Logo de la página"
          className="h-auto w-auto cursor-pointer"
        />
      </div>

      {/* BARRA DE BÚSQUEDA */}
      <SearchBar></SearchBar>

      {/* MENSAJES Y PERFIL */}
      <div className="relative flex items-center space-x-4 text-azulOscuro p-3 cursor-pointer h-16 -mr-4">
        {user ? (
          <>
            {/* BOTÓN DE MENSAJES */}
            <div className="relative">
              <img
                src="src/assets/chat_40dp_1F375B_FILL0_wght400_GRAD0_opsz40.png"
                alt="Mensajes"
                className="h-8 w-8 cursor-pointer"
                onClick={toggleMessages}
              />
            </div>

            {/* MENÚ DE MENSAJES */}
            {isMessagesOpen && <MessagesMenu isMessagesOpen={isMessagesOpen} />}

            {/* NOMBRE Y FOTO DEL USUARIO */}
            <span className="font-semibold text-azulOscuro">{user.nombre}</span>
            <img
              src={user.foto ? `${API_URL}${user.foto}` : "/assets/user.png"}
              alt="Imagen de usuario"
              className="h-12 w-12 rounded-full"
              onClick={toggledDropdown}
            />

            {/* MENÚ DESPLEGABLE */}
            {isDropDownOpen && (
              <div className="w-56 absolute top-full -right-52 -translate-x-full mt-2 bg-azulClaro rounded-md shadow-lg z-50 text-left text-azulOscuro">
                <h2 className="text-lg font-semibold px-4">Mi Perfil</h2>
                <p className="px-4">Nombre: {user.nombre}</p>
                <p className="px-4">Correo: {user.mail}</p>
                <h3 className="text-sm font-medium px-4 mt-2">Opciones:</h3>
                <ul className="text-sm">
                  <li
                    className="px-4 py-2 hover:bg-azulBrillante cursor-pointer"
                    onClick={handleProfileClick}
                  >
                    Ver perfil
                  </li>
                  <li
                    className="px-4 py-2 hover:bg-azulBrillante cursor-pointer"
                    onClick={handleClickMisTrabajos}
                  >
                    Mis trabajos
                  </li>
                  <li className="px-4 py-2 hover:bg-azulBrillante cursor-pointer">
                    Configuraciones
                  </li>
                  <li
                    className="px-4 py-2 hover:bg-azulBrillante cursor-pointer"
                    onClick={cerrarSesion}
                  >
                    Cerrar sesión
                  </li>
                </ul>
              </div>
            )}
          </>
        ) : (
          <button
            className="bg-azulBrillante text-white py-2 px-4 rounded-full hover:bg-azulOscuro"
            onClick={handleGetStarted}
          >
            Get Started
          </button>
        )}
      </div>
    </header>
  );
}
