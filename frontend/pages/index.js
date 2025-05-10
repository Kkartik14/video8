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
        <div className="relative overflow-hidden rounded-2xl bg-gradient-to-br from-blue-500/10 to-purple-600/10 dark:from-blue-900/20 dark:to-purple-900/20 p-8 mb-12">
          <HeroAnimation />
          <div className="relative z-10 text-center py-10">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-extrabold text-gray-900 dark:text-white">
              <span className="inline-block wavy-text">
                {'Prompt-to-2D-Video Generator'.split('').map((char, i) => (
                  <span key={i} style={{ '--i': i }}>{char}</span>
                ))}
              </span>
            </h1>
            <p className="mt-6 max-w-3xl mx-auto text-lg md:text-xl text-gray-600 dark:text-gray-300">
              Transform your ideas into stunning mathematical animations using AI and Manim.
              Just describe what you want to visualize, and watch your concepts come to life.
            </p>
            <div className="mt-8 flex justify-center space-x-4">
              <a href="#generator" className="px-8 py-3 text-base font-medium rounded-md text-white bg-gradient-to-r from-primary to-accent hover:from-blue-600 hover:to-purple-600 shadow-lg hover:shadow-blue-500/30 transition-all duration-300">
                Start Creating
              </a>
              <a href="#how-it-works" className="px-8 py-3 text-base font-medium rounded-md text-gray-700 dark:text-white bg-white dark:bg-dark-100 border border-gray-300 dark:border-gray-700 hover:bg-gray-50 dark:hover:bg-dark-200 shadow-lg transition-all duration-300">
                Learn More
              </a>
            </div>
          </div>
        </div>

        <div id="generator" className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div className="lg:col-span-8 space-y-6">
            <div className="bg-white dark:bg-dark-100 shadow-xl dark:shadow-black/30 rounded-xl overflow-hidden transition-all duration-300 transform hover:scale-[1.01]">
              <div className="p-6">
                <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center">
                  <span className="inline-block w-10 h-10 rounded-full bg-primary flex items-center justify-center text-white mr-3">1</span>
                  Create Your Animation
                </h2>
                <PromptForm onSubmit={handleSubmit} isLoading={isLoading} />
              </div>
            </div>
            
            {error && (
              <div className="bg-red-50 dark:bg-red-900/20 border-l-4 border-red-400 p-4 mb-6 rounded-md shadow-lg animate-fade-in">
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
              <div className="bg-white dark:bg-dark-100 shadow-xl dark:shadow-black/30 rounded-xl overflow-hidden transition-all duration-300 transform hover:scale-[1.01]">
                <div className="p-6">
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white flex items-center">
                    <span className="inline-block w-10 h-10 rounded-full bg-secondary flex items-center justify-center text-white mr-3">2</span>
                    Your Generated Animation
                  </h2>
                  <VideoResult videoPath={videoPath} scriptPath={scriptPath} narrationScript={narrationScript} />
                </div>
              </div>
            )}
          </div>
          
          <div className="lg:col-span-4">
            <div className="sticky top-24 space-y-6">
              <div className="bg-white dark:bg-dark-100 shadow-xl dark:shadow-black/30 rounded-xl overflow-hidden transition-all duration-300 transform hover:scale-[1.01]">
                <InfoSection />
              </div>
              
              <div className="bg-gradient-to-br from-blue-400 to-purple-500 dark:from-blue-600 dark:to-purple-700 p-6 rounded-xl text-white shadow-lg">
                <h3 className="text-lg font-bold mb-3">Pro Tip!</h3>
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