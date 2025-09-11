import { useState, useEffect } from "react";

const API_URL = "http://127.0.0.1:8000/v1/usuarios-servicios/";

export default function useFetchServicesDetail(id_usuario, id_servicio) {
  const [services, setServices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Verifica que los parámetros sean válidos antes de hacer la petición
    if (!id_usuario || !id_servicio) {
      setError("Faltan parámetros en la solicitud.");
      setLoading(false);
      return;
    }

    const fetchServices = async () => {
      setLoading(true);
      try {
        const url = new URL(API_URL);
        url.searchParams.append("id_usuario", id_usuario);
        url.searchParams.append("id_servicio", id_servicio);

        const response = await fetch(url);
        if (!response.ok) {
          throw new Error("Error al cargar los servicios");
        }

        const data = await response.json();
        console.log("Datos obtenidos:", data); // Verifica en la consola

        setServices(data.length > 0 ? data : []);
      } catch (error) {
        setError(error.message);
      } finally {
        setLoading(false);
      }
    };

    fetchServices();
  }, [id_usuario, id_servicio]); // Se ejecuta solo cuando los parámetros cambian

  return { services, loading, error };
}
