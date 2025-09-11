import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { login } from '../Context/userSlice'; // Asegúrate de que la ruta es correcta
import { useDispatch, useSelector } from 'react-redux';

export function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [errorMessage, setErrorMessage] = useState('');
    const navigate = useNavigate();
    const dispatch = useDispatch();
    const user = useSelector((state) => state.user.user);

    const handleSubmit = async (e) => {
        e.preventDefault();

        if (!email || !password) {
            setErrorMessage("Por favor, ingresa tu correo electrónico y contraseña.");
            return;
        }

        try {
            const response = await fetch(`/v1/usuarios/buscar_por_mail?mail=`+ email);
            const data = await response.json();

            if (!response.ok || data.contraseña !== password) {
                setErrorMessage("Correo electrónico o contraseña incorrectos.");
                return;
            }

            setErrorMessage('');
            dispatch(login(data)); // ✅ Usar dispatch en lugar de llamar directo
            navigate('/principal');
        } catch (error) {
            console.error("Error en la solicitud:", error);
            setErrorMessage("Hubo un problema al verificar las credenciales.");
        }
    };

    const handleRegisterRedirect = () => {
        navigate('/register');
    };

    return (
        <div className="flex h-screen w-auto">
            {/* Contenedor de la imagen */}
            <div className="hidden md:flex w-2/5 ">
                <img
                    src="/src/assets/login3.jpg"
                    alt="Fondo de inicio de sesión"
                    className="w-full h-screen object-cover  rounded-lg shadow-md"
                />
            </div>
            {/* Contenedor del formulario */}
            <div className="flex flex-col justify-center items-center bg-azulClaro w-full md:w-1/2 p-8 ml-20">
                <div className="bg-white p-8 rounded-lg shadow-lg w-full max-w-md">
                    <h2 className="text-2xl font-bold mb-6 text-azulBrillante">Iniciar Sesión</h2>
                    <form onSubmit={handleSubmit}>
                        <div className="mb-4">
                            <label htmlFor="email" className="block text-azulOscuro font-semibold mb-2">
                                Correo Electrónico
                            </label>
                            <input
                                type="email"
                                id="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-customCyan"
                                required
                            />
                        </div>
                        <div className="mb-4">
                            <label htmlFor="password" className="block text-azulOscuro font-semibold mb-2">
                                Contraseña
                            </label>
                            <input
                                type="password"
                                id="password"
                                value={password}
                                onChange={(e) => setPassword(e.target.value)}
                                className="w-full p-2 border border-gray-300 rounded-lg focus:outline-none focus:border-customCyan"
                                required
                            />
                        </div>
                        {errorMessage && (
                            <p className="text-red-500 text-sm mb-4">{errorMessage}</p>
                        )}
                        <button
                            type="submit"
                            className="w-full bg-azulOscuro text-white py-2 rounded-lg hover:bg-azulBrillante transition duration-200"
                        >
                            Iniciar Sesión
                        </button>
                    </form>
                    <p className="text-azulOscuro mt-4 text-center">
                        ¿No tienes una cuenta?{' '}
                        <span
                            className="text-azulBrillante font-semibold cursor-pointer"
                            onClick={handleRegisterRedirect}
                        >
                            Regístrate aquí
                        </span>
                    </p>
                </div>
            </div>
        </div>
    );
}
