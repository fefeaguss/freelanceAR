import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useUser } from "../context/UserContext"; 
import { useSelector} from "react-redux";// Asegúrate de importar el contexto

const MessagesMenu = ({ isMessagesOpen }) => {
    const navigate = useNavigate();
    const  user  = useSelector((state) => state.user.user); // Obtén el usuario directamente del contexto
    const [conversations, setConversations] = useState([]);
    const [searchTerm, setSearchTerm] = useState("");
    const [fetchError, setFetchError] = useState(false);
   




    useEffect(() => {
      if (isMessagesOpen && user) {
        fetch(`http://localhost:8000/v1/mensajes/conversaciones/${user.id}`)
          .then((response) => {
            if (!response.ok) throw new Error("Error en el servidor");
            return response.json();
          })
          .then((data) => setConversations(data))
          .catch((error) => {
            console.error("Error cargando conversaciones:", error);
            setFetchError(true);
          });
      }
    }, [isMessagesOpen, user]);
  
    const handleChat = (idConversacion, id_usuario_recibe) => {
        navigate(`/Chat`, { state: { idConversacion, id_usuario_recibe } }); // Pasamos el id_conversacion y el id_usuario_recibe
      };
      
  
    const filteredConversations = Array.isArray(conversations)
      ? conversations.filter(
          (conv) =>
            !(conv.id_usuario_inicia === user.id && conv.id_usuario_recibe === user.id) && // Excluir conversaciones propias
            (conv.nombre_usuario_inicia
              .toLowerCase()
              .includes(searchTerm.toLowerCase()) ||
              conv.nombre_usuario_recibe
                .toLowerCase()
                .includes(searchTerm.toLowerCase()))
        )
      : [];
  
    return (
      <div className="absolute top-full -left-80 mt-2 w-80 bg-white rounded-md shadow-lg z-50 text-black p-4">
        <h2 className="text-lg font-semibold mb-2">Chats</h2>
        {fetchError && (
          <p className="text-red-500">
            No se pudieron cargar las conversaciones. Intenta nuevamente más tarde.
          </p>
        )}
        <div className="mt-2 h-64 overflow-y-auto">
          {filteredConversations.map((conv) => {
            const isUserInitiator = conv.id_usuario_inicia === user.id;
            const chatUserName = isUserInitiator
              ? conv.nombre_usuario_recibe
              : conv.nombre_usuario_inicia;
            const chatUserPhoto = isUserInitiator
              ? conv.foto_usuario_recibe || "/assets/user.png"
              : conv.foto_usuario_inicia || "/assets/user.png";
  
            return (
              <div
                key={conv.id_conversacion}
                className="flex items-center p-2 hover:bg-gray-200 cursor-pointer"
                onClick={() => handleChat(conv.id_conversacion)}
              >
                <img
                  src={`http://localhost:8000${chatUserPhoto}`}
                  className="h-10 w-10 rounded-full"
                  alt="Foto de usuario"
                  onError={(e) => (e.target.src = "/assets/user.png")}
                />
                <div className="ml-3">
                  <p className="font-semibold">{chatUserName}</p>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    );
  };
  
  export default MessagesMenu;
  