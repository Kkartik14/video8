import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gray-800 text-white py-6 mt-16">
      <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="md:flex md:items-center md:justify-between">
          <div className="text-center md:text-left mb-4 md:mb-0">
            <p>&copy; {new Date().getFullYear()} Prompt-to-2D-Video Generator</p>
          </div>
          <div className="flex justify-center md:justify-end space-x-6">
            <a href="https://www.manim.community/" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white">
              Powered by Manim
            </a>
            <a href="https://www.anthropic.com/" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white">
              Claude
            </a>
            <a href="https://groq.com/" target="_blank" rel="noopener noreferrer" className="text-gray-400 hover:text-white">
              Groq
            </a>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 