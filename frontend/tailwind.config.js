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
        primary: '#3B82F6', // Bright blue
        secondary: '#10B981', // Emerald green
        accent: '#8B5CF6', // Purple
        highlight: '#F59E0B', // Amber
        manim: {
          blue: '#3B82F6',
          green: '#10B981',
          red: '#EF4444',
          purple: '#8B5CF6',
          yellow: '#F59E0B',
          cyan: '#06B6D4',
          black: '#1E293B',
          background: '#0F172A', // Dark blue background like Manim
        },
        dark: {
          100: '#1E293B',
          200: '#0F172A',
          300: '#0B1120',
        },
      },
      boxShadow: {
        'glow': '0 0 15px rgba(59, 130, 246, 0.5)',
        'glow-green': '0 0 15px rgba(16, 185, 129, 0.5)',
        'glow-purple': '0 0 15px rgba(139, 92, 246, 0.5)',
      },
      animation: {
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'bounce-slow': 'bounce 3s infinite',
        'spin-slow': 'spin 3s linear infinite',
        'float': 'float 6s ease-in-out infinite',
        'wave': 'wave 8s ease-in-out infinite',
        'typewriter': 'typewriter 2s steps(40) forwards',
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
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
      },
    },
  },
  plugins: [
    require('@tailwindcss/aspect-ratio'),
  ],
} 