import { useState } from 'react';
import Head from 'next/head';
import Header from '../components/Header';
import Footer from '../components/Footer';
import PromptForm from '../components/PromptForm';
import VideoResult from '../components/VideoResult';
import InfoSection from '../components/InfoSection';
import Particles from '../components/Particles';
import HeroAnimation from '../components/HeroAnimation';
import { generateVideo } from '../utils/api';

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [videoPath, setVideoPath] = useState(null);
  const [scriptPath, setScriptPath] = useState(null);
  const [narrationScript, setNarrationScript] = useState(null);
  const [error, setError] = useState(null);

  const handleSubmit = async (formData) => {
    setIsLoading(true);
    setError(null);
    
    try {
      const result = await generateVideo(formData.prompt, formData.model);
      setVideoPath(result.video_path);
      setScriptPath(result.script_path);
      setNarrationScript(result.narration_script);
    } catch (err) {
      console.error("Error generating video:", err);
      
      if (err.toString().includes('ERR_CONNECTION_REFUSED')) {
        setError("Could not connect to the backend server. Please make sure it's running at " + 
                 (process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8002'));
      } else {
        setError(err.toString());
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-manim-background transition-colors duration-300">
      <Head>
        <title>Prompt-to-2D-Video Generator - Manim-Powered AI Animation Studio</title>
        <meta name="description" content="Generate beautiful mathematical animations from natural language prompts with AI and Manim" />
        <link rel="icon" href="/favicon.ico" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet" />
      </Head>

      <Particles count={40} />
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10 relative">
        <div className="relative overflow-hidden rounded-lg bg-gradient-animation p-8 mb-12">
          <HeroAnimation />
          
          <div className="relative z-10 text-center py-10">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold text-gray-900 dark:text-white mb-6">
              <span className="gradient-text">
                Prompt-to-2D-Video Generator
              </span>
            </h1>
            <p className="mt-6 max-w-3xl mx-auto text-lg md:text-xl text-gray-600 dark:text-gray-300 animate-fade-in">
              Transform your ideas into stunning mathematical animations using AI and Manim.
              Just describe what you want to visualize, and watch your concepts come to life.
            </p>
            <div className="mt-8 flex flex-wrap justify-center gap-4">
              <a href="#generator" className="px-8 py-3 text-base font-medium rounded-md text-white bg-gradient-to-r from-primary to-accent hover:from-blue-600 hover:to-purple-600 transition-all duration-300 animate-fade-in">
                Start Creating
              </a>
              <a href="#how-it-works" className="px-8 py-3 text-base font-medium rounded-md text-gray-700 dark:text-white bg-white/10 dark:bg-white/5 border border-gray-300 dark:border-gray-800 backdrop-blur-sm hover:bg-white/20 dark:hover:bg-white/10 transition-all duration-300 animate-fade-in" style={{animationDelay: '100ms'}}>
                Learn More
              </a>
            </div>
          </div>
        </div>

        <div id="generator" className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div className="lg:col-span-8 space-y-6">
            <div className="bg-white dark:bg-dark-100 shadow-card rounded-lg overflow-hidden transition-all duration-300 border border-transparent dark:border-gray-800/30">
              <div className="p-6">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center mb-4">
                  <span className="inline-block w-8 h-8 rounded-md bg-primary flex items-center justify-center text-white mr-3">1</span>
                  Create Your Animation
                </h2>
                <PromptForm onSubmit={handleSubmit} isLoading={isLoading} />
              </div>
            </div>
            
            {error && (
              <div className="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-400 p-4 mb-6 rounded-md shadow-card animate-fade-in">
                <div className="flex">
                  <div className="flex-shrink-0">
                    <svg className="h-5 w-5 text-red-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" aria-hidden="true">
                      <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <div className="ml-3">
                    <p className="text-sm text-red-700 dark:text-red-300">{error}</p>
                    {error.includes('backend server') && (
                      <p className="text-sm text-red-700 dark:text-red-300 mt-2">
                        Try running the backend manually: <code className="bg-red-100 dark:bg-red-900/40 px-1 rounded">python3 backend/main.py</code>
                      </p>
                    )}
                  </div>
                </div>
              </div>
            )}
            
            {videoPath && (
              <div className="bg-white dark:bg-dark-100 shadow-card rounded-lg overflow-hidden transition-all duration-300 border border-transparent dark:border-gray-800/30 animate-fade-in">
                <div className="p-6">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center mb-4">
                    <span className="inline-block w-8 h-8 rounded-md bg-secondary flex items-center justify-center text-white mr-3">2</span>
                    Your Generated Animation
                  </h2>
                  <VideoResult videoPath={videoPath} scriptPath={scriptPath} narrationScript={narrationScript} />
                </div>
              </div>
            )}
          </div>
          
          <div className="lg:col-span-4">
            <div className="sticky top-24 space-y-6">
              <div className="bg-white dark:bg-dark-100 shadow-card rounded-lg overflow-hidden transition-all duration-300 border border-transparent dark:border-gray-800/30">
                <InfoSection />
              </div>
              
              <div className="bg-gradient-to-r from-purple-500/10 to-blue-500/10 dark:from-purple-800/20 dark:to-blue-800/20 backdrop-blur-sm rounded-lg p-6 text-gray-800 dark:text-white border border-gray-200 dark:border-gray-800/30">
                <h3 className="text-lg font-bold mb-3 flex items-center">
                  <span className="inline-block w-6 h-6 rounded-md bg-purple-500/20 flex items-center justify-center mr-2">
                    <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-purple-500" viewBox="0 0 20 20" fill="currentColor">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" />
                    </svg>
                  </span>
                  Pro Tip!
                </h3>
                <p className="text-sm opacity-90">
                  Try using specific mathematical terms in your prompts for more precise visualizations. 
                  For example, "Show how the sine and cosine functions relate to the unit circle" will 
                  produce better results than "Show a circle with waves."
                </p>
              </div>
            </div>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
} 