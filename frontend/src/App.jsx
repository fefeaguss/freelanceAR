import React  from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
//import { UserProvider } from "./context/UserContext.jsx";
import { Provider } from "react-redux";
import { store } from "./Context/store.js";

import { Headers } from "./components/Header.jsx";
import { Footer } from "./components/Footer.jsx";
import { Presentacion } from "./components/Presentacion.jsx";
import  {Login}  from "./components/Login.jsx";
import { Register } from "./components/Register.jsx";
import { Principal } from "./components/Principal.jsx";
import { ServiceDetailPage } from "./components/ServiceCardDetail.jsx";
import { ChatComponent } from "./components/Chat.jsx";
import { UserProfile } from "./components/UserPerfil.jsx";
//import { MisServicios } from "./components/MisServicios.jsx";
import { CreateServicePage } from "./components/CreateService.jsx";
import { OrderConfirmationPage } from "./components/PedidoPage.jsx";
import { PerfilUsuario } from "./components/PerfilesUsuarios.jsx";
import { ModificarServicio } from "./components/ModificarServicio.jsx";




import "./App.css";
import { useEffect, useState } from "react";

export function App() {

  useEffect(() => {
    console.log("Ejecutando useEffect para getWelcomeMensaje");
    getWelcomeMensaje();
  }, []);

  
  const getWelcomeMensaje = async () => {
    try {
      const requestOptions = {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      };
  
      const response = await fetch("/ping", requestOptions);
      const responseText = await response.text(); // Lee la respuesta como texto
      console.log("Contenido de la respuesta:", responseText); // Muestra el contenido recibido
    } catch (error) {
      console.error("Error en la solicitud:", error);
    }
  };
  

  return (
    <>
      <Provider store={store}>
        <Router>
          <Headers />
          <Routes>
            <Route path="/" element={<Presentacion></Presentacion>} />
            <Route path="/login-register" element={<Login></Login>}></Route>
            <Route path="/register" element={<Register></Register>}></Route>
            <Route path="/principal" element={<Principal></Principal>}></Route>
            <Route path="/service" element={<ServiceDetailPage />} />
            <Route path="/Chat" element={<ChatComponent></ChatComponent>}></Route>
            <Route path="/user-profile" element={<UserProfile></UserProfile>}></Route>
            {/* <Route path="/Mis-servicios" element={<MisServicios></MisServicios>}></Route> */}
            <Route path="/crear-servicio" element={<CreateServicePage></CreateServicePage>}></Route>
            <Route path="/pedido-page" element={<OrderConfirmationPage></OrderConfirmationPage>}></Route>
            <Route path="/perfil-usuario" element={<PerfilUsuario></PerfilUsuario>} />
            <Route path="/modificar-servicio" element={<ModificarServicio />} />;
          </Routes>
        <Footer />
        </Router>
      </Provider>
    </>
  );
}
