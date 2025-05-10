/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './pages/**/*.{js,ts,jsx,tsx,mdx}',
    './components/**/*.{js,ts,jsx,tsx,mdx}',
    './app/**/*.{js,ts,jsx,tsx,mdx}',
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        primary: '#00B4D8', // Bright cyan
        secondary: '#00D084', // Green
        accent: '#8B5CF6', // Purple
        highlight: '#FF3366', // Red-pink
        manim: {
          blue: '#00B4D8',
          green: '#00D084',
          red: '#FF3366',
          purple: '#8B5CF6',
          yellow: '#FFD166',
          cyan: '#00B4D8',
          black: '#121212',
          background: '#0A0A0A', // Darker background
          surface: '#181818',
        },
        dark: {
          100: '#181818',
          200: '#121212',
          300: '#0A0A0A',
        },
      },
      boxShadow: {
        'subtle': '0 4px 12px rgba(0, 0, 0, 0.15)',
        'card': '0 2px 8px rgba(0, 0, 0, 0.12)',
        'accent': '0 2px 8px rgba(139, 92, 246, 0.2)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-slow': 'bounce 3s infinite',
        'spin-slow': 'spin 3s linear infinite',
        'float': 'float 6s ease-in-out infinite',
        'wave': 'wave 8s ease-in-out infinite',
        'typewriter': 'typewriter 2s steps(40) forwards',
        'morph': 'morph 8s ease-in-out infinite',
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.5s ease-in-out',
        'slide-in': 'slideIn 0.5s ease-in-out',
        'reveal': 'reveal 1s ease-in-out',
        'theme-toggle-dark': 'themeToggleDark 0.5s ease-in-out forwards',
        'theme-toggle-light': 'themeToggleLight 0.5s ease-in-out forwards',
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        wave: {
          '0%, 100%': { transform: 'translateX(0)' },
          '50%': { transform: 'translateX(-5px)' },
        },
        typewriter: {
          '0%': { width: '0' },
          '100%': { width: '100%' },
        },
        morph: {
          '0%, 100%': { borderRadius: '10px' },
          '50%': { borderRadius: '15px' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(20px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideIn: {
          '0%': { transform: 'translateX(-20px)', opacity: '0' },
          '100%': { transform: 'translateX(0)', opacity: '1' },
        },
        reveal: {
          '0%': { clipPath: 'inset(0 100% 0 0)' },
          '100%': { clipPath: 'inset(0 0 0 0)' },
        },
        themeToggleDark: {
          '0%': { transform: 'scale(1)', opacity: '1' },
          '100%': { transform: 'scale(15)', opacity: '0' },
        },
        themeToggleLight: {
          '0%': { transform: 'scale(1)', opacity: '1' },
          '100%': { transform: 'scale(15)', opacity: '0' },
        },
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'cursor-gradient': 'linear-gradient(to right, #8B5CF6, #FF3366, #00D084)',
      },
    },
  },
  plugins: [
    require('@tailwindcss/aspect-ratio'),
  ],
} 