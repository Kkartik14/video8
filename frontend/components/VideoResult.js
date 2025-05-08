import React from 'react';
import { FaDownload } from 'react-icons/fa';

const VideoResult = ({ videoPath }) => {
  if (!videoPath) return null;

  // Ensure the video path is a full URL
  const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002';
  const fullVideoPath = videoPath.startsWith('http') 
    ? videoPath 
    : `${apiUrl}/${videoPath.replace(/^\//, '')}`;

  console.log("Video path:", videoPath);
  console.log("Full video path:", fullVideoPath);

  const handleDownload = () => {
    // Create an anchor element and trigger download
    const link = document.createElement('a');
    link.href = fullVideoPath;
    link.download = `animation_${videoPath.split('/').pop()}`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
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
      
      <button
        onClick={handleDownload}
        className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary"
      >
        <FaDownload className="mr-2" />
        Download Video
      </button>
    </div>
  );
};

export default VideoResult; 