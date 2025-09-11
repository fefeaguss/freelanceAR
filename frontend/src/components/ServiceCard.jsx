import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import fetchServiceImages from "../api/fetchImagenes";
import { FaChevronLeft, FaChevronRight } from "react-icons/fa"; // Flechas

export function ServiceCard({ id_usuario, id_servicio, username, serviceName, price }) {
    const navigate = useNavigate();
    const [imagenes, setImagenes] = useState([]);
    const [indexActual, setIndexActual] = useState(0);
    const imagenDefault = "/images/placeholder.png"; // Imagen de respaldo

    useEffect(() => {
        const obtenerImagenes = async () => {
            try {
                const imagenesObtenidas = await fetchServiceImages(id_servicio);
                setImagenes(imagenesObtenidas || []);
                setIndexActual(0); // Reiniciar índice cuando cambien las imágenes
            } catch (error) {
                console.error("Error al obtener imágenes:", error);
                setImagenes([]); // Evitar errores si la API falla
            }
        };

        obtenerImagenes();
    }, [id_servicio]);

    const handleCardClick = () => {
        navigate(`/service?id_usuario=${id_usuario}&id_servicio=${id_servicio}`);
    };

    const siguienteImagen = (e) => {
        e.stopPropagation();
        if (imagenes.length > 1) {
            setIndexActual((prevIndex) => (prevIndex + 1) % imagenes.length);
        }
    };

    const anteriorImagen = (e) => {
        e.stopPropagation();
        if (imagenes.length > 1) {
            setIndexActual((prevIndex) => (prevIndex - 1 + imagenes.length) % imagenes.length);
        }
    };

    return (
        <div 
            className="w-full max-w-xs bg-white shadow-lg rounded-lg overflow-hidden cursor-pointer hover:shadow-xl transform hover:scale-105 transition duration-300 ease-in-out "
            onClick={handleCardClick}
        >
            {/* Carrusel de imágenes */}
            <div className="relative w-full min-h-48 h-48 overflow-hidden">
                {imagenes.length > 0 ? (
                    imagenes.map((imagen, index) => (
                        <img 
                            key={index}
                            src={`http://localhost:8000/${imagen.url}`} 
                            alt={serviceName} 
                            className={`absolute top-0 left-0 w-full h-full object-cover transition-opacity duration-500 ${
                                index === indexActual ? "opacity-100" : "opacity-0"
                            }`}
                        />
                    ))
                ) : (
                    <img 
                        src={imagenDefault} 
                        alt="No disponible" 
                        className="w-full h-full object-cover"
                    />
                )}

                {/* Flechas de navegación */}
                {imagenes.length > 1 && (
                    <>
                        <button 
                            className="absolute left-2 top-1/2 transform -translate-y-1/2 bg-black bg-opacity-50 text-white p-2 rounded-full"
                            onClick={anteriorImagen}
                        >
                            <FaChevronLeft />
                        </button>
                        <button 
                            className="absolute right-2 top-1/2 transform -translate-y-1/2 bg-black bg-opacity-50 text-white p-2 rounded-full"
                            onClick={siguienteImagen}
                        >
                            <FaChevronRight />
                        </button>
                    </>
                )}
            </div>

            {/* Información del servicio */}
            <div className="p-8">
                <h3 className="text-xl font-bold text-azulOscuro mb-2 -mt-4">{serviceName}</h3>
                <p className="text-gray-600">Vendido por: <span className="font-medium">{username}</span></p>
                <p className="text-lg font-semibold text-yellow-500 mt-4">${price}</p>
            </div>
        </div>
    );
}
