import React, { useEffect, useState } from "react";
import { useNavigate, useLocation } from "react-router-dom";
import useFetchServices from "../api/fetchServicesDetail";
import fetchServiceImages from "../api/fetchImagenes";
//import { useUser } from "../context/UserContext";
import { useSelector } from "react-redux";

import axios from "axios";
import { FaChevronLeft, FaChevronRight } from "react-icons/fa";

export function ServiceDetailPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const user = useSelector((state) => state.user.user); // Usuario logueado

  const searchParams = new URLSearchParams(location.search);
  const id_usuario = searchParams.get("id_usuario");
  const id_servicio = searchParams.get("id_servicio");

  const { services, loading, error } = useFetchServices(
    id_usuario,
    id_servicio
  );
  const [promedio, setPromedio] = useState(null);
  const [imagenes, setImagenes] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0); // 🔹 Índice de la imagen actual

  const [selectedServiceUser, setSelectedServiceUser] = useState(null);

  useEffect(() => {
    const fetchPromedio = async () => {
      try {
        const response = await axios.get(
          `http://localhost:8000/v1/valoraciones/promedio?id_usuario_valorado=${services.id_usuario}`
        );
        setPromedio(response.data.promedio);
      } catch (error) {
        console.error("Error al obtener el promedio de valoraciones", error);
      }
    };

    fetchPromedio();
  }, [id_usuario]);

  useEffect(() => {
    const fetchImages = async () => {
      const imgs = await fetchServiceImages(id_servicio);
      setImagenes(imgs);
    };

    fetchImages();
  }, [id_servicio]);

  const handleNext = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % imagenes.length);
  };

  const handlePrev = () => {
    setCurrentIndex(
      (prevIndex) => (prevIndex - 1 + imagenes.length) % imagenes.length
    );
  };

  const handleImageClick = (index) => {
    setCurrentIndex(index);
  };

  const handleComunicarse = async () => {
    if (!user || !id_usuario) {
      console.error("Usuario no definido o ID de usuario receptor inválido");
      return;
    }

    console.log("ID usuario inicia:", user.id);
    console.log("ID usuario recibe:", id_usuario);

    try {
      const response = await axios.post(
        "http://localhost:8000/v1/mensajes/crear_conversacion",
        {
          id_usuario_inicia: user.id, // ID del usuario logueado
          id_usuario_recibe: id_usuario, // ID del vendedor del servicio
        }
      );
      console.log("Respuesta del servidor:", response.data);

      // Obtén el id_conversacion desde la respuesta del servidor
      const idConversacion = response.data.id_conversacion;

      // Navega al componente de chat y pasa el id_conversacion
      navigate(`/Chat`, { state: { idConversacion } });
    } catch (error) {
      console.error(
        "Error al crear o unirse a la conversación:",
        error.response?.data || error
      );
    }
  };

  // Verificamos si es el mismo usuario
  const isCurrentUser = user?.id === id_usuario;

  if (loading) return <div>Cargando...</div>;
  if (error) return <div>Error: {error}</div>;

  //ver perfil del usuario que brinda servicio
  const handlePerfil = () => {
    navigate("/perfil-usuario", {
      state: { usuario: services[0] }, // Pasa el proveedor del servicio
    });
  };

  return (
    <div className="flex flex-row max-w-5xl mx-auto mt-20 space-x-6">
      <div className="flex-1 w-2/3 p-4 bg-white border border-gray-300 rounded-lg">
        <h1 className="text-3xl font-bold mb-4 text-center">
          {services[0]?.nombre_servicio || "Servicio no encontrado"}
        </h1>

        <div className="flex items-center mt-4">
          <img
            src={`http://localhost:8000${services[0]?.foto}`}
            alt="Usuario"
            className="h-10 w-10 rounded-full"
          />
          <div className="-mt-3">
            <p className="text-lg font-semibold ml-3 mt-3">
              {services[0]?.nombre_usuario}
            </p>
            {promedio !== null && (
              <p className="text-sm text-gray-600 text-left ml-4">
                {promedio} ⭐
              </p>
            )}
          </div>
        </div>

        <div className="about-service mb-6">
          <h2 className="text-2xl font-bold mb-2">Acerca de este Servicio</h2>
          <p className="text-gray-700 mb-4">
            {services[0]?.descripcion_servicio}
          </p>
        </div>

        {/* 🔹 Contenedor de imagen con flechas */}
        <div className="relative w-full h-96 mb-4">
          {imagenes.length > 0 ? (
            <>
              <img
                src={`http://localhost:8000/${imagenes[currentIndex].url}`}
                alt="Imagen principal"
                className="w-full h-full object-contain rounded-lg shadow-md"
              />
              {/* 🔹 Flecha izquierda */}
              <button
                className="absolute top-1/2 left-2 transform -translate-y-1/2 bg-gray-700 text-white p-2 rounded-full shadow-md hover:bg-gray-900"
                onClick={handlePrev}
              >
                <FaChevronLeft size={20} />
              </button>
              {/* 🔹 Flecha derecha */}
              <button
                className="absolute top-1/2 right-2 transform -translate-y-1/2 bg-gray-700 text-white p-2 rounded-full shadow-md hover:bg-gray-900"
                onClick={handleNext}
              >
                <FaChevronRight size={20} />
              </button>
            </>
          ) : (
            <p>No hay imágenes disponibles</p>
          )}
        </div>

        {/* 🔹 Miniaturas de imágenes */}
        <div className="flex space-x-2 overflow-x-auto">
          {imagenes.map((imagen, index) => (
            <img
              key={index}
              src={`http://localhost:8000/${imagen.url}`}
              alt={`Miniatura ${index + 1}`}
              className={`w-20 h-20 object-cover rounded-lg cursor-pointer border-2 ${
                currentIndex === index ? "border-blue-500" : "border-gray-300"
              }`}
              onClick={() => handleImageClick(index)}
            />
          ))}
        </div>

        {/* 🔹 seccion de perfil de vendedor */}
        <div className="seller-info p-6 rounded-lg mt-12">
          {/* Título */}
          <h2 className="text-2xl font-bold mb-4 text-azulBrillante text-center">
            Conoce a {services[0]?.nombre_usuario}
          </h2>

          {/* Información del vendedor */}
          <div className="flex items-center mb-4">
            <img
              src={`http://localhost:8000${services[0]?.foto}`}
              alt="Vendedor"
              className="w-14 h-14 rounded-full mr-4 border border-gray-300"
            />
            <div>
              <p
                onClick={handlePerfil}
                className="font-semibold text-lg  text-blue-600 cursor-pointer hover:underline"
              >
                {services[0]?.nombre_usuario}
              </p>

              {promedio !== null && (
                <p className="text-sm text-gray-600 flex items-center -ml-2">
                  ⭐ {promedio}{" "}
                  <span className="ml-1 text-gray-500"> valoraciones</span>
                </p>
              )}
            </div>
          </div>

          {/* Botón de Contacto */}
          {isCurrentUser ? (
            <p className="text-gray-500 font-medium">
              Eres el proveedor de este servicio
            </p>
          ) : (
            <button
              className="bg-azulBrillante text-white py-2 px-4 rounded-md font-semibold hover:bg-azulOscuro transition"
              onClick={handleComunicarse}
            >
              Contáctame
            </button>
          )}

          {/* Caja con información adicional */}
          <div className="border rounded-md p-4 mt-6 bg-gray-50">
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-azulOscuro font-semibold">De</p>
                <p className="font-medium text-azulBrillante">
                  {services[0]?.direccion || "No especificado"}
                </p>
              </div>
              <div>
                <p className="text-azulOscuro font-semibold">Miembro desde</p>
                <p className="font-medium text-azulBrillante">
                  {services[0]?.fecha_alta || "No disponible"}
                </p>
              </div>

              <div className="col-span-2">
                <p className="text-azulOscuro font-semibold">Idiomas</p>
                <p className="font-medium text-azulBrillante">
                  {services[0]?.idioma || "No especificado"}
                </p>
              </div>
            </div>
          </div>

         
        </div>
      </div>

      <div className="packages-tabs w-1/3 bg-white rounded-lg shadow-lg p-6 border border-gray-300 sticky top-20 h-full">
        <div className="package-content mb-4">
          <header className="header-recurring mb-4">
            <div className="price-wrapper flex items-baseline mb-2">
              <span className="price text-3xl font-bold text-azulOscuro mr-2">
                {services[0]?.precio_servicio} US$
              </span>
            </div>
            <p className="text-lg font-semibold">
              {services[0]?.nombre_servicio}
            </p>
          </header>
        </div>

        <footer className="tab-footer text-center mt-4">
          <button
            className="order-button bg-azulOscuro text-white py-2 px-4 rounded-md hover:bg-azulBrillante transition duration-200"
            onClick={() =>
              navigate("/pedido-page", { state: { serviceData: services[0] } })
            }
          >
            Solicitud de pedido
          </button>
        </footer>

        <div className="contact-section text-center mt-6">
          {isCurrentUser ? (
            <p className="text-gray-500 font-medium">
              Eres el proveedor de este servicio
            </p>
          ) : (
            <h3
              className="text-azulOscuro cursor-pointer hover:underline"
              onClick={handleComunicarse}
            >
              Contáctame
            </h3>
          )}
        </div>
      </div>
    </div>
  );
}
