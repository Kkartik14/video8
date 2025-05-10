import React, { useState, useEffect, useRef } from 'react';
import { FaDownload, FaCode, FaFileAlt, FaPlay, FaPause, FaExpand, FaVolumeUp, FaVolumeMute } from 'react-icons/fa';
import { getScriptData } from '../utils/api';

const VideoResult = ({ videoPath, scriptPath, narrationScript }) => {
  const [script, setScript] = useState(null);
  const [showScript, setShowScript] = useState(false);
  const [showNarrationScript, setShowNarrationScript] = useState(false);
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(0);
  const [isMuted, setIsMuted] = useState(false);
  const [volume, setVolume] = useState(1);
  const videoRef = useRef(null);
  
  useEffect(() => {
    // Reset script state when new video is generated
    setScript(null);
    setShowScript(false);
    setShowNarrationScript(false);
    setIsPlaying(false);
    setCurrentTime(0);
    setDuration(0);
  }, [videoPath, scriptPath, narrationScript]);

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
  console.log("Narration script available:", !!narrationScript);

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
  
  const handleDownloadNarration = () => {
    // Create a Blob and trigger download
    const blob = new Blob([narrationScript], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `narration_${scriptPath.split('/').pop()}.txt`;
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
  
  const handleViewNarration = () => {
    setShowNarrationScript(!showNarrationScript);
  };

  const togglePlay = () => {
    if (videoRef.current) {
      if (isPlaying) {
        videoRef.current.pause();
      } else {
        videoRef.current.play();
      }
      setIsPlaying(!isPlaying);
    }
  };

  const toggleMute = () => {
    if (videoRef.current) {
      videoRef.current.muted = !isMuted;
      setIsMuted(!isMuted);
    }
  };

  const handleVolumeChange = (e) => {
    const newVolume = parseFloat(e.target.value);
    if (videoRef.current) {
      videoRef.current.volume = newVolume;
      setVolume(newVolume);
      setIsMuted(newVolume === 0);
    }
  };

  const handleFullScreen = () => {
    if (videoRef.current) {
      if (videoRef.current.requestFullscreen) {
        videoRef.current.requestFullscreen();
      } else if (videoRef.current.webkitRequestFullscreen) {
        videoRef.current.webkitRequestFullscreen();
      } else if (videoRef.current.msRequestFullscreen) {
        videoRef.current.msRequestFullscreen();
      }
    }
  };

  const handleTimeUpdate = () => {
    if (videoRef.current) {
      setCurrentTime(videoRef.current.currentTime);
      setDuration(videoRef.current.duration);
    }
  };

  const handleSeek = (e) => {
    const seekTime = parseFloat(e.target.value);
    if (videoRef.current) {
      videoRef.current.currentTime = seekTime;
      setCurrentTime(seekTime);
    }
  };

  const formatTime = (time) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds < 10 ? '0' : ''}${seconds}`;
  };

  return (
    <div className="space-y-6">
      <div className="relative group">
        <div className="video-container overflow-hidden rounded-xl bg-black">
          <video
            ref={videoRef}
            src={fullVideoPath}
            onTimeUpdate={handleTimeUpdate}
            onPlay={() => setIsPlaying(true)}
            onPause={() => setIsPlaying(false)}
            onEnded={() => setIsPlaying(false)}
            onLoadedMetadata={handleTimeUpdate}
            className="w-full h-full object-contain"
          />
          
          {/* Play/Pause button overlay */}
          <div className="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <button
              onClick={togglePlay}
              className="p-4 bg-black/50 rounded-full text-white transform transition-transform duration-300 hover:scale-110"
              aria-label={isPlaying ? 'Pause' : 'Play'}
            >
              {isPlaying ? <FaPause size={24} /> : <FaPlay size={24} />}
            </button>
          </div>
        </div>
        
        {/* Video controls */}
        <div className="mt-2 bg-gray-100 dark:bg-dark-100 rounded-lg p-3 opacity-90 group-hover:opacity-100 transition-opacity">
          <div className="flex items-center space-x-2 mb-2">
            <button
              onClick={togglePlay}
              className="text-gray-700 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors"
              aria-label={isPlaying ? 'Pause' : 'Play'}
            >
              {isPlaying ? <FaPause /> : <FaPlay />}
            </button>
            
            <div className="flex-1 flex items-center space-x-2">
              <span className="text-xs text-gray-500 dark:text-gray-400 w-10">
                {formatTime(currentTime)}
              </span>
              <input
                type="range"
                min="0"
                max={duration || 100}
                value={currentTime}
                onChange={handleSeek}
                className="w-full h-2 bg-gray-300 dark:bg-gray-700 rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:h-3 [&::-webkit-slider-thumb]:w-3 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-primary"
              />
              <span className="text-xs text-gray-500 dark:text-gray-400 w-10">
                {formatTime(duration)}
              </span>
            </div>
            
            <div className="flex items-center space-x-2">
              <button
                onClick={toggleMute}
                className="text-gray-700 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors"
                aria-label={isMuted ? 'Unmute' : 'Mute'}
              >
                {isMuted ? <FaVolumeMute /> : <FaVolumeUp />}
              </button>
              <input
                type="range"
                min="0"
                max="1"
                step="0.01"
                value={volume}
                onChange={handleVolumeChange}
                className="w-16 h-2 bg-gray-300 dark:bg-gray-700 rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:h-3 [&::-webkit-slider-thumb]:w-3 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-primary"
              />
              <button
                onClick={handleFullScreen}
                className="text-gray-700 dark:text-gray-300 hover:text-primary dark:hover:text-primary transition-colors"
                aria-label="Fullscreen"
              >
                <FaExpand />
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <div className="flex flex-wrap gap-2">
        <button
          onClick={handleDownload}
          className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-gradient-to-r from-primary to-accent hover:from-blue-600 hover:to-purple-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all duration-300 transform hover:scale-105"
        >
          <FaDownload className="mr-2" />
          Download Video
        </button>
        
        {scriptPath && (
          <button
            onClick={handleViewScript}
            className="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-dark-100 hover:bg-gray-50 dark:hover:bg-dark-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all duration-300"
          >
            <FaCode className="mr-2 text-manim-green" />
            {showScript ? 'Hide Code' : 'View Code'}
          </button>
        )}
        
        {narrationScript && narrationScript !== "No narration script available for this model." && (
          <button
            onClick={handleViewNarration}
            className="inline-flex items-center px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-md shadow-sm text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-dark-100 hover:bg-gray-50 dark:hover:bg-dark-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary transition-all duration-300"
          >
            <FaFileAlt className="mr-2 text-manim-yellow" />
            {showNarrationScript ? 'Hide Script' : 'View Narration Script'}
          </button>
        )}
      </div>
      
      {showNarrationScript && narrationScript && (
        <div className="mt-4 animate-fade-in">
          <div className="flex justify-between items-center mb-2">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white flex items-center">
              <FaFileAlt className="mr-2 text-manim-yellow" />
              Narration Script
            </h3>
            <button
              onClick={handleDownloadNarration}
              className="inline-flex items-center px-3 py-1 border border-transparent rounded-md shadow-sm text-xs font-medium text-white bg-manim-yellow hover:bg-yellow-500 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-yellow-500 transition-all duration-300"
            >
              <FaDownload className="mr-1" />
              Download Script
            </button>
          </div>
          <div className="bg-yellow-50 dark:bg-yellow-900/20 border border-yellow-200 dark:border-yellow-700 rounded-lg p-4 overflow-auto max-h-96 text-gray-800 dark:text-gray-200">
            {narrationScript.split('\n').map((line, index) => (
              <p key={index} className="mb-2">{line}</p>
            ))}
          </div>
        </div>
      )}
      
      {showScript && script && (
        <div className="mt-4 animate-fade-in">
          <div className="flex justify-between items-center mb-2">
            <h3 className="text-lg font-medium text-gray-900 dark:text-white flex items-center">
              <FaCode className="mr-2 text-manim-green" />
              Animation Code
            </h3>
            <button
              onClick={handleDownloadScript}
              className="inline-flex items-center px-3 py-1 border border-transparent rounded-md shadow-sm text-xs font-medium text-white bg-manim-green hover:bg-green-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-all duration-300"
            >
              <FaDownload className="mr-1" />
              Download Code
            </button>
          </div>
          <pre className="bg-gray-800 dark:bg-gray-900 text-gray-200 rounded-lg p-4 overflow-auto max-h-96 text-sm font-mono shadow-md">
            {script}
          </pre>
        </div>
      )}
    </div>
  );
};

export default VideoResult; 