import React from 'react';
import { FaInfoCircle, FaLightbulb } from 'react-icons/fa';

const InfoSection = () => {
  return (
    <div className="bg-white shadow rounded-lg p-6">
      <div className="mb-6">
        <div className="flex items-center mb-4">
          <FaInfoCircle className="text-primary mr-2" />
          <h2 className="text-xl font-semibold text-gray-900">About</h2>
        </div>
        <p className="text-gray-700 mb-4">
          This app uses AI to generate beautiful math and physics animations from natural language prompts.
        </p>
        <h3 className="text-lg font-medium text-gray-900 mb-2">How it works:</h3>
        <ol className="list-decimal list-inside text-gray-700 space-y-1 pl-4">
          <li>You enter a prompt describing what you want to see</li>
          <li>An LLM (Claude or Groq) generates Manim code</li>
          <li>The Manim library renders the animation</li>
          <li>You get a downloadable video!</li>
        </ol>
      </div>

      <div>
        <div className="flex items-center mb-4">
          <FaLightbulb className="text-yellow-500 mr-2" />
          <h2 className="text-xl font-semibold text-gray-900">Tips for good prompts</h2>
        </div>
        <ul className="list-disc list-inside text-gray-700 space-y-1 pl-4">
          <li>Be specific about what concepts you want to visualize</li>
          <li>Mention colors, shapes, and movements you'd like to see</li>
          <li>Specify labels or annotations that would help explain the concept</li>
          <li>For mathematical concepts, mention equations or formulas to include</li>
          <li>Describe the steps or transitions you want in the animation</li>
        </ul>
      </div>
    </div>
  );
};

export default InfoSection; 