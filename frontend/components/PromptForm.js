import React, { useState, useEffect } from 'react';
import { FaSpinner, FaStar, FaLightbulb, FaMagic, FaBrain, FaRandom, FaPuzzlePiece } from 'react-icons/fa';

const PromptForm = ({ onSubmit, isLoading }) => {
  const [prompt, setPrompt] = useState('');
  const [model, setModel] = useState('claude');
  const [useModular, setUseModular] = useState(true);
  const [characterCount, setCharacterCount] = useState(0);
  const [showSuggestions, setShowSuggestions] = useState(false);

  useEffect(() => {
    setCharacterCount(prompt.length);
  }, [prompt]);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (prompt.trim()) {
      onSubmit({ prompt, model, use_modular: useModular });
    }
  };

  const handleExamplePrompt = (examplePrompt) => {
    setPrompt(examplePrompt);
    setShowSuggestions(false);
  };

  const handleRandomExample = () => {
    const randomIndex = Math.floor(Math.random() * examples.length);
    setPrompt(examples[randomIndex]);
    setShowSuggestions(false);
  };

  const examples = [
    "Visualize the Pythagorean theorem with animated squares on the sides of a right triangle",
    "Show how binary search works with an array of numbers using step-by-step animation",
    "Demonstrate the concept of gravitational force between two objects with varying masses",
    "Illustrate the quadratic formula solving process with step-by-step animations",
    "Visualize sorting algorithms like bubble sort and quick sort with animated arrays",
    "Show wave interference patterns when two waves combine in a medium",
    "Demonstrate how derivatives represent the slope of a function at a point",
    "Visualize the double-slit experiment in quantum mechanics",
    "Illustrate the concept of electric fields around positive and negative charges"
  ];

  return (
    <div>
      <form onSubmit={handleSubmit} className="space-y-6">
        <div className="relative">
          <div className="flex items-center mb-2">
            <FaMagic className="text-primary dark:text-blue-400 mr-2" />
            <label htmlFor="prompt" className="block text-sm font-medium text-gray-700 dark:text-gray-300">
              What would you like to visualize?
            </label>
            <button 
              type="button" 
              onClick={() => setShowSuggestions(!showSuggestions)}
              className="ml-2 inline-flex items-center px-2 py-1 text-xs font-medium rounded-full bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 hover:bg-blue-200 dark:hover:bg-blue-800 focus:outline-none transition-colors"
            >
              <FaLightbulb className="mr-1" /> Need ideas?
            </button>
          </div>

          <div className="relative">
            <textarea
              id="prompt"
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Example: Visualize the Pythagorean theorem with animated squares and triangles"
              rows={4}
              className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:ring-2 focus:ring-primary focus:border-transparent dark:bg-dark-100 dark:text-white transition-all duration-200"
              required
            />
            
            <div className="absolute bottom-3 right-3 text-xs text-gray-500 dark:text-gray-400">
              {characterCount} characters
            </div>
          </div>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label htmlFor="model" className="flex items-center mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
              <FaBrain className="text-purple-500 mr-2" />
              Choose LLM model:
            </label>
            <select
              id="model"
              value={model}
              onChange={(e) => setModel(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg shadow-sm focus:ring-2 focus:ring-primary focus:border-transparent dark:bg-dark-100 dark:text-white transition-all duration-200"
            >
              <option value="claude">Claude (more creative)</option>
              <option value="groq">Groq (faster)</option>
            </select>
          </div>
          
          <div>
            <label htmlFor="useModular" className="flex items-center mb-2 text-sm font-medium text-gray-700 dark:text-gray-300">
              <FaPuzzlePiece className="text-green-500 mr-2" />
              Generation approach:
            </label>
            <div className="flex items-center space-x-2">
              <input
                type="checkbox"
                id="useModular"
                checked={useModular}
                onChange={(e) => setUseModular(e.target.checked)}
                className="h-4 w-4 text-primary focus:ring-primary border-gray-300 rounded"
              />
              <label htmlFor="useModular" className="text-sm text-gray-700 dark:text-gray-300">
                Use modular scene generation (better for complex animations)
              </label>
            </div>
            <p className="mt-1 text-xs text-gray-500 dark:text-gray-400">
              Breaking the animation into smaller scenes helps reduce errors and improves quality
            </p>
          </div>
        </div>
        
        <div>
          <button
            type="submit"
            disabled={isLoading}
            className="w-full flex justify-center items-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-gradient-to-r from-primary to-accent hover:from-blue-600 hover:to-purple-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:opacity-70 disabled:cursor-not-allowed transition-all duration-300 transform hover:scale-[1.02] active:scale-[0.98]"
          >
            {isLoading ? (
              <>
                <FaSpinner className="animate-spin mr-2" />
                Generating Animation...
              </>
            ) : (
              <>
                <FaStar className="mr-2" />
                Generate Animation
              </>
            )}
          </button>
        </div>
      </form>
      
      {showSuggestions && (
        <div className="mt-6 bg-gray-50 dark:bg-dark-200/50 rounded-lg p-4 border border-gray-200 dark:border-gray-700 animate-fade-in">
          <div className="flex items-center justify-between mb-3">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white flex items-center">
              <FaLightbulb className="text-yellow-400 mr-2" />
              Example Prompts
            </h3>
            <button
              type="button"
              onClick={handleRandomExample}
              className="inline-flex items-center px-3 py-1 text-sm font-medium rounded-md bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 hover:bg-blue-200 dark:hover:bg-blue-800 focus:outline-none transition-colors"
            >
              <FaRandom className="mr-1" />
              Random Example
            </button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
            {examples.map((example, index) => (
              <button
                key={index}
                type="button"
                onClick={() => handleExamplePrompt(example)}
                className="text-left text-sm text-gray-700 dark:text-gray-300 hover:text-primary dark:hover:text-primary bg-white dark:bg-dark-100 hover:bg-blue-50 dark:hover:bg-blue-900/20 p-3 rounded-md shadow-sm border border-gray-200 dark:border-gray-700 transition-colors"
              >
                {example}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};

export default PromptForm; 