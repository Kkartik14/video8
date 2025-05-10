import React from 'react';
import { FaFilm, FaCode, FaLightbulb } from 'react-icons/fa';
import ThemeToggle from './ThemeToggle';

const Header = () => {
  return (
    <header className="sticky top-0 z-[5] bg-white dark:bg-manim-black shadow-md transition-all duration-300">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="relative">
              <div className="glow absolute inset-0 rounded-full bg-primary opacity-20"></div>
              <FaFilm className="h-8 w-8 text-primary relative animate-pulse-slow" />
            </div>
            <h1 className="text-2xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent dark:from-blue-400 dark:to-purple-400">
              Prompt-to-2D-Video
            </h1>
          </div>
          
          <nav className="hidden md:flex items-center space-x-6">
            <a href="#" className="flex items-center space-x-1 text-gray-700 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors">
              <FaCode className="h-4 w-4" />
              <span>How It Works</span>
            </a>
            <a href="#" className="flex items-center space-x-1 text-gray-700 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors">
              <FaLightbulb className="h-4 w-4" />
              <span>Examples</span>
            </a>
          </nav>
          
          <ThemeToggle />
        </div>
      </div>
      <div className="loading-bar"></div>
    </header>
  );
};

export default Header; 