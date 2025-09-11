import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

export function Register() {
  const [step, setStep] = useState(1); // Controla la etapa del formulario
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [nombre, setNombre] = useState("");
  const [apellido, setApellido] = useState("");
  const [username, setUsername] = useState("");
  const [direccion, setDireccion] = useState("");
  const [idioma, setIdioma] = useState("Español");
  const [descripcion, setDescripcion] = useState("");
  const [foto, setFoto] = useState(null);
  const navigate = useNavigate();

  const postCreateUser = async (userData) => {
    try {
      const formData = new FormData();
      formData.append("nombre", userData.nombre);
      formData.append("apellido", userData.apellido);
      formData.append("mail", userData.email);
      formData.append("username", userData.username);
      formData.append("direccion", userData.direccion || "");
      formData.append("idioma", userData.idioma);
      formData.append("descripcion", userData.descripcion);
      formData.append("contraseña", userData.password);
      formData.append("foto", userData.foto);

      const response = await fetch("http://localhost:8000/v1/usuarios/", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status} ${response.statusText}`);
      }

      alert("Usuario registrado exitosamente");
      navigate("/login-register");
    } catch (error) {
      console.error("Error en la solicitud:", error);
      alert("Hubo un error al registrar el usuario");
    }
  };

  const handleNextStep = (e) => {
    e.preventDefault();

    if (password !== confirmPassword) {
      alert("Las contraseñas no coinciden");
      return;
    }

    setStep(2); // Avanza a la segunda etapa
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    const userData = {
      email,
      password,
      nombre,
      apellido,
      username,
      direccion,
      idioma,
      descripcion,
      foto,
    };

    postCreateUser(userData);
  };

  return (
    <div className="flex justify-center items-center min-h-auto bg-azulClaro mt-28">
      <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-lg">
        {step === 1 && (
          <form onSubmit={handleNextStep}>
            <h2 className="text-2xl font-bold mb-6 text-azulOscuro">Paso 1: Credenciales</h2>
            <div className="mb-4">
              <label htmlFor="email" className="block text-gray-700 font-semibold mb-2">
                Correo Electrónico
              </label>
              <input
                type="email"
                id="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-azulClaro"
                required
              />
            </div>
            <div className="mb-4">
              <label htmlFor="password" className="block text-gray-700 font-semibold mb-2">
                Contraseña
              </label>
              <input
                type="password"
                id="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-azulClaro"
                required
              />
            </div>
            <div className="mb-4">
              <label htmlFor="confirmPassword" className="block text-gray-700 font-semibold mb-2">
                Confirmar Contraseña
              </label>
              <input
                type="password"
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-azulClaro"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full bg-azulOscuro text-white py-2 rounded-lg hover:bg-azulBrillante transition duration-200"
            >
              Siguiente
            </button>
          </form>
        )}

        {step === 2 && (
          <form onSubmit={handleSubmit}>
            <h2 className="text-2xl font-bold mb-6 text-azulOscuro">Paso 2: Datos Adicionales</h2>
            <div className="mb-4">
              <label htmlFor="nombre" className="block text-gray-700 font-semibold mb-2">
                Nombre
              </label>
              <input
                type="text"
                id="nombre"
                value={nombre}
                onChange={(e) => setNombre(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-azulClaro"
                required
              />
            </div>
            <div className="mb-4">
              <label htmlFor="apellido" className="block text-gray-700 font-semibold mb-2">
                Apellido
              </label>
              <input
                type="text"
                id="apellido"
                value={apellido}
                onChange={(e) => setApellido(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-azulClaro"
                required
              />
            </div>
            <div className="mb-4">
              <label htmlFor="username" className="block text-gray-700 font-semibold mb-2">
                Nombre de Usuario
              </label>
              <input
                type="text"
                id="username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-azulClaro"
                required
              />
            </div>
            <div className="mb-4">
              <label htmlFor="direccion" className="block text-gray-700 font-semibold mb-2">
                Ubicación
              </label>
              <input
                type="text"
                id="direccion"
                value={direccion}
                onChange={(e) => setDireccion(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-azulClaro"
              />
            </div>
            <div className="mb-4">
              <label htmlFor="idioma" className="block text-gray-700 font-semibold mb-2">
                Idioma
              </label>
              <select
                id="idioma"
                value={idioma}
                onChange={(e) => setIdioma(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-azulClaro"
              >
                <option value="Español">Español</option>
                <option value="Inglés">Inglés</option>
                <option value="Francés">Francés</option>
              </select>
            </div>
            <div className="mb-4">
              <label htmlFor="descripcion" className="block text-gray-700 font-semibold mb-2">
                Descripción
              </label>
              <textarea
                id="descripcion"
                value={descripcion}
                onChange={(e) => setDescripcion(e.target.value)}
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-azulClaro"
                rows="3"
              ></textarea>
            </div>
            <div className="mb-6">
              <label htmlFor="foto" className="block text-gray-700 font-semibold mb-2">
                Foto de Perfil
              </label>
              <input
                type="file"
                id="foto"
                onChange={(e) => setFoto(e.target.files[0])}
                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-azulClaro"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full bg-azulOscuro text-white py-2 rounded-lg hover:bg-azulBrillante transition duration duration-200"
            >
              Registrar
            </button>
          </form>
        )}
      </div>
    </div>
  );
}
