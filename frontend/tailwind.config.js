/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        eco: {
          50: "#f1fbf4",
          100: "#dbf5e2",
          200: "#b7eac6",
          300: "#83d9a0",
          400: "#49c176",
          500: "#27a85e",
          600: "#1b8b4d",
          700: "#156f3f",
          800: "#125735",
          900: "#0f472c",
        },
      },
    },
  },
  plugins: [],
};
