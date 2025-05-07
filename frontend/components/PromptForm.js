import React, { useState } from 'react';
import { FaSpinner } from 'react-icons/fa';

const PromptForm = ({ onSubmit, isLoading }) => {
  const [prompt, setPrompt] = useState('');
  const [model, setModel] = useState('claude');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (prompt.trim()) {
      onSubmit({ prompt, model });
    }
  };

  const handleExamplePrompt = (examplePrompt) => {
    setPrompt(examplePrompt);
  };

  const examples = [
    "Visualize the Pythagorean theorem with animated squares and triangles",
    "Show how binary search works with an array of numbers",
    "Demonstrate the concept of gravitational force between two objects",
    "Illustrate the quadratic formula solving process",
    "Visualize sorting algorithms like bubble sort and quick sort"
  ];

  return (
    <div className="bg-white shadow rounded-lg p-6 mb-6">
      <form onSubmit={handleSubmit}>
        <div className="mb-4">
          <label htmlFor="prompt" className="block text-sm font-medium text-gray-700 mb-1">
            Enter your animation prompt:
          </label>
          <textarea
            id="prompt"
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="Example: Visualize the Pythagorean theorem with animated squares and triangles"
            rows={4}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
            required
          />
        </div>
        
        <div className="mb-4">
          <label htmlFor="model" className="block text-sm font-medium text-gray-700 mb-1">
            Choose LLM model:
          </label>
          <select
            id="model"
            value={model}
            onChange={(e) => setModel(e.target.value)}
            className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary focus:border-primary"
          >
            <option value="claude">Claude</option>
            <option value="groq">Groq</option>
          </select>
        </div>
        
        <button
          type="submit"
          disabled={isLoading}
          className="w-full flex justify-center py-2 px-4 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary disabled:bg-blue-300"
        >
          {isLoading ? (
            <>
              <FaSpinner className="animate-spin mr-2" />
              Generating Animation...
            </>
          ) : (
            'Generate Animation'
          )}
        </button>
      </form>

      <div className="mt-6">
        <h3 className="text-lg font-medium text-gray-900 mb-2">Example Prompts</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {examples.map((example, index) => (
            <button
              key={index}
              type="button"
              onClick={() => handleExamplePrompt(example)}
              className="text-left text-sm text-gray-700 hover:text-primary bg-gray-50 hover:bg-gray-100 px-3 py-2 rounded-md"
            >
              {example}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default PromptForm; 