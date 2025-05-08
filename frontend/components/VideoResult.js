import React, { useState, useEffect } from 'react';
import { FaDownload, FaCode } from 'react-icons/fa';
import { getScriptData } from '../utils/api';

const VideoResult = ({ videoPath, scriptPath }) => {
  const [script, setScript] = useState(null);
  const [showScript, setShowScript] = useState(false);
  
  useEffect(() => {
    // Reset script state when new video is generated
    setScript(null);
    setShowScript(false);
  }, [videoPath, scriptPath]);

  if (!videoPath) return null;

  // Ensure the video path is a full URL
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002';
  const fullVideoPath = videoPath.startsWith('http') 
    ? videoPath 
    : `${apiUrl}/${videoPath.replace(/^\//, '')}`;
    
  const fullScriptPath = scriptPath?.startsWith('http') 
    ? scriptPath 
    : `${apiUrl}/${scriptPath?.replace(/^\//, '')}`;

  console.log("Video path:", videoPath);
  console.log("Full video path:", fullVideoPath);
  console.log("Script path:", scriptPath);

  const handleDownload = () => {
    // Create an anchor element and trigger download
    const link = document.createElement('a');
    link.href = fullVideoPath;
    link.download = `animation_${videoPath.split('/').pop()}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };
  
  const handleDownloadScript = () => {
    // Create a Blob and trigger download
    const blob = new Blob([script], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `script_${scriptPath.split('/').pop()}.py`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
  };
  
  const handleViewScript = async () => {
    if (!script && scriptPath) {
      try {
        const scriptData = await getScriptData(scriptPath);
        setScript(scriptData);
      } catch (error) {
        console.error("Failed to load script:", error);
      }
    }
    
    setShowScript(!showScript);
  };

  return (
    <div className="bg-white shadow rounded-lg p-6 mb-6">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">Generated Animation</h2>
      
      <div className="video-container mb-4">
        <video 
          src={fullVideoPath} 
          controls 
        />
      </div>
      
      <div className="flex space-x-4">
        <button
          onClick={handleDownload}
          className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
        >
          <FaDownload className="mr-2" />
          Download Video
        </button>
        
        {scriptPath && (
          <button
            onClick={handleViewScript}
            className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
          >
            <FaCode className="mr-2" />
            {showScript ? 'Hide Script' : 'View Script'}
          </button>
        )}
      </div>
      
      {showScript && script && (
        <div className="mt-4">
          <div className="flex justify-between items-center mb-2">
            <h3 className="text-lg font-medium text-gray-900">Animation Script</h3>
            <button
              onClick={handleDownloadScript}
              className="inline-flex items-center px-3 py-1 border border-transparent rounded-md shadow-sm text-xs font-medium text-white bg-primary hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
            >
              <FaDownload className="mr-1" />
              Download Script
            </button>
          </div>
          <pre className="bg-gray-100 rounded-md p-4 overflow-auto max-h-96 text-sm">
            {script}
          </pre>
        </div>
      )}
    </div>
  );
};

export default VideoResult; 