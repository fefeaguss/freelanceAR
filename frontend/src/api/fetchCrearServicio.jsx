export const obtenerCategorias = async () => {
    try {
      const response = await fetch("http://localhost:8000/v1/categorias/");
      const data = await response.json();
  
      if (!response.ok) {
        throw new Error(data.message || "Error al obtener las categorías");
      }
  
      return { success: true, data };
    } catch (error) {
      return { success: false, message: error.message };
    }
  };
  
  export const crearServicio = async ({ nombre, descripcion, precio, id_usuario, id_categoria, imagenes }) => {
    const formData = new FormData();
    formData.append("nombre_servicio", nombre);
    formData.append("descripcion_servicio", descripcion);
    formData.append("precio", precio);
    formData.append("id_usuario", id_usuario);
    formData.append("id_categoria", id_categoria);
    imagenes.forEach((img) => formData.append("imagenes", img.file));
  
    try {
      const response = await fetch("http://localhost:8000/v1/servicios/", {
        method: "POST",
        body: formData,
      });
  
      const data = await response.json();
  
      if (!response.ok) {
        throw new Error(data.estado || "Error al crear el servicio");
      }
  
      return { success: true, data };
    } catch (error) {
      return { success: false, message: error.message };
    }
  };
  