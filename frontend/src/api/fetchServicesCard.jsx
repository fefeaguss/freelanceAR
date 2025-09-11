import { useState, useEffect } from 'react';

const API_URL = 'http://localhost:8000/v1/usuarios-servicios/';

export default function useFetchServices() {
    const [services, setServices] = useState([]);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchServices = async () => {
            try {
                const response = await fetch(API_URL);
                if (!response.ok) {
                    throw new Error('Error al cargar servicios');
                }
                const data = await response.json();

                // Filtramos los servicios para solo mostrar los que son del rol 'vendedor'
                const filteredServices = data.filter(service => service.rol === 'vendedor');
                console.log(data)
                setServices(filteredServices);
            } catch (error) {
                setError(error.message);
            } finally {
                setLoading(false);
            }
        };

        fetchServices();
    }, []);

    return { services, loading, error };
}
