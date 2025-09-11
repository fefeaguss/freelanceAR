import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server:{
    proxy: {
      '/ping': {
        target: 'http://localhost:8000', // Cambia esto por el puerto en el que se ejecuta tu servidor FastAPI
        changeOrigin: true,
      },
      '/v1/usuarios':{
        target:'http://localhost:8000',
        changeOrigin:true,
      },
      '/v1/usuarios/buscar_por_mail':{
        target:'http://localhost:8000',
        changeOrigin:true,
      },
      '/v1/usuarios-servicios':{
        target:'http://localhost:8000',
        changeOrigin:true,
      },
  }
},})
