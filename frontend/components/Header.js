import React from 'react';
import { FaFilm } from 'react-icons/fa';

const Header = () => {
  return (
    <header className="bg-white shadow mb-6">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
        <div className="flex items-center">
          <FaFilm className="h-8 w-8 text-primary mr-2" />
          <h1 className="text-2xl font-bold text-gray-900">Prompt-to-2D-Video Generator</h1>
        </div>
      </div>
    </header>
  );
};

export default Header; 