/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html","./src/**/*.{html,jsx,js}"],
  theme: {
    extend: {
      colors:{
        customCyan: '#53E1ED',
        azulClaro: '#E9F1FA',
        azulBrillante: '#00ABE4',
        blanco:'#FFFFFF',
        azulOscuro: '#1F375B'
      }
    },
  },
  plugins: [],
}