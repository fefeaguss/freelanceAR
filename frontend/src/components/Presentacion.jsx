import React, { useState } from "react";

export function Presentacion() {
  return (
    <main className="flex flex-col w-full items-center justify-center min-h-screen bg-azulClaro text-gray-800 ">
      {/* Logo y Descripción */}
      <section className=" grid grid-rows-1 grid-flow-col gap-4  min-h-screen items-center   text-center">
        <div className="row-span-2 ">
          <img
            src="/src/assets/ChatGPT Image 17 sept 2025, 15_34_18.png"
            alt="Logo de la página"
            className="mx-auto h-100 w-100vh object-contain"
          />
        </div>

        <div class="row-span-1 ">
          <h1 className="text-4xl font-extrabold text-yellow-400 mb-4">
            Bienvenido a FreelanceAR
          </h1>
          <p className="text-xl text-azulOscuro">
            La plataforma ideal para conectar a profesionales independientes con
            quienes buscan sus servicios. Encuentra talentos en diseño,
            desarrollo, marketing y mucho más para llevar tus proyectos al
            siguiente nivel.
          </p>
        </div>
      </section>

      {/* Secciones de Revista */}
      <section className="grid gap-6 max-w-screen">
        {/* Primer div - Imagen a la izquierda */}
        <div className="bg-white shadow-lg rounded-lg overflow-hidden flex h-72  items-center mt-10">
          <img
            src="src\assets\confianza-sitio-web.png"
            alt="Confianza"
            className="h-72 w-1/2 object-cover"
          />
          <div className="p-6 w-1/2">
            <h3 className="text-2xl font-extrabold text-customCyan mb-2">
              Confianza y Calidad
            </h3>
            <p className="text-azulOscuro">
              Explora perfiles detallados con reseñas verificadas y un
              portafolio de trabajos anteriores para contratar con seguridad.
            </p>
          </div>
        </div>

        {/* Segundo div - Imagen a la derecha */}
        <div className="bg-white shadow-lg rounded-lg overflow-hidden flex h-72 flex-row-reverse items-center mt-10">
          <img
            src="src\assets\talentoIdeal.png"
            alt="Talento Ideal"
            className="h-72 w-1/2 object-cover"
          />
          <div className="p-6 w-1/2">
            <h3 className="text-2xl font-extrabold text-customCyan mb-2">
              Encuentra el Talento Ideal
            </h3>
            <p className="text-azulOscuro">
              Una amplia variedad de freelancers especializados listos para
              ayudarte en cualquier categoría de proyecto.
            </p>
          </div>
        </div>

        {/* Tercer div - Imagen a la izquierda */}
        <div className="bg-white shadow-lg rounded-lg overflow-hidden flex h-72 items-center mt-10">
          <img
            src="src\assets\SoporteySeguridad.png"
            alt="Soporte y Seguridad"
            className="h-72 w-1/2 object-cover"
          />
          <div className="p-6 w-1/2">
            <h3 className="text-2xl font-extrabold text-customCyan mb-2">
              Soporte y Seguridad
            </h3>
            <p className="text-azulOscuro">
              Asistencia dedicada y sistema de pago seguro para una experiencia
              de contratación libre de preocupaciones.
            </p>
          </div>
        </div>
      </section>
    </main>
  );
}
