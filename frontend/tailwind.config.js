/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        page: '#F5F5F7',
        subtle: '#F4F4F6',
        ink: '#111114',
        border: {
          hairline: '#EFEFF2',
          card: '#E9E9EE',
        },
        primary: '#0B0B0F',
        muted: {
          DEFAULT: '#6B6B76',
          soft: '#9A9AA5',
        },
        data: {
          1: '#1F5FFF',
          2: '#B13BF0',
          3: '#FF8A1F',
          4: '#1FA63A',
          alert: '#E5483D',
        },
      },
      borderRadius: {
        card: '28px',
      },
      boxShadow: {
        card: '0 1px 2px rgba(16, 16, 24, 0.04), 0 8px 24px rgba(16, 16, 24, 0.06)',
        control: '0 1px 2px rgba(16, 16, 24, 0.08), 0 0 0 1px rgba(16, 16, 24, 0.04)',
        primary: '0 6px 16px rgba(16, 16, 24, 0.22)',
      },
      fontFamily: {
        sans: ['Inter', 'Geist', '-apple-system', 'Segoe UI', 'sans-serif'],
      },
    },
  },
  plugins: [],
};
