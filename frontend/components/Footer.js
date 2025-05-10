import React from 'react';
import { FaHeart, FaGithub, FaTwitter, FaLinkedin } from 'react-icons/fa';

const Footer = () => {
  return (
    <footer className="mt-20 bg-white dark:bg-manim-black shadow-md dark:shadow-none border-t border-gray-200 dark:border-gray-800 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div className="space-y-3">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Prompt-to-2D-Video</h3>
            <p className="text-sm text-gray-600 dark:text-gray-300">
              Transform natural language prompts into beautiful educational animations using AI and Manim.
            </p>
          </div>
          
          <div className="space-y-3">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Resources</h3>
            <ul className="space-y-2 text-sm">
              <li>
                <a href="https://github.com/Kkartik14/video8" className="text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors">
                  GitHub Repository
                </a>
              </li>
              <li>
                <a href="https://docs.manim.community/" className="text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors">
                  Manim Documentation
                </a>
              </li>
              <li>
                <a href="https://claude.ai/" className="text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors">
                  Claude AI
                </a>
              </li>
              <li>
                <a href="https://groq.com/" className="text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors">
                  Groq
                </a>
              </li>
            </ul>
          </div>
          
          <div className="space-y-3">
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white">Connect</h3>
            <div className="flex space-x-4">
              <a 
                href="https://github.com/Kkartik14" 
                className="text-gray-600 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors"
                aria-label="GitHub"
              >
                <FaGithub size={24} />
              </a>
              <a 
                href="#" 
                className="text-gray-600 dark:text-gray-300 hover:text-blue-400 transition-colors"
                aria-label="Twitter"
              >
                <FaTwitter size={24} />
              </a>
              <a 
                href="#" 
                className="text-gray-600 dark:text-gray-300 hover:text-blue-700 transition-colors"
                aria-label="LinkedIn"
              >
                <FaLinkedin size={24} />
              </a>
            </div>
            
            <p className="text-sm text-gray-600 dark:text-gray-300">
              Have suggestions? <a href="mailto:contact@example.com" className="text-primary dark:text-blue-400 hover:underline">Contact us</a>
            </p>
          </div>
        </div>
        
        <div className="mt-8 pt-6 border-t border-gray-200 dark:border-gray-800 flex flex-col items-center justify-center">
          <p className="text-sm text-gray-600 dark:text-gray-300 flex items-center">
            Made with <FaHeart className="text-red-500 mx-1 animate-pulse" /> using Manim, Claude and Groq
          </p>
          <p className="mt-2 text-xs text-gray-500 dark:text-gray-400">
            © {new Date().getFullYear()} Prompt-to-2D-Video Generator. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer; 