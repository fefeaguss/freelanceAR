import React from "react";

export function Footer() {
    return (
        <footer className="relative bottom-0 left-0 flex justify-between items-center bg-azulClaro text-white p-6 w-full h-16 mt-14">
            <div className="footer-logo">
                <img src="src/assets/freelancear.png" alt="Logo" className="h-16 w-auto" />
            </div>

            <div className="footer-socials flex space-x-4">
                <a href="https://facebook.com" target="_blank" rel="noopener noreferrer" className="hover:opacity-80">
                    <img src="src/assets/2023_Facebook_icon.svg" alt="Facebook" className="h-8 w-8" />
                </a>
                <a href="https://twitter.com" target="_blank" rel="noopener noreferrer" className="hover:opacity-80">
                    <img src="src/assets/X_logo_2023.svg.png" alt="Twitter" className="h-8 w-8" />
                </a>
                <a href="https://instagram.com" target="_blank" rel="noopener noreferrer" className="hover:opacity-80">
                    <img src="src/assets/Instagram_logo_2022.svg.png" alt="Instagram" className="h-8 w-8" />
                </a>
            </div>

            <div className="footer-contact text-sm text-azulOscuro">
                <h3 className="text-lg font-semibold">Contáctanos</h3>
                <p>Email: contacto@tuempresa.com</p>
                <p>Teléfono: +123 456 7890</p>
            </div>
        </footer>
    );
}

