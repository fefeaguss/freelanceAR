import axios from "axios";

const fetchServiceImages = async (id_servicio) => {
  if (!id_servicio) {
    console.warn("id_servicio es undefined, no se puede hacer la petición.");
    return [];
  }

  try {
    const response = await axios.get(`http://localhost:8000/v1/v1/servicios/${id_servicio}/imagenes`);
    return response.data;
  } catch (error) {
    console.error("Error al obtener las imágenes del servicio", error);
    return [];
  }
};

export default fetchServiceImages;
