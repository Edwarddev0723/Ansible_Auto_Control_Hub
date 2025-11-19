/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{vue,js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        primary: '#343C6A',
        'primary-blue': '#2D60FF',
        'active-blue': '#1814F3',
      },
      fontFamily: {
        fredoka: ['"Fredoka One"', 'cursive'],
        inter: ['Inter', 'sans-serif'],
        nunito: ['"Nunito Sans"', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
