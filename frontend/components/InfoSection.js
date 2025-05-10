import React from 'react';
import { FaInfoCircle, FaLightbulb, FaRocket, FaMagic, FaCode, FaGithub } from 'react-icons/fa';

const InfoSection = () => {
  return (
    <div className="p-6">
      <div className="mb-8">
        <div className="flex items-center mb-4">
          <div className="relative mr-2">
            <div className="glow absolute inset-0 rounded-full bg-primary opacity-20"></div>
            <FaInfoCircle className="text-primary dark:text-blue-400 relative animate-pulse-slow" size={20} />
          </div>
          <h2 className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-primary to-accent dark:from-blue-400 dark:to-purple-400">
            About This Tool
          </h2>
        </div>
        
        <p className="text-gray-700 dark:text-gray-300 mb-4 leading-relaxed">
          Create stunning math and physics animations from natural language prompts using AI and the 
          powerful Manim animation engine.
        </p>
        
        <h3 className="flex items-center text-lg font-medium text-gray-900 dark:text-white mb-3">
          <FaRocket className="text-manim-purple mr-2" />
          How it works:
        </h3>
        
        <ol className="space-y-3 pl-4">
          <li className="flex items-start text-gray-700 dark:text-gray-300">
            <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-primary text-white text-xs font-medium mr-2 shrink-0">1</span>
            <span>You enter a prompt describing what you want to visualize</span>
          </li>
          <li className="flex items-start text-gray-700 dark:text-gray-300">
            <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-accent text-white text-xs font-medium mr-2 shrink-0">2</span>
            <span>An LLM (Claude or Groq) generates Manim Python code</span>
          </li>
          <li className="flex items-start text-gray-700 dark:text-gray-300">
            <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-secondary text-white text-xs font-medium mr-2 shrink-0">3</span>
            <span>The Manim library renders the animation with precise mathematical accuracy</span>
          </li>
          <li className="flex items-start text-gray-700 dark:text-gray-300">
            <span className="inline-flex items-center justify-center w-6 h-6 rounded-full bg-highlight text-white text-xs font-medium mr-2 shrink-0">4</span>
            <span>You get a downloadable video with your animated concept!</span>
          </li>
        </ol>
      </div>

      <div className="relative">
        <div className="absolute -inset-1 bg-gradient-to-r from-blue-500 to-purple-600 rounded-lg blur opacity-25"></div>
        <div className="relative bg-white dark:bg-dark-100 p-4 rounded-lg border border-gray-200 dark:border-gray-700">
          <div className="flex items-center mb-3">
            <FaLightbulb className="text-yellow-500 mr-2 animate-pulse-slow" />
            <h2 className="text-lg font-medium text-gray-900 dark:text-white">Tips for great prompts</h2>
          </div>
          
          <ul className="space-y-2 text-gray-700 dark:text-gray-300 text-sm">
            <li className="flex items-start">
              <FaMagic className="text-primary mt-1 mr-2 shrink-0" />
              <span>Be specific about which concepts you want to visualize</span>
            </li>
            <li className="flex items-start">
              <FaMagic className="text-primary mt-1 mr-2 shrink-0" />
              <span>Mention colors, shapes, and movements you'd like to see</span>
            </li>
            <li className="flex items-start">
              <FaMagic className="text-primary mt-1 mr-2 shrink-0" />
              <span>Specify labels or annotations to help explain the concept</span>
            </li>
            <li className="flex items-start">
              <FaMagic className="text-primary mt-1 mr-2 shrink-0" />
              <span>For math concepts, include equations or formulas to visualize</span>
            </li>
            <li className="flex items-start">
              <FaMagic className="text-primary mt-1 mr-2 shrink-0" />
              <span>Describe step-by-step animations or transitions you want to see</span>
            </li>
          </ul>
        </div>
      </div>
      
      <div className="mt-6 text-center">
        <a 
          href="https://github.com/Kkartik14/video8" 
          target="_blank" 
          rel="noopener noreferrer"
          className="inline-flex items-center px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors"
        >
          <FaGithub className="mr-2" />
          View on GitHub
        </a>
        <a 
          href="https://docs.manim.community/" 
          target="_blank" 
          rel="noopener noreferrer"
          className="inline-flex items-center px-4 py-2 text-sm text-gray-700 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors"
        >
          <FaCode className="mr-2" />
          Manim Docs
        </a>
      </div>
    </div>
  );
};

export default InfoSection; 