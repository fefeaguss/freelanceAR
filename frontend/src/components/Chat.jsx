import React, { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
//import { useUser } from "../context/UserContext";
import { useSelector } from "react-redux";


import useFetchServices from "../api/fetchServicesCard"; // Importamos el hook
import axios from "axios"; // Importar axios para realizar la solicitud

export function ChatComponent() {
  const  user  = useSelector((state) => state.user.user); // Usuario logueado
  const { services, loading, error } = useFetchServices(); // Servicios desde el hook
  const [message, setMessage] = useState("");
  const [messages, setMessages] = useState([]);
  const [selectedServiceUser, setSelectedServiceUser] = useState(null); // Usuario del servicio seleccionado
  const location = useLocation();
  const { idConversacion, id_usuario_recibe } = location.state || {};
  console.log("ID usuario recibe en ChatComponent:", id_usuario_recibe);

  // Formatear fecha
  const formatFecha = (fecha) => {
    return new Intl.DateTimeFormat("es-ES", {
      dateStyle: "short",
      timeStyle: "short",
    }).format(new Date(fecha));
  };

  // Seleccionar el usuario del servicio
  useEffect(() => {
    if (services.length > 0) {
      setSelectedServiceUser(services[0]); // Selecciona el primer servicio por defecto
    }
  }, [services]);


  const [recipientInfo, setRecipientInfo] = useState(null); // State for recipient's data

useEffect(() => {
  const fetchRecipientInfo = async () => {
    if (!id_usuario_recibe) return; // No recipient to fetch

    try {
      const response = await axios.get(`http://localhost:8000/v1/usuarios/${id_usuario_recibe}`);
      setRecipientInfo(response.data); // Set recipient's data
      console.log(response.data)
    } catch (error) {
      console.error("Error fetching recipient information:", error);
    }
  };

  fetchRecipientInfo();
}, [id_usuario_recibe]);


  //fetch para traer los mensajes
  useEffect(() => {
    const fetchMessages = () => {
      if (!idConversacion) return; // Usa idConversacion de location.state

      console.log("ID de conversación:", idConversacion); // Verifica que no sea undefined

      axios
        .get(`http://localhost:8000/v1/mensajes/conversacion/${idConversacion}`)
        .then((response) => {
          console.log("Mensajes cargados:", response.data); // Depuración de la respuesta
          setMessages(response.data);
        })
        .catch((error) => {
          console.error("Error al cargar mensajes:", error);
        });
    };

    fetchMessages();
    const intervalId = setInterval(fetchMessages, 3000);

    return () => clearInterval(intervalId);
  }, [idConversacion]); // Cambia dependencia a idConversacion

  // Enviar mensaje
  const sendMessage = (e) => {
    e.preventDefault();
    if (!message.trim() || !user || !selectedServiceUser) return;

    const newMessage = {
      id_conversacion: idConversacion,
      id_usuario_envia: user.id,
      id_usuario_recibe: selectedServiceUser.id_usuario,
      contenido_mensaje: message,
      estado_mensaje: 1,
      fecha_alta_mensaje: new Date().toISOString(),
    };

    // Actualizar estado local
    setMessages((prevMessages) => [...prevMessages, newMessage]);

    // Enviar al servidor
    axios
      .post("http://localhost:8000/v1/mensajes", newMessage)
      .then((response) => {
        console.log("Mensaje enviado:", response.data);
      })
      .catch((error) => {
        console.error("Error al enviar mensaje:", error);
      });

    setMessage("");
  };

  if (loading) return <div>Cargando servicios...</div>;
  if (error) return <div>Error al cargar servicios: {error}</div>;
  if (!user || !selectedServiceUser) return <div>Cargando chat...</div>;

  return (
    <div className="container mx-auto mt-16 flex w-3/4 h-full max-w-6xl gap-4">
      {/* Chat principal */}
      <div className="flex-1 border border-gray-300 rounded-lg shadow p-4 flex flex-col bg-white">
        <div className="border-b pb-4 mb-4 flex items-center justify-between">
          <h2 className="font-semibold text-azulOscuro text-xl">
            Chat con {selectedServiceUser.nombre_usuario || "Desconocido"}
          </h2>
        </div>
        <div className="flex-1 overflow-y-auto space-y-4 mb-4">
          {messages.length > 0 ? (
            messages.map((msg, index) => (
              <div
                key={index}
                className={`flex gap-2 ${
                  msg.id_usuario_envia === user.id ? "justify-end" : "justify-start"
                }`}
              >
                <div className="h-8 w-8 bg-gray-300 rounded-full flex items-center justify-center">
                  <img
                    src={`http://localhost:8000${
                      msg.id_usuario_envia === user.id
                        ? user.foto
                        : msg.foto_usuario_envia
                    }`}
                    alt="Foto de usuario"
                    className="h-full w-full rounded-full object-cover"
                  />
                </div>
                <div className="max-w-xs">
                  <div className="text-sm font-semibold">
                    {msg.id_usuario_envia === user.id ? user.nombre : selectedServiceUser.nombre}
                    <span className="text-xs text-gray-500 ml-2">
                      {formatFecha(msg.fecha_alta_mensaje)}
                    </span>
                  </div>
                  <p
                    className={`text-sm p-2 rounded-lg ${
                      msg.id_usuario_envia === user.id ? "bg-blue-200 text-azulOscuro" : "bg-blue-200 text-azulOscuro"
                    }`}
                  >
                    {msg.contenido_mensaje}
                  </p>
                </div>
              </div>
            ))
          ) : (
            <p className="text-gray-500 text-center">No hay mensajes en esta conversación.</p>
          )}
        </div>
        <form onSubmit={sendMessage} className="border-t pt-4 flex items-center gap-2">
          <input
            type="text"
            placeholder="Escribe un mensaje..."
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="flex-1 border p-2 rounded-lg focus:outline-none focus:border-azulClaro"
          />
          <button
            type="submit"
            className="bg-azulOscuro text-white py-2 px-4 rounded-lg hover:bg-azulBrillante transition duration-200"
          >
            Enviar
          </button>
        </form>
      </div>


    </div>
  );
}
