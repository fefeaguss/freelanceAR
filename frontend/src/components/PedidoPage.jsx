import React from "react";
import { useLocation } from "react-router-dom";

export function OrderConfirmationPage() {
  const location = useLocation();
  const serviceData = location.state?.serviceData || {}; // Recibimos los datos del servicio desde el estado

  return (
    <div className="flex justify-center items-start min-h-screen bg-gray-100 py-8">
      <div className="w-full max-w-5xl bg-white shadow-md rounded-lg p-8 flex flex-col md:flex-row gap-8">
        {/* Sección de Pago */}
        <div className="w-full md:w-2/3">
          <h2 className="text-2xl font-bold mb-6 text-azulOscuro">
            Confirmar y Pagar
          </h2>
          <form>
            {/* Detalles de la tarjeta */}
            <div className="mb-4">
              <label htmlFor="cardNumber" className="block text-gray-700 font-semibold mb-2">
                Número de Tarjeta
              </label>
              <input
                type="text"
                id="cardNumber"
                placeholder="1234 5678 9101 1121"
                className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-azulClaro"
                required
              />
            </div>
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <label htmlFor="expirationDate" className="block text-gray-700 font-semibold mb-2">
                  Fecha de Expiración
                </label>
                <input
                  type="text"
                  id="expirationDate"
                  placeholder="MM/YY"
                  className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-azulClaro"
                  required
                />
              </div>
              <div>
                <label htmlFor="cvv" className="block text-gray-700 font-semibold mb-2">
                  CVV
                </label>
                <input
                  type="text"
                  id="cvv"
                  placeholder="123"
                  className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-azulClaro"
                  required
                />
              </div>
            </div>
            <div className="mb-6">
              <label htmlFor="cardholderName" className="block text-gray-700 font-semibold mb-2">
                Nombre del Titular
              </label>
              <input
                type="text"
                id="cardholderName"
                placeholder="Tu nombre"
                className="w-full p-3 border border-gray-300 rounded-lg focus:outline-none focus:border-azulClaro"
                required
              />
            </div>
            <button
              type="submit"
              className="w-full bg-azulOscuro text-white py-3 rounded-lg hover:bg-azulBrillante transition duration-200 font-semibold"
            >
              Confirmar y Pagar
            </button>
          </form>
        </div>

        {/* Resumen del Pedido */}
        <div className="w-full md:w-1/3 bg-gray-50 p-6 rounded-lg border border-gray-300">
          <h3 className="text-xl font-bold mb-4 text-azulOscuro">Resumen del Pedido</h3>
          <p className="mb-2 text-gray-700">
            <span className="font-semibold">Servicio:</span> {serviceData.nombre_servicio || "Servicio no especificado"}
          </p>
          <p className="mb-2 text-gray-700">
            <span className="font-semibold">Precio:</span> {serviceData.precio_servicio || "0"} US$
          </p>
          <p className="mb-2 text-gray-700">
            <span className="font-semibold">Incluye:</span> {serviceData.descripcion_servicio || "No especificado"}
          </p>
          <p className="mb-2 text-gray-700">
            <span className="font-semibold">Entregado en:</span> {serviceData.tiempo_entrega || "No especificado"} días
          </p>
          <hr className="my-4" />
          <p className="mb-4 text-gray-700">
            <span className="font-semibold">Total:</span>{" "}
            {parseFloat(serviceData.precio_servicio || 0) + 3.55} US$ (incl. cargos)
          </p>
          <p className="text-sm text-gray-600">
            <strong>Nota:</strong> Este servicio es ofrecido por un vendedor independiente.
          </p>
        </div>
      </div>
    </div>
  );
}
